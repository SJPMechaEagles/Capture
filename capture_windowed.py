import sys
from PyQt5 import QtCore, QtWidgets, QtGui, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtMultimedia import QCamera, QCameraInfo, QMediaObject, QCameraViewfinderSettings, QCameraImageCapture
from PyQt5.QtMultimediaWidgets import QCameraViewfinder


class Camera(QObject):
    def __init__(self, parent=QObject()):
        super(Camera, self).__init__(parent)
        self.cam = QCamera()
        self.caminfo = QCameraInfo(self.cam)
        self.camvfind = QCameraViewfinder()
        self.camvfindset = QCameraViewfinderSettings()
        self.cammode = self.cam.CaptureMode(0)
        self.camimgcap = QCameraImageCapture(self.cam)

    def iniCamera(self):
        print(self.caminfo.description())
        print(self.caminfo.availableCameras())

        if self.cam.isCaptureModeSupported(self.cammode):
            print("Capturemode supported")

    def startVid(self):
        self.cam.load()
        self.camvfindset.setResolution(1920, 1080)
        for frameRange in self.cam.supportedViewfinderFrameRateRanges():
            print(frameRange.maximumFrameRate)
        self.camvfindset.setMinimumFrameRate(24)
        self.camvfindset.setMaximumFrameRate(24)

        self.camvfind.show()
        self.cam.setViewfinder(self.camvfind)

        self.cam.setCaptureMode(self.cammode)
        self.cam.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    cam = Camera()
    cam.iniCamera()
    cam.startVid()

    del cam
    sys.exit(app.exec_())