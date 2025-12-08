import cv2
import datetime
import pandas as pd
from config import *

def film_thread(ready_event, stop_event, video_file):
    df_log = pd.DataFrame(columns= ['frame_id', 'Timestamp'])
    frame_count = 0
    try:
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW) # 1 is the secondary camera 
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        start = datetime.datetime.now()
        filename = f"vids/video_{start.strftime('%Y-%m-%d_%H-%M-%S-%f')}.avi"
        out = cv2.VideoWriter(filename, fourcc, CAM_FPS, (640, 360)) #make sure the framesize aligns with the camera
        ready_event.set()
        while((cap.isOpened()) and (not stop_event.is_set())):
            time= datetime.datetime.now()
            ret, frame = cap.read()
            if ret==True:
                frame_count +=1
                df_log.loc[len(df_log)] = [frame_count, time]
                out.write(frame)
                cv2.imshow('frame',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    stop_event.set()
                    break
            else:
                break

        #realse everything (needed, if interruped before the files dont work)
        video_file[0] = filename
        print(filename)
        df_log.to_csv(f"logs/marker/time_log{start.strftime('%Y-%m-%d_%H-%M-%S')}.csv")
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        
    except Exception as e:
        print(f"video failure:", e)