import os
import bcrypt 
from PyQt5 import QtWidgets, QtCore
from login import LoginDialog
from register import RegisterDialog
from user import UserMainWindow
from admin import AdminMainWindow

class LandingPage(QtWidgets.QWidget):
    def __init__(self, db):
        super().__init__()
        self.setWindowTitle("Li-BER")
        self.setMinimumSize(900, 700)
        
        css_file_path = os.path.join(os.path.dirname(__file__), "styles.css")
        with open(css_file_path, "r") as f:
            stylesheet = f.read()
        
        self.setStyleSheet(stylesheet)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        # horizontal layout for the buttons
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.setContentsMargins(20, 0, 20, 20)  # adjust margins for spacing
        buttons_layout.setSpacing(20)  # spacing between buttons
        welcome_label = self.create_title_label("Li-BER: Library Management System")
        login_button = QtWidgets.QPushButton("Login")
        login_button.setObjectName("login-button")  # Add the class name
        login_button.clicked.connect(self.login)

        register_button = QtWidgets.QPushButton("Register")
        register_button.setObjectName("register-button")  # Add the class name
        register_button.clicked.connect(self.register)
        buttons_layout.addWidget(login_button)
        buttons_layout.addWidget(register_button)

        # vertical layout for the entire page
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(welcome_label, alignment=QtCore.Qt.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # stretch to push the buttons to the bottom
        main_layout.addStretch(1)
        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

    def create_title_label(self, text):
        label = QtWidgets.QLabel(text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            margin-top: 300px;
            margin-bottom: 30px;
            font-weight: bold;
            color: rgb(0, 0, 0);
            text-align: center;
        """)
        return label

    def login(self):
        login_dialog = LoginDialog(self, self.db)
        result = login_dialog.exec_()
        if result == QtWidgets.QDialog.Accepted:
            print("Login successful")
            
    def register(self):
        register_dialog = RegisterDialog(self, self.db)
        result = register_dialog.exec_()
        if result == QtWidgets.QDialog.Accepted:
            print("Registration successful")
    
    def handle_login(self, email, password):
        if email:
            print(f"Logged in as: {email}")
            user = self.db.get_user_by_email(email)
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                if user['is_admin']:
                    admin_window = AdminMainWindow(user['username'])
                    admin_window.show()
                else:
                    user_window = UserMainWindow(user['username'])
                    user_window.show()
                self.hide()
            else:
                print("Login failed: Invalid email or password")
                QtWidgets.QMessageBox.warning(self, "Login", "Login failed: Invalid email or password")
        else:
            print("Login failed: Empty email")
            QtWidgets.QMessageBox.warning(self, "Login", "Login failed: Empty email")