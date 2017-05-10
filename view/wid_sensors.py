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

# PyQt4
from PyQt4 import QtCore
from PyQt4 import QtGui

# model
import model.pc_altimeter_feed as altfd
import model.pc_camera_feed as camfd
import model.pc_gps_feed as gpsfd

# view
import view.wid_altimeter as walt
import view.wid_camera as wcam
import view.wid_gps as wgps
import view.wid_plot_papi as wplp

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CWidgetSensors >-------------------------------------------------------------------------------

class CWidgetSensors(QtGui.QWidget):
    """
    a port packet monitor that plots live data using PyQwt
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

        # monitor
        self.__monitor = f_monitor
        
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
        llo_grid.addWidget(self.__gbx_cam,  0, 0, 1, 1)
        llo_grid.addWidget(self.__gbx_plot, 0, 1, 1, 1)
        llo_grid.addWidget(self.__gbx_gps,  1, 0, 1, 1)
        llo_grid.addWidget(self.__gbx_alt,  1, 1, 1, 1)

    # ---------------------------------------------------------------------------------------------
    def __create_gbx_alt(self):
        """
        create altimeter groupBox
        """
        # create altimeter feed
        self.__alt_feed = altfd.CAltimeterFeed(self.__control.sck_rcv_sns, self.__monitor)
        assert self.__alt_feed

        # create altimeter widget
        lwid_altimeter = walt.CWidgetAltimeter(self.__alt_feed, self)
        assert lwid_altimeter

        # setup
        lwid_altimeter.setFixedHeight(280)

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

        # create camera feed
        self.__cam_feed = camfd.CCameraFeed(self.__control.sck_rcv_img)
        assert self.__cam_feed

        # create camera widget
        lwid_camera = wcam.CWidgetCamera(self.__cam_feed, self)
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
    def __create_gbx_gps(self):
        """
        create GPS groupBox
        """
        # create GPS feed
        self.__gps_feed = gpsfd.CGPSFeed(self.__control.sck_rcv_sns)
        assert self.__gps_feed

        # create GPS widget
        lwid_gps = wgps.CWidgetGPS(self.__gps_feed, self)
        assert lwid_gps

        # setup
        lwid_gps.setFixedHeight(280)

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
        # create the plot and curves
        lwid_plp = wplp.CWidgetPlotPAPI(self) 
        assert lwid_plp 

        # place the horizontal panel widget
        llay_gbx = QtGui.QHBoxLayout()
        assert llay_gbx is not None
        
        # put plot on layout
        llay_gbx.addWidget(lwid_plp)

        # create groupBox plot
        self.__gbx_plot = QtGui.QGroupBox("Plot", self)
        assert self.__gbx_plot

        # setup
        self.__gbx_plot.setStyleSheet(gdefs.D_GBX_STYLE)

        # set groupBox layout 
        self.__gbx_plot.setLayout(llay_gbx)

# < the end >--------------------------------------------------------------------------------------
        