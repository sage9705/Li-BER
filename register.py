import datetime
from PyQt5 import QtWidgets, QtCore
import os

class RegisterDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.setWindowTitle("Register")
        
        css_file_path = os.path.join(os.path.dirname(__file__), "styles.css")
        with open(css_file_path, "r") as f:
            stylesheet = f.read()
        
        self.setStyleSheet(stylesheet)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.db = db  
        self.first_name_entry = QtWidgets.QLineEdit()
        self.middle_name_entry = QtWidgets.QLineEdit()
        self.last_name_entry = QtWidgets.QLineEdit()
        self.address_entry = QtWidgets.QLineEdit()
        self.email_entry = QtWidgets.QLineEdit()
        self.phone_entry = QtWidgets.QLineEdit()
        self.password_entry = QtWidgets.QLineEdit()
        self.password_entry.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_entry = QtWidgets.QLineEdit()
        self.confirm_entry.setEchoMode(QtWidgets.QLineEdit.Password)
        self.create_widgets()

    def create_widgets(self):
        label = QtWidgets.QLabel("Please enter your registration details:")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")

        first_name_label = QtWidgets.QLabel("First Name:")
        middle_name_label = QtWidgets.QLabel("Middle Name:")
        last_name_label = QtWidgets.QLabel("Last Name:")
        address_label = QtWidgets.QLabel("Address:")
        email_label = QtWidgets.QLabel("Email:")
        phone_label = QtWidgets.QLabel("Phone:")
        password_label = QtWidgets.QLabel("Password:")
        confirm_label = QtWidgets.QLabel("Confirm Password:")

        register_button = QtWidgets.QPushButton("Register")
        register_button.clicked.connect(self.register)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(first_name_label)
        layout.addWidget(self.first_name_entry)
        layout.addWidget(middle_name_label)
        layout.addWidget(self.middle_name_entry)
        layout.addWidget(last_name_label)
        layout.addWidget(self.last_name_entry)
        layout.addWidget(address_label)
        layout.addWidget(self.address_entry)
        layout.addWidget(email_label)
        layout.addWidget(self.email_entry)
        layout.addWidget(phone_label)
        layout.addWidget(self.phone_entry)
        layout.addWidget(password_label)
        layout.addWidget(self.password_entry)
        layout.addWidget(confirm_label)
        layout.addWidget(self.confirm_entry)
        layout.addWidget(register_button)
        self.setLayout(layout)

    def get_first_name(self):
        return self.first_name_entry.text()

    def get_middle_name(self):
        return self.middle_name_entry.text()

    def get_last_name(self):
        return self.last_name_entry.text()

    def get_address(self):
        return self.address_entry.text()

    def get_email(self):
        return self.email_entry.text()

    def get_phone(self):
        return self.phone_entry.text()

    def get_password(self):
        return self.password_entry.text()

    def get_confirm_password(self):
        return self.confirm_entry.text()

    def register(self):
        try:
            first_name = self.get_first_name()
            middle_name = self.get_middle_name()
            last_name = self.get_last_name()
            address = self.get_address()
            email = self.get_email()
            phone = self.get_phone()
            password = self.get_password()
            confirm_password = self.get_confirm_password()

            if not first_name or not last_name or not email or not phone or not password or not confirm_password:
                raise ValueError("Please fill in all the required fields.")
            if password != confirm_password:
                raise ValueError("Password and Confirm Password do not match.")
            # Use the LibraryDatabase instance to register the user
            if not self.db.is_email_taken(email):
                # email is not available, proceed with registration
                member_since = datetime.datetime.now().isoformat()  # Get current date and time
                success = self.db.register_user(
                    email, password, phone, first_name, middle_name, last_name, address, member_since
                )
                if success:
                    QtWidgets.QMessageBox.information(
                        self,
                        "Registration Successful",
                        "Registration successful. You can now log in.",
                        QtWidgets.QMessageBox.Ok
                    )
                    self.accept()
                else:
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Registration Failed",
                        "An error occurred during registration. Please try again later.",
                        QtWidgets.QMessageBox.Ok
                    )
            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Registration Failed",
                    "Email already exists. Please choose a different email address.",
                    QtWidgets.QMessageBox.Ok
                )
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Registration Failed",
                str(e),
                QtWidgets.QMessageBox.Ok
            )
