
import sys

from PySide.QtCore import QEvent, Qt, QObject
from PySide.QtGui import QApplication, QMainWindow, QLineEdit, QLabel, QMessageBox
from PySide.QtGui import QVBoxLayout, QPushButton, QWidget

import maliit.client as maliit

class ActionKeyFilter(QObject):

    def __init__(self, login, password, parent):
        QObject.__init__(self, parent)

        self.loginEdit = login
        self.passwordEdit = password

    def eventFilter(self, obj, event):
        if not event:
            return False

        if event.type() != QEvent.KeyPress:
            return False

        if event.key() not in (Qt.Key_Return, Qt.Key_Enter):
            return False

        print "Obj", obj
        if obj == self.loginEdit:
            print "Changing focus"
            self.passwordEdit.setFocus(Qt.OtherFocusReason)
        elif obj == self.passwordEdit:
            message = ""
            icon = None

            if not (self.loginEdit.text() or self.passwordEdit.text()):
                message = "Please enter your credentials"
                icon = QMessageBox.Warning
            else:
                message = "Login Successfull"
                icon = QMessageBox.Information

            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.addButton("OK", QMessageBox.AcceptRole)
            messageBox.setIcon(icon)
            messageBox.exec_()

        return False





class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.loginExtension = maliit.AttributeExtension()
        self.passwordExtension = maliit.AttributeExtension()

        self.setWindowTitle("Maliit key override test application")

        vbox = QVBoxLayout()

        # Steals focus from text edit, hiding the virtual keyboard
        hideVkb = QPushButton("Hide virtual keyboard")
        vbox.addWidget(hideVkb)

        loginLabel = QLabel("Login:")
        loginEdit = QLineEdit()
        passwordLabel = QLabel("Password:")
        passwordEdit = QLineEdit()
        keyFilter = ActionKeyFilter(loginEdit, passwordEdit, self)

        loginEdit.installEventFilter(keyFilter)
        loginEdit.setProperty(maliit.InputMethodQuery.getAttributeExtensionId(),
                              self.loginExtension.id())
        self.loginExtension.setAttribute("/keys/actionKey/label", "Next")

        passwordEdit.installEventFilter(keyFilter)
        passwordEdit.setProperty(maliit.InputMethodQuery.getAttributeExtensionId(),
                                self.passwordExtension.id())
        self.passwordExtension.setAttribute("/keys/actionKey/label", "Login")
        passwordEdit.setEchoMode(QLineEdit.Password)

        vbox.addWidget(loginLabel)
        vbox.addWidget(loginEdit)
        vbox.addWidget(passwordLabel)
        vbox.addWidget(passwordEdit)

        closeApp = QPushButton("Close Application")
        vbox.addWidget(closeApp)

        closeApp.clicked.connect(self.close)

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(vbox)

def main(argv=None):
    if argv is None:
        argv = sys.argv

    app = QApplication(argv)

    window = MainWindow()
    window.show()

    return app.exec_()

if __name__ == '__main__':
    main()
