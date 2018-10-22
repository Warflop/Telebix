from PyQt4 import QtCore, QtGui
from daemon import Daemon
import sys
import time
import jobs

def start_program():

    app = QtGui.QApplication(sys.argv)

    splash_pix = QtGui.QPixmap('resources/telebix_splash.png')
    splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setWindowIcon(QtGui.QIcon('resources/icon.png'))
    splash.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
    splash.setEnabled(False)
    Bar = QtGui.QProgressBar(splash)
    Bar.setMaximum(10)
    Bar.setGeometry(0, splash_pix.height() - 20, splash_pix.width(), 20)
    splash.show()

    for i in range(1, 11):
        Bar.setValue(i)
        t = time.time()
        while time.time() < t + 0.2:
            app.processEvents()

    splash.close()

    ui = jobs.App()
    ui.plot_conf()
    ui.init_button()
    ui.show()
    app.exec_()

class daemon_server(Daemon):
    def run(self):
        start_program()

daemon_service = daemon_server('/tmp/telebix.pid')

if __name__ == '__main__':

#    start_program()

    daemon_service.restart()