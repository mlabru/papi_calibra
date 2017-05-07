#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wid_sensors

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

# openCV
import cv2.cv as cv

# PyQt
from PyQt4 import QtCore
from PyQt4 import QtGui

# view
import view.camera_feed as cf
import view.sensor_feed as sf

import view.wid_altimeter as walt
import view.wid_camera as wcam
import view.wid_gps as wgps

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CWidgetSensors >-------------------------------------------------------------------------------

class CWidgetSensors(QtGui.QWidget):
    """
    a serial port packet monitor that plots live data using PyQwt
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control, f_monitor, f_parent=None):
        """
        constructor

        @param f_control: control
        @param f_monitor: data monitor
        @param f_parent: parent widget
        """
        # check input
        assert f_control
        assert f_monitor
        
        # init super class
        super(CWidgetSensors, self).__init__(f_parent)

        # control
        self.__control = f_control
        
        # create camera feed
        self.__cf = cf.CCameraFeed(self.__control.sck_rcv_img, f_monitor)
        assert self.__cf

        # create sensor feed
        self.__sf = sf.CSensorFeed(self.__control.sck_rcv_sns, f_monitor)
        assert self.__sf

        # create camera groupBox
        self.__create_gbx_cam()

        # create plot groupBox
        self.__create_gbx_plot()

        # create altimeter groupBox
        self.__create_gbx_alt()

        # create GPS groupBox
        self.__create_gbx_gps()

        # create frame layout
        llo_grid = QtGui.QGridLayout(self)
        assert llo_grid is not None

        # put all groupBoxes on a grid
        llo_grid.addWidget(self.__gbx_cam,  1, 0, 1, 1)
        llo_grid.addWidget(self.__gbx_plot, 1, 1, 1, 1)
        llo_grid.addWidget(self.__gbx_gps,  2, 0, 1, 1)
        llo_grid.addWidget(self.__gbx_alt,  2, 1, 1, 1)
    '''
    # ---------------------------------------------------------------------------------------------
    # QEvent
    def changeEvent(self, e):

        super(CWidgetSensors, self).changeEvent(e)

        if QtCore.QEvent.LanguageChange == e.type():
            self.retranslateUi(self)

    # ---------------------------------------------------------------------------------------------
    def checkDocument(self):

        if self.__v_documentIsDirty:
            if QMessageBox.No == QMessageBox.warning(0, "", "Current configuration was changed but not saved.\nAre you sure you want to proceed ?", QMessageBox.Yes, QMessageBox.No | QMessageBox.Default):
                return False

        return True

    # ---------------------------------------------------------------------------------------------
    # QCloseEvent
    def closeEvent(self, e):

        if self.__v_portValid:
            port.requestToStop()

        if not checkDocument():
            e.ignore()
    '''
    # ---------------------------------------------------------------------------------------------
    def __create_gbx_alt(self):
        """
        create altimeter groupBox
        """
        # create altimeter widget
        lwid_altimeter = walt.CWidgetAltimeter(self.__sf, self)
        assert lwid_altimeter

        # create horizontal layout
        llay_gbx = QtGui.QHBoxLayout()
        assert llay_gbx is not None
        
        # put altimeter on layout 
        llay_gbx.addWidget(lwid_altimeter)

        # create groupBox altimeter
        self.__gbx_alt = QtGui.QGroupBox(u"Altímetro", self)
        assert self.__gbx_alt

        # setup
        self.__gbx_alt.setStyleSheet(gdefs.D_GBX_STYLE)

        # set groupBox layout 
        self.__gbx_alt.setLayout(llay_gbx)

    # ---------------------------------------------------------------------------------------------
    def __create_gbx_cam(self):
        """
        create camera groupBox
        """
        # clear to go
        assert self.__control.sck_rcv_img

        # create camera widget
        lwid_camera = wcam.CWidgetCamera(self.__cf, self)
        assert lwid_camera

        # create horizontal layout
        llay_gbx = QtGui.QHBoxLayout()
        assert llay_gbx is not None
        
        # put camera on layout 
        llay_gbx.addWidget(lwid_camera)

        # create groupBox camera
        self.__gbx_cam = QtGui.QGroupBox("Camera", self)
        assert self.__gbx_cam

        # setup
        self.__gbx_cam.setStyleSheet(gdefs.D_GBX_STYLE)

        # set groupBox layout 
        self.__gbx_cam.setLayout(llay_gbx)

    # ---------------------------------------------------------------------------------------------
    def __create_gbx_baro(self):
        """
        create barometer groupBox
        """
        # create the plot and curves
        #self.plot_bar, self.curve_bar = self.__create_plot("Barometer", gdata.ACC_YMIN, gdata.ACC_YMAX)

        #self.gCheckBox = [self.__create_checkbox("Barometer(x)", QtCore.Qt.green,  self.__activate_curve, 0),
        #                  self.__create_checkbox("Barometer(y)", QtCore.Qt.red,    self.__activate_curve, 1),
        #                  self.__create_checkbox("Barometer(z)", QtCore.Qt.yellow, self.__activate_curve, 2)
        #                 ]

        # clear screen button
        lbtn_clear = QtGui.QPushButton("clear plot")
        assert lbtn_clear

        # connect clear screen button        
        #lbtn_clear.clicked.connect(self.__clear_screen)

        # place the horizontal panel widget
        llay_gbx = QtGui.QGridLayout()
        assert llay_gbx is not None
        
        #llay_gbx.addWidget(self.plot_bar, 0, 0, 8, 7)
        #llay_gbx.addWidget(self.gCheckBox[0], 0, 8)
        #llay_gbx.addWidget(self.gCheckBox[1], 1, 8)
        #llay_gbx.addWidget(self.gCheckBox[2], 2, 8)
        llay_gbx.addWidget(lbtn_clear, 3, 8)
        # llay_gbx.addStretch()

        #self.__gbx_baro.setLayout(llay_gbx)
        #self.__gbx_baro.setFixedHeight(300)

    # ---------------------------------------------------------------------------------------------
    def __create_gbx_gps(self):
        """
        create GPS groupBox
        """
        # create GPS widget
        lwid_gps = wgps.CWidgetGPS(self.__sf, self)
        assert lwid_gps

        # create horizontal layout
        llay_gbx = QtGui.QHBoxLayout()
        assert llay_gbx is not None
        
        # put GPS on layout 
        llay_gbx.addWidget(lwid_gps)

        # create groupBox GPS
        self.__gbx_gps = QtGui.QGroupBox(u"GPS", self)
        assert self.__gbx_gps

        # setup
        self.__gbx_gps.setStyleSheet(gdefs.D_GBX_STYLE)

        # set groupBox layout 
        self.__gbx_gps.setLayout(llay_gbx)

    # ---------------------------------------------------------------------------------------------
    def __create_gbx_plot(self):
        """
        create plot groupBox
        """
        # create groupBox plot
        self.__gbx_plot = QtGui.QGroupBox("Plot", self)
        assert self.__gbx_plot

        # create the plot and curves
        #self.plot_plt, self.curve_plt = self.__create_plot("Plot", gdata.ACC_YMIN, gdata.ACC_YMAX)

        # clear screen button
        lbtn_clear = QtGui.QPushButton("clear plot")
        assert lbtn_clear

        # connect clear screen button        
        #lbtn_clear.clicked.connect(self.__clear_screen)

        # place the horizontal panel widget
        llay_gbx = QtGui.QGridLayout()
        assert llay_gbx is not None
        
        #llay_gbx.addWidget(self.plot_plt, 0, 0, 8, 7)
        #llay_gbx.addWidget(self.gCheckBox[0], 0, 8)
        #llay_gbx.addWidget(self.gCheckBox[1], 1, 8)
        #llay_gbx.addWidget(self.gCheckBox[2], 2, 8)
        llay_gbx.addWidget(lbtn_clear, 3, 8)
        # llay_gbx.addStretch()

        self.__gbx_plot.setLayout(llay_gbx)
        #self.__gbx_plot.setFixedHeight(250)
    '''
    # ---------------------------------------------------------------------------------------------
    # const QString&
    def __load_document(self, filePath):

        success = True
        file = QFile(filePath)

        if file.open(QIODevice.ReadOnly):

            textStream = QTextStream(file)
            self.configurationText.setPlainText(textStream.readAll())
            updateDocumentFilePath(filePath)
            success = True


        if not success:
            QMessageBox.critical(0, "", "Could not load file: " + filePath)

        return success

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

    # ---------------------------------------------------------------------------------------------
    # const QString&
    def saveDocument(self, filePath):

        success = False
        file = QFile(filePath)

        if file.open(QIODevice.WriteOnly):

            textStream = QTextStream(file)
            textStream << self.configurationText.toPlainText()
            textStream.flush()

            self.__v_documentIsDirty  = False

            updateDocumentFilePath(filePath)

            success = True

        if not success:
            QMessageBox.critical(0, "", "Could not save file: " + filePath)

        else:
            self.statusBar.showMessage("File Saved", 2000)

        return success

    # ---------------------------------------------------------------------------------------------
    # const QString&
    def updateDocumentFilePath(self, filePath):

        documentFilePath = filePath

        settings.setValue("Last Configuration", filePath)

        self.setWindowTitle("TTY Monitor - " + QFileInfo(filePath).fileName())

        self.__v_documentIsDirty  = False

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

        if checkDocument():

            self.configurationText.clear()
            documentFilePath = ""
            self.statusBar.showMessage(documentFilePath)
            self.__v_documentIsDirty  = False

    # ---------------------------------------------------------------------------------------------
    def on_actionOpen_triggered(self):

        if not checkDocument():
            return

        filePath = QFileDialog.getOpenFileName(self, tr("Open File"), 
                       documentFilePath, tr("TTY Monitor Configuration (*.scc)All Files (*.*)"))

        if not filePath.isEmpty():
            self.__load_document(filePath)

    # ---------------------------------------------------------------------------------------------
    def on_actionRun_triggered(self):

        self.__config.parse( self.configurationText.toPlainText())
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
            saveDocument(documentFilePath)

    # ---------------------------------------------------------------------------------------------
    def on_actionSaveAs_triggered(self):

        filePath = QFileDialog.getSaveFileName(self, tr("Save File"),
                       documentFilePath, tr("TTY Monitor Configuration (*.scc)All Files (*.*)"))

        if not filePath.isEmpty():
            self.saveDocument(filePath)

    # ---------------------------------------------------------------------------------------------
    def on_actionStop_triggered(self):

        self.actionStop.setEnabled(False)
        self.sendButton.setEnabled(False)

        port.requestToStop()

    # ---------------------------------------------------------------------------------------------
    def on_actionToolbar_toggled(self, b):

        self.mainToolBar.setVisible(b)

    # ---------------------------------------------------------------------------------------------
    def on_configurationText_textChanged(self):

        self.__v_documentIsDirty = True

    # ---------------------------------------------------------------------------------------------
    def on_sendButton_clicked(self):

        if self.__v_portValid:
            port.send(self.sendText.text())
    '''
# < the end >--------------------------------------------------------------------------------------
        