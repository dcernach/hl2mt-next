__appname__ = "hl2mt"
__module__ = "main"

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui import mainWindow
import os
from herolab import HeroLabIndex, HeroLab


class Main(QMainWindow, mainWindow.Ui_mainWindow):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(__appname__)

        self.load_initial_settings()

        self.actionExit.triggered.connect(self.close)


    def load_initial_settings(self):
        """Setup the initial values"""
        self.settings = QSettings(QSettings.NativeFormat, QSettings.UserScope, "Tarsis", "hl2mt")

        self.tableWidget.setColumnCount(6)
        self.tableWidget.hideColumn(0)
        self.tableWidget.hideColumn(1)
        self.tableWidget.setColumnWidth(2, 200)
        self.tableWidget.setColumnWidth(3, 300)
        self.tableWidget.setColumnWidth(4, 300)
        self.createButton.setDisabled(True)

        for opt in ['folderInput', 'folderPOG', 'folderOutput', 'folderPortrait']:
            if not self.settings.contains(opt):
                self.settings.setValue(opt, os.getcwd())

        for opt in ['vision', 'maneuvers', 'weapons', 'skills', 'hp', 'basicDice', 'items']:
            if not self.settings.contains(opt):
                self.settings.setValue(opt, False)

        if not self.settings.contains("indexing"):
            self.settings.setValue("indexing", "None")

        if not self.settings.contains("zipFile"):
            self.settings.setValue("zipFile", "HeroLabIndex.zip")

        if not self.settings.contains("httpBase"):
            self.settings.setValue("httpBase", "")

        if not self.settings.contains("properties/propName"):
            self.settings.setValue("properties/propName", "Basic")

        if not self.settings.contains("properties/characterName"):
            self.settings.setValue("properties/characterName", "Name")

        if not self.settings.contains("properties/HPMax"):
            self.settings.setValue("properties/HPMax", "HP")

        if not self.settings.contains("properties/speed"):
            self.settings.setValue("properties/HPMax", "Movement")

        for opt in ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma', 'race', 'alignment']:
            if not self.settings.contains("properties/" + opt):
                self.settings.setValue("properties/" + opt, opt.title())

        for opt in ['sheet', 'skills', 'attacks', 'hp', 'init', 'cmb', 'saves', 'specials', 'basic', 'maneuvers',
                    'sub']:
            if not self.settings.contains("colors/" + opt + "B"):
                self.settings.setValue("colors/" + opt + "B", "white")
            if not self.settings.contains("colors/" + opt + "F"):
                self.settings.setValue("colors/" + opt + "F", "black")



def main():
    QCoreApplication.setApplicationName("hl2mt")
    QCoreApplication.setApplicationVersion("0.1")
    QCoreApplication.setOrganizationName("Tarsis")
    QCoreApplication.setOrganizationDomain("tarsis.org")

    app = QApplication(sys.argv)
    program = Main()
    program.show()
    app.exec_()

if __module__ == "main":
    main()

