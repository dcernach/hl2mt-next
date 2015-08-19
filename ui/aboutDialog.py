# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aboutDialog.ui'
#
# Created: Fri Nov 15 21:19:43 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_aboutDialog(object):
    def setupUi(self, aboutDialog):
        aboutDialog.setObjectName(_fromUtf8("aboutDialog"))
        aboutDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        aboutDialog.resize(285, 341)
        aboutDialog.setMinimumSize(QtCore.QSize(285, 341))
        aboutDialog.setMaximumSize(QtCore.QSize(285, 341))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/user_info.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        aboutDialog.setWindowIcon(icon)
        aboutDialog.setStyleSheet(_fromUtf8("#aboutDialog {\n"
"background-color: rgb(255, 255, 255);\n"
"}\n"
"#imageLabel {\n"
"background-color: rgb(255, 255, 255);\n"
"}\n"
"#textLabel {\n"
"background-color: rgb(255, 255, 255);\n"
"}\n"
""))
        self.imageLabel = QtGui.QLabel(aboutDialog)
        self.imageLabel.setGeometry(QtCore.QRect(10, 10, 101, 101))
        self.imageLabel.setText(_fromUtf8(""))
        self.imageLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/hl2mt.png")))
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setObjectName(_fromUtf8("imageLabel"))
        self.textLabel = QtGui.QLabel(aboutDialog)
        self.textLabel.setGeometry(QtCore.QRect(130, 30, 131, 71))
        self.textLabel.setObjectName(_fromUtf8("textLabel"))
        self.webView = QtWebKit.QWebView(aboutDialog)
        self.webView.setGeometry(QtCore.QRect(10, 120, 261, 171))
        self.webView.setAutoFillBackground(False)
        self.webView.setObjectName(_fromUtf8("webView"))
        self.OKButton = QtGui.QPushButton(aboutDialog)
        self.OKButton.setGeometry(QtCore.QRect(110, 300, 85, 31))
        self.OKButton.setMaximumSize(QtCore.QSize(140, 16777215))
        self.OKButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.OKButton.setObjectName(_fromUtf8("OKButton"))

        self.retranslateUi(aboutDialog)
        QtCore.QObject.connect(self.OKButton, QtCore.SIGNAL(_fromUtf8("clicked()")), aboutDialog.close)
        QtCore.QMetaObject.connectSlotsByName(aboutDialog)

    def retranslateUi(self, aboutDialog):
        aboutDialog.setWindowTitle(QtGui.QApplication.translate("aboutDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel.setText(QtGui.QApplication.translate("aboutDialog", "<html><head/><body><p><a href=\"http://hg.tarsis.org/hl2mt\"><span style=\" font-size:36pt; text-decoration: underline; color:#0000ff;\">hl2mt</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.OKButton.setText(QtGui.QApplication.translate("aboutDialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
from . import icons_rc
