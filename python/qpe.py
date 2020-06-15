"""
Created by Zack Miller
Version 

Contact: zdmiller12@gmail.com
""" 

import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

from mainHandler import MainHandler

qtCreatorFile = os.path.join(".", "resource", "qpe_mainWindow.ui")
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class QPE(QMainWindow, Ui_MainWindow, MainHandler):
    def __init__(self, parent=None):
        self.books  = ["SEA", "STEA"]
        self.qpe_directory = os.path.dirname(os.path.realpath(__file__))
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        MainHandler.__init__(self)
        self.setupUi(self)
        self.showMaximized()
        #
        ##
        ###
        ##    SIGNALS
        #
        #
        self.comboBox_book.currentTextChanged.connect(self.dialog_update_SLOT)
        self.pushButton_save.clicked.connect(self.save_exercises_SLOT)
        self.pushButton_solve.clicked.connect(self.solve_exercises_SLOT)
        self.spinBox_chapter.valueChanged.connect(self.dialog_update_SLOT)
        self.spinBox_problem.valueChanged.connect(self.dialog_update_SLOT)
        #
        ##
        ###
    #######
    ###
    ##    SLOTS
    #
    def dialog_update_SLOT(self):
        self.update_tables()
        self.update_labels()
        
    def save_exercises_SLOT(self):
        self.show_status_message(self.save_exercises())

    def solve_exercises_SLOT(self):
        self.show_status_message(self.solve_exercises())
        self.dialog_update_SLOT()


if __name__ == '__main__':
    # # for windows screen
    # from win32api import GetSystemMetrics
    # print("Width =", GetSystemMetrics(0))
    # print("Height =", GetSystemMetrics(1))

    # this may not work with windows/mac
    app      = QApplication(sys.argv)
    screen   = app.desktop().screenGeometry()
    w, h     = screen.width(), screen.height()
    qpe_main = QPE()

    # minimized
    # gallery.move( (0.4*w)-(0.1*h), 0.1*h )
    # gallery.resize( 0.6*w, 0.6*h )

    # 
    qpe_main.show()
    app.exec()
    #sys.exit( app.exec_() )
    