# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'indexingDialog.ui'
#
# Created: Thu May  9 16:01:20 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_indexDialog(object):
    def setupUi(self, indexDialog):
        indexDialog.setObjectName(_fromUtf8("indexDialog"))
        indexDialog.resize(472, 207)
        indexDialog.setMinimumSize(QtCore.QSize(472, 207))
        indexDialog.setMaximumSize(QtCore.QSize(472, 207))
        self.buttonBox = QtGui.QDialogButtonBox(indexDialog)
        self.buttonBox.setGeometry(QtCore.QRect(340, 170, 120, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.layoutWidget = QtGui.QWidget(indexDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 451, 151))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelIndex = QtGui.QLabel(self.layoutWidget)
        self.labelIndex.setObjectName(_fromUtf8("labelIndex"))
        self.horizontalLayout.addWidget(self.labelIndex)
        self.comboIndex = QtGui.QComboBox(self.layoutWidget)
        self.comboIndex.setObjectName(_fromUtf8("comboIndex"))
        self.comboIndex.addItem(_fromUtf8(""))
        self.comboIndex.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.comboIndex)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.labelURL = QtGui.QLabel(self.layoutWidget)
        self.labelURL.setObjectName(_fromUtf8("labelURL"))
        self.horizontalLayout_3.addWidget(self.labelURL)
        self.editURL = QtGui.QLineEdit(self.layoutWidget)
        self.editURL.setObjectName(_fromUtf8("editURL"))
        self.horizontalLayout_3.addWidget(self.editURL)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.labelZip = QtGui.QLabel(self.layoutWidget)
        self.labelZip.setObjectName(_fromUtf8("labelZip"))
        self.horizontalLayout_4.addWidget(self.labelZip)
        self.editZip = QtGui.QLineEdit(self.layoutWidget)
        self.editZip.setObjectName(_fromUtf8("editZip"))
        self.horizontalLayout_4.addWidget(self.editZip)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(indexDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), indexDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), indexDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(indexDialog)

    def retranslateUi(self, indexDialog):
        indexDialog.setWindowTitle(QtGui.QApplication.translate("indexDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.labelIndex.setText(QtGui.QApplication.translate("indexDialog", "Index Option", None, QtGui.QApplication.UnicodeUTF8))
        self.comboIndex.setItemText(0, QtGui.QApplication.translate("indexDialog", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.comboIndex.setItemText(1, QtGui.QApplication.translate("indexDialog", "HTML", None, QtGui.QApplication.UnicodeUTF8))
        self.labelURL.setText(QtGui.QApplication.translate("indexDialog", "Base HTTP URL", None, QtGui.QApplication.UnicodeUTF8))
        self.labelZip.setText(QtGui.QApplication.translate("indexDialog", "Zip Filename", None, QtGui.QApplication.UnicodeUTF8))

