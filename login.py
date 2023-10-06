from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
import os
from PyQt5.QtCore import pyqtSignal

class LoginDialog(QtWidgets.QDialog):
    login_successful = pyqtSignal(str)
    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.db = db  # database instance to the dialog
        self.email_entry = QtWidgets.QLineEdit()
        self.password_entry = QtWidgets.QLineEdit()
        self.password_entry.setEchoMode(QtWidgets.QLineEdit.Password)
        self.create_widgets()

        css_file_path = os.path.join(os.path.dirname(__file__), "styles.css")
        with open(css_file_path, "r") as f:
            stylesheet = f.read()
        
        self.setStyleSheet(stylesheet)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

    def create_widgets(self):
        label = QtWidgets.QLabel("Please enter your login credentials:")
        label.setAlignment(QtCore.Qt.AlignCenter)

        email_label = QtWidgets.QLabel("Email:")
        password_label = QtWidgets.QLabel("Password:")

        login_button = QtWidgets.QPushButton("Login")
        login_button.clicked.connect(self.login)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(email_label)
        layout.addWidget(self.email_entry)
        layout.addWidget(password_label)
        layout.addWidget(self.password_entry)
        layout.addWidget(login_button)
        self.setLayout(layout)

    def get_email(self):
        return self.email_entry.text()

    def get_password(self):
        return self.password_entry.text()

    def login(self):
        try:
            email = self.get_email()
            password = self.get_password()

           # verify the user's credentials
            if self.db.verify_user(email, password):
                self.accept()  # Login successful, close the dialog.
            else:
                QMessageBox.warning(
                    self,
                    "Login Failed",
                    "Invalid email or password. Please check your details.",
                    QMessageBox.Ok
                )
        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            QMessageBox.warning(
                self,
                "Login Failed",
                "An error occurred during login. Please check your details.",
                QMessageBox.Ok
            )


