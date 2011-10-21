
import sys
import itertools

from PySide.QtCore import QObject, Qt
from PySide.QtGui import QApplication, QMainWindow, QPushButton
from PySide.QtGui import QWidget, QVBoxLayout, QTextEdit

import maliit.client as maliit

class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.orientations = itertools.cycle([maliit.Angle0, maliit.Angle90,
                                             maliit.Angle180, maliit.Angle270])

        currentOrientation = maliit.InputMethod.instance().orientationAngle()

        while self.orientations.next() != currentOrientation:
            pass

        self.rotateKeyboardButton = QPushButton()
        self.textEdit = QTextEdit()

        self.rotateKeyboardButton.clicked.connect(self.onRotateKeyboardClicked)

        self.setWindowTitle("Maliit test application")

        vbox = QVBoxLayout()
        self.rotateKeyboardButton.setText("Rotate keyboard")

        vbox.addWidget(self.rotateKeyboardButton)

        # Steals the focus when clicked
        hideVkb = QPushButton("Hide virtual keyboard")
        vbox.addWidget(hideVkb)
        vbox.addWidget(self.textEdit)

        self.rotateKeyboardButton.setFocusProxy(self.textEdit)

        closeApp = QPushButton("Close application")
        vbox.addWidget(closeApp)
        closeApp.clicked.connect(self.close)

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(vbox)

    def onRotateKeyboardClicked(self):
        maliit.InputMethod.instance().setOrientationAngle(self.orientations.next())

def main(argv=None):

    if argv is None:
        argv = sys.argv

    app = QApplication(argv)

    window = MainWindow()
    window.show()

    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())
