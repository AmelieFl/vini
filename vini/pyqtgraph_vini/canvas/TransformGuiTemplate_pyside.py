# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyqtgraph/canvas/TransformGuiTemplate.ui'
#
# Created: Wed Nov  9 17:57:16 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(224, 117)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy.Preferred, QtGui.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.translateLabel = QtGui.QLabel(Form)
        self.translateLabel.setObjectName("translateLabel")
        self.verticalLayout.addWidget(self.translateLabel)
        self.rotateLabel = QtGui.QLabel(Form)
        self.rotateLabel.setObjectName("rotateLabel")
        self.verticalLayout.addWidget(self.rotateLabel)
        self.scaleLabel = QtGui.QLabel(Form)
        self.scaleLabel.setObjectName("scaleLabel")
        self.verticalLayout.addWidget(self.scaleLabel)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mirrorImageBtn = QtGui.QPushButton(Form)
        self.mirrorImageBtn.setToolTip("")
        self.mirrorImageBtn.setObjectName("mirrorImageBtn")
        self.horizontalLayout.addWidget(self.mirrorImageBtn)
        self.reflectImageBtn = QtGui.QPushButton(Form)
        self.reflectImageBtn.setObjectName("reflectImageBtn")
        self.horizontalLayout.addWidget(self.reflectImageBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, QtWidgets.QApplication.UnicodeUTF8))
        self.translateLabel.setText(QtWidgets.QApplication.translate("Form", "Translate:", None, QtWidgets.QApplication.UnicodeUTF8))
        self.rotateLabel.setText(QtWidgets.QApplication.translate("Form", "Rotate:", None, QtWidgets.QApplication.UnicodeUTF8))
        self.scaleLabel.setText(QtWidgets.QApplication.translate("Form", "Scale:", None, QtWidgets.QApplication.UnicodeUTF8))
        self.mirrorImageBtn.setText(QtWidgets.QApplication.translate("Form", "Mirror", None, QtWidgets.QApplication.UnicodeUTF8))
        self.reflectImageBtn.setText(QtWidgets.QApplication.translate("Form", "Reflect", None, QtWidgets.QApplication.UnicodeUTF8))

