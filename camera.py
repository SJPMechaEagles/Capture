import os

import PyQt5.QtMultimedia as QtMultimedia
from PyQt5.QtCore import QUrl, QObject
from PyQt5.QtMultimedia import QMediaRecorder, QCamera, QCameraInfo, QCameraViewfinderSettings, QAudioEncoderSettings, \
    QVideoEncoderSettings
from PyQt5.QtMultimediaWidgets import QCameraViewfinder


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
            if (cameraInfo.description().find("Capture") is not -1):
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

        print(self.recorder.outputLocation())

    def startRecording(self, filename):
        directory = os.path.abspath(str(os.getcwd()))
        abs_path = os.path.join(directory, filename)
        self.recorder.setOutputLocation(QUrl(abs_path))
        self.recorder.record()

    def stopRecording(self):
        self.recorder.stop()

    def getViewFinder(self):
        return self.camvfind