# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'foldersDialog.ui'
#
# Created: Fri May 10 15:47:12 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_foldersDialog(object):
    def setupUi(self, foldersDialog):
        foldersDialog.setObjectName(_fromUtf8("foldersDialog"))
        foldersDialog.setEnabled(True)
        foldersDialog.resize(527, 294)
        foldersDialog.setMinimumSize(QtCore.QSize(527, 294))
        foldersDialog.setMaximumSize(QtCore.QSize(527, 294))
        self.buttonBox = QtGui.QDialogButtonBox(foldersDialog)
        self.buttonBox.setGeometry(QtCore.QRect(170, 250, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.layoutWidget = QtGui.QWidget(foldersDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 501, 231))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.buttonInput = QtGui.QPushButton(self.layoutWidget)
        self.buttonInput.setMinimumSize(QtCore.QSize(150, 0))
        self.buttonInput.setObjectName(_fromUtf8("buttonInput"))
        self.horizontalLayout.addWidget(self.buttonInput)
        self.editInput = QtGui.QLineEdit(self.layoutWidget)
        self.editInput.setReadOnly(True)
        self.editInput.setObjectName(_fromUtf8("editInput"))
        self.horizontalLayout.addWidget(self.editInput)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.buttonPOG = QtGui.QPushButton(self.layoutWidget)
        self.buttonPOG.setMinimumSize(QtCore.QSize(150, 0))
        self.buttonPOG.setObjectName(_fromUtf8("buttonPOG"))
        self.horizontalLayout_2.addWidget(self.buttonPOG)
        self.editPOG = QtGui.QLineEdit(self.layoutWidget)
        self.editPOG.setReadOnly(True)
        self.editPOG.setObjectName(_fromUtf8("editPOG"))
        self.horizontalLayout_2.addWidget(self.editPOG)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.buttonPortrait = QtGui.QPushButton(self.layoutWidget)
        self.buttonPortrait.setMinimumSize(QtCore.QSize(150, 0))
        self.buttonPortrait.setObjectName(_fromUtf8("buttonPortrait"))
        self.horizontalLayout_3.addWidget(self.buttonPortrait)
        self.editPortrait = QtGui.QLineEdit(self.layoutWidget)
        self.editPortrait.setReadOnly(True)
        self.editPortrait.setObjectName(_fromUtf8("editPortrait"))
        self.horizontalLayout_3.addWidget(self.editPortrait)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.buttonOutput = QtGui.QPushButton(self.layoutWidget)
        self.buttonOutput.setMinimumSize(QtCore.QSize(150, 0))
        self.buttonOutput.setObjectName(_fromUtf8("buttonOutput"))
        self.horizontalLayout_4.addWidget(self.buttonOutput)
        self.editOutput = QtGui.QLineEdit(self.layoutWidget)
        self.editOutput.setReadOnly(True)
        self.editOutput.setObjectName(_fromUtf8("editOutput"))
        self.horizontalLayout_4.addWidget(self.editOutput)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(foldersDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), foldersDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), foldersDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(foldersDialog)

    def retranslateUi(self, foldersDialog):
        foldersDialog.setWindowTitle(QtGui.QApplication.translate("foldersDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonInput.setText(QtGui.QApplication.translate("foldersDialog", "Input Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonPOG.setText(QtGui.QApplication.translate("foldersDialog", "POG Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonPortrait.setText(QtGui.QApplication.translate("foldersDialog", "Portrait Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonOutput.setText(QtGui.QApplication.translate("foldersDialog", "Output Directory", None, QtGui.QApplication.UnicodeUTF8))

