from src.MyMainWindow import MyWindow
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = MyWindow()
    Window.show()
    sys.exit(app.exec_())
