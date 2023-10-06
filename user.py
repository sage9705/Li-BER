from PyQt5 import QtWidgets, QtCore
import os

class UserMainWindow(QtWidgets.QMainWindow):
    def __init__(self, username, db=None):
        super().__init__()
        self.setWindowTitle("Library Management System - User")
        self.setMinimumSize(900, 700)
        
        css_file_path = os.path.join(os.path.dirname(__file__), "styles.css")
        with open(css_file_path, "r") as f:
            stylesheet = f.read()
        
        self.setStyleSheet(stylesheet)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.username = username
        self.db = db  

        self.create_widgets()

    def create_widgets(self):
        main_layout = QtWidgets.QVBoxLayout()
        welcome_label = QtWidgets.QLabel(f"Welcome, {self.username} (User)")
        main_layout.addWidget(welcome_label)

        # view available books
        view_books_button = QtWidgets.QPushButton("View Books")
        view_books_button.clicked.connect(self.view_books)
        main_layout.addWidget(view_books_button)

        # borrow a book
        borrow_book_button = QtWidgets.QPushButton("Borrow Book")
        borrow_book_button.clicked.connect(self.borrow_book)
        main_layout.addWidget(borrow_book_button)

        # return a book
        return_book_button = QtWidgets.QPushButton("Return Book")
        return_book_button.clicked.connect(self.return_book)
        main_layout.addWidget(return_book_button)

        # set the main layout
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)    

    def view_books(self):
        try:
            # fetch and display the available books from the database
            available_books = self.db.get_available_books()
            if available_books:
                book_list = "\n".join([f"{book['title']} by {book['author']}" for book in available_books])
                QtWidgets.QMessageBox.information(
                    self,
                    "Available Books",
                    f"Available Books:\n{book_list}",
                    QtWidgets.QMessageBox.Ok
                )
            else:
                QtWidgets.QMessageBox.information(
                    self,
                    "Available Books",
                    "No available books at the moment.",
                    QtWidgets.QMessageBox.Ok
                )
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Error",
                f"An error occurred while fetching available books: {str(e)}",
                QtWidgets.QMessageBox.Ok
            )

    def borrow_book(self):
        try:
            selected_book = self.select_book_to_borrow()  
            if selected_book:
                success = self.db.borrow_book(selected_book['book_id'], self.logged_in_user_id)
                if success:
                    QtWidgets.QMessageBox.information(
                        self,
                        "Borrow Book",
                        f"Successfully borrowed '{selected_book['title']}' by {selected_book['author']}.",
                        QtWidgets.QMessageBox.Ok
                    )
                else:
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Borrow Book",
                        "An error occurred while borrowing the book. Please try again later.",
                        QtWidgets.QMessageBox.Ok
                    )
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Error",
                f"An error occurred while borrowing the book: {str(e)}",
                QtWidgets.QMessageBox.Ok
            )

    def return_book(self):
        try:
            selected_book = self.select_book_to_return() 
            if selected_book:
                success = self.db.return_book(selected_book['transaction_id'])
                if success:
                    QtWidgets.QMessageBox.information(
                        self,
                        "Return Book",
                        f"Successfully returned '{selected_book['title']}' by {selected_book['author']}.",
                        QtWidgets.QMessageBox.Ok
                    )
                else:
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Return Book",
                        "An error occurred while returning the book. Please try again later.",
                        QtWidgets.QMessageBox.Ok
                    )
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Error",
                f"An error occurred while returning the book: {str(e)}",
                QtWidgets.QMessageBox.Ok
            )

