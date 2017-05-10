#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wid_net_monitor

a serial port packet monitor that plots live data using PyQwt

revision 0.1  2017/abr  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/04"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging

# PyQt
from PyQt4 import QtCore
from PyQt4 import QtGui

# model
import model.pc_syntax as sntx

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CWidgetNetMonitor >----------------------------------------------------------------------------

class CWidgetNetMonitor(QtGui.QWidget):
    """
    network packet monitor that plots live data using PyQwt
    """
    # signals
    C_SIG_MSG_CAM = QtCore.pyqtSignal(str)
    C_SIG_MSG_CCC = QtCore.pyqtSignal(str)
    C_SIG_MSG_SNS = QtCore.pyqtSignal(str)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_settings, f_parent=None):
        """
        constructor
        """
        # init super class
        super(CWidgetNetMonitor, self).__init__(f_parent)

        # flag dirty
        self.__v_document_is_dirty = False

        # flag port ok
        self.__v_portValid = False

        # config
        self.__config = None  # Configuration(self)
        # assert self.__config 

        # save settings
        self.__settings = f_settings
        
        # create camera groupBox
        self.__create_gbx_cam()

        # create CCC groupBox
        self.__create_gbx_ccc()

        # create sensors groupBox
        self.__create_gbx_sns()

        # create configuration groupBox
        self.__create_gbx_config()

        # create frame layout
        llo_grid = QtGui.QGridLayout(self)
        assert llo_grid is not None

        # put all groupBoxes on a grid
        llo_grid.addWidget(self.__gbx_cnf, 0, 0, 1, 1)
        llo_grid.addWidget(self.__gbx_cam, 0, 1, 1, 1)
        llo_grid.addWidget(self.__gbx_ccc, 1, 0, 1, 1)
        llo_grid.addWidget(self.__gbx_sns, 1, 1, 1, 1)

        # make connections
        self.C_SIG_MSG_CAM.connect(self.__on_msg_camera)
        self.C_SIG_MSG_CCC.connect(self.__on_msg_ccc)
        self.C_SIG_MSG_SNS.connect(self.__on_msg_sensor)

        # load configuration file
        self.__load_document()
    '''
    # ---------------------------------------------------------------------------------------------
    # QEvent
    def changeEvent(self, e):

        super(CWidgetNetMonitor, self).changeEvent(e)

        if QtCore.QEvent.LanguageChange == e.type():
            self.retranslateUi(self)
    '''
    # ---------------------------------------------------------------------------------------------
    def __check_document(self):
        """
        check document
        """
        # dirty ?
        if self.__v_document_is_dirty:
            # save ?
            if QtGui.QMessageBox.No == QtGui.QMessageBox.warning(0, "", 
                "Current configuration was changed but not saved.\nAre you sure you want to proceed ?", 
                QtGui.QMessageBox.Yes, QtGui.QMessageBox.No | QtGui.QMessageBox.Default):
                # return
                return False

        # return 
        return True

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(QtGui.QCloseEvent)
    def closeEvent(self, f_evt):
        """
        close event callback
        """
        # don't save document ?
        if not __check_document():
            # ignore
            f_evt.ignore()

    # ---------------------------------------------------------------------------------------------
    def __create_gbx_cam(self):
        """
        create camera groupBox
        """
        # create font
        l_font = QtGui.QFont()
        assert l_font

        l_font.setFamily("Courier")
        l_font.setPointSize(10)

        # create QPlainTextEdit camera
        self.__pte_camera = QtGui.QPlainTextEdit()
        assert self.__pte_camera 

        # setup
        self.__pte_camera.setFont(l_font)
        self.__pte_camera.setStyleSheet(gdefs.D_PTE_STYLE)
        self.__pte_camera.setMinimumSize(QtCore.QSize(500, 270))
        self.__pte_camera.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)

        # create horizontal layout
        llay_gbx = QtGui.QHBoxLayout()
        assert llay_gbx is not None

        # put camera on layout
        llay_gbx.addWidget(self.__pte_camera)

        # create groupBox camera
        self.__gbx_cam = QtGui.QGroupBox(u"Camera", self)
        assert self.__gbx_cam
        
        # setup
        self.__gbx_cam.setStyleSheet(gdefs.D_GBX_STYLE)

        # set groupBox layout
        self.__gbx_cam.setLayout(llay_gbx)

    # ---------------------------------------------------------------------------------------------
    def __create_gbx_ccc(self):
        """
        create CCC groupBox
        """
        # create altimeter widget
        # create font
        l_font = QtGui.QFont()
        assert l_font

        l_font.setFamily("Courier")
        l_font.setPointSize(10)

        # create QPlainTextEdit CCC
        self.__pte_ccc = QtGui.QPlainTextEdit()
        assert self.__pte_ccc
        
        self.__pte_ccc.setFont(l_font)
        self.__pte_ccc.setStyleSheet(gdefs.D_PTE_STYLE)
        self.__pte_ccc.setMinimumSize(QtCore.QSize(660, 270))

        # frame to qle and btn
        lfrm_text = QtGui.QFrame()
        assert lfrm_text

        lfrm_text.setAutoFillBackground(True)
        lfrm_text.setFrameShape(QtGui.QFrame.Panel)
        lfrm_text.setFrameShadow(QtGui.QFrame.Raised)

        # lineEdit command
        self.qle_ccc = QtGui.QLineEdit(lfrm_text)
        assert self.qle_ccc

        self.qle_ccc.setEnabled(True)
        self.qle_ccc.setText("")

        # bottom send command 
        self.btn_send_ccc = QtGui.QPushButton("Send", lfrm_text)
        assert self.btn_send_ccc
         
        self.btn_send_ccc.setEnabled(False)

        # layout to frame
        llay_frm = QtGui.QHBoxLayout(lfrm_text)
        assert llay_frm is not None
        
        llay_frm.setMargin(0)
        llay_frm.setSpacing(0)
        llay_frm.addWidget(self.qle_ccc)
        llay_frm.addWidget(self.btn_send_ccc)

        # create horizontal layout
        llay_gbx = QtGui.QVBoxLayout()
        assert llay_gbx is not None

        # put CCC on layout
        llay_gbx.addWidget(self.__pte_ccc)
        llay_gbx.addWidget(lfrm_text)

        # create groupBox altimeter
        self.__gbx_ccc = QtGui.QGroupBox(u"Comando/Controle/Configuração", self)
        assert self.__gbx_ccc
        
        # setup
        self.__gbx_ccc.setStyleSheet(gdefs.D_GBX_STYLE)

        # set groupBox layout
        self.__gbx_ccc.setLayout(llay_gbx)

    # ---------------------------------------------------------------------------------------------
    def __create_gbx_sns(self):
        """
        create sensors groupBox
        """
        # create font
        l_font = QtGui.QFont()
        assert l_font

        l_font.setFamily("Courier")
        l_font.setPointSize(10)

        # create QPlainTextEdit sensor
        self.__pte_sensor = QtGui.QPlainTextEdit()
        assert self.__pte_sensor
        
        self.__pte_sensor.setFont(l_font)
        self.__pte_sensor.setStyleSheet(gdefs.D_PTE_STYLE)
        self.__pte_sensor.setMinimumSize(QtCore.QSize(500, 270))
        self.__pte_sensor.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)

        # create horizontal layout
        llay_gbx = QtGui.QHBoxLayout()
        assert llay_gbx is not None

        # put altimeter on layout
        llay_gbx.addWidget(self.__pte_sensor)

        # create groupBox altimeter
        self.__gbx_sns = QtGui.QGroupBox(u"Sensores", self)
        assert self.__gbx_sns
        
        # setup
        self.__gbx_sns.setStyleSheet(gdefs.D_GBX_STYLE)

        # set groupBox layout
        self.__gbx_sns.setLayout(llay_gbx)

    # ---------------------------------------------------------------------------------------------
    def __create_gbx_config(self):
        """
        create configuration groupBox
        """
        # create font
        l_font = QtGui.QFont()
        assert l_font

        l_font.setFamily("Courier")
        l_font.setPointSize(10)

        # create QPlainTextEdit configuração
        self.__pte_editor = QtGui.QPlainTextEdit()
        assert self.__pte_editor

        self.__pte_editor.setFont(l_font)
        self.__pte_editor.setReadOnly(False)
        self.__pte_editor.setStyleSheet(gdefs.D_PTE_STYLE)
        self.__pte_editor.setMinimumSize(QtCore.QSize(660, 270))

        # syntax highlight
        self.highlight = sntx.CConfigHighlighter(self.__pte_editor.document())
        assert self.highlight 

        self.__pte_editor.show()

        # connections
        self.__pte_editor.textChanged.connect(self.on_pte_editor_textChanged)

        # create horizontal layout
        llay_gbx = QtGui.QHBoxLayout()
        assert llay_gbx is not None

        # put altimeter on layout
        llay_gbx.addWidget(self.__pte_editor)

        # create groupBox configuração
        self.__gbx_cnf = QtGui.QGroupBox(u"Configuração", self)
        assert self.__gbx_cnf
        
        # setup
        self.__gbx_cnf.setStyleSheet(gdefs.D_GBX_STYLE)

        # set groupBox layout
        self.__gbx_cnf.setLayout(llay_gbx)

    # ---------------------------------------------------------------------------------------------
    def __load_document(self):
        """
        load configuration file
        """
        # get last configuration file in use
        l_config = str(self.__settings.value("lastConfig").toString())

        if l_config:
            fs_file_path = l_config

        # senão,...
        else:
            fs_file_path = "papical.cfg" 

        # flag ok
        lv_ok = True

        # create file object
        file = QtCore.QFile(fs_file_path)
        assert file

        # open file ok ?
        if file.open(QtCore.QIODevice.ReadOnly):
            # load text stream
            textStream = QtCore.QTextStream(file)

            # put text on widget
            self.__pte_editor.setPlainText(textStream.readAll())

            # update settings
            self.__updateDocumentFilePath(fs_file_path)

            # ok
            lv_ok = True

        # error in loading file ?
        if not lv_ok:
            # show message box
            QtGui.QMessageBox.critical(0, "", "Could not load file: {}".format(fs_file_path))

        # return
        return lv_ok
    '''
    # ---------------------------------------------------------------------------------------------
    # const QString&, const QString&
    def message(self, text, type):

        if "critical" == type:
            QMessageBox.critical(0, "", text)

        else:
            QMessageBox.information(0, "", text)

    # ---------------------------------------------------------------------------------------------
    def portStopped(self):

        self.actionStop.setEnabled(False)
        self.sendButton.setEnabled(False)
        self.actionRun.setEnabled(True)

        port.deleteLater()

        self.__v_portValid = False
    '''
    ''' 
    # ---------------------------------------------------------------------------------------------
    # const QString&
    def __save_document(self, filePath):

        lv_ok = False
        file = QFile(filePath)

        if file.open(QIODevice.WriteOnly):

            textStream = QTextStream(file)
            textStream << self.__pte_editor.toPlainText()
            textStream.flush()

            self.__v_document_is_dirty  = False

            updateDocumentFilePath(filePath)

            lv_ok = True

        if not lv_ok:
            QMessageBox.critical(0, "", "Could not save file: " + filePath)

        else:
            self.statusBar.showMessage("File Saved", 2000)

        return lv_ok
    ''' 
    # ---------------------------------------------------------------------------------------------
    # const QString&
    def __updateDocumentFilePath(self, filePath):
        """
        update settings
        """
        # actual config
        documentFilePath = filePath

        # save on settings
        self.__settings.setValue("lastConfig", filePath)

        # set title
        self.__gbx_cnf.setTitle("Config File: " + QtCore.QFileInfo(filePath).fileName())

        # flag dirty
        self.__v_document_is_dirty  = False
    '''
    # =============================================================================================
    # callbacks
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    def on_actionAbout_triggered(self):

        QMessageBox.about(0, "XXX", "YYY")

    # ---------------------------------------------------------------------------------------------
    def on_actionChart_toggled(self, b):

        self.dockWidgetChart.setVisible(b)

    # ---------------------------------------------------------------------------------------------
    def on_actionConfiguration_toggled(self, b):

        self.dockWidgetConfiguration.setVisible(b)

    # ---------------------------------------------------------------------------------------------
    def on_actionExit_triggered(self):

        self.close()

    # ---------------------------------------------------------------------------------------------
    def on_actionNew_triggered(self):

        if __check_document():

            self.__pte_editor.clear()
            documentFilePath = ""
            self.statusBar.showMessage(documentFilePath)
            self.__v_document_is_dirty  = False

    # ---------------------------------------------------------------------------------------------
    def on_actionOpen_triggered(self):

        if not __check_document():
            return

        filePath = QFileDialog.getOpenFileName(self, tr("Open File"), 
                       documentFilePath, tr("TTY Monitor Configuration (*.scc)All Files (*.*)"))

        if not filePath.isEmpty():
            self.__load_document(filePath)

    # ---------------------------------------------------------------------------------------------
    def on_actionRun_triggered(self):

        self.__config.parse( self.__pte_editor.toPlainText())
        self.dataText.setMaximumBlockCount(MAX(1, self.__config.get("_setup_", "width").toInt()))

        self.chart.init(self.__config)
        self.actionRun.setEnabled(False)
        self.actionStop.setEnabled(True)
        self.sendButton.setEnabled(True)
        self.dataText.clear()

        port = createPort(self.__config)

        decoder = createDecoder(self, self.__config)
        display = createDisplay(self, self.__config)

        self.__v_portValid = True

        # port signals
        #connect(port,SIGNAL(newData(const QByteArray&)),decoder,SLOT(newData(const QByteArray&)))
        #connect(port,SIGNAL(packetSeparator()),decoder,SLOT(packetSeparator()))
        #connect(port,SIGNAL(stopped()),self,SLOT(portStopped()))
        #connect(port,SIGNAL(message(const QString&,const QString&)),self,SLOT(message(const QString&,const QString&)))

        # decoder signals
        #connect(decoder,SIGNAL(newPacket(DecoderBase*)),self.chart,SLOT(newPacket(DecoderBase*)))
        #connect(decoder,SIGNAL(newPacket(DecoderBase*)),display,SLOT(newPacket(DecoderBase*)))

        # display signals
        #connect(display,SIGNAL(newDisplay(const QString&)),self.dataText,SLOT(appendPlainText(const QString&)))

        port.start()

    # ---------------------------------------------------------------------------------------------
    def on_actionSave_triggered(self):

        if documentFilePath.isEmpty():
            on_actionSaveAs_triggered()

        else:
            self.__save_document(documentFilePath)

    # ---------------------------------------------------------------------------------------------
    def on_actionSaveAs_triggered(self):

        filePath = QFileDialog.getSaveFileName(self, tr("Save File"),
                       documentFilePath, tr("TTY Monitor Configuration (*.scc)All Files (*.*)"))

        if not filePath.isEmpty():
            self.__save_document(filePath)

    # ---------------------------------------------------------------------------------------------
    def on_actionStop_triggered(self):

        self.actionStop.setEnabled(False)
        self.sendButton.setEnabled(False)

        port.requestToStop()

    # ---------------------------------------------------------------------------------------------
    def on_actionToolbar_toggled(self, b):

        self.mainToolBar.setVisible(b)
    '''
    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def on_pte_editor_textChanged(self):
        """
        change in config file
        """
        # set dirty flag
        self.__v_document_is_dirty = True

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(str)
    def __on_msg_camera(self, fs_msg):
        """
        message from camera
        """    
        # put text on textEditor
        self.__pte_camera.appendPlainText(fs_msg)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(str)
    def __on_msg_ccc(self, fs_msg):
        """
        message of command/control/config
        """    
        # put text on textEditor
        self.__pte_ccc.appendPlainText(fs_msg)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(str)
    def __on_msg_sensor(self, fs_msg):
        """
        message from sensors
        """    
        # put text on textEditor
        self.__pte_sensor.appendPlainText(fs_msg)
    '''
    # ---------------------------------------------------------------------------------------------
    def on_sendButton_clicked(self):

        if self.__v_portValid:
            port.send(self.sendText.text())
    '''
# < the end >--------------------------------------------------------------------------------------
        
        
        
