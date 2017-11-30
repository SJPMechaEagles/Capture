import numpy as np
import cv2
from time import sleep, gmtime, strftime

import sys
from imaging import ImageGrabber, ImageSaver

def startVideo(cap, out_width, out_height, disp_width, disp_height, RECORD_FPS, out, vid):
    
    #fourcc = cv2.VideoWriter_fourcc(*'avc1')
    fourcc = cv2.VideoWriter_fourcc(*'divx')
    out = cv2.VideoWriter(out, fourcc, RECORD_FPS, (out_width, out_height), RECORD_FPS)
    grabber = ImageGrabber(cap)
    writer = ImageSaver(grabber, out, (out_width, out_height), RECORD_FPS)

    #starts grabbing and recording
    grabber.start()
    writer.start()

    frame = grabber.getLatest()
    while(frame is None):
        frame = grabber.getLatest()
        vid.update(frame)
        sleep(0.2)
        continue
    
    while(True):
        sleep(.5)
        # When everything done, release the capture, also quit on control-C
        try:
            if (cv2.waitKey(500) & 0xFF == ord('q')):
                cap.release()
                out.release()
                cv2.destroyAllWindows()
                break
        except KeyboardInterrupt:
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            break


# Define the codec and create VideoWriter object
#FPS = 60.0
RECORD_FPS = 5.0
WIDTH = 1920
HEIGHT = 1080
OUT_WIDTH = 1280
OUT_HEIGHT = 720
DISP_WIDTH = 800
DISP_HEIGHT = 450
RECORD_FPS = 5

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,HEIGHT)
cap.set(cv2.CAP_PROP_FPS, RECORD_FPS)

print("Please type in the match number:")
match_number = int(input())
datetime = strftime("%Y%m%d_%H%M%S_Match_", gmtime())
filename = datetime + str(match_number) + ".avi"
print("The filename is: " + filename + "\nPlease press 'q' inside the video window to end the recording'")

startVideo(cap, OUT_WIDTH, OUT_HEIGHT, DISP_WIDTH, DISP_HEIGHT, RECORD_FPS, filename, vid)
sys.exit(app.exec_())