import cv2

# Read a video file
cap = cv2.VideoCapture('vids/video_2025-12-02_10-35-58.avi')

# Check if the video file was opened successfully
if not cap.isOpened():
    print("Error: Unable to open video file")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Unable to read frame from video file")
        exit()

    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()