# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'propertiesDialog.ui'
#
# Created: Sun Nov  3 14:40:12 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_propertiesDialog(object):
    def setupUi(self, propertiesDialog):
        propertiesDialog.setObjectName(_fromUtf8("propertiesDialog"))
        propertiesDialog.resize(640, 470)
        propertiesDialog.setMinimumSize(QtCore.QSize(640, 470))
        propertiesDialog.setMaximumSize(QtCore.QSize(640, 470))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/tokens.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        propertiesDialog.setWindowIcon(icon)
        self.formLayout = QtGui.QFormLayout(propertiesDialog)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.frame = QtGui.QFrame(propertiesDialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.basicButton = QtGui.QToolButton(self.frame)
        self.basicButton.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.basicButton.sizePolicy().hasHeightForWidth())
        self.basicButton.setSizePolicy(sizePolicy)
        self.basicButton.setMinimumSize(QtCore.QSize(80, 80))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/user.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.basicButton.setIcon(icon1)
        self.basicButton.setIconSize(QtCore.QSize(32, 32))
        self.basicButton.setCheckable(True)
        self.basicButton.setAutoExclusive(True)
        self.basicButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.basicButton.setObjectName(_fromUtf8("basicButton"))
        self.gridLayout.addWidget(self.basicButton, 0, 0, 1, 1)
        self.offenseButton = QtGui.QToolButton(self.frame)
        self.offenseButton.setMinimumSize(QtCore.QSize(80, 80))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/swords.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.offenseButton.setIcon(icon2)
        self.offenseButton.setIconSize(QtCore.QSize(32, 32))
        self.offenseButton.setCheckable(True)
        self.offenseButton.setAutoExclusive(True)
        self.offenseButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.offenseButton.setObjectName(_fromUtf8("offenseButton"))
        self.gridLayout.addWidget(self.offenseButton, 0, 1, 1, 1)
        self.defenseButton = QtGui.QToolButton(self.frame)
        self.defenseButton.setMinimumSize(QtCore.QSize(80, 80))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/shield.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.defenseButton.setIcon(icon3)
        self.defenseButton.setIconSize(QtCore.QSize(32, 32))
        self.defenseButton.setCheckable(True)
        self.defenseButton.setAutoExclusive(True)
        self.defenseButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.defenseButton.setObjectName(_fromUtf8("defenseButton"))
        self.gridLayout.addWidget(self.defenseButton, 0, 2, 1, 1)
        self.miscButton = QtGui.QToolButton(self.frame)
        self.miscButton.setMinimumSize(QtCore.QSize(80, 80))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/plus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.miscButton.setIcon(icon4)
        self.miscButton.setIconSize(QtCore.QSize(32, 32))
        self.miscButton.setCheckable(True)
        self.miscButton.setAutoExclusive(True)
        self.miscButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.miscButton.setObjectName(_fromUtf8("miscButton"))
        self.gridLayout.addWidget(self.miscButton, 0, 3, 1, 1)
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.frame)
        self.stackedWidget = QtGui.QStackedWidget(propertiesDialog)
        self.stackedWidget.setMinimumSize(QtCore.QSize(500, 300))
        self.stackedWidget.setObjectName(_fromUtf8("stackedWidget"))
        self.pageBasic = QtGui.QWidget()
        self.pageBasic.setObjectName(_fromUtf8("pageBasic"))
        self.line = QtGui.QFrame(self.pageBasic)
        self.line.setGeometry(QtCore.QRect(30, 120, 551, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.layoutWidget = QtGui.QWidget(self.pageBasic)
        self.layoutWidget.setGeometry(QtCore.QRect(9, 150, 591, 131))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout_3 = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.labelInt = QtGui.QLabel(self.layoutWidget)
        self.labelInt.setObjectName(_fromUtf8("labelInt"))
        self.gridLayout_3.addWidget(self.labelInt, 0, 3, 1, 3)
        self.editInt = QtGui.QLineEdit(self.layoutWidget)
        self.editInt.setObjectName(_fromUtf8("editInt"))
        self.gridLayout_3.addWidget(self.editInt, 0, 6, 1, 1)
        self.labelCon = QtGui.QLabel(self.layoutWidget)
        self.labelCon.setObjectName(_fromUtf8("labelCon"))
        self.gridLayout_3.addWidget(self.labelCon, 2, 0, 1, 2)
        self.editCon = QtGui.QLineEdit(self.layoutWidget)
        self.editCon.setObjectName(_fromUtf8("editCon"))
        self.gridLayout_3.addWidget(self.editCon, 2, 2, 1, 1)
        self.editStr = QtGui.QLineEdit(self.layoutWidget)
        self.editStr.setObjectName(_fromUtf8("editStr"))
        self.gridLayout_3.addWidget(self.editStr, 0, 2, 1, 1)
        self.editDex = QtGui.QLineEdit(self.layoutWidget)
        self.editDex.setObjectName(_fromUtf8("editDex"))
        self.gridLayout_3.addWidget(self.editDex, 1, 2, 1, 1)
        self.labelDex = QtGui.QLabel(self.layoutWidget)
        self.labelDex.setObjectName(_fromUtf8("labelDex"))
        self.gridLayout_3.addWidget(self.labelDex, 1, 0, 1, 2)
        self.labelStr = QtGui.QLabel(self.layoutWidget)
        self.labelStr.setObjectName(_fromUtf8("labelStr"))
        self.gridLayout_3.addWidget(self.labelStr, 0, 0, 1, 2)
        self.editWis = QtGui.QLineEdit(self.layoutWidget)
        self.editWis.setObjectName(_fromUtf8("editWis"))
        self.gridLayout_3.addWidget(self.editWis, 1, 6, 1, 1)
        self.editCha = QtGui.QLineEdit(self.layoutWidget)
        self.editCha.setObjectName(_fromUtf8("editCha"))
        self.gridLayout_3.addWidget(self.editCha, 2, 6, 1, 1)
        self.labelCha = QtGui.QLabel(self.layoutWidget)
        self.labelCha.setObjectName(_fromUtf8("labelCha"))
        self.gridLayout_3.addWidget(self.labelCha, 2, 3, 1, 3)
        self.labelWis = QtGui.QLabel(self.layoutWidget)
        self.labelWis.setObjectName(_fromUtf8("labelWis"))
        self.gridLayout_3.addWidget(self.labelWis, 1, 3, 1, 3)
        self.line_3 = QtGui.QFrame(self.pageBasic)
        self.line_3.setGeometry(QtCore.QRect(20, 50, 551, 20))
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.layoutWidget1 = QtGui.QWidget(self.pageBasic)
        self.layoutWidget1.setGeometry(QtCore.QRect(60, 10, 481, 33))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelPropName = QtGui.QLabel(self.layoutWidget1)
        self.labelPropName.setMinimumSize(QtCore.QSize(0, 0))
        self.labelPropName.setObjectName(_fromUtf8("labelPropName"))
        self.horizontalLayout.addWidget(self.labelPropName)
        self.editPropName = QtGui.QLineEdit(self.layoutWidget1)
        self.editPropName.setObjectName(_fromUtf8("editPropName"))
        self.horizontalLayout.addWidget(self.editPropName)
        self.layoutWidget2 = QtGui.QWidget(self.pageBasic)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 80, 591, 33))
        self.layoutWidget2.setObjectName(_fromUtf8("layoutWidget2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelPlayer = QtGui.QLabel(self.layoutWidget2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelPlayer.sizePolicy().hasHeightForWidth())
        self.labelPlayer.setSizePolicy(sizePolicy)
        self.labelPlayer.setMinimumSize(QtCore.QSize(0, 0))
        self.labelPlayer.setObjectName(_fromUtf8("labelPlayer"))
        self.horizontalLayout_2.addWidget(self.labelPlayer)
        self.editPlayer = QtGui.QLineEdit(self.layoutWidget2)
        self.editPlayer.setObjectName(_fromUtf8("editPlayer"))
        self.horizontalLayout_2.addWidget(self.editPlayer)
        self.labelName = QtGui.QLabel(self.layoutWidget2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelName.sizePolicy().hasHeightForWidth())
        self.labelName.setSizePolicy(sizePolicy)
        self.labelName.setMinimumSize(QtCore.QSize(0, 0))
        self.labelName.setObjectName(_fromUtf8("labelName"))
        self.horizontalLayout_2.addWidget(self.labelName)
        self.editName = QtGui.QLineEdit(self.layoutWidget2)
        self.editName.setObjectName(_fromUtf8("editName"))
        self.horizontalLayout_2.addWidget(self.editName)
        self.stackedWidget.addWidget(self.pageBasic)
        self.pageOffense = QtGui.QWidget()
        self.pageOffense.setObjectName(_fromUtf8("pageOffense"))
        self.layoutWidget3 = QtGui.QWidget(self.pageOffense)
        self.layoutWidget3.setGeometry(QtCore.QRect(25, 51, 571, 101))
        self.layoutWidget3.setObjectName(_fromUtf8("layoutWidget3"))
        self.gridLayout_4 = QtGui.QGridLayout(self.layoutWidget3)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.labelBAB = QtGui.QLabel(self.layoutWidget3)
        self.labelBAB.setObjectName(_fromUtf8("labelBAB"))
        self.gridLayout_4.addWidget(self.labelBAB, 0, 3, 1, 1)
        self.editBAB = QtGui.QLineEdit(self.layoutWidget3)
        self.editBAB.setObjectName(_fromUtf8("editBAB"))
        self.gridLayout_4.addWidget(self.editBAB, 0, 4, 1, 1)
        self.labelRanged = QtGui.QLabel(self.layoutWidget3)
        self.labelRanged.setObjectName(_fromUtf8("labelRanged"))
        self.gridLayout_4.addWidget(self.labelRanged, 1, 0, 1, 2)
        self.editRanged = QtGui.QLineEdit(self.layoutWidget3)
        self.editRanged.setObjectName(_fromUtf8("editRanged"))
        self.gridLayout_4.addWidget(self.editRanged, 1, 2, 1, 1)
        self.labelCMB = QtGui.QLabel(self.layoutWidget3)
        self.labelCMB.setObjectName(_fromUtf8("labelCMB"))
        self.gridLayout_4.addWidget(self.labelCMB, 1, 3, 1, 1)
        self.editCMB = QtGui.QLineEdit(self.layoutWidget3)
        self.editCMB.setObjectName(_fromUtf8("editCMB"))
        self.gridLayout_4.addWidget(self.editCMB, 1, 4, 1, 1)
        self.editMelee = QtGui.QLineEdit(self.layoutWidget3)
        self.editMelee.setObjectName(_fromUtf8("editMelee"))
        self.gridLayout_4.addWidget(self.editMelee, 0, 2, 1, 1)
        self.labelMelee = QtGui.QLabel(self.layoutWidget3)
        self.labelMelee.setObjectName(_fromUtf8("labelMelee"))
        self.gridLayout_4.addWidget(self.labelMelee, 0, 0, 1, 2)
        self.stackedWidget.addWidget(self.pageOffense)
        self.pageDefense = QtGui.QWidget()
        self.pageDefense.setObjectName(_fromUtf8("pageDefense"))
        self.line_2 = QtGui.QFrame(self.pageDefense)
        self.line_2.setGeometry(QtCore.QRect(40, 100, 551, 20))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.layoutWidget4 = QtGui.QWidget(self.pageDefense)
        self.layoutWidget4.setGeometry(QtCore.QRect(20, 130, 561, 33))
        self.layoutWidget4.setObjectName(_fromUtf8("layoutWidget4"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.layoutWidget4)
        self.horizontalLayout_7.setMargin(0)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.labelCMD = QtGui.QLabel(self.layoutWidget4)
        self.labelCMD.setObjectName(_fromUtf8("labelCMD"))
        self.horizontalLayout_7.addWidget(self.labelCMD)
        self.editCMD = QtGui.QLineEdit(self.layoutWidget4)
        self.editCMD.setObjectName(_fromUtf8("editCMD"))
        self.horizontalLayout_7.addWidget(self.editCMD)
        self.labelCMDFlat = QtGui.QLabel(self.layoutWidget4)
        self.labelCMDFlat.setObjectName(_fromUtf8("labelCMDFlat"))
        self.horizontalLayout_7.addWidget(self.labelCMDFlat)
        self.editCMDFlat = QtGui.QLineEdit(self.layoutWidget4)
        self.editCMDFlat.setObjectName(_fromUtf8("editCMDFlat"))
        self.horizontalLayout_7.addWidget(self.editCMDFlat)
        self.layoutWidget5 = QtGui.QWidget(self.pageDefense)
        self.layoutWidget5.setGeometry(QtCore.QRect(22, 21, 561, 71))
        self.layoutWidget5.setObjectName(_fromUtf8("layoutWidget5"))
        self.gridLayout_5 = QtGui.QGridLayout(self.layoutWidget5)
        self.gridLayout_5.setMargin(0)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.labelAC = QtGui.QLabel(self.layoutWidget5)
        self.labelAC.setObjectName(_fromUtf8("labelAC"))
        self.gridLayout_5.addWidget(self.labelAC, 0, 0, 1, 2)
        self.editAC = QtGui.QLineEdit(self.layoutWidget5)
        self.editAC.setObjectName(_fromUtf8("editAC"))
        self.gridLayout_5.addWidget(self.editAC, 0, 2, 1, 1)
        self.labelACFlat = QtGui.QLabel(self.layoutWidget5)
        self.labelACFlat.setObjectName(_fromUtf8("labelACFlat"))
        self.gridLayout_5.addWidget(self.labelACFlat, 0, 3, 1, 1)
        self.editACFlat = QtGui.QLineEdit(self.layoutWidget5)
        self.editACFlat.setObjectName(_fromUtf8("editACFlat"))
        self.gridLayout_5.addWidget(self.editACFlat, 0, 4, 1, 1)
        self.editACTouch = QtGui.QLineEdit(self.layoutWidget5)
        self.editACTouch.setObjectName(_fromUtf8("editACTouch"))
        self.gridLayout_5.addWidget(self.editACTouch, 1, 2, 1, 1)
        self.labelACTouch = QtGui.QLabel(self.layoutWidget5)
        self.labelACTouch.setObjectName(_fromUtf8("labelACTouch"))
        self.gridLayout_5.addWidget(self.labelACTouch, 1, 0, 1, 2)
        self.stackedWidget.addWidget(self.pageDefense)
        self.pageMisc = QtGui.QWidget()
        self.pageMisc.setObjectName(_fromUtf8("pageMisc"))
        self.layoutWidget6 = QtGui.QWidget(self.pageMisc)
        self.layoutWidget6.setGeometry(QtCore.QRect(19, 29, 571, 181))
        self.layoutWidget6.setObjectName(_fromUtf8("layoutWidget6"))
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget6)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.labelHP = QtGui.QLabel(self.layoutWidget6)
        self.labelHP.setObjectName(_fromUtf8("labelHP"))
        self.gridLayout_2.addWidget(self.labelHP, 0, 0, 1, 2)
        self.editHP = QtGui.QLineEdit(self.layoutWidget6)
        self.editHP.setObjectName(_fromUtf8("editHP"))
        self.gridLayout_2.addWidget(self.editHP, 0, 2, 1, 1)
        self.labelHPMax = QtGui.QLabel(self.layoutWidget6)
        self.labelHPMax.setObjectName(_fromUtf8("labelHPMax"))
        self.gridLayout_2.addWidget(self.labelHPMax, 0, 3, 1, 2)
        self.editHPMax = QtGui.QLineEdit(self.layoutWidget6)
        self.editHPMax.setObjectName(_fromUtf8("editHPMax"))
        self.gridLayout_2.addWidget(self.editHPMax, 0, 5, 1, 1)
        self.labelAlignment = QtGui.QLabel(self.layoutWidget6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelAlignment.sizePolicy().hasHeightForWidth())
        self.labelAlignment.setSizePolicy(sizePolicy)
        self.labelAlignment.setMinimumSize(QtCore.QSize(80, 0))
        self.labelAlignment.setObjectName(_fromUtf8("labelAlignment"))
        self.gridLayout_2.addWidget(self.labelAlignment, 2, 0, 1, 2)
        self.editAlignment = QtGui.QLineEdit(self.layoutWidget6)
        self.editAlignment.setObjectName(_fromUtf8("editAlignment"))
        self.gridLayout_2.addWidget(self.editAlignment, 2, 2, 1, 1)
        self.editSpeed = QtGui.QLineEdit(self.layoutWidget6)
        self.editSpeed.setObjectName(_fromUtf8("editSpeed"))
        self.gridLayout_2.addWidget(self.editSpeed, 1, 2, 1, 1)
        self.labelSpeed = QtGui.QLabel(self.layoutWidget6)
        self.labelSpeed.setObjectName(_fromUtf8("labelSpeed"))
        self.gridLayout_2.addWidget(self.labelSpeed, 1, 0, 1, 2)
        self.editReach = QtGui.QLineEdit(self.layoutWidget6)
        self.editReach.setObjectName(_fromUtf8("editReach"))
        self.gridLayout_2.addWidget(self.editReach, 1, 5, 1, 1)
        self.editRace = QtGui.QLineEdit(self.layoutWidget6)
        self.editRace.setObjectName(_fromUtf8("editRace"))
        self.gridLayout_2.addWidget(self.editRace, 2, 5, 1, 1)
        self.labelReach = QtGui.QLabel(self.layoutWidget6)
        self.labelReach.setObjectName(_fromUtf8("labelReach"))
        self.gridLayout_2.addWidget(self.labelReach, 1, 3, 1, 2)
        self.labelRace = QtGui.QLabel(self.layoutWidget6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelRace.sizePolicy().hasHeightForWidth())
        self.labelRace.setSizePolicy(sizePolicy)
        self.labelRace.setObjectName(_fromUtf8("labelRace"))
        self.gridLayout_2.addWidget(self.labelRace, 2, 3, 1, 2)
        self.stackedWidget.addWidget(self.pageMisc)
        self.formLayout.setWidget(1, QtGui.QFormLayout.SpanningRole, self.stackedWidget)
        self.buttonBox = QtGui.QDialogButtonBox(propertiesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.buttonBox)

        self.retranslateUi(propertiesDialog)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), propertiesDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), propertiesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(propertiesDialog)
        propertiesDialog.setTabOrder(self.editPropName, self.editPlayer)
        propertiesDialog.setTabOrder(self.editPlayer, self.editStr)
        propertiesDialog.setTabOrder(self.editStr, self.editInt)
        propertiesDialog.setTabOrder(self.editInt, self.editDex)
        propertiesDialog.setTabOrder(self.editDex, self.editWis)
        propertiesDialog.setTabOrder(self.editWis, self.editCon)
        propertiesDialog.setTabOrder(self.editCon, self.editCha)
        propertiesDialog.setTabOrder(self.editCha, self.editMelee)
        propertiesDialog.setTabOrder(self.editMelee, self.editBAB)
        propertiesDialog.setTabOrder(self.editBAB, self.editRanged)
        propertiesDialog.setTabOrder(self.editRanged, self.editCMB)
        propertiesDialog.setTabOrder(self.editCMB, self.editAC)
        propertiesDialog.setTabOrder(self.editAC, self.editACFlat)
        propertiesDialog.setTabOrder(self.editACFlat, self.editACTouch)
        propertiesDialog.setTabOrder(self.editACTouch, self.editCMD)
        propertiesDialog.setTabOrder(self.editCMD, self.editCMDFlat)
        propertiesDialog.setTabOrder(self.editCMDFlat, self.editHP)
        propertiesDialog.setTabOrder(self.editHP, self.editHPMax)
        propertiesDialog.setTabOrder(self.editHPMax, self.editSpeed)
        propertiesDialog.setTabOrder(self.editSpeed, self.editReach)
        propertiesDialog.setTabOrder(self.editReach, self.defenseButton)
        propertiesDialog.setTabOrder(self.defenseButton, self.basicButton)
        propertiesDialog.setTabOrder(self.basicButton, self.offenseButton)
        propertiesDialog.setTabOrder(self.offenseButton, self.miscButton)

    def retranslateUi(self, propertiesDialog):
        propertiesDialog.setWindowTitle(QtGui.QApplication.translate("propertiesDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.basicButton.setText(QtGui.QApplication.translate("propertiesDialog", "Basic", None, QtGui.QApplication.UnicodeUTF8))
        self.offenseButton.setText(QtGui.QApplication.translate("propertiesDialog", "Offense", None, QtGui.QApplication.UnicodeUTF8))
        self.defenseButton.setText(QtGui.QApplication.translate("propertiesDialog", "Defense", None, QtGui.QApplication.UnicodeUTF8))
        self.miscButton.setText(QtGui.QApplication.translate("propertiesDialog", "Misc", None, QtGui.QApplication.UnicodeUTF8))
        self.labelInt.setText(QtGui.QApplication.translate("propertiesDialog", "Intelligence", None, QtGui.QApplication.UnicodeUTF8))
        self.labelCon.setText(QtGui.QApplication.translate("propertiesDialog", "Constitution", None, QtGui.QApplication.UnicodeUTF8))
        self.labelDex.setText(QtGui.QApplication.translate("propertiesDialog", "Dexterity", None, QtGui.QApplication.UnicodeUTF8))
        self.labelStr.setText(QtGui.QApplication.translate("propertiesDialog", "Strength", None, QtGui.QApplication.UnicodeUTF8))
        self.labelCha.setText(QtGui.QApplication.translate("propertiesDialog", "Charisma", None, QtGui.QApplication.UnicodeUTF8))
        self.labelWis.setText(QtGui.QApplication.translate("propertiesDialog", "Wisdom", None, QtGui.QApplication.UnicodeUTF8))
        self.labelPropName.setText(QtGui.QApplication.translate("propertiesDialog", "<b>Token Property Name</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelPlayer.setText(QtGui.QApplication.translate("propertiesDialog", "Player Name", None, QtGui.QApplication.UnicodeUTF8))
        self.labelName.setText(QtGui.QApplication.translate("propertiesDialog", "Character Name", None, QtGui.QApplication.UnicodeUTF8))
        self.labelBAB.setText(QtGui.QApplication.translate("propertiesDialog", "BAB", None, QtGui.QApplication.UnicodeUTF8))
        self.labelRanged.setText(QtGui.QApplication.translate("propertiesDialog", "Ranged Attack", None, QtGui.QApplication.UnicodeUTF8))
        self.labelCMB.setText(QtGui.QApplication.translate("propertiesDialog", "CMB", None, QtGui.QApplication.UnicodeUTF8))
        self.labelMelee.setText(QtGui.QApplication.translate("propertiesDialog", "Melee Attack", None, QtGui.QApplication.UnicodeUTF8))
        self.labelCMD.setText(QtGui.QApplication.translate("propertiesDialog", "CMD", None, QtGui.QApplication.UnicodeUTF8))
        self.labelCMDFlat.setText(QtGui.QApplication.translate("propertiesDialog", "CMD Flatfooted", None, QtGui.QApplication.UnicodeUTF8))
        self.labelAC.setText(QtGui.QApplication.translate("propertiesDialog", "AC Normal", None, QtGui.QApplication.UnicodeUTF8))
        self.labelACFlat.setText(QtGui.QApplication.translate("propertiesDialog", "AC Flatfooted", None, QtGui.QApplication.UnicodeUTF8))
        self.labelACTouch.setText(QtGui.QApplication.translate("propertiesDialog", "AC Touch", None, QtGui.QApplication.UnicodeUTF8))
        self.labelHP.setText(QtGui.QApplication.translate("propertiesDialog", "HP Current", None, QtGui.QApplication.UnicodeUTF8))
        self.labelHPMax.setText(QtGui.QApplication.translate("propertiesDialog", "HP Max", None, QtGui.QApplication.UnicodeUTF8))
        self.labelAlignment.setText(QtGui.QApplication.translate("propertiesDialog", "Alignment", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSpeed.setText(QtGui.QApplication.translate("propertiesDialog", "Speed", None, QtGui.QApplication.UnicodeUTF8))
        self.labelReach.setText(QtGui.QApplication.translate("propertiesDialog", "Reach", None, QtGui.QApplication.UnicodeUTF8))
        self.labelRace.setText(QtGui.QApplication.translate("propertiesDialog", "Race", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc
