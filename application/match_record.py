import sys
from application.gui import *

app = QApplication(sys.argv)
ex = MainPage()
sys.exit(app.exec_())