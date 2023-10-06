import sys
from PyQt5 import QtWidgets, QtCore
from libdb import LibraryDatabase
from landing import LandingPage
from libdb import LibraryDatabase


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_DisableWindowContextHelpButton)
    db = LibraryDatabase()
    landing_page = LandingPage(db)
    landing_page.show()
    
    sys.exit(app.exec_())
