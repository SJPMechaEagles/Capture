from PyQt5.QtMultimedia import QMediaRecorder, QCamera, QCameraInfo, QCameraViewfinderSettings, QAudioEncoderSettings, QVideoEncoderSettings, QCameraImageCapture
import PyQt5.QtMultimedia as QtMultimedia
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
import PyQt5.QtWidgets
import PyQt5.QtGui
from PyQt5.QtCore import QUrl, QObject

import time
import sys
import os
import pathlib

class Camera(QObject):
    def __init__(self, parent=QObject()):
        super(Camera, self).__init__(parent)
        # chooses the system default camera
        self.cam = QCamera()
        self.caminfo = QCameraInfo(self.cam)
        self.camvfind = QCameraViewfinder()
        self.camvfindset = QCameraViewfinderSettings()
        self.recorder = QMediaRecorder(self.cam)

    def iniCamera(self):
    	cameras = QCameraInfo.availableCameras()
    	for cameraInfo in cameras:
    		# select the capturing device if it is available
    		if(cameraInfo.description().find("Capture") is not -1):
    			self.cam = QCamera(cameraInfo)
    			self.caminfo = QCameraInfo(self.cam)
    			self.recorder = QMediaRecorder(self.cam)
    	print("Camera Chosen: " + self.caminfo.description())
    	print(self.cam.supportedViewfinderFrameRateRanges())
    	if self.cam.isCaptureModeSupported(QCamera.CaptureVideo):
            print("Capturemode supported")

    def startVid(self):
        self.cam.load()
        # self.camvfind.show()
        self.cam.setViewfinder(self.camvfind)
        self.cam.setCaptureMode(QCamera.CaptureVideo)
        self.cam.start()

        audio = QAudioEncoderSettings()
        audio.setCodec("audio/amr")
        audio.setQuality(QtMultimedia.QMultimedia.NormalQuality)
        video = QVideoEncoderSettings()
        # video.setCodec("video/mp4")
        video.setQuality(QtMultimedia.QMultimedia.NormalQuality)
        video.setResolution(1920, 1080)
        video.setFrameRate(30.0)
        # self.recorder.setAudioSettings(audio)
        self.recorder.setVideoSettings(video)
        self.recorder.setContainerFormat("mp4")

        # print(self.recorder.supportedVideoCodecs())
        # print(self.recorder.state())
        # print(self.recorder.error())
        print(self.recorder.outputLocation())
        
    def startRecording(self):
        directory = os.path.abspath(str(os.getcwd()))
        filename = "test" + str(time.time()) + ".mp4"
        abs_path = os.path.join(directory, filename)
        self.recorder.setOutputLocation(QUrl(abs_path))
        self.recorder.record()

    def stopRecording(self):
        self.recorder.stop()
        
    def getViewFinder(self):
    	return self.camvfind
    	
class VideoWindow(PyQt5.QtWidgets.QMainWindow):
    def __init__(self, camera, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.camera = camera
        #quit on alt+f4 or ctrl+w
        self.shortcut = PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence.Close, self)
        self.shortcut.activated.connect(self.onQuit)
        #by default, camera recording is off
        self.isRecording = False
        # Create a widget for window contents
        centralWidget = PyQt5.QtWidgets.QWidget(self)
        self.setCentralWidget(centralWidget)
        
        #create the bottom control layout with buttons
        self.recordButton = PyQt5.QtWidgets.QPushButton()
        self.recordButton.setIcon(self.style().standardIcon(PyQt5.QtWidgets.QStyle.SP_MediaPlay))
        self.recordButton.setStyleSheet('QPushButton {background-color: #26c6da}')
        self.recordButton.clicked.connect(self.toggleRecording)
        controlLayout = PyQt5.QtWidgets.QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.recordButton)
        
        #create the mainlayout that contains the viewfiner and controls
        mainLayout = PyQt5.QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.camera.getViewFinder())
        mainLayout.addLayout(controlLayout)
        
        #apply the mainlayout
        centralWidget.setLayout(mainLayout)
        
    def toggleRecording(self):
        if (self.isRecording):
            self.stopRecording()
        else:
            self.startRecording()
            
    def startRecording(self):
        self.camera.startRecording()
        self.recordButton.setIcon(self.style().standardIcon(PyQt5.QtWidgets.QStyle.SP_MediaStop))
        #recording color: red
        self.recordButton.setStyleSheet('QPushButton {background-color: #e57373}')
        self.isRecording = True
    
    def stopRecording(self):
        self.camera.stopRecording()
        self.recordButton.setIcon(self.style().standardIcon(PyQt5.QtWidgets.QStyle.SP_MediaPlay))
        #default color: cyan
        self.recordButton.setStyleSheet('QPushButton {background-color: #26c6da}')
        self.isRecording = False
    
    def onQuit(self):
        self.stopRecording()
        self.close()

if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    camera = Camera()
    camera.iniCamera()
    camera.startVid()
    print("start")
    
    window = VideoWindow(camera)
    window.resize(1000, 600)
    window.setWindowTitle('Match Recorder')
    window.show()
    
    #run the app
    returnCode = app.exec_()
    camera.stopRecording()
    print("stopped")
    sys.exit(returnCode)