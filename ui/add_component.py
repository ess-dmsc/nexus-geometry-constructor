from PySide2 import QtCore, QtWidgets
from PySide2.QtWebEngineWidgets import QWebEngineView


class Ui_AddComponentDialog(object):
    def setupUi(self, AddComponentDialog):
        AddComponentDialog.setObjectName("AddComponentDialog")
        AddComponentDialog.resize(1600, 900)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            AddComponentDialog.sizePolicy().hasHeightForWidth()
        )
        AddComponentDialog.setSizePolicy(sizePolicy)
        self.gridLayout_3 = QtWidgets.QGridLayout(AddComponentDialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.ok_button = QtWidgets.QPushButton(AddComponentDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ok_button.sizePolicy().hasHeightForWidth())
        self.ok_button.setSizePolicy(sizePolicy)
        self.ok_button.setMinimumSize(QtCore.QSize(104, 23))
        self.ok_button.setMaximumSize(QtCore.QSize(200, 16777215))
        self.ok_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ok_button.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ok_button.setAutoDefault(False)
        self.ok_button.setObjectName("buttonBox")
        self.gridLayout_3.addWidget(self.ok_button, 1, 0, 1, 1)
        self.widget = QtWidgets.QWidget(AddComponentDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label)
        self.nameLineEdit = QtWidgets.QLineEdit(self.widget)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.horizontalLayout_5.addWidget(self.nameLineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_6.addWidget(self.label_2)
        self.descriptionPlainTextEdit = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.descriptionPlainTextEdit.sizePolicy().hasHeightForWidth()
        )
        self.descriptionPlainTextEdit.setSizePolicy(sizePolicy)
        self.descriptionPlainTextEdit.setObjectName("descriptionPlainTextEdit")
        self.horizontalLayout_6.addWidget(self.descriptionPlainTextEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.componentTypeComboBox = QtWidgets.QComboBox(self.widget)
        self.componentTypeComboBox.setObjectName("componentTypeComboBox")
        self.horizontalLayout_4.addWidget(self.componentTypeComboBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.shapeTypeBox = QtWidgets.QGroupBox(self.widget)
        self.shapeTypeBox.setObjectName("shapeTypeBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.shapeTypeBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.noShapeRadioButton = QtWidgets.QRadioButton(self.shapeTypeBox)
        self.noShapeRadioButton.setObjectName("noShapeRadioButton")
        self.horizontalLayout.addWidget(self.noShapeRadioButton)
        self.meshRadioButton = QtWidgets.QRadioButton(self.shapeTypeBox)
        self.meshRadioButton.setObjectName("meshRadioButton")
        self.horizontalLayout.addWidget(self.meshRadioButton)
        self.CylinderRadioButton = QtWidgets.QRadioButton(self.shapeTypeBox)
        self.CylinderRadioButton.setObjectName("CylinderRadioButton")
        self.horizontalLayout.addWidget(self.CylinderRadioButton)
        self.verticalLayout_2.addWidget(self.shapeTypeBox)
        self.shapeOptionsBox = QtWidgets.QGroupBox(self.widget)
        self.shapeOptionsBox.setObjectName("shapeOptionsBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.shapeOptionsBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.geometryFileBox = QtWidgets.QGroupBox(self.shapeOptionsBox)
        self.geometryFileBox.setObjectName("geometryFileBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.geometryFileBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.fileLineEdit = QtWidgets.QLineEdit(self.geometryFileBox)
        self.fileLineEdit.setReadOnly(True)
        self.fileLineEdit.setObjectName("fileLineEdit")
        self.horizontalLayout_2.addWidget(self.fileLineEdit)
        self.fileBrowseButton = QtWidgets.QPushButton(self.geometryFileBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.fileBrowseButton.sizePolicy().hasHeightForWidth()
        )
        self.fileBrowseButton.setSizePolicy(sizePolicy)
        self.fileBrowseButton.setMinimumSize(QtCore.QSize(80, 23))
        self.fileBrowseButton.setObjectName("fileBrowseButton")
        self.horizontalLayout_2.addWidget(self.fileBrowseButton)
        self.gridLayout_2.addWidget(self.geometryFileBox, 1, 0, 1, 1)
        self.cylinderOptionsBox = QtWidgets.QGroupBox(self.shapeOptionsBox)
        self.cylinderOptionsBox.setObjectName("cylinderOptionsBox")
        self.gridLayout = QtWidgets.QGridLayout(self.cylinderOptionsBox)
        self.gridLayout.setObjectName("gridLayout")
        self.cylinderXLineEdit = QtWidgets.QDoubleSpinBox(self.cylinderOptionsBox)
        self.cylinderXLineEdit.setMaximum(100000.0)
        self.cylinderXLineEdit.setObjectName("cylinderXLineEdit")
        self.gridLayout.addWidget(self.cylinderXLineEdit, 2, 1, 1, 1)
        self.cylinderRadiusLineEdit = QtWidgets.QDoubleSpinBox(self.cylinderOptionsBox)
        self.cylinderRadiusLineEdit.setMaximum(100000.0)
        self.cylinderRadiusLineEdit.setObjectName("cylinderRadiusLineEdit")
        self.gridLayout.addWidget(self.cylinderRadiusLineEdit, 0, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.cylinderOptionsBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.cylinderYLineEdit = QtWidgets.QDoubleSpinBox(self.cylinderOptionsBox)
        self.cylinderYLineEdit.setMaximum(100000.0)
        self.cylinderYLineEdit.setObjectName("cylinderYLineEdit")
        self.gridLayout.addWidget(self.cylinderYLineEdit, 2, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.cylinderOptionsBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.cylinderOptionsBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.cylinderOptionsBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.cylinderOptionsBox)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 4, 1, 1)
        self.cylinderHeightLineEdit = QtWidgets.QDoubleSpinBox(self.cylinderOptionsBox)
        self.cylinderHeightLineEdit.setMaximum(100000.0)
        self.cylinderHeightLineEdit.setObjectName("cylinderHeightLineEdit")
        self.gridLayout.addWidget(self.cylinderHeightLineEdit, 0, 1, 1, 1)
        self.cylinderZLineEdit = QtWidgets.QDoubleSpinBox(self.cylinderOptionsBox)
        self.cylinderZLineEdit.setMaximum(100000.0)
        self.cylinderZLineEdit.setProperty("value", 1.0)
        self.cylinderZLineEdit.setObjectName("cylinderZLineEdit")
        self.gridLayout.addWidget(self.cylinderZLineEdit, 2, 5, 1, 1)
        self.cylinderCountLabel = QtWidgets.QLabel(self.cylinderOptionsBox)
        self.cylinderCountLabel.setObjectName("cylinderCountLabel")
        self.gridLayout.addWidget(self.cylinderCountLabel, 3, 0, 1, 1)
        self.cylinderCountSpinBox = QtWidgets.QSpinBox(self.cylinderOptionsBox)
        self.cylinderCountSpinBox.setEnabled(False)
        self.cylinderCountSpinBox.setMinimum(1)
        self.cylinderCountSpinBox.setMaximum(999999999)
        self.cylinderCountSpinBox.setObjectName("cylinderCountSpinBox")
        self.gridLayout.addWidget(self.cylinderCountSpinBox, 3, 1, 1, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(3, 1)
        self.gridLayout.setColumnStretch(5, 1)
        self.gridLayout_2.addWidget(self.cylinderOptionsBox, 3, 0, 1, 1)
        self.unitsbox = QtWidgets.QGroupBox(self.shapeOptionsBox)
        self.unitsbox.setObjectName("unitsbox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.unitsbox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.unitsLineEdit = QtWidgets.QLineEdit(self.unitsbox)
        self.unitsLineEdit.setPlaceholderText("")
        self.unitsLineEdit.setObjectName("unitsLineEdit")
        self.horizontalLayout_3.addWidget(self.unitsLineEdit)
        self.gridLayout_2.addWidget(self.unitsbox, 0, 0, 1, 1)
        self.pixelOptionsWidget = QtWidgets.QWidget(self.shapeOptionsBox)
        self.gridLayout_2.addWidget(self.pixelOptionsWidget, 4, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.shapeOptionsBox)
        self.fieldsBox = QtWidgets.QGroupBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fieldsBox.sizePolicy().hasHeightForWidth())
        self.fieldsBox.setSizePolicy(sizePolicy)
        self.fieldsBox.setObjectName("fieldsBox")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.fieldsBox)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.addFieldPushButton = QtWidgets.QPushButton(self.fieldsBox)
        self.addFieldPushButton.setObjectName("addFieldPushButton")
        self.gridLayout_5.addWidget(self.addFieldPushButton, 0, 0, 1, 1)
        self.removeFieldPushButton = QtWidgets.QPushButton(self.fieldsBox)
        self.removeFieldPushButton.setObjectName("removeFieldPushButton")
        self.gridLayout_5.addWidget(self.removeFieldPushButton, 0, 1, 1, 1)
        self.fieldsListWidget = QtWidgets.QListWidget(self.fieldsBox)
        self.fieldsListWidget.setObjectName("fieldsListWidget")
        self.gridLayout_5.addWidget(self.fieldsListWidget, 1, 0, 1, 2)
        self.verticalLayout_2.addWidget(self.fieldsBox)
        self.verticalLayout_2.setStretch(5, 1)
        self.gridLayout_4.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.webEngineView = QWebEngineView(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.webEngineView.sizePolicy().hasHeightForWidth()
        )
        self.webEngineView.setSizePolicy(sizePolicy)
        self.webEngineView.setProperty("url", QtCore.QUrl("about:blank"))
        self.webEngineView.setObjectName("webEngineView")
        self.gridLayout_4.addWidget(self.webEngineView, 0, 1, 1, 1)
        self.gridLayout_4.setColumnStretch(0, 1)
        self.gridLayout_4.setColumnStretch(1, 1)
        self.gridLayout_3.addWidget(self.widget, 0, 0, 1, 1)

        self.retranslateUi(AddComponentDialog)
        QtCore.QObject.connect(
            self.ok_button,
            QtCore.SIGNAL("clicked()"),
            AddComponentDialog.close_without_msg_box,
        )
        QtCore.QMetaObject.connectSlotsByName(AddComponentDialog)

    def retranslateUi(self, AddComponentDialog):
        AddComponentDialog.setWindowTitle(
            QtWidgets.QApplication.translate(
                "AddComponentDialog", "Add Component", None, -1
            )
        )
        self.ok_button.setText(
            QtWidgets.QApplication.translate(
                "AddComponentDialog", "Add component", None, -1
            )
        )
        self.label.setText(
            QtWidgets.QApplication.translate("AddComponentDialog", "Name:", None, -1)
        )
        self.label_2.setText(
            QtWidgets.QApplication.translate(
                "AddComponentDialog", "Description:", None, -1
            )
        )
        self.label_3.setText(
            QtWidgets.QApplication.translate(
                "AddComponentDialog", "Component type:", None, -1
            )
        )
        self.shapeTypeBox.setTitle(
            QtWidgets.QApplication.translate(
                "AddComponentDialog", "Shape type:", None, -1
            )
        )
        self.noShapeRadioButton.setText(
            QtWidgets.QApplication.translate("AddComponentDialog", "No Shape", None, -1)
        )
        self.meshRadioButton.setText(
            QtWidgets.QApplication.translate("AddComponentDialog", "Mesh", None, -1)
        )
        self.CylinderRadioButton.setText(
            QtWidgets.QApplication.translate("AddComponentDialog", "Cylinder", None, -1)
        )
        self.shapeOptionsBox.setTitle(
            QtWidgets.QApplication.translate(
                "AddComponentDialog", "Shape options:", None, -1
            )
        )
        self.geometryFileBox.setTitle(
            QtWidgets.QApplication.translate("AddComponentDialog", "CAD file", None, -1)
        )
        self.fileBrowseButton.setText(
            QtWidgets.QApplication.translate(
                "AddComponentDialog", "Browse...", None, -1
            )
        )
        self.cylinderOptionsBox.setTitle(
            QtWidgets.QApplication.translate(
                "AddComponentDialog", "Cylinder options", None, -1
            )
        )
        self.label_6.setText(
            QtWidgets.QApplication.translate("AddComponentDialog", "X:", None, -1)
        )
        self.label_5.setText(
            QtWidgets.QApplication.translate("AddComponentDialog", "Radius", None, -1)
        )
        self.label_7.setText(
            QtWidgets.QApplication.translate("AddComponentDialog", "Y:", None, -1)
        )
        self.label_4.setText(
            QtWidgets.QApplication.translate("AddComponentDialog", "Height", None, -1)
        )
        self.label_8.setText(
            QtWidgets.QApplication.translate("AddComponentDialog", "Z:", None, -1)
        )
        self.cylinderCountLabel.setText(
            QtWidgets.QApplication.translate(
                "AddComponentDialog", "Cylinder Count:", None, -1
            )
        )
        self.unitsbox.setTitle(
            QtWidgets.QApplication.translate("AddComponentDialog", "Units", None, -1)
        )
        self.unitsLineEdit.setText(
            QtWidgets.QApplication.translate("AddComponentDialog", "m", None, -1)
        )
        self.fieldsBox.setTitle(
            QtWidgets.QApplication.translate("AddComponentDialog", "Fields", None, -1)
        )
        self.addFieldPushButton.setText(
            QtWidgets.QApplication.translate(
                "AddComponentDialog", "Add field", None, -1
            )
        )
        self.removeFieldPushButton.setText(
            QtWidgets.QApplication.translate(
                "AddComponentDialog", "Remove field", None, -1
            )
        )
