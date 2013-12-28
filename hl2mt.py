__appname__ = "hl2mt"
__version__ = "0.80"
__module__ = "main"

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui import mainWindow, foldersDialog, colorsDialog, indexingDialog, outputDialog, propertiesDialog, htmlDialog
from ui import aboutDialog, helpDialog, macrosDialog
import os
import ConfigParser
from herolab import HeroLabIndex, HeroLab
import zipfile
import hashlib
import re


class Main(QMainWindow, mainWindow.Ui_mainWindow):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(__appname__)

        self.load_initial_settings()
        self.check_defaults()

        self.searchThread = SearchThread()
        self.searchThread.entryFoundSignal.connect(self.entry_found)
        self.searchThread.searchFinishedSignal.connect(self.search_finished)
        self.searchThread.searchErrorSignal.connect(self.search_error)

        self.createThread = CreateThread()
        self.createThread.tokenCreatedSignal.connect(self.token_created)
        self.createThread.createFinishedSignal.connect(self.create_finished)

        self.actionExit.triggered.connect(self.close)
        self.actionFolders.triggered.connect(self.action_folders_triggered)
        self.actionProperties.triggered.connect(self.action_properties_triggered)
        self.actionColors.triggered.connect(self.action_colors_triggered)
        self.actionIndexing.triggered.connect(self.action_indexing_triggered)
        self.actionOutput.triggered.connect(self.action_output_triggered)
        self.actionImport.triggered.connect(self.action_import_triggered)
        self.actionSave.triggered.connect(self.action_save_triggered)
        self.actionHelp.triggered.connect(self.action_help_triggered)
        self.actionAbout.triggered.connect(self.action_about_triggered)
        self.actionMacros.triggered.connect(self.action_macros_triggered)

        self.processButton.clicked.connect(self.process_button_clicked)
        self.createButton.clicked.connect(self.create_button_clicked)

        self.tableWidget.cellDoubleClicked.connect(self.table_widget_doubleclicked)

    def load_initial_settings(self):
        """Setup the initial values"""
        self.settings = QSettings(QSettings.NativeFormat, QSettings.UserScope, "Tarsis", "hl2mt")

        self.tableWidget.setColumnCount(7)
        self.tableWidget.hideColumn(0)
        self.tableWidget.hideColumn(1)
        self.tableWidget.hideColumn(2)

        for column in [3, 4, 5, 6]:
            width, _ = self.settings.value("tablewidth" + str(column)).toInt()
            if width:
                self.tableWidget.setColumnWidth(column, width)
            else:
                self.tableWidget.setColumnWidth(column, 200)

        self.createButton.setDisabled(True)

        self.restoreGeometry(self.settings.value("geometry").toByteArray())
        self.restoreState(self.settings.value("windowstate").toByteArray())

    def check_defaults(self):

        for opt in ['folderinput', 'folderpog', 'folderoutput', 'folderportrait']:
            if not self.settings.contains(opt):
                self.settings.setValue(opt, os.getcwd())

        for opt in ['vision', 'maneuvers']:
            if not self.settings.contains(opt):
                self.settings.setValue(opt, False)

        for opt in ['weapons', 'skills', 'hp', 'basicdice', 'items', 'ability']:
            if not self.settings.contains(opt):
                self.settings.setValue(opt, True)

        if not self.settings.contains("indexing"):
            self.settings.setValue("indexing", "None")

        if not self.settings.contains("zipfile"):
            self.settings.setValue("zipfile", "HeroLabIndex.zip")

        if not self.settings.contains("httpbase"):
            self.settings.setValue("httpbase", "")

        if not self.settings.contains("properties/propname"):
            self.settings.setValue("properties/propname", "Basic")

        if not self.settings.contains("properties/charactername"):
            self.settings.setValue("properties/charactername", "Name")

        if not self.settings.contains("properties/hptemp"):
            self.settings.setValue("properties/charactername", "HPT")

        if not self.settings.contains("properties/items"):
            self.settings.setValue("properties/charactername", "Items")

        if not self.settings.contains("properties/hpmax"):
            self.settings.setValue("properties/hpmax", "HP")

        if not self.settings.contains("properties/ac"):
            self.settings.setValue("properties/ac", "AC")

        if not self.settings.contains("properties/xpvalue"):
            self.settings.setValue("properties/xpvalue", "XPValue")

        if not self.settings.contains("properties/speed"):
            self.settings.setValue("properties/speed", "Movement")

        for opt in ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma', 'race', 'alignment']:
            if not self.settings.contains("properties/" + opt):
                self.settings.setValue("properties/" + opt, opt.title())

        for opt in ['colors/sheetf', 'colors/skillsf', 'colors/hpf', 'colors/cmbf', 'colors/basicb',
                    'colors/maneuversf', 'colors/subb', 'colors/gmf']:
            if not self.settings.contains(opt):
                self.settings.setValue(opt, "black")

        for opt in ['colors/initf', 'colors/attacksf', 'colors/specialsf', 'colors/basicf', 'colors/savesf',
                    'colors/subf', 'colors/abilityf', 'colors/fullf', 'colors/gmb']:
            if not self.settings.contains(opt):
                self.settings.setValue(opt, "white")

        if not self.settings.contains('colors/cmbb'):
            self.settings.setValue('colors/cmbb', "teal")
        if not self.settings.contains('colors/maneuversb'):
            self.settings.setValue('colors/maneuversb', "teal")
        if not self.settings.contains('colors/skillsb'):
            self.settings.setValue('colors/skillsb', "silver")
        if not self.settings.contains('colors/sheetb'):
            self.settings.setValue('colors/sheetb', "gray")
        if not self.settings.contains('colors/hpb'):
            self.settings.setValue('colors/hpb', "cyan")
        if not self.settings.contains('colors/initb'):
            self.settings.setValue('colors/initb', "blue")
        if not self.settings.contains('colors/attacksb'):
            self.settings.setValue('colors/attacksb', "red")
        if not self.settings.contains('colors/savesb'):
            self.settings.setValue('colors/savesb', "green")
        if not self.settings.contains('colors/specialsb'):
            self.settings.setValue('colors/specialsb', "navy")
        if not self.settings.contains('colors/abilityb'):
            self.settings.setValue('colors/abilityb', "purple")
        if not self.settings.contains('colors/fullb'):
            self.settings.setValue('colors/fullb', "maroon")

    def closeEvent(self, event):

        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowstate", self.saveState())
        self.settings.setValue("tablewidth3", self.tableWidget.columnWidth(3))
        self.settings.setValue("tablewidth4", self.tableWidget.columnWidth(4))
        self.settings.setValue("tablewidth5", self.tableWidget.columnWidth(5))
        self.settings.setValue("tablewidth6", self.tableWidget.columnWidth(6))
        QMainWindow.closeEvent(self, event)

    def action_folders_triggered(self):
        dialog = FoldersDialog(self, self.settings)
        if dialog.exec_():
            self.settings = dialog.settings

    def action_macros_triggered(self):
        dialog = MacrosDialog(self, self.settings)
        if dialog.exec_():
            for row in xrange(0, dialog.tableWidget.rowCount()):
                if dialog.tableWidget.item(row, 0) is not None:
                    self.settings.setValue("cm_name_" + str(row), dialog.tableWidget.item(row, 0).text())
                    self.settings.setValue("cm_group_" + str(row), dialog.tableWidget.item(row, 1).text())
                    self.settings.setValue("cm_font_" + str(row), dialog.tableWidget.item(row, 2).text())
                    self.settings.setValue("cm_background_" + str(row), dialog.tableWidget.item(row, 3).text())
                    self.settings.setValue("cm_value_" + str(row), dialog.tableWidget.item(row, 4).text())

    def action_properties_triggered(self):
        dialog = PropertiesDialog(self, self.settings)
        if dialog.exec_():
            self.settings.setValue("properties/ac", dialog.editAC.text())
            self.settings.setValue("properties/acflat", dialog.editACFlat.text())
            self.settings.setValue("properties/actouch", dialog.editACTouch.text())
            self.settings.setValue("properties/alignment", dialog.editAlignment.text())
            self.settings.setValue("properties/bab", dialog.editBAB.text())
            self.settings.setValue("properties/strength", dialog.editStr.text())
            self.settings.setValue("properties/dexterity", dialog.editDex.text())
            self.settings.setValue("properties/constitution", dialog.editCon.text())
            self.settings.setValue("properties/intelligence", dialog.editInt.text())
            self.settings.setValue("properties/wisdom", dialog.editWis.text())
            self.settings.setValue("properties/charisma", dialog.editCha.text())
            self.settings.setValue("properties/cmb", dialog.editCMB.text())
            self.settings.setValue("properties/cmd", dialog.editCMD.text())
            self.settings.setValue("properties/cmdflat", dialog.editCMDFlat.text())
            self.settings.setValue("properties/player", dialog.editPlayer.text())
            self.settings.setValue("properties/race", dialog.editRace.text())
            self.settings.setValue("properties/melee", dialog.editMelee.text())
            self.settings.setValue("properties/ranged", dialog.editRanged.text())
            self.settings.setValue("properties/reach", dialog.editReach.text())
            self.settings.setValue("properties/speed", dialog.editSpeed.text())
            self.settings.setValue("properties/name", dialog.editName.text())
            self.settings.setValue("properties/propname", dialog.editPropName.text())
            self.settings.setValue("properties/hp", dialog.editHP.text())
            self.settings.setValue("properties/hptemp", dialog.editHPTemp.text())
            self.settings.setValue("properties/hpmax", dialog.editHPMax.text())
            self.settings.setValue("properties/items", dialog.editItems.text())
            self.settings.setValue("properties/xpvalue", dialog.editXP.text())

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
            self.settings.setValue("colors/abilityf", dialog.comboAbilityF.currentText())
            self.settings.setValue("colors/abilityb", dialog.comboAbilityB.currentText())
            self.settings.setValue("colors/fullf", dialog.comboFullF.currentText())
            self.settings.setValue("colors/fullb", dialog.comboFullB.currentText())
            self.settings.setValue("colors/gmf", dialog.comboGMF.currentText())
            self.settings.setValue("colors/gmb", dialog.comboGMB.currentText())

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
            self.settings.setValue("basicdice", dialog.checkBasic.isChecked())
            self.settings.setValue("hp", dialog.checkHP.isChecked())
            self.settings.setValue("items", dialog.checkItems.isChecked())
            self.settings.setValue("maneuvers", dialog.checkMan.isChecked())
            self.settings.setValue("skills", dialog.checkSkill.isChecked())
            self.settings.setValue("ability", dialog.checkAbility.isChecked())

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
                if name not in ['geometry', 'windowstate', 'tablewidth3', 'tablewidth4', 'tablewidth5', 'tablewidth6']:
                    config.set('DEFAULT', str(name), self.settings.value(name).toString())

            with open(filename, 'wb') as cf:
                config.write(cf)
                cf.close()

    def action_help_triggered(self):
        html = "<html>"
        html += "<head><title>hl2mt Help</title></head>"

        html += "<body>"
        html += "<h2>" + __appname__ + " Help</h2>"

        html += "<a name=\"toc\"></a>"
        html += "<ul id=\"toc\">"
        html += "<li><a href=\"#chapter1\">Chapter 1</a>: <span>Introduction</span></li>"
        html += "<li><a href=\"#chapter2\">Chapter 2</a>: <span>Basics of a Token</span></li>"
        html += "<li><a href=\"#chapter3\">Chapter 3</a>: <span>Folders</span></li>"
        html += "<li><a href=\"#chapter4\">Chapter 4</a>: <span>Token Naming</span></li>"
        html += "<li><a href=\"#chapter5\">Chapter 5</a>: <span>Token Properties</span></li>"
        html += "<li><a href=\"#chapter6\">Chapter 6</a>: <span>Macro Colors</span></li>"
        html += "<li><a href=\"#chapter7\">Chapter 7</a>: <span>Indexing</span></li>"
        html += "<li><a href=\"#chapter8\">Chapter 8</a>: <span>Output Options</span></li>"
        html += "<li><a href=\"#chapter9\">Chapter 9</a>: <span>Importing and Exporting Configs</span></li>"
        html += "</ul>"
        html += "<br><br><br>"

        # Chapter 1
        html += "<a name=\"chapter1\"></a>"
        html += "<h3>Chapter 1: Introduction</h3>"

        html += "hl2mt parses save files from Hero Lab and converts them into usable Maptool tokens that have die roll "
        html += "macros and text references. The application has a lot of configuration options that should allow "
        html += "anyone to customize the created tokens so they work with existing Maptool frameworks."

        html += "<br><br><a href=\"#toc\">Back to table of contents</a>"
        html += "<br><br><br>"

        # Chapter 2
        html += "<a name=\"chapter2\"></a>"
        html += "<h3>Chapter 2: Basics of a Token</h3>"

        html += "The basic usage concept behind hl2mt is you do up your encounters, PCs and monsters in Hero Lab and "
        html += "then save them into a directory. hl2mt then opens the files, parses the data, pulls out the creatures "
        html += "and associates a portrait and token image to them. It then saves the creature into a Maptool token."

        html += "<br><br><a href=\"#toc\">Back to table of contents</a>"
        html += "<br><br><br>"

        # Chapter 3
        html += "<a name=\"chapter3\"></a>"
        html += "<h3>Chapter 3: Folders</h3>"

        html += "Normally Hero Lab save files don't contain images in them and Maptool needs both a portrait and "
        html += "token(called a POG from now on) image to stamp out a token. So for hl2mt to function you need "
        html += "to tell it where to find the portrait and pog images and tell it where you save out all the tokens "
        html += "it creates."
        html += "<br>"
        html += "In the config options for hl2mt, you'll be able to setup the following 4 directories:"

        html += "<ul>"
        html += "<li><b>Input Directory</b>: Where the Hero save files are</li>"
        html += "<li><b>POG Directory</b>: Where hl2mt will search for token images for each creature</li>"
        html += "<li><b>Portrait Directory</b>: Where hl2mt will search for portrait images for each creature</li>"
        html += "<li><b>Output Directory</b>: Where hl2mt will save the tokens</li>"
        html += "</ul>"

        html += "<br><br><a href=\"#toc\">Back to table of contents</a>"
        html += "<br><br><br>"

        # Chapter 4
        html += "<a name=\"chapter4\"></a>"
        html += "<h3>Chapter 4: Token Naming</h3>"

        html += "hl2mt has its own way of handling names."

        html += "The filename on the Hero Lab file doesn't matter. It's the creature names that hl2mt works with. If "
        html += "you have an orcs.por file with an Orc, Orc Champion and Chief Orc hl2mt will individually create "
        html += "\"Orc\", \"Orc Champion\" and \"Chief Orc\" tokens and expect to find image files with those names "
        html += "in the POG and Portrait directories."

        html += "<br><br>"
        html += "hl2mt tries to be intelligent when it looks for images and chooses a token file save name, but "
        html += "you can double click on the appropriate column in the main table to pick a new pog/portrait image "
        html += "or save file name."

        html += "<br><br><a href=\"#toc\">Back to table of contents</a>"
        html += "<br><br><br>"

        # Chapter 5
        html += "<a name=\"chapter5\"></a>"
        html += "<h3>Chapter 5: Token Properties</h3>"

        html += "Within Maptool there's a campaign properties option which allows you to set properties(variables) "
        html += "onto tokens. By default there's a simple Basic campaign property that has a few simple settings on "
        html += "it. Most frameworks create their own campaign properties and assign a lot more values to a token that "
        html += "the framework manipulates via macros."

        html += "<br><br>"

        html += "hl2mt allows you to customize how the Hero Lab data gets converted into token properties. Below are "
        html += "the properties hl2mt works with:<br>"

        html += "<h4>Basic Properties</h4>"
        html += "<ul>"
        html += "<li><b>Token Property Name</b>: The campaign property name(Basic, Pathfinder, etc)</li>"
        html += "<li><b>Character Name</b>: What property the character name in Hero Lab should be assigned to</li>"
        html += "<li><b>Player Name</b>: What property the player name in Hero Lab should be assigned to</li>"
        html += "<li><b>Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma</b>: The numerical stat</li>"
        html += "</ul>"

        html += "<h4>Offense Properties</h4>"
        html += "<ul>"
        html += "<li><b>CMB</b>: The creature's basic CMB</li>"
        html += "<li><b>Melee Attack, Ranged Attack, BAB</b>: Basic attack values</li>"
        html += "</ul>"

        html += "<h4>Defense Properties</h4>"
        html += "<ul>"
        html += "<li><b>AC Normal, AC Flatfooted, AC Touch</b>: Basic defenses</li>"
        html += "<li><b>CMD, CMD Flatfooted</b>: Maneuver defenses</li>"
        html += "</ul>"

        html += "<h4>Misc Properties</h4>"
        html += "<ul>"
        html += "<li><b>Race, Alignment</b>: Basic character information</li>"
        html += "<li><b>HP Current</b>: The current hit points of the creature(after damage is applied)</li>"
        html += "<li><b>HP Max</b>: The max hit points of the creature</li>"
        html += "<li><b>Speed, Reach</b>: More basic stats</li>"
        html += "</ul>"

        html += "<br><br><a href=\"#toc\">Back to table of contents</a>"
        html += "<br><br><br>"

        # Chapter 6
        html += "<a name=\"chapter6\"></a>"
        html += "<h3>Chapter 6: Macro Colors</h3>"

        html += "Macro buttons have 2 colors associated to them: font and background. From the macro colors "
        html += "option window you can pick and choose what colors you want for each kind of macro."

        html += "<br><br><b>Macro color options:</b>"
        html += "<ul>"
        html += "<li><b>Sheet</b>: Character sheet macro</li>"
        html += "<li><b>Skills</b>: Character skill macros</li>"
        html += "<li><b>Attacks</b>: Weapon macros along with base melee/ranged attack</li>"
        html += "<li><b>HP Change</b>: The HP change macro</li>"
        html += "<li><b>Init</b>: The initiative roll macro</li>"
        html += "<li><b>CMB</b>: CMB macro</li>"
        html += "<li><b>Saves</b>: Wil/Fort/Ref save macros</li>"
        html += "<li><b>Specials</b>: Macros that deal with feats, spells, and other specials</li>"
        html += "<li><b>Basic Dice</b>: Simple dice roll macros: d4, d6, d8, d10, d12, d20</li>"
        html += "<li><b>Maneuvers</b>: The individual CMB macros(bull rush, trip, etc)</li>"
        html += "<li><b>Submacros</b>: These macros are not used directly, they support other macros</li>"
        html += "</ul>"

        html += "<br><br><a href=\"#toc\">Back to table of contents</a>"
        html += "<br><br><br>"

        # Chapter 7
        html += "<a name=\"chapter7\"></a>"
        html += "<h3>Chapter 7: Indexing</h3>"

        html += "Hero Lab outputs extremely detailed data on feats, traits, special abilities, spells and so on in "
        html += "the output it generates for your creatures. This is too much data to store on each token. If your "
        html += "library has 100 spellcasters all with magic missile it's wasteful to have 100 copies of magic "
        html += "missile described in your campaign. Also some creatures might have hundreds of feats, special "
        html += "abilities and spells and trying to include very detailed descriptions for each in a single token "
        html += "would make the token very unwieldy to work with in."

        html += "<br><br>"

        html += "So by default when hl2mt creates tokens it doesn't include this detailed data. Instead it creates "
        html += "simple lists on the token of feats, spells and so on, unless you turn on indexing."

        html += "<br><br>"

        html += "Indexing requires the Nerps variant of Maptool which allows for the software to pull in data off "
        html += "of remote servers. When you choose the HTML option for indexing hl2mt will create html pages "
        html += "of all the feats, spells, character sheets and so on and zip them up into a file you can manually "
        html += "copy to a web server."

        html += "<br><br>"

        html += "Simply choose this option, input the base URL of where you'll unpack the index files and hl2mt will "
        html += "pack all the html pages into a zip file you can upload to your server."

        html += "<br><br>"

        html += "As an example, my base URL is http://tarsis.org/maptool/ and when I'm finished running hl2mt "
        html += "I upload my zip file to that directory and unpack it. I also make sure the files are world "
        html += "readable by running:"
        html += "<br>"

        html += "<pre>chmod 644 *</pre>"

        html += "Now in game when I link to a Feat or spell Maptool will fetch the data from that URL over the web "
        html += "and display it in game."

        html += "<br><br><a href=\"#toc\">Back to table of contents</a>"
        html += "<br><br><br>"

        # Chapter 8
        html += "<a name=\"chapter8\"></a>"
        html += "<h3>Chapter 8: Output Options</h3>"

        html += "Not everyone wants all the same things on their tokens, so here you can optionally choose what you "
        html += "want on your created tokens."

        html += "<h4>Multiple Darkvision Ranges</h4>"

        html += "Basic campaign frameworks typically just have a single Darkvision vision property that's assumed "
        html += "to be 60ft in range. Pathfinder however has races with different ranges of darkvision. If your "
        html += "framework supports these, you can click this option and your token will output darkvision in the "
        html += "following way: Darkvision30, Darkvision60, Darkvision120 and Lowlight, etc. "

        html += "<h4>Individual Maneuver Macros</h4>"

        html += "Hero Lab has individual values for all the maneuvers(trip, bull rush, etc). If you'd prefer to see "
        html += "a macro for each maneuver in addition to the basic CMB macro select this option. This can be useful "
        html += "if you have creatures who have bonuses to certain maneuvers."

        html += "<h4>Skill Macros</h4>"

        html += "This option will create a macro for every skill the creature has. These are very "
        html += "simple \"d20 + skill\" dice rolling macros."

        html += "<h4>Weapon Macros</h4>"

        html += "Hero Lab contains attack to hit and damage data for every weapon carried by creatures(including "
        html += "natural attacks). If you'd like a weapon to-hit/damage roll macro created click this option. hl2mt "
        html += "will attempt to eliminate duplicate items(if your PCs like to carry 20 daggers) and will also create "
        html += "a Thrown option for any weapon that can also be thrown."

        html += "<h4>Basic Dice Macros</h4>"

        html += "These are just macros for basic die rolls: d4, d6, d8, d10, d12 and d20"
        html += "<br><br>"
        html += "They can be useful if you have newer players who aren't using to typing die rolls into chat."

        html += "<h4>Ability Check Macros</h4>"

        html += "These are d20 dice roll macros that add in the ability check modifier. They can be useful for things "
        html += "like strength checks."

        html += "<h4>Items Macros</h4>"

        html += "This is a simple list of every item carried by the creature. Unfortunately it's not editable as "
        html += "that requires forms which would necessitate the use of library tokens."

        html += "<h4>HP Change Macros</h4>"

        html += "This will create a very simple hit point change macro. If your token properties includes both "
        html += "current and max hp fields then hl2mt will work with both and create a macro that uses a health bar "
        html += "over your tokens. If you only have max hp on your framework then hl2mt will create a simpler macro "
        html += "which only works with that."

        html += "<h4>GM Macros</h4>"

        html += "These are some simple GM macros that allow you to change the displayed token name. "

        html += "<br><br><a href=\"#toc\">Back to table of contents</a>"
        html += "<br><br><br>"

        # Chapter 9
        html += "<a name=\"chapter9\"></a>"
        html += "<h3>Chapter 9: Importing and Exporting Configs</h3>"

        html += "Sometimes you'll want to work on a few different setups with how hl2mt operates. For example, "
        html += "you might be running Rise of the Runelords with one group and doing a PFS scenario with another."
        html += "It can be useful to keep the modules/groups separated with their own folder setup and maybe "
        html += "even options. To help with this hl2mt allows you to export and import different configs."

        html += "<br><br>"

        html += "Simple setup hl2mt the way you want and export the config. Later you can import it to bring it "
        html += "back to that state."

        html += "<br><br><a href=\"#toc\">Back to table of contents</a>"

        html += "</body>"
        html += "</html>"

        helpDialog = HelpDialog(self)
        helpDialog.show_html(html)

    def action_about_triggered(self):
        html = "<html>"
        html += "<head><title>About hl2mt</title></head>"

        html += "<body>"
        html += "<h2>" + __appname__ + " version " + __version__ + "</h2>"
        html += "<b>hl2mt</b> is a Hero Lab to Maptool save file converter for "
        html += "the Pathfinder roleplaying game."

        html += "</body>"
        html += "</html>"

        aboutDialog = AboutDialog(self)
        aboutDialog.show_html(html)

    def table_widget_doubleclicked(self, row, col):
        subdir = self.tableWidget.item(row, 0).text()
        filename = self.tableWidget.item(row, 1).text()
        source = self.tableWidget.item(row, 2).text()
        input_folder = self.settings.value("folderinput").toString()
        pog_folder = self.settings.value("folderpog").toString()
        portrait_folder = self.settings.value("folderportrait").toString()
        token_folder = self.settings.value("folderoutput").toString()

        # Character name brings up HTML sheet
        if col == 3:
            heroLab = HeroLab(input_folder, subdir, source, filename)
            if heroLab.html != '':
                htmlDialog = HtmlDialog(self)
                htmlDialog.show_html(heroLab.html)
            else:
                QMessageBox.warning(self, __appname__ + " Error", "Could not find HTML in file")

        # Portrait and POG bring up file open dialogs
        if col == 4:
            filename = QFileDialog.getOpenFileName(self, __appname__ + ": Choose Image", portrait_folder,
                                                   filter="Image files (*.png *.jpg *.jpeg *.gif *.bmp)")
            if filename != '' and os.path.isfile(filename):
                self.tableWidget.setItem(row, col, QTableWidgetItem(filename))

        if col == 5:
            filename = QFileDialog.getOpenFileName(self, __appname__ + ": Choose Image", pog_folder,
                                                   filter="Image files (*.png *.jpg *.jpeg *.gif *.bmp)")
            if filename != '' and os.path.isfile(filename):
                self.tableWidget.setItem(row, col, QTableWidgetItem(filename))

        # Token column brings up a save dialog
        if col == 6:
            filename = QFileDialog.getSaveFileName(self, __appname__ + ": Save Token As...", token_folder,
                                                   filter="Token files (*.rptok)")
            if filename != '':
                self.tableWidget.setItem(row, col, QTableWidgetItem(filename))

    def process_button_clicked(self):
        """Search through the files and display the output"""
        self.row = 0
        self.errors = ""
        self.processButton.setDisabled(True)
        self.createButton.setDisabled(True)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.searchThread.input_folder = self.settings.value("folderinput").toString()
        self.searchThread.pog_folder = self.settings.value("folderpog").toString()
        self.searchThread.portrait_folder = self.settings.value("folderportrait").toString()
        self.searchThread.token_folder = self.settings.value("folderoutput").toString()
        self.searchThread.start()

    def create_button_clicked(self):
        """Create the tokens"""
        self.processButton.setDisabled(True)
        self.createButton.setDisabled(True)
        self.tableWidget.setSortingEnabled(False)
        self.createThread.settings = self.settings
        self.createThread.table_widget = self.tableWidget
        self.createThread.start()

    def entry_found(self, subdir, source, filename, name, portrait, pog, token):
        if self.tableWidget.rowCount() < self.row + 1:
            self.tableWidget.setRowCount(self.row + 1)

        self.tableWidget.setItem(self.row, 0, QTableWidgetItem(subdir))
        self.tableWidget.setItem(self.row, 1, QTableWidgetItem(filename))
        self.tableWidget.setItem(self.row, 2, QTableWidgetItem(source))
        self.tableWidget.setItem(self.row, 3, QTableWidgetItem(name))
        self.tableWidget.setItem(self.row, 4, QTableWidgetItem(portrait))
        self.tableWidget.setItem(self.row, 5, QTableWidgetItem(pog))
        self.tableWidget.setItem(self.row, 6, QTableWidgetItem(token))
        self.row += 1

    def search_finished(self):
        self.processButton.setDisabled(False)
        if self.errors:
            QMessageBox.warning(self, __appname__ + " Errors", self.errors)

        if self.tableWidget.rowCount() < 1:
            QMessageBox.information(self, __appname__ + " No Files", "Nothing found to create tokens from")
        else:
            self.createButton.setDisabled(False)

        self.tableWidget.setSortingEnabled(True)

    def search_error(self, error):
        self.errors += error

    def token_created(self, row):

        self.tableWidget.setRowHidden(row, True)

    def create_finished(self):

        self.processButton.setDisabled(False)
        self.tableWidget.setSortingEnabled(True)
        QMessageBox.information(self, __appname__ + " Finished", "Tokens have been created")


