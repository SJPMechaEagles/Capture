import PyQt5.QtGui
from camera import *

import sys

from gui import *

if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    camera = Camera()
    camera.iniCamera()
    camera.startVid()
    
    window = VideoWindow(camera)
    window.resize(1000, 600)
    window.show()
    
    #run the app
    returnCode = app.exec_()
    camera.stopRecording()
    print("stopped")
    sys.exit(returnCode)