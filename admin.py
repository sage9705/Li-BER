from PyQt5 import QtWidgets, QtCore
import os

class AdminMainWindow(QtWidgets.QMainWindow):
    def __init__(self, username, db=None):
        super().__init__()
        self.setWindowTitle("Li-BER - Admin")
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
        welcome_label = QtWidgets.QLabel(f"Welcome, {self.username} (Admin)")
        main_layout.addWidget(welcome_label)

        add_book_button = QtWidgets.QPushButton("Add Book")
        add_book_button.clicked.connect(self.open_add_book_dialog)
        main_layout.addWidget(add_book_button)

        delete_book_button = QtWidgets.QPushButton("Delete Book")
        delete_book_button.clicked.connect(self.open_delete_book_dialog)  # button click event connection
        main_layout.addWidget(delete_book_button)

        # main layout
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def open_add_book_dialog(self):
        dialog = self.AddBookDialog(self)  # Pass self as the parent
        dialog.exec_()    

    def open_delete_book_dialog(self):
        dialog = self.DeleteBookDialog(self)  # Pass self as the parent
        dialog.exec_()

    class AddBookDialog(QtWidgets.QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Add Book")
            self.setStyleSheet("background-color: white;")
            self.title_entry = QtWidgets.QLineEdit()
            self.author_entry = QtWidgets.QLineEdit()
            self.isbn_entry = QtWidgets.QLineEdit()
            self.genre_entry = QtWidgets.QLineEdit()
            self.year_entry = QtWidgets.QLineEdit()
            self.publisher_entry = QtWidgets.QLineEdit()
            self.total_copies_entry = QtWidgets.QLineEdit()
            self.description_entry = QtWidgets.QTextEdit()
            self.create_widgets()

        def create_widgets(self):
            label = QtWidgets.QLabel("Please enter book details:")
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")

            title_label = QtWidgets.QLabel("Title:")
            author_label = QtWidgets.QLabel("Author:")
            isbn_label = QtWidgets.QLabel("ISBN:")
            genre_label = QtWidgets.QLabel("Genre:")
            year_label = QtWidgets.QLabel("Publication Year:")
            publisher_label = QtWidgets.QLabel("Publisher:")
            total_copies_label = QtWidgets.QLabel("Total Copies:")
            description_label = QtWidgets.QLabel("Description (optional):")

            add_button = QtWidgets.QPushButton("Add Book")
            add_button.setStyleSheet("""
                QPushButton {
                    background-color: #70c883;
                    color: white;
                    font-size: 14px;
                    padding: 8px 16px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #58a86c;
                }
            """)
            add_button.clicked.connect(self.add_book)

            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(label)
            layout.addWidget(title_label)
            layout.addWidget(self.title_entry)
            layout.addWidget(author_label)
            layout.addWidget(self.author_entry)
            layout.addWidget(isbn_label)
            layout.addWidget(self.isbn_entry)
            layout.addWidget(genre_label)
            layout.addWidget(self.genre_entry)
            layout.addWidget(year_label)
            layout.addWidget(self.year_entry)
            layout.addWidget(publisher_label)
            layout.addWidget(self.publisher_entry)
            layout.addWidget(total_copies_label)
            layout.addWidget(self.total_copies_entry)
            layout.addWidget(description_label)
            layout.addWidget(self.description_entry)
            layout.addWidget(add_button)
            self.setLayout(layout)

        def get_book_details(self):
            title = self.title_entry.text()
            author = self.author_entry.text()
            isbn = self.isbn_entry.text()
            genre = self.genre_entry.text()
            year = self.year_entry.text()
            publisher = self.publisher_entry.text()
            total_copies = self.total_copies_entry.text()
            description = self.description_entry.toPlainText()
            
            keywords = [keyword.strip() for keyword in self.keywords_entry.text().split(',')]
            cover_image_url = self.cover_image_url_entry.text()
            
            return {
                "title": title,
                "author": author,
                "isbn": isbn,
                "genre": genre,
                "year": year,
                "publisher": publisher,
                "total_copies": int(total_copies),  # Convert total_copies to integer
                "description": description,
                "keywords": keywords,  # Add keywords field
                "cover_image_url": cover_image_url  # Add cover_image_url field
            }

        def add_book(self):
            try:
                book_details = self.get_book_details()
                # Check if all required book details are provided
                if not all(book_details.values()):
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Incomplete Information",
                        "Please fill in all the book details.",
                        QtWidgets.QMessageBox.Ok
                    )
                else:
                    success = self.db.add_book(book_details)
                    if success:
                        QtWidgets.QMessageBox.information(
                            self,
                            "Book Added",
                            "The book has been successfully added to the library.",
                            QtWidgets.QMessageBox.Ok
                        )
                        self.accept()
                    else:
                        QtWidgets.QMessageBox.warning(
                            self,
                            "Error",
                            "An error occurred while adding the book to the library.",
                            QtWidgets.QMessageBox.Ok
                        )
            except Exception as e:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Error",
                    f"An error occurred while adding the book: {str(e)}",
                    QtWidgets.QMessageBox.Ok
                )


    class DeleteBookDialog(QtWidgets.QDialog):
        def __init__(self, db, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Delete Book")
            self.setStyleSheet("background-color: white;")
            self.db = db  
            self.book_id_entry = QtWidgets.QLineEdit()
            self.create_widgets()

        def create_widgets(self):
            label = QtWidgets.QLabel("Please enter the Book ID to delete:")
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")

            book_id_label = QtWidgets.QLabel("Book ID:")

            delete_button = QtWidgets.QPushButton("Delete Book")
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: #e84a4a;
                    color: white;
                    font-size: 14px;
                    padding: 8px 16px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #a85858;
                }
            """)
            delete_button.clicked.connect(self.delete_book)

            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(label)
            layout.addWidget(book_id_label)
            layout.addWidget(self.book_id_entry)
            layout.addWidget(delete_button)
            self.setLayout(layout)

        def get_book_id(self):
            return self.book_id_entry.text()

        def delete_book(self):
            try:
                book_id = self.get_book_id()

                if not book_id:
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Missing Book ID",
                        "Please enter the Book ID to delete.",
                        QtWidgets.QMessageBox.Ok
                    )
                else:
                    success = self.db.delete_book(book_id)
                    if success:
                        QtWidgets.QMessageBox.information(
                            self,
                            "Book Deleted",
                            "The book has been successfully deleted from the library.",
                            QtWidgets.QMessageBox.Ok
                        )
                        self.accept()
                    else:
                        QtWidgets.QMessageBox.warning(
                            self,
                            "Error",
                            "An error occurred while deleting the book from the library.",
                            QtWidgets.QMessageBox.Ok
                        )
            except Exception as e:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Error",
                    f"An error occurred while deleting the book: {str(e)}",
                    QtWidgets.QMessageBox.Ok
                )
