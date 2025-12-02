import cv2
import datetime

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW) # 1 is the secondary camera 
fourcc = cv2.VideoWriter_fourcc(*'XVID')
start = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
out = cv2.VideoWriter(f'vids/video_{start}.avi', fourcc, 180.0, (640, 360)) #make sure the framesize aligns with the camera

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        out.write(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

#realse everything (needed, if interruped before the files dont work)
cap.release()
out.release()
cv2.destroyAllWindows()
