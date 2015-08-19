# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'htmlDialog.ui'
#
# Created: Sat Oct 19 17:45:45 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_htmlDialog(object):
    def setupUi(self, htmlDialog):
        htmlDialog.setObjectName(_fromUtf8("htmlDialog"))
        htmlDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        htmlDialog.resize(743, 622)
        htmlDialog.setMinimumSize(QtCore.QSize(743, 622))
        htmlDialog.setMaximumSize(QtCore.QSize(743, 622))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/user_info.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        htmlDialog.setWindowIcon(icon)
        htmlDialog.setStyleSheet(_fromUtf8("#htmlDialog{\n"
"background-color: rgb(255, 255, 255);\n"
"}"))
        self.widget = QtGui.QWidget(htmlDialog)
        self.widget.setGeometry(QtCore.QRect(9, 9, 731, 611))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.webView = QtWebKit.QWebView(self.widget)
        self.webView.setObjectName(_fromUtf8("webView"))
        self.verticalLayout.addWidget(self.webView)
        self.OKButton = QtGui.QPushButton(self.widget)
        self.OKButton.setMaximumSize(QtCore.QSize(140, 16777215))
        self.OKButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.OKButton.setObjectName(_fromUtf8("OKButton"))
        self.verticalLayout.addWidget(self.OKButton)

        self.retranslateUi(htmlDialog)
        QtCore.QObject.connect(self.OKButton, QtCore.SIGNAL(_fromUtf8("clicked()")), htmlDialog.close)
        QtCore.QMetaObject.connectSlotsByName(htmlDialog)

    def retranslateUi(self, htmlDialog):
        htmlDialog.setWindowTitle(QtGui.QApplication.translate("htmlDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.OKButton.setText(QtGui.QApplication.translate("htmlDialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
from . import icons_rc
