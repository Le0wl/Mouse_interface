import cv2
import datetime
from config import *

def film_thread(ready_event, stop_event, video_file):
    try:
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW) # 1 is the secondary camera 
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        start = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
        filename = f'vids/video_{start}.avi'
        out = cv2.VideoWriter(filename, fourcc, CAM_FPS, (640, 360)) #make sure the framesize aligns with the camera
        ready_event.set()
        while((cap.isOpened()) and (not stop_event.is_set())):
            ret, frame = cap.read()
            if ret==True:
                out.write(frame)
                cv2.imshow('frame',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    stop_event.set()
                    break
            else:
                break

        #realse everything (needed, if interruped before the files dont work)
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        video_file[0] = filename
        print(filename)
    except Exception as e:
        print(f"video failure:", e)