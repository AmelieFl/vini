# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './pyqtgraph/console/template.ui'
#
# Created: Wed Mar 26 15:09:29 2014
#      by: PyQt6 UI code generator 5.0.1
#
# WARNING! All changes made in this file will be lost!

try:
    from PyQt6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(710, 497)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.output = QtWidgets.QPlainTextEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.output.setFont(font)
        self.output.setReadOnly(True)
        self.output.setObjectName("output")
        self.verticalLayout.addWidget(self.output)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.input = CmdInput(self.layoutWidget)
        self.input.setObjectName("input")
        self.horizontalLayout.addWidget(self.input)
        self.historyBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.historyBtn.setCheckable(True)
        self.historyBtn.setObjectName("historyBtn")
        self.horizontalLayout.addWidget(self.historyBtn)
        self.exceptionBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.exceptionBtn.setCheckable(True)
        self.exceptionBtn.setObjectName("exceptionBtn")
        self.horizontalLayout.addWidget(self.exceptionBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.historyList = QtWidgets.QListWidget(self.splitter)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.historyList.setFont(font)
        self.historyList.setObjectName("historyList")
        self.exceptionGroup = QtWidgets.QGroupBox(self.splitter)
        self.exceptionGroup.setObjectName("exceptionGroup")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.exceptionGroup)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.catchAllExceptionsBtn = QtWidgets.QPushButton(self.exceptionGroup)
        self.catchAllExceptionsBtn.setCheckable(True)
        self.catchAllExceptionsBtn.setObjectName("catchAllExceptionsBtn")
        self.gridLayout_2.addWidget(self.catchAllExceptionsBtn, 0, 1, 1, 1)
        self.catchNextExceptionBtn = QtWidgets.QPushButton(self.exceptionGroup)
        self.catchNextExceptionBtn.setCheckable(True)
        self.catchNextExceptionBtn.setObjectName("catchNextExceptionBtn")
        self.gridLayout_2.addWidget(self.catchNextExceptionBtn, 0, 0, 1, 1)
        self.onlyUncaughtCheck = QtWidgets.QCheckBox(self.exceptionGroup)
        self.onlyUncaughtCheck.setChecked(True)
        self.onlyUncaughtCheck.setObjectName("onlyUncaughtCheck")
        self.gridLayout_2.addWidget(self.onlyUncaughtCheck, 0, 2, 1, 1)
        self.exceptionStackList = QtWidgets.QListWidget(self.exceptionGroup)
        self.exceptionStackList.setAlternatingRowColors(True)
        self.exceptionStackList.setObjectName("exceptionStackList")
        self.gridLayout_2.addWidget(self.exceptionStackList, 2, 0, 1, 5)
        self.runSelectedFrameCheck = QtWidgets.QCheckBox(self.exceptionGroup)
        self.runSelectedFrameCheck.setChecked(True)
        self.runSelectedFrameCheck.setObjectName("runSelectedFrameCheck")
        self.gridLayout_2.addWidget(self.runSelectedFrameCheck, 3, 0, 1, 5)
        self.exceptionInfoLabel = QtWidgets.QLabel(self.exceptionGroup)
        self.exceptionInfoLabel.setObjectName("exceptionInfoLabel")
        self.gridLayout_2.addWidget(self.exceptionInfoLabel, 1, 0, 1, 5)
        self.clearExceptionBtn = QtWidgets.QPushButton(self.exceptionGroup)
        self.clearExceptionBtn.setEnabled(False)
        self.clearExceptionBtn.setObjectName("clearExceptionBtn")
        self.gridLayout_2.addWidget(self.clearExceptionBtn, 0, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Console"))
        self.historyBtn.setText(_translate("Form", "History.."))
        self.exceptionBtn.setText(_translate("Form", "Exceptions.."))
        self.exceptionGroup.setTitle(_translate("Form", "Exception Handling"))
        self.catchAllExceptionsBtn.setText(_translate("Form", "Show All Exceptions"))
        self.catchNextExceptionBtn.setText(_translate("Form", "Show Next Exception"))
        self.onlyUncaughtCheck.setText(_translate("Form", "Only Uncaught Exceptions"))
        self.runSelectedFrameCheck.setText(_translate("Form", "Run commands in selected stack frame"))
        self.exceptionInfoLabel.setText(_translate("Form", "Exception Info"))
        self.clearExceptionBtn.setText(_translate("Form", "Clear Exception"))

from .CmdInput import CmdInput
