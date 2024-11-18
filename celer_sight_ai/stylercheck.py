from PyQt6 import QtCore, QtGui, QtWidgets, uic
import sys

# LoadedUi2 = uic.loadUi('C:\\Users\\manos\\Documents\\TestStylemain.ui')
class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        # LoadedUi = uic.loadUi('C:\\Users\\manos\\Documents/TestStylemain.ui', self)
        pass
        # self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec())
