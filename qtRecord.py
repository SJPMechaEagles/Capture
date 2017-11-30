from PyQt5.QtMultimedia import QMediaRecorder, QCamera, QCameraInfo, QCameraViewfinderSettings, QAudioEncoderSettings, QVideoEncoderSettings, QCameraImageCapture
import PyQt5.QtMultimedia as QtMultimedia
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
import PyQt5.QtWidgets
from PyQt5.QtCore import QUrl, QObject

import time
import sys

class Camera(QObject):
    def __init__(self, parent=QObject()):
        super(Camera, self).__init__(parent)
        self.cam = QCamera()
        self.caminfo = QCameraInfo(self.cam)
        self.camvfind = QCameraViewfinder()
        self.camvfindset = QCameraViewfinderSettings()
        self.recorder = QMediaRecorder(self.cam)

    def iniCamera(self):
        print(self.caminfo.description())
        print(self.caminfo.availableCameras())

        if self.cam.isCaptureModeSupported(QCamera.CaptureVideo):
            print("Capturemode supported")

    def startVid(self):
        self.cam.load()
        self.camvfind.show()
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
        path = "file:///Users/chrisjerrett/Desktop/jerretdata/cv_cap/test"
        self.recorder.setOutputLocation(QUrl(path + str(time.time()) + ".mp4"))
        self.recorder.record()

        print(self.recorder.supportedVideoCodecs())
        print(self.recorder.state())
        print(self.recorder.error())
        print(self.recorder.outputLocation())

    def stopRecording(self):
        self.recorder.stop()


if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    camera = Camera()
    camera.iniCamera()
    camera.startVid()
    print("start")
    returnCode = app.exec_()
    camera.stopRecording()
    print("stopped")
    sys.exit(returnCode)