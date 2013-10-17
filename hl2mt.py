__appname__ = "hl2mt"
__module__ = "main"

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui import mainWindow, foldersDialog, colorsDialog, indexingDialog, outputDialog, propertiesDialog
import os
import ConfigParser
from herolab import HeroLabIndex, HeroLab


class Main(QMainWindow, mainWindow.Ui_mainWindow):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(__appname__)

        self.load_initial_settings()
        self.check_defaults()

        self.actionExit.triggered.connect(self.close)
        self.actionFolders.triggered.connect(self.action_folders_triggered)
        self.actionProperties.triggered.connect(self.action_properties_triggered)
        self.actionColors.triggered.connect(self.action_colors_triggered)
        self.actionIndexing.triggered.connect(self.action_indexing_triggered)
        self.actionOutput.triggered.connect(self.action_output_triggered)
        self.actionImport.triggered.connect(self.action_import_triggered)
        self.actionSave.triggered.connect(self.action_save_triggered)

    # TODO Create a help trigger and dialog
    # TODO Create an About trigger and dialog

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

    def check_defaults(self):

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
            self.settings.setValue("properties/AC", dialog.editAC.text())
            self.settings.setValue("properties/ACFlat", dialog.editACFlat.text())
            self.settings.setValue("properties/ACTouch", dialog.editACTouch.text())
            self.settings.setValue("properties/Alignment", dialog.editAlignment.text())
            self.settings.setValue("properties/BAB", dialog.editBAB.text())
            self.settings.setValue("properties/Strength", dialog.editStr.text())
            self.settings.setValue("properties/Dexterity", dialog.editDex.text())
            self.settings.setValue("properties/Constitution", dialog.editCon.text())
            self.settings.setValue("properties/Intelligence", dialog.editInt.text())
            self.settings.setValue("properties/Wisdom", dialog.editWis.text())
            self.settings.setValue("properties/Charisma", dialog.editCha.text())
            self.settings.setValue("properties/CMB", dialog.editCMB.text())
            self.settings.setValue("properties/CMD", dialog.editCMD.text())
            self.settings.setValue("properties/CMDFlat", dialog.editCMDFlat.text())
            self.settings.setValue("properties/Player", dialog.editPlayer.text())
            self.settings.setValue("properties/Race", dialog.editRace.text())
            self.settings.setValue("properties/Melee", dialog.editMelee.text())
            self.settings.setValue("properties/Ranged", dialog.editRanged.text())
            self.settings.setValue("properties/Reach", dialog.editReach.text())
            self.settings.setValue("properties/Speed", dialog.editSpeed.text())
            self.settings.setValue("properties/Name", dialog.editName.text())
            self.settings.setValue("properties/PropName", dialog.editPropName.text())
            self.settings.setValue("properties/HP", dialog.editHP.text())
            self.settings.setValue("properties/HPMax", dialog.editHPMax.text())

    def action_colors_triggered(self):
        dialog = ColorsDialog(self, self.settings)
        if dialog.exec_():
            self.settings.setValue("colors/attacksf", dialog.comboAttacksF.currentText())
            self.settings.setValue("colors/attacksb", dialog.comboAttacksB.currentText())
            self.settings.setValue("colors/basicf", dialog.comboBasicF.currentText())
            self.settings.setValue("colors/basicb", dialog.comboBasicB.currentText())
            self.settings.setValue("colors/cmbf", dialog.comboCMBF.currentText())
            self.settings.setValue("colors/cmbb", dialog.comboCMBB.currentText())
            self.settings.setValue("colors/hpf", dialog.comboHPF.currentText())
            self.settings.setValue("colors/hpb", dialog.comboHPB.currentText())
            self.settings.setValue("colors/initf", dialog.comboInitF.currentText())
            self.settings.setValue("colors/initb", dialog.comboInitB.currentText())
            self.settings.setValue("colors/maneuversf", dialog.comboManF.currentText())
            self.settings.setValue("colors/maneuversb", dialog.comboManB.currentText())
            self.settings.setValue("colors/savesf", dialog.comboSavesF.currentText())
            self.settings.setValue("colors/savesb", dialog.comboSavesB.currentText())
            self.settings.setValue("colors/sheetf", dialog.comboSheetF.currentText())
            self.settings.setValue("colors/sheetb", dialog.comboSheetB.currentText())
            self.settings.setValue("colors/skillsf", dialog.comboSkillsF.currentText())
            self.settings.setValue("colors/skillsb", dialog.comboSkillsB.currentText())
            self.settings.setValue("colors/specialsf", dialog.comboSpecialsF.currentText())
            self.settings.setValue("colors/specialsb", dialog.comboSpecialsB.currentText())
            self.settings.setValue("colors/subf", dialog.comboSubF.currentText())
            self.settings.setValue("colors/subb", dialog.comboSubB.currentText())

    def action_indexing_triggered(self):
        dialog = IndexingDialog(self, self.settings)
        if dialog.exec_():
            self.settings.setValue("indexing", dialog.comboIndex.currentText())
            self.settings.setValue("httpbase", dialog.editURL.text())
            self.settings.setValue("zipfile", dialog.editZip.text())

    def action_output_triggered(self):
        dialog = OutputDialog(self, self.settings)
        if dialog.exec_():

            self.settings.setValue("weapons", dialog.checkAttack.isChecked())
            self.settings.setValue("vision", dialog.checkDark.isChecked())
            self.settings.setValue("basicDice", dialog.checkBasic.isChecked())
            self.settings.setValue("hp", dialog.checkHP.isChecked())
            self.settings.setValue("items", dialog.checkItems.isChecked())
            self.settings.setValue("maneuvers", dialog.checkMan.isChecked())
            self.settings.setValue("skills", dialog.checkSkill.isChecked())

    def action_import_triggered(self):
        filename = QFileDialog.getOpenFileName(self, __appname__ + ": Import Config", os.getcwd(),
                                               filter="Conf files (*.conf)")
        if filename != '' and os.path.isfile(filename):
            config = ConfigParser.ConfigParser()
            config.read(str(filename))
            for name, value in config.defaults().items():
                self.settings.setValue(name, value)

            self.check_defaults()

    def action_save_triggered(self):
        filename = QFileDialog.getSaveFileName(self, __appname__ + ": Save Config As...", os.getcwd(),
                                               filter="Conf files (*.conf)")
        if filename != '':
            config = ConfigParser.ConfigParser()
            for name in self.settings.allKeys():
                config.set('DEFAULT', str(name), self.settings.value(name).toString())

            with open(filename, 'wb') as cf:
                config.write(cf)
                cf.close()


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

        self.basicButton.clicked.connect(self.clicked_basic_button)
        self.defenseButton.clicked.connect(self.clicked_defense_button)
        self.miscButton.clicked.connect(self.clicked_misc_button)
        self.offenseButton.clicked.connect(self.clicked_offense_button)

        self.basicButton.click()

        self.load_settings()

    def clicked_basic_button(self):
        self.stackedWidget.setCurrentIndex(0)

    def clicked_offense_button(self):
        self.stackedWidget.setCurrentIndex(1)

    def clicked_defense_button(self):
        self.stackedWidget.setCurrentIndex(2)

    def clicked_misc_button(self):
        self.stackedWidget.setCurrentIndex(3)

    def load_settings(self):

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
        self.editReach.setText(self.settings.value("properties/Reach").toString())
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
        self.load_settings()

    def load_settings(self):

        self.comboAttacksF.setCurrentIndex(self.comboAttacksF.findText(self.settings.value("colors/attacksf").toString()))
        self.comboAttacksB.setCurrentIndex(self.comboAttacksB.findText(self.settings.value("colors/attacksb").toString()))
        self.comboBasicF.setCurrentIndex(self.comboBasicF.findText(self.settings.value("colors/basicf").toString()))
        self.comboBasicB.setCurrentIndex(self.comboBasicB.findText(self.settings.value("colors/basicb").toString()))
        self.comboCMBF.setCurrentIndex(self.comboCMBF.findText(self.settings.value("colors/cmbf").toString()))
        self.comboCMBB.setCurrentIndex(self.comboCMBB.findText(self.settings.value("colors/cmbb").toString()))
        self.comboHPF.setCurrentIndex(self.comboHPF.findText(self.settings.value("colors/hpf").toString()))
        self.comboHPB.setCurrentIndex(self.comboHPB.findText(self.settings.value("colors/hpb").toString()))
        self.comboInitF.setCurrentIndex(self.comboInitF.findText(self.settings.value("colors/initf").toString()))
        self.comboInitB.setCurrentIndex(self.comboInitB.findText(self.settings.value("colors/initb").toString()))
        self.comboManF.setCurrentIndex(self.comboManF.findText(self.settings.value("colors/maneuversf").toString()))
        self.comboManB.setCurrentIndex(self.comboManB.findText(self.settings.value("colors/maneuversb").toString()))
        self.comboSavesF.setCurrentIndex(self.comboSavesF.findText(self.settings.value("colors/savesf").toString()))
        self.comboSavesB.setCurrentIndex(self.comboSavesB.findText(self.settings.value("colors/savesb").toString()))
        self.comboSheetF.setCurrentIndex(self.comboSheetF.findText(self.settings.value("colors/sheetf").toString()))
        self.comboSheetB.setCurrentIndex(self.comboSheetB.findText(self.settings.value("colors/sheetb").toString()))
        self.comboSkillsF.setCurrentIndex(self.comboSkillsF.findText(self.settings.value("colors/skillsf").toString()))
        self.comboSkillsB.setCurrentIndex(self.comboSkillsB.findText(self.settings.value("colors/skillsb").toString()))
        self.comboSpecialsF.setCurrentIndex(self.comboSpecialsF.findText(self.settings.value("colors/specialsf").toString()))
        self.comboSpecialsB.setCurrentIndex(self.comboSpecialsB.findText(self.settings.value("colors/specialsb").toString()))
        self.comboSubF.setCurrentIndex(self.comboSubF.findText(self.settings.value("colors/subf").toString()))
        self.comboSubB.setCurrentIndex(self.comboSubB.findText(self.settings.value("colors/subb").toString()))


