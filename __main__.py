import PyQt5.QtGui
from camera import *

import sys

from gui import *
from datasource import *
from tournamentDialogs import *

if __name__ == '__main__':
    #create_test_tournament()
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    camera = Camera()
    camera.iniCamera()
    camera.startVid()
    
    window = VideoWindow(camera)
    window.resize(1600, 900)
    window.show()

    #run the app
    returnCode = app.exec_()
    camera.stopRecording()
    print("stopped")
    sys.exit(returnCode)