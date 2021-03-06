# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './wid_tty_monitor.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_widMon(object):
    def setupUi(self, widMon):
        widMon.setObjectName(_fromUtf8("widMon"))
        widMon.resize(1099, 612)
        self.gridLayout = QtGui.QGridLayout(widMon)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gbx_chart = QtGui.QGroupBox(widMon)
        self.gbx_chart.setObjectName(_fromUtf8("gbx_chart"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.gbx_chart)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.scrollArea = QtGui.QScrollArea(self.gbx_chart)
        self.scrollArea.setAutoFillBackground(False)
        self.scrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtGui.QFrame.Plain)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 511, 258))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.formLayout = QtGui.QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout.setMargin(0)
        self.formLayout.setSpacing(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.chart = Chart(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chart.sizePolicy().hasHeightForWidth())
        self.chart.setSizePolicy(sizePolicy)
        self.chart.setMinimumSize(QtCore.QSize(500, 200))
        self.chart.setObjectName(_fromUtf8("chart"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.chart)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_4.addWidget(self.scrollArea)
        self.gridLayout.addWidget(self.gbx_chart, 1, 1, 1, 1)
        self.gbx_setup = QtGui.QGroupBox(widMon)
        self.gbx_setup.setMaximumSize(QtCore.QSize(16777215, 250))
        self.gbx_setup.setObjectName(_fromUtf8("gbx_setup"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gbx_setup)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lbl_port = QtGui.QLabel(self.gbx_setup)
        self.lbl_port.setObjectName(_fromUtf8("lbl_port"))
        self.gridLayout_2.addWidget(self.lbl_port, 0, 1, 1, 1)
        self.btn_stop = QtGui.QPushButton(self.gbx_setup)
        self.btn_stop.setObjectName(_fromUtf8("btn_stop"))
        self.gridLayout_2.addWidget(self.btn_stop, 1, 4, 1, 1)
        self.btn_start = QtGui.QPushButton(self.gbx_setup)
        self.btn_start.setObjectName(_fromUtf8("btn_start"))
        self.gridLayout_2.addWidget(self.btn_start, 0, 4, 1, 1)
        self.lbl_baud = QtGui.QLabel(self.gbx_setup)
        self.lbl_baud.setObjectName(_fromUtf8("lbl_baud"))
        self.gridLayout_2.addWidget(self.lbl_baud, 1, 1, 1, 1)
        self.cbx_port = QtGui.QComboBox(self.gbx_setup)
        self.cbx_port.setObjectName(_fromUtf8("cbx_port"))
        self.gridLayout_2.addWidget(self.cbx_port, 0, 2, 1, 1)
        self.cbx_baud = QtGui.QComboBox(self.gbx_setup)
        self.cbx_baud.setObjectName(_fromUtf8("cbx_baud"))
        self.gridLayout_2.addWidget(self.cbx_baud, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.gbx_setup, 1, 0, 1, 1)
        self.gbx_data = QtGui.QGroupBox(widMon)
        self.gbx_data.setObjectName(_fromUtf8("gbx_data"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.gbx_data)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.frm_data = QtGui.QFrame(self.gbx_data)
        self.frm_data.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frm_data.setFrameShadow(QtGui.QFrame.Raised)
        self.frm_data.setObjectName(_fromUtf8("frm_data"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frm_data)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pte_data = QtGui.QPlainTextEdit(self.frm_data)
        self.pte_data.setMinimumSize(QtCore.QSize(350, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier"))
        font.setPointSize(10)
        self.pte_data.setFont(font)
        self.pte_data.setObjectName(_fromUtf8("pte_data"))
        self.verticalLayout.addWidget(self.pte_data)
        self.frm_text = QtGui.QFrame(self.frm_data)
        self.frm_text.setAutoFillBackground(True)
        self.frm_text.setFrameShape(QtGui.QFrame.Panel)
        self.frm_text.setFrameShadow(QtGui.QFrame.Raised)
        self.frm_text.setObjectName(_fromUtf8("frm_text"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frm_text)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.qle_text = QtGui.QLineEdit(self.frm_text)
        self.qle_text.setEnabled(True)
        self.qle_text.setText(_fromUtf8(""))
        self.qle_text.setObjectName(_fromUtf8("qle_text"))
        self.horizontalLayout_3.addWidget(self.qle_text)
        self.btn_send = QtGui.QPushButton(self.frm_text)
        self.btn_send.setEnabled(False)
        self.btn_send.setObjectName(_fromUtf8("btn_send"))
        self.horizontalLayout_3.addWidget(self.btn_send)
        self.verticalLayout.addWidget(self.frm_text)
        self.verticalLayout_2.addWidget(self.frm_data)
        self.gridLayout.addWidget(self.gbx_data, 0, 0, 1, 1)
        self.gbx_config = QtGui.QGroupBox(widMon)
        self.gbx_config.setObjectName(_fromUtf8("gbx_config"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.gbx_config)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.pte_config = QtGui.QPlainTextEdit(self.gbx_config)
        self.pte_config.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier"))
        font.setPointSize(10)
        self.pte_config.setFont(font)
        self.pte_config.setDocumentTitle(_fromUtf8(""))
        self.pte_config.setReadOnly(False)
        self.pte_config.setPlainText(_fromUtf8(""))
        self.pte_config.setObjectName(_fromUtf8("pte_config"))
        self.verticalLayout_3.addWidget(self.pte_config)
        self.gridLayout.addWidget(self.gbx_config, 0, 1, 1, 1)

        self.retranslateUi(widMon)
        QtCore.QMetaObject.connectSlotsByName(widMon)

    def retranslateUi(self, widMon):
        widMon.setWindowTitle(_translate("widMon", "TTY Monitor", None))
        self.gbx_chart.setTitle(_translate("widMon", "Chart", None))
        self.gbx_setup.setTitle(_translate("widMon", "Setup", None))
        self.lbl_port.setText(_translate("widMon", "Port:", None))
        self.btn_stop.setText(_translate("widMon", "Stop", None))
        self.btn_start.setText(_translate("widMon", "Start", None))
        self.lbl_baud.setText(_translate("widMon", "Baudrate:", None))
        self.gbx_data.setTitle(_translate("widMon", "Data", None))
        self.btn_send.setText(_translate("widMon", "Send", None))
        self.gbx_config.setTitle(_translate("widMon", "Configuration", None))

from chart import Chart