class IndexingDialog(QDialog, indexingDialog.Ui_indexDialog):

    def __init__(self, parent, settings):
        super(IndexingDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(__appname__ + ": Indexing Options")
        self.settings = settings
        self.load_settings()

    def load_settings(self):

        self.comboIndex.setCurrentIndex(self.comboIndex.findText(self.settings.value("indexing").toString()))
        self.editURL.setText(self.settings.value("httpbase").toString())
        self.editZip.setText(self.settings.value("zipfile").toString())


class OutputDialog(QDialog, outputDialog.Ui_outputDialog):

    def __init__(self, parent, settings):
        super(OutputDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(__appname__ + ": Token Output Options")
        self.settings = settings
        self.load_settings()

    def load_settings(self):

        self.checkAttack.setChecked(self.settings.value("weapons").toBool())
        self.checkDark.setChecked(self.settings.value("vision").toBool())
        self.checkBasic.setChecked(self.settings.value("basicDice").toBool())
        self.checkHP.setChecked(self.settings.value("hp").toBool())
        self.checkItems.setChecked(self.settings.value("items").toBool())
        self.checkMan.setChecked(self.settings.value("maneuvers").toBool())
        self.checkSkill.setChecked(self.settings.value("skills").toBool())


def main():
    QCoreApplication.setApplicationName("hl2mt")
    QCoreApplication.setApplicationVersion("0.5")
    QCoreApplication.setOrganizationName("Tarsis")
    QCoreApplication.setOrganizationDomain("tarsis.org")

    app = QApplication(sys.argv)
    program = Main()
    program.show()
    app.exec_()

if __module__ == "main":
    main()

# TODO Wire in file scanning from HeroLabIndex to output to main window table
# TODO Create new class to generate filenames for rptok and pull in pog/portrait
# TODO Wire in process files to use main window table to lookup XML's from HeroLab class and stamp out tokens via Token
# TODO Pass HeroLab class HTML to Token and use that for char sheets
# TODO Clean up and rename Token class file
# TODO Allow user to click on table fields to show char data and change token name, pog and portrait
# TODO Create an indexing option that doesn't require remote HTTP