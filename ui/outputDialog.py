# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'outputDialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_outputDialog(object):
    def setupUi(self, outputDialog):
        outputDialog.setObjectName(_fromUtf8("outputDialog"))
        outputDialog.resize(300, 340)
        outputDialog.setMinimumSize(QtCore.QSize(300, 340))
        outputDialog.setMaximumSize(QtCore.QSize(300, 400))
        self.buttonBox = QtGui.QDialogButtonBox(outputDialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 290, 280, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.layoutWidget = QtGui.QWidget(outputDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 281, 271))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget)
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
        self.checkDesc = QtGui.QCheckBox(self.layoutWidget)
        self.checkDesc.setObjectName(_fromUtf8("checkDesc"))
        self.verticalLayout.addWidget(self.checkDesc)
        self.checkStatBlock = QtGui.QCheckBox(self.layoutWidget)
        self.checkStatBlock.setObjectName(_fromUtf8("checkStatBlock"))
        self.verticalLayout.addWidget(self.checkStatBlock)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(outputDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), outputDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), outputDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(outputDialog)

    def retranslateUi(self, outputDialog):
        outputDialog.setWindowTitle(_translate("outputDialog", "Dialog", None))
        self.checkDark.setText(_translate("outputDialog", "Use Multiple Darkvision Ranges", None))
        self.checkMan.setText(_translate("outputDialog", "Create Individual Maneuver Macros", None))
        self.checkAttack.setText(_translate("outputDialog", "Create Weapon Macros", None))
        self.checkSkill.setText(_translate("outputDialog", "Create Skill Macros", None))
        self.checkAbility.setText(_translate("outputDialog", "Create Ability Check Macros", None))
        self.checkHP.setText(_translate("outputDialog", "Create HP Change Macro", None))
        self.checkItems.setText(_translate("outputDialog", "Create Items Macro", None))
        self.checkBasic.setText(_translate("outputDialog", "Create Basic Die Roll Macros", None))
        self.checkDesc.setText(_translate("outputDialog", "Create Abilities/Feats Descriptions", None))
        self.checkStatBlock.setText(_translate("outputDialog", "Create Herolab StatBlock", None))

