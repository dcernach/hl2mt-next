# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'outputDialog.ui'
#
# Created: Tue Dec 10 13:28:04 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_outputDialog(object):
    def setupUi(self, outputDialog):
        outputDialog.setObjectName(_fromUtf8("outputDialog"))
        outputDialog.resize(326, 340)
        outputDialog.setMinimumSize(QtCore.QSize(326, 340))
        outputDialog.setMaximumSize(QtCore.QSize(326, 340))
        self.buttonBox = QtGui.QDialogButtonBox(outputDialog)
        self.buttonBox.setGeometry(QtCore.QRect(-20, 290, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.layoutWidget = QtGui.QWidget(outputDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 272, 261))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.checkDark = QtGui.QCheckBox(self.layoutWidget)
        self.checkDark.setObjectName(_fromUtf8("checkDark"))
        self.verticalLayout.addWidget(self.checkDark)
        self.checkMan = QtGui.QCheckBox(self.layoutWidget)
        self.checkMan.setObjectName(_fromUtf8("checkMan"))
        self.verticalLayout.addWidget(self.checkMan)
        self.checkAttack = QtGui.QCheckBox(self.layoutWidget)
        self.checkAttack.setObjectName(_fromUtf8("checkAttack"))
        self.verticalLayout.addWidget(self.checkAttack)
        self.checkSkill = QtGui.QCheckBox(self.layoutWidget)
        self.checkSkill.setObjectName(_fromUtf8("checkSkill"))
        self.verticalLayout.addWidget(self.checkSkill)
        self.checkAbility = QtGui.QCheckBox(self.layoutWidget)
        self.checkAbility.setObjectName(_fromUtf8("checkAbility"))
        self.verticalLayout.addWidget(self.checkAbility)
        self.checkHP = QtGui.QCheckBox(self.layoutWidget)
        self.checkHP.setObjectName(_fromUtf8("checkHP"))
        self.verticalLayout.addWidget(self.checkHP)
        self.checkItems = QtGui.QCheckBox(self.layoutWidget)
        self.checkItems.setObjectName(_fromUtf8("checkItems"))
        self.verticalLayout.addWidget(self.checkItems)
        self.checkBasic = QtGui.QCheckBox(self.layoutWidget)
        self.checkBasic.setObjectName(_fromUtf8("checkBasic"))
        self.verticalLayout.addWidget(self.checkBasic)
        self.checkGM = QtGui.QCheckBox(self.layoutWidget)
        self.checkGM.setObjectName(_fromUtf8("checkGM"))
        self.verticalLayout.addWidget(self.checkGM)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(outputDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), outputDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), outputDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(outputDialog)

    def retranslateUi(self, outputDialog):
        outputDialog.setWindowTitle(QtGui.QApplication.translate("outputDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.checkDark.setText(QtGui.QApplication.translate("outputDialog", "Use Multiple Darkvision Ranges", None, QtGui.QApplication.UnicodeUTF8))
        self.checkMan.setText(QtGui.QApplication.translate("outputDialog", "Create Individual Maneuver Macros", None, QtGui.QApplication.UnicodeUTF8))
        self.checkAttack.setText(QtGui.QApplication.translate("outputDialog", "Create Weapon Macros", None, QtGui.QApplication.UnicodeUTF8))
        self.checkSkill.setText(QtGui.QApplication.translate("outputDialog", "Create Skill Macros", None, QtGui.QApplication.UnicodeUTF8))
        self.checkAbility.setText(QtGui.QApplication.translate("outputDialog", "Create Ability Check Macros", None, QtGui.QApplication.UnicodeUTF8))
        self.checkHP.setText(QtGui.QApplication.translate("outputDialog", "Create HP Change Macro", None, QtGui.QApplication.UnicodeUTF8))
        self.checkItems.setText(QtGui.QApplication.translate("outputDialog", "Create Items Macro", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBasic.setText(QtGui.QApplication.translate("outputDialog", "Create Basic Die Roll Macros", None, QtGui.QApplication.UnicodeUTF8))
        self.checkGM.setText(QtGui.QApplication.translate("outputDialog", "Create GM Macros", None, QtGui.QApplication.UnicodeUTF8))

