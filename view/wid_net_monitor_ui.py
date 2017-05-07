# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './wid_net_monitor.ui'
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
        widMon.resize(1099, 688)
        self.gridLayout = QtGui.QGridLayout(widMon)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gbx_ccc = QtGui.QGroupBox(widMon)
        self.gbx_ccc.setObjectName(_fromUtf8("gbx_ccc"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.gbx_ccc)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.pte_ccc = QtGui.QPlainTextEdit(self.gbx_ccc)
        self.pte_ccc.setMinimumSize(QtCore.QSize(350, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier"))
        font.setPointSize(10)
        self.pte_ccc.setFont(font)
        self.pte_ccc.setObjectName(_fromUtf8("pte_ccc"))
        self.verticalLayout_2.addWidget(self.pte_ccc)
        self.frm_text = QtGui.QFrame(self.gbx_ccc)
        self.frm_text.setAutoFillBackground(True)
        self.frm_text.setFrameShape(QtGui.QFrame.Panel)
        self.frm_text.setFrameShadow(QtGui.QFrame.Raised)
        self.frm_text.setObjectName(_fromUtf8("frm_text"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frm_text)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.qle_ccc = QtGui.QLineEdit(self.frm_text)
        self.qle_ccc.setEnabled(True)
        self.qle_ccc.setText(_fromUtf8(""))
        self.qle_ccc.setObjectName(_fromUtf8("qle_ccc"))
        self.horizontalLayout_3.addWidget(self.qle_ccc)
        self.btn_send_ccc = QtGui.QPushButton(self.frm_text)
        self.btn_send_ccc.setEnabled(False)
        self.btn_send_ccc.setObjectName(_fromUtf8("btn_send_ccc"))
        self.horizontalLayout_3.addWidget(self.btn_send_ccc)
        self.verticalLayout_2.addWidget(self.frm_text)
        self.gridLayout.addWidget(self.gbx_ccc, 0, 1, 1, 1)
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
        self.gridLayout.addWidget(self.gbx_config, 0, 0, 1, 1)
        self.gbx_cam = QtGui.QGroupBox(widMon)
        self.gbx_cam.setObjectName(_fromUtf8("gbx_cam"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.gbx_cam)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.pte_camera = QtGui.QPlainTextEdit(self.gbx_cam)
        self.pte_camera.setMinimumSize(QtCore.QSize(350, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier"))
        font.setPointSize(10)
        self.pte_camera.setFont(font)
        self.pte_camera.setObjectName(_fromUtf8("pte_camera"))
        self.verticalLayout_4.addWidget(self.pte_camera)
        self.gridLayout.addWidget(self.gbx_cam, 1, 0, 1, 1)
        self.gbx_sns = QtGui.QGroupBox(widMon)
        self.gbx_sns.setObjectName(_fromUtf8("gbx_sns"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.gbx_sns)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.pte_sensor = QtGui.QPlainTextEdit(self.gbx_sns)
        self.pte_sensor.setMinimumSize(QtCore.QSize(400, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier"))
        font.setPointSize(10)
        self.pte_sensor.setFont(font)
        self.pte_sensor.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.pte_sensor.setObjectName(_fromUtf8("pte_sensor"))
        self.verticalLayout_6.addWidget(self.pte_sensor)
        self.gridLayout.addWidget(self.gbx_sns, 1, 1, 1, 1)

        self.retranslateUi(widMon)
        QtCore.QMetaObject.connectSlotsByName(widMon)

    def retranslateUi(self, widMon):
        widMon.setWindowTitle(_translate("widMon", "NET Monitor", None))
        self.gbx_ccc.setTitle(_translate("widMon", "Commando/Controle/Configuração", None))
        self.btn_send_ccc.setText(_translate("widMon", "Send", None))
        self.gbx_config.setTitle(_translate("widMon", "Configuração", None))
        self.gbx_cam.setTitle(_translate("widMon", "Camera", None))
        self.gbx_sns.setTitle(_translate("widMon", "Sensores", None))
        self.pte_sensor.setDocumentTitle(_translate("widMon", "Sensores", None))

