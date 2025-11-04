import numpy as np
#import icra_vision as iv
from ur_controller import UR
import time

#det = iv.detector(cam=1,model="none")
#det.collect_images(name="comp1")



#test robot connect
ur = UR("UR5e","169.254.217.10")
ur.connect()
currentPose = ur.recv.getActualTCPPose() #cartesian tool center point
newPos = np.array(currentPose)+np.array([0.02,0,0,0,0,0])
ur.move_pose_absolute(newPos.tolist())
time.sleep(1)
ur.move_pose_absolute(currentPose)
#det = iv.detector(cam=1,model="runs/detect/gc_train/weights/best.pt")
#while True:
#    cal_obj = det.calibration_image(labels=["beans"])
#    input("Homing on {}, press enter to continue".format(cal_obj))
#    offset = det.home_on_object(ur,cal_obj,labels=["beans"])
#    input("Found offset {}, press enter to go again".format(offset))

#test object homing
#ur = UR("UR5e","169.254.217.10")
#ur.connect()
#det = iv.detector(cam=1,model="runs/detect/gc_train/weights/best.pt")
#while True:
#    cal_obj = det.calibration_image(labels=["beans"])
#    input("Homing on {}, press enter to continue".format(cal_obj))
#    offset = det.home_on_object(ur,cal_obj,labels=["beans"])
#    input("Found offset {}, press enter to go again".format(offset))


##test marker homing
#ur = UR("UR5e","169.254.217.10")
#ur.connect()
#det = iv.detector(cam=1,model="none")
#while True:
#    cal_marker = det.calibration_marker(marker_id=0)
#    input("Homing on {}, press enter to continue".format(cal_marker))
#    offset = det.home_on_marker(ur,cal_marker)
#    input("Found offset {}, press enter to go again".format(offset))


#test detector only
#det = iv.detector(cam=1,model="runs/detect/gc_train/weights/best.pt")
#det = iv.detector(cam=1,model="best(2).pt")
#while True:
#    cal_obj = det.calibration_image(labels=["all"])

#test button detector only
# det = iv.detector(cam=1,model="best_button.pt")
# while True:
#     cal_obj = det.calibration_image(labels=["inductionbutton"])


##test marker only
#det = iv.detector(cam=1,model="none")
#while True:
#    cal_marker = det.calibration_marker(marker_id=0)
#    input("Found marker: {}, press enter to go again".format(cal_marker))


##gather training images
#det.collect_images()


##train on roboflow labelled dataset
#det.train(name="beanfinder8000.v2i.yolov8",epochs=3)
