__appname__ = "hl2mt"
__module__ = "main"

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui import mainWindow, foldersDialog, colorsDialog, indexingDialog, outputDialog, propertiesDialog
import os
from herolab import HeroLabIndex, HeroLab


class Main(QMainWindow, mainWindow.Ui_mainWindow):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(__appname__)

        self.load_initial_settings()

        self.actionExit.triggered.connect(self.close)
        self.actionFolders.triggered.connect(self.action_folders_triggered)
        self.actionProperties.triggered.connect(self.action_properties_triggered)
        self.actionColors.triggered.connect(self.action_colors_triggered)
        self.actionIndexing.triggered.connect(self.action_indexing_triggered)
        self.actionOutput.triggered.connect(self.action_output_triggered)
        self.actionImport.triggered.connect(self.action_import_triggered)
        self.actionSave.triggered.connect(self.action_save_triggered)

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

    def action_folders_triggered(self):
        dialog = FoldersDialog(self, self.settings)
        if dialog.exec_():
            self.settings = dialog.settings

    def action_properties_triggered(self):
        dialog = PropertiesDialog(self, self.settings)
        if dialog.exec_():
            self.settings = dialog.settings

    def action_colors_triggered(self):
        dialog = ColorsDialog(self, self.settings)
        if dialog.exec_():
            self.settings = dialog.settings

    def action_indexing_triggered(self):
        dialog = IndexingDialog(self, self.settings)
        if dialog.exec_():
            self.settings = dialog.settings

    def action_output_triggered(self):
        dialog = OutputDialog(self, self.settings)
        if dialog.exec_():
            self.settings = dialog.settings

    def action_import_triggered(self):
        filename = QFileDialog.getOpenFileName(self, __appname__ + ": Import Config", os.getcwd(),
                                               filter="Conf files (*.conf)")
        if filename != '':
            print filename

    def action_save_triggered(self):
        filename = QFileDialog.getSaveFileName(self, __appname__ + ": Save Config As...", os.getcwd(),
                                               filter="Conf files (*.conf)")
        if filename != '':
            print filename


class FoldersDialog(QDialog, foldersDialog.Ui_foldersDialog):

    def __init__(self, parent, settings):
        super(FoldersDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(__appname__ + ": Token Folders")
        self.settings = settings

        self.buttonInput.clicked.connect(self.button_input_clicked)
        self.buttonPortrait.clicked.connect(self.button_portrait_clicked)
        self.buttonPOG.clicked.connect(self.button_pog_clicked)
        self.buttonOutput.clicked.connect(self.button_output_clicked)

        self.load_settings()

    def load_settings(self):
        self.editInput.setText(self.settings.value("folderInput").toString())
        self.editPortrait.setText(self.settings.value("folderPortrait").toString())
        self.editPOG.setText(self.settings.value("folderPOG").toString())
        self.editOutput.setText(self.settings.value("folderOutput").toString())

    def button_input_clicked(self):
        folder = QFileDialog.getExistingDirectory(self, "Input Folder", self.settings.value("folderInput").toString(),
                                                  QFileDialog.ShowDirsOnly)
        if folder != '':
            self.settings.setValue("folderInput", folder)
            self.load_settings()

    def button_portrait_clicked(self):
        folder = QFileDialog.getExistingDirectory(self, "Portrait Folder",
                                                  self.settings.value("folderPortrait").toString(),
                                                  QFileDialog.ShowDirsOnly)
        if folder != '':
            self.settings.setValue("folderPortrait", folder)
            self.load_settings()

    def button_pog_clicked(self):
        folder = QFileDialog.getExistingDirectory(self, "POG Folder", self.settings.value("folderPOG").toString(),
                                                  QFileDialog.ShowDirsOnly)
        if folder != '':
            self.settings.setValue("folderPOG", folder)
            self.load_settings()

    def button_output_clicked(self):
        folder = QFileDialog.getExistingDirectory(self, "Output Folder", self.settings.value("folderOutput").toString(),
                                                  QFileDialog.ShowDirsOnly)
        if folder != '':
            self.settings.setValue("folderOutput", folder)
            self.load_settings()


class PropertiesDialog(QDialog, propertiesDialog.Ui_propertiesDialog):

    def __init__(self, parent, settings):
        super(PropertiesDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(__appname__ + ": Token Properties")
        self.settings = settings

        self.load_settings()

    def load_settings(self):
        # TODO Make sure all the below have default values
        self.editAC.setText(self.settings.value("properties/AC").toString())
        self.editACFlat.setText(self.settings.value("properties/ACFlat").toString())
        self.editACTouch.setText(self.settings.value("properties/ACTouch").toString())
        self.editAlignment.setText(self.settings.value("properties/Alignment").toString())
        self.editBAB.setText(self.settings.value("properties/BAB").toString())
        self.editStr.setText(self.settings.value("properties/Strength").toString())
        self.editDex.setText(self.settings.value("properties/Dexterity").toString())
        self.editCon.setText(self.settings.value("properties/Constitution").toString())
        self.editInt.setText(self.settings.value("properties/Intelligence").toString())
        self.editWis.setText(self.settings.value("properties/Wisdom").toString())
        self.editCha.setText(self.settings.value("properties/Charisma").toString())
        self.editCMB.setText(self.settings.value("properties/CMB").toString())
        self.editCMD.setText(self.settings.value("properties/CMD").toString())
        self.editCMDFlat.setText(self.settings.value("properties/CMDFlat").toString())
        self.editPlayer.setText(self.settings.value("properties/Player").toString())
        self.editRace.setText(self.settings.value("properties/Race").toString())
        self.editMelee.setText(self.settings.value("properties/Melee").toString())
        self.editRanged.setText(self.settings.value("properties/Ranged").toString())
        self.editSpeed.setText(self.settings.value("properties/Speed").toString())
        self.editName.setText(self.settings.value("properties/Name").toString())
        self.editPropName.setText(self.settings.value("properties/PropName").toString())
        self.editHP.setText(self.settings.value("properties/HP").toString())
        self.editHPMax.setText(self.settings.value("properties/HPMax").toString())


class ColorsDialog(QDialog, colorsDialog.Ui_colorsDialog):

    def __init__(self, parent, settings):
        super(ColorsDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(__appname__ + ": Macro Colors")
        self.settings = settings


class IndexingDialog(QDialog, indexingDialog.Ui_indexDialog):

    def __init__(self, parent, settings):
        super(IndexingDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(__appname__ + ": Indexing Options")
        self.settings = settings


class OutputDialog(QDialog, outputDialog.Ui_outputDialog):

    def __init__(self, parent, settings):
        super(OutputDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(__appname__ + ": Token Output Options")
        self.settings = settings


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
