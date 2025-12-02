import cv2
import time

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('vids/output.avi', fourcc, 260.0, (640, 360))
num_frames = 100

    
while(cap.isOpened()):
    start = time.time()
    for i in range(num_frames):
        ret, frame = cap.read()
        if ret==True:
            out.write(frame)
            cv2.imshow('frame',frame)

        else:
            break
        if not ret:
            break
    end = time.time()

    fps = num_frames / (end - start)
    print(f"Actual FPS: {fps:.2f}")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()