class HtmlDialog(QDialog, htmlDialog.Ui_htmlDialog):

    def __init__(self, parent):
        super(HtmlDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(__appname__ + " Statblock")

    def show_html(self, html):
        self.webView.setHtml(html)
        self.show()


class AboutDialog(QDialog, aboutDialog.Ui_aboutDialog):

    def __init__(self, parent):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("About " + __appname__)

    def show_html(self, html):
        self.webView.setHtml(html)
        self.show()


class HelpDialog(QDialog, helpDialog.Ui_helpDialog):

    def __init__(self, parent):
        super(HelpDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(__appname__ + " Help")

    def show_html(self, html):
        self.webView.setHtml(html)
        self.show()


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
        self.editInput.setText(self.settings.value("folderinput").toString())
        self.editPortrait.setText(self.settings.value("folderportrait").toString())
        self.editPOG.setText(self.settings.value("folderpog").toString())
        self.editOutput.setText(self.settings.value("folderoutput").toString())

    def button_input_clicked(self):
        folder = QFileDialog.getExistingDirectory(self, "Input Folder", self.settings.value("folderinput").toString(),
                                                  QFileDialog.ShowDirsOnly)
        if folder != '':
            self.settings.setValue("folderinput", folder)
            self.load_settings()

    def button_portrait_clicked(self):
        folder = QFileDialog.getExistingDirectory(self, "Portrait Folder",
                                                  self.settings.value("folderportrait").toString(),
                                                  QFileDialog.ShowDirsOnly)
        if folder != '':
            self.settings.setValue("folderportrait", folder)
            self.load_settings()

    def button_pog_clicked(self):
        folder = QFileDialog.getExistingDirectory(self, "POG Folder", self.settings.value("folderpog").toString(),
                                                  QFileDialog.ShowDirsOnly)
        if folder != '':
            self.settings.setValue("folderpog", folder)
            self.load_settings()

    def button_output_clicked(self):
        folder = QFileDialog.getExistingDirectory(self, "Output Folder", self.settings.value("folderoutput").toString(),
                                                  QFileDialog.ShowDirsOnly)
        if folder != '':
            self.settings.setValue("folderoutput", folder)
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

        self.editAC.setText(self.settings.value("properties/ac").toString())
        self.editACFlat.setText(self.settings.value("properties/acflat").toString())
        self.editACTouch.setText(self.settings.value("properties/actouch").toString())
        self.editAlignment.setText(self.settings.value("properties/alignment").toString())
        self.editBAB.setText(self.settings.value("properties/bab").toString())
        self.editStr.setText(self.settings.value("properties/strength").toString())
        self.editDex.setText(self.settings.value("properties/dexterity").toString())
        self.editCon.setText(self.settings.value("properties/constitution").toString())
        self.editInt.setText(self.settings.value("properties/intelligence").toString())
        self.editWis.setText(self.settings.value("properties/wisdom").toString())
        self.editCha.setText(self.settings.value("properties/charisma").toString())
        self.editCMB.setText(self.settings.value("properties/cmb").toString())
        self.editCMD.setText(self.settings.value("properties/cmd").toString())
        self.editCMDFlat.setText(self.settings.value("properties/cmdflat").toString())
        self.editPlayer.setText(self.settings.value("properties/player").toString())
        self.editRace.setText(self.settings.value("properties/race").toString())
        self.editMelee.setText(self.settings.value("properties/melee").toString())
        self.editRanged.setText(self.settings.value("properties/ranged").toString())
        self.editReach.setText(self.settings.value("properties/reach").toString())
        self.editSpeed.setText(self.settings.value("properties/speed").toString())
        self.editName.setText(self.settings.value("properties/name").toString())
        self.editPropName.setText(self.settings.value("properties/propname").toString())
        self.editHP.setText(self.settings.value("properties/hp").toString())
        self.editHPMax.setText(self.settings.value("properties/hpmax").toString())
        self.editHPTemp.setText(self.settings.value("properties/hptemp").toString())
        self.editItems.setText(self.settings.value("properties/items").toString())
        self.editXP.setText(self.settings.value("properties/xpvalue").toString())


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
        self.comboAbilityF.setCurrentIndex(self.comboAbilityF.findText(self.settings.value("colors/abilityf").toString()))
        self.comboAbilityB.setCurrentIndex(self.comboAbilityB.findText(self.settings.value("colors/abilityb").toString()))
        self.comboFullF.setCurrentIndex(self.comboFullF.findText(self.settings.value("colors/fullf").toString()))
        self.comboFullB.setCurrentIndex(self.comboFullB.findText(self.settings.value("colors/fullb").toString()))
        self.comboGMF.setCurrentIndex(self.comboGMF.findText(self.settings.value("colors/gmf").toString()))
        self.comboGMB.setCurrentIndex(self.comboGMB.findText(self.settings.value("colors/gmb").toString()))


class IndexingDialog(QDialog, indexingDialog.Ui_indexDialog):

    def __init__(self, parent, settings):
        super(IndexingDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(__appname__ + ": Indexing Options")
        self.settings = settings
        self.load_settings()
        self.comboIndex.currentIndexChanged.connect(self.combo_index_changed)

    def load_settings(self):

        self.comboIndex.setCurrentIndex(self.comboIndex.findText(self.settings.value("indexing").toString()))
        self.editURL.setText(self.settings.value("httpbase").toString())
        self.editZip.setText(self.settings.value("zipfile").toString())
        self.combo_index_changed()

    def combo_index_changed(self):
        if self.comboIndex.currentText() == 'None':
            self.editZip.setDisabled(True)
            self.editURL.setDisabled(True)
        else:
            self.editZip.setDisabled(False)
            self.editURL.setDisabled(False)


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
        self.checkBasic.setChecked(self.settings.value("basicdice").toBool())
        self.checkHP.setChecked(self.settings.value("hp").toBool())
        self.checkItems.setChecked(self.settings.value("items").toBool())
        self.checkMan.setChecked(self.settings.value("maneuvers").toBool())
        self.checkSkill.setChecked(self.settings.value("skills").toBool())
        self.checkAbility.setChecked(self.settings.value("ability").toBool())


class MacrosDialog(QDialog, macrosDialog.Ui_macrosDialog):

    def __init__(self, parent, settings):
        super(MacrosDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(__appname__ + ": Custom Macros")
        self.settings = settings
        self.load_settings()

    def load_settings(self):

        self.tableWidget.setRowCount(50)

        # Set up the rows based on the custom macro values
        # cm_name_x
        # cm_group_x
        # cm_font_x
        # cm_background_x
        # cm_value_x
        for row in xrange(0, self.tableWidget.rowCount()):

            if self.settings.contains("cm_name_" + str(row)):
                self.tableWidget.setItem(row, 0, QTableWidgetItem(QTableWidgetItem(self.settings.value("cm_name_" + str(row)).toString())))
                self.tableWidget.setItem(row, 1, QTableWidgetItem(QTableWidgetItem(self.settings.value("cm_group_" + str(row)).toString())))
                self.tableWidget.setItem(row, 2, QTableWidgetItem(QTableWidgetItem(self.settings.value("cm_font_" + str(row)).toString())))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(QTableWidgetItem(self.settings.value("cm_background_" + str(row)).toString())))
                self.tableWidget.setItem(row, 4, QTableWidgetItem(QTableWidgetItem(self.settings.value("cm_value_" + str(row)).toString())))


class SearchThread(QThread):

    entryFoundSignal = pyqtSignal(str, str, str, str, str, str, str)
    searchFinishedSignal = pyqtSignal()
    searchErrorSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SearchThread, self).__init__(parent)

    def run(self):
        """Here we'll search through the files and pass the output up"""

        heroLabIndex = HeroLabIndex(self.input_folder, self.pog_folder, self.portrait_folder, self.token_folder)

        for entry in heroLabIndex.get_creatures():
            self.entryFoundSignal.emit(entry["subdir"], entry["source"], entry["filename"], entry["name"],
                                       entry["portrait"], entry["pog"], entry["token"])

        for bad_file in heroLabIndex.bad_files:
            self.searchErrorSignal.emit("Could not open file %s\n" % bad_file)

        self.searchFinishedSignal.emit()


class CreateThread(QThread):

    tokenCreatedSignal = pyqtSignal(int)
    createFinishedSignal = pyqtSignal()

    def __init__(self, parent=None):
        super(CreateThread, self).__init__(parent)

        self.table_widget = QTableWidget
        self.settings = QSettings
        self.values = []

    def run(self):
        """Loop through the table and create a token for each row"""

        input_folder = self.settings.value("folderinput").toString()

        if self.settings.value("indexing").toString() == 'HTML':
            filename = str(self.settings.value("folderoutput").toString() + '/' + self.settings.value("zipfile").toString())
            mtzip = zipfile.ZipFile(filename, 'w')

        for row in xrange(0, self.table_widget.rowCount()):
            subdir = self.table_widget.item(row, 0).text()
            filename = self.table_widget.item(row, 1).text()
            source = self.table_widget.item(row, 2).text()
            name = self.table_widget.item(row, 3).text()
            portrait = self.table_widget.item(row, 4).text()
            pog = self.table_widget.item(row, 5).text()
            token = self.table_widget.item(row, 6).text()

            herolab = HeroLab(input_folder, subdir, source, filename)
            herolab.values = self.values
            herolab.settings = self.settings
            herolab.create_token(name, portrait, pog, token)
            self.values = herolab.values

            if self.settings.value("indexing").toString() == 'HTML':
                html = re.sub(r"\<meta http-equiv.*?\>", '', herolab.html)
                mtzip.writestr(herolab.html_filename, html)

            self.tokenCreatedSignal.emit(row)

        if self.settings.value("indexing").toString() == 'HTML':
            for name, contents in self.make_files():
                mtzip.writestr(name, contents.encode('utf-8'))
            mtzip.close()

        self.createFinishedSignal.emit()

    def make_files(self):

        for value in self.values:
            content = '<html>'
            content += '<head>'
            content += '<title></title>'
            content += '</head>'
            content += '<body>'

            content += value

            content += '</body>'
            content += '</html>'

            yield self.create_filename(value), content

    def create_filename(self, name):

        return hashlib.sha224(name.encode('utf-8')).hexdigest() + '.html'


def main():
    QCoreApplication.setApplicationName(__appname__)
    QCoreApplication.setApplicationVersion(__version__)
    QCoreApplication.setOrganizationName("Tarsis")
    QCoreApplication.setOrganizationDomain("tarsis.org")

    app = QApplication(sys.argv)
    program = Main()
    program.show()
    app.exec_()

if __module__ == "main":
    main()
