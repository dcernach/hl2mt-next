# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'helpDialog.ui'
#
# Created: Thu Jan  2 23:29:38 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_helpDialog(object):
    def setupUi(self, helpDialog):
        helpDialog.setObjectName(_fromUtf8("helpDialog"))
        helpDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        helpDialog.resize(503, 467)
        helpDialog.setMinimumSize(QtCore.QSize(503, 467))
        helpDialog.setMaximumSize(QtCore.QSize(503, 467))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/user_info.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        helpDialog.setWindowIcon(icon)
        helpDialog.setStyleSheet(_fromUtf8("#helpDialog {\n"
"background-color: rgb(255, 255, 255);\n"
"}\n"
"#imageLabel {\n"
"background-color: rgb(255, 255, 255);\n"
"}\n"
"#textLabel {\n"
"background-color: rgb(255, 255, 255);\n"
"}\n"
""))
        self.imageLabel = QtGui.QLabel(helpDialog)
        self.imageLabel.setGeometry(QtCore.QRect(10, 10, 101, 101))
        self.imageLabel.setText(_fromUtf8(""))
        self.imageLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/help_book.png")))
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setObjectName(_fromUtf8("imageLabel"))
        self.textLabel = QtGui.QLabel(helpDialog)
        self.textLabel.setGeometry(QtCore.QRect(140, 20, 291, 71))
        self.textLabel.setObjectName(_fromUtf8("textLabel"))
        self.webView = QtWebKit.QWebView(helpDialog)
        self.webView.setGeometry(QtCore.QRect(10, 110, 481, 311))
        self.webView.setAutoFillBackground(False)
        self.webView.setObjectName(_fromUtf8("webView"))
        self.OKButton = QtGui.QPushButton(helpDialog)
        self.OKButton.setGeometry(QtCore.QRect(220, 430, 85, 31))
        self.OKButton.setMaximumSize(QtCore.QSize(140, 16777215))
        self.OKButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.OKButton.setObjectName(_fromUtf8("OKButton"))

        self.retranslateUi(helpDialog)
        QtCore.QObject.connect(self.OKButton, QtCore.SIGNAL(_fromUtf8("clicked()")), helpDialog.close)
        QtCore.QMetaObject.connectSlotsByName(helpDialog)

    def retranslateUi(self, helpDialog):
        helpDialog.setWindowTitle(QtGui.QApplication.translate("helpDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel.setText(QtGui.QApplication.translate("helpDialog", "<html><head/><body><p><span style=\" font-size:36pt; font-weight:600;\">hl2mt Help</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.OKButton.setText(QtGui.QApplication.translate("helpDialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
from . import icons_rc
