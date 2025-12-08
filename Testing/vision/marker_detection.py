import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
import csv
import re
import pandas as pd
import datetime as datetime
from config import *

class ArucoMarker:
    """
    This class represents an ArUco marker. 
    """

    def __init__(self, marker_id, start_time):

        self.pos = np.array([0, 0])
        self.angle = 0
        self.marker_size = 15 # 15mm
        self.marker_id = marker_id
        self.logfile = open(f"logs/marker/marker_{marker_id}_log{start_time.strftime('%Y-%m-%d_%H-%M-%S')}.csv", "w", newline="")
        self.logger = csv.writer(self.logfile)
        self.logger.writerow(["frame", "x", "y"])
        self.frame_count = 0
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.parameters = cv2.aruco.DetectorParameters_create() if hasattr(cv2.aruco, 'DetectorParameters_create') else cv2.aruco.DetectorParameters()
        

    def update_marker(self, frame, frame_count):
        # Camera parameters
        focal_length = 1 
        center = (frame.shape[1] / 2, frame.shape[0] / 2)  # Center of the frame

        # Camera matrix 
        cameraMatrix = np.array([[focal_length, 0, center[0]],
                                     [0, focal_length, center[1]],
                                    [0, 0, 1]], dtype=np.float64)

        distCoeffs = np.zeros((4, 1))  
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = cv2.aruco.detectMarkers(gray, self.aruco_dict, parameters=self.parameters)
        
        if ids is not None and self.marker_id in ids:
            idx = np.where(ids == self.marker_id)[0][0]
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners[idx], self.marker_size, cameraMatrix, distCoeffs)

            self.marker_pxl_size = np.linalg.norm(corners[idx][0][0] - corners[idx][0][1])

            axis_length = self.marker_size / 2
            points = np.float32([[0, 0, 0], [axis_length, 0, 0], [0, axis_length, 0], [0, 0, -axis_length]]).reshape(-1, 3, 1)
            axis_points, _ = cv2.projectPoints(points, rvecs[0], tvecs[0], cameraMatrix, distCoeffs)
            axis_points = axis_points.astype(int)

            angle = np.arctan2(axis_points[0].ravel()[0] - axis_points[1].ravel()[0], axis_points[0].ravel()[1] - axis_points[1].ravel()[1])
            angle = np.degrees(angle) + 90
            self.pos = axis_points[0].ravel()
            frame = cv2.circle(frame, tuple(self.pos), 3, (0, 255, 0), -1)
            self.logger.writerow([frame_count, self.pos[0], self.pos[1]])
    
        return frame
    
    
    
def marker_logging(source):
    match = re.search(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}-\d{6}', source)
    start_time = datetime.datetime.strptime(match.group(), '%Y-%m-%d_%H-%M-%S-%f')
    markers = [ArucoMarker(marker_id, start_time) for marker_id in range(1, 5)]  # Create instances for each ArUco marker

    frame_count = 0
    cap = cv2.VideoCapture(source)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    last_reported = -1
    # Check if the video file was opened successfully
    if not cap.isOpened():
        print("Error: Unable to open video file")
        exit()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (video end?). Exiting ...")
            break
        frame_count +=1
        for marker in markers:
            frame = marker.update_marker(frame, frame_count)
    
        if SHOW:
            cv2.imshow('Markers Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        percent = int((frame_count / length) * 100)
        if percent // 10 != last_reported and percent % 10 == 0:
            print(f'Marker detection status {percent}%')
            last_reported = percent // 10

    cap.release()
    cv2.destroyAllWindows()
    files= []
    for marker in markers:
        files.append(marker.logfile)
    return files


def test_detection():

    cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
    markers = [ArucoMarker(marker_id, datetime.datetime.now()) for marker_id in range(1, 5)] 
        
    while(cap.isOpened()):
        ret, frame = cap.read()
        for marker in markers:
            frame = marker.update_marker(frame, 1)
        
        cv2.imshow('Markers Detection', frame)

        if not ret:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        

    # Release everything if job is finished
    cap.release()
    cv2.destroyAllWindows()

