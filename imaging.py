from threading import Thread, Timer
from queue import Queue
import cv2
from time import sleep

class ImageGrabber(Thread):

    def __init__(self, video_capture):
        Thread.__init__(self)
        #thread goes down with the process
        self.cap = video_capture
        self.queue = Queue(maxsize=15)
        self.latest_frame = None
        self.daemon = True
        print ("Image grabber started")

    def getLatest(self):
        #return self.queue.get()
        return self.latest_frame
    
    def run(self):
        #keeps grabber images
        while True:
            ret, frame = self.cap.read()
            self.latest_frame = frame
            sleep(0.01)
            #self.queue.put(frame)
            #if(self.queue.full()):
                #print("Queue Full! Video encoding is slower than image grabber!")
            

class ImageSaver(Thread):

    #takes in a grabber and writes all frames to the video writer
    def __init__(self, image_grabber, video_writer, resolution, rec_fps):
        Thread.__init__(self)
        #thread goes down with the process
        self.writer = video_writer
        self.grabber = image_grabber
        self.resolution = resolution
        self.FONT = cv2.FONT_HERSHEY_SIMPLEX
        self.last_frame = None
        self.rec_fps = rec_fps
        
        self.daemon = True
        self.is_running = False
        #getting seconds per frame
        #MAGIC: function call lag
        MAGIC = 0.0683181689
        self.seconds_per_frame = (1.0 - MAGIC) / rec_fps

    def run(self):
        while(self.grabber.getLatest() is None):
            sleep(0.2)
        sleep(2)
        print ("Image saver started")
        while(True):
            worker = Thread(target=self.__encode_worker, args=[])
            worker.start()
            sleep(self.seconds_per_frame)
        #self.__start_timer()
            
    def __start_timer(self):
        if not self.is_running:
            self._timer = Timer(self.seconds_per_frame, self.__encode_latest)
            self._timer.start()
            self.is_running = True
            
    def __encode_latest(self):
        self.is_running = False
        self.__start_timer()
        #starts the worker to grab and encode a frame
        worker = Thread(target=self.__encode_worker, args=[self.grabber, self.writer, self.resolution])
        worker.start()
        
    def __encode_worker(self):
        try:
            frame = self.grabber.getLatest()
            out_frame = cv2.resize(frame, self.resolution)
            #cv2.putText(out_frame,'VEX Match 1',(10,500), self.FONT, 4,(255,255,255),2,cv2.LINE_AA)
            self.writer.write(out_frame)
            #stops the enocding unless signaled
        except:
            print ("stream not ready")
            pass
