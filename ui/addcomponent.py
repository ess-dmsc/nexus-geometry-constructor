# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addcomponent.ui',
# licensing of 'addcomponent.ui' applies.
#
# Created: Thu May 30 16:48:49 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_AddComponentDialog(object):
    def setupUi(self, AddComponentDialog):
        AddComponentDialog.setObjectName("AddComponentDialog")
        AddComponentDialog.resize(1177, 919)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddComponentDialog)
        self.buttonBox.setGeometry(QtCore.QRect(1000, 890, 164, 20))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(AddComponentDialog)
        self.label.setGeometry(QtCore.QRect(1, 11, 30, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(AddComponentDialog)
        self.label_2.setGeometry(QtCore.QRect(1, 37, 61, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(AddComponentDialog)
        self.label_3.setGeometry(QtCore.QRect(1, 133, 87, 16))
        self.label_3.setObjectName("label_3")
        self.webView = QtWebKit.QWebView(AddComponentDialog)
        self.webView.setGeometry(QtCore.QRect(660, 10, 491, 831))
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")
        self.geometryOptionsBox = QtWidgets.QGroupBox(AddComponentDialog)
        self.geometryOptionsBox.setGeometry(QtCore.QRect(0, 240, 571, 411))
        self.geometryOptionsBox.setObjectName("geometryOptionsBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.geometryOptionsBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pixelOptionsBox = QtWidgets.QGroupBox(self.geometryOptionsBox)
        self.pixelOptionsBox.setObjectName("pixelOptionsBox")
        self.gridLayout_2.addWidget(self.pixelOptionsBox, 3, 0, 1, 1)
        self.geometryFileBox = QtWidgets.QGroupBox(self.geometryOptionsBox)
        self.geometryFileBox.setObjectName("geometryFileBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.geometryFileBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.fileLineEdit = QtWidgets.QLineEdit(self.geometryFileBox)
        self.fileLineEdit.setObjectName("fileLineEdit")
        self.horizontalLayout_2.addWidget(self.fileLineEdit)
        self.fileBrowseButton = QtWidgets.QPushButton(self.geometryFileBox)
        self.fileBrowseButton.setObjectName("fileBrowseButton")
        self.horizontalLayout_2.addWidget(self.fileBrowseButton)
        self.gridLayout_2.addWidget(self.geometryFileBox, 0, 0, 1, 1)
        self.groupBox_5 = QtWidgets.QGroupBox(self.geometryOptionsBox)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_2.addWidget(self.groupBox_5, 2, 0, 1, 1)
        self.unitsbox = QtWidgets.QGroupBox(self.geometryOptionsBox)
        self.unitsbox.setObjectName("unitsbox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.unitsbox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.unitsLineEdit = QtWidgets.QLineEdit(self.unitsbox)
        self.unitsLineEdit.setObjectName("unitsLineEdit")
        self.horizontalLayout_3.addWidget(self.unitsLineEdit)
        self.checkBox = QtWidgets.QCheckBox(self.unitsbox)
        self.checkBox.setText("")
        self.checkBox.setCheckable(False)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_3.addWidget(self.checkBox)
        self.gridLayout_2.addWidget(self.unitsbox, 1, 0, 1, 1)
        self.geometryTypeBox = QtWidgets.QGroupBox(AddComponentDialog)
        self.geometryTypeBox.setGeometry(QtCore.QRect(0, 170, 561, 61))
        self.geometryTypeBox.setObjectName("geometryTypeBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.geometryTypeBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.meshRadioButton = QtWidgets.QRadioButton(self.geometryTypeBox)
        self.meshRadioButton.setObjectName("meshRadioButton")
        self.horizontalLayout.addWidget(self.meshRadioButton)
        self.cylinderRadioButton = QtWidgets.QRadioButton(self.geometryTypeBox)
        self.cylinderRadioButton.setObjectName("cylinderRadioButton")
        self.horizontalLayout.addWidget(self.cylinderRadioButton)
        self.noGeometryRadioButton = QtWidgets.QRadioButton(self.geometryTypeBox)
        self.noGeometryRadioButton.setObjectName("noGeometryRadioButton")
        self.horizontalLayout.addWidget(self.noGeometryRadioButton)
        self.fieldsBox = QtWidgets.QGroupBox(AddComponentDialog)
        self.fieldsBox.setGeometry(QtCore.QRect(10, 640, 561, 253))
        self.fieldsBox.setObjectName("fieldsBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.fieldsBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.fieldsLineEdit = QtWidgets.QLineEdit(self.fieldsBox)
        self.fieldsLineEdit.setObjectName("fieldsLineEdit")
        self.verticalLayout.addWidget(self.fieldsLineEdit)
        self.fieldsListView = QtWidgets.QListView(self.fieldsBox)
        self.fieldsListView.setObjectName("fieldsListView")
        self.verticalLayout.addWidget(self.fieldsListView)
        self.descriptionPlainTextEdit = QtWidgets.QPlainTextEdit(AddComponentDialog)
        self.descriptionPlainTextEdit.setGeometry(QtCore.QRect(92, 37, 471, 51))
        self.descriptionPlainTextEdit.setObjectName("descriptionPlainTextEdit")
        self.nameLineEdit = QtWidgets.QLineEdit(AddComponentDialog)
        self.nameLineEdit.setGeometry(QtCore.QRect(92, 11, 471, 22))
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.componentTypeComboBox = QtWidgets.QComboBox(AddComponentDialog)
        self.componentTypeComboBox.setGeometry(QtCore.QRect(110, 130, 451, 22))
        self.componentTypeComboBox.setObjectName("componentTypeComboBox")

        self.retranslateUi(AddComponentDialog)
        QtCore.QMetaObject.connectSlotsByName(AddComponentDialog)

    def retranslateUi(self, AddComponentDialog):
        AddComponentDialog.setWindowTitle(QtWidgets.QApplication.translate("AddComponentDialog", "Add Component", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("AddComponentDialog", "Name", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("AddComponentDialog", "Description:", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("AddComponentDialog", "Component type:", None, -1))
        self.geometryOptionsBox.setTitle(QtWidgets.QApplication.translate("AddComponentDialog", "Geometry options:", None, -1))
        self.pixelOptionsBox.setTitle(QtWidgets.QApplication.translate("AddComponentDialog", "Pixel options", None, -1))
        self.geometryFileBox.setTitle(QtWidgets.QApplication.translate("AddComponentDialog", "Geometry file", None, -1))
        self.fileBrowseButton.setText(QtWidgets.QApplication.translate("AddComponentDialog", "Browse...", None, -1))
        self.groupBox_5.setTitle(QtWidgets.QApplication.translate("AddComponentDialog", "Cylinder options", None, -1))
        self.unitsbox.setTitle(QtWidgets.QApplication.translate("AddComponentDialog", "Units", None, -1))
        self.geometryTypeBox.setTitle(QtWidgets.QApplication.translate("AddComponentDialog", "Geometry type:", None, -1))
        self.meshRadioButton.setText(QtWidgets.QApplication.translate("AddComponentDialog", "Mesh", None, -1))
        self.cylinderRadioButton.setText(QtWidgets.QApplication.translate("AddComponentDialog", "Cylinder", None, -1))
        self.noGeometryRadioButton.setText(QtWidgets.QApplication.translate("AddComponentDialog", "No Geometry", None, -1))
        self.fieldsBox.setTitle(QtWidgets.QApplication.translate("AddComponentDialog", "Fields", None, -1))

from PySide2 import QtWebKit
