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
import model.pc_barometer_feed as barfd
import model.pc_gps_feed as gpsfd
import model.pc_thermometer_feed as thrfd

# view
import view.wid_altimeter as walt
import view.wid_barometer as wbar
import view.wid_gps as wgps
import view.wid_thermometer as wthr

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
        
        # parent
        self.__parent = f_parent
        
        # create altimeter groupBox
        self.__create_gbx_alt()

        # create GPS groupBox
        self.__create_gbx_gps()

        # create barameter groupBox
        self.__create_gbx_bar()

        # create thermometer groupBox
        self.__create_gbx_thr()

        # create frame layout
        llo_grid = QtGui.QGridLayout(self)
        assert llo_grid is not None

        # put all groupBoxes on a grid
        llo_grid.addWidget(self.__gbx_alt, 0, 0, 1, 1)
        llo_grid.addWidget(self.__gbx_gps, 0, 1, 1, 1)
        llo_grid.addWidget(self.__gbx_bar, 1, 0, 1, 1)
        llo_grid.addWidget(self.__gbx_thr, 1, 1, 1, 1)

    # ---------------------------------------------------------------------------------------------
    def __create_gbx_alt(self):
        """
        create altimeter groupBox
        """
        # create altimeter feed
        self.__alt_feed = altfd.CAltimeterFeed(self.__control, self.__monitor)
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
    def __create_gbx_bar(self):
        """
        create barometer groupBox
        """
        # create barometer feed
        self.__bar_feed = barfd.CBarometerFeed(self.__control, self.__monitor)
        assert self.__bar_feed

        # create barometer widget
        lwid_barometer = wbar.CWidgetBarometer(self.__bar_feed, self)
        assert lwid_barometer

        # setup
        lwid_barometer.setFixedHeight(280)

        # create horizontal layout
        llay_gbx = QtGui.QHBoxLayout()
        assert llay_gbx is not None
        
        # put barometer on layout 
        llay_gbx.addWidget(lwid_barometer)

        # create groupBox barometer
        self.__gbx_bar = QtGui.QGroupBox(u"Barômetro", self)
        assert self.__gbx_bar

        # setup
        self.__gbx_bar.setStyleSheet(gdefs.D_GBX_STYLE)

        # set groupBox layout 
        self.__gbx_bar.setLayout(llay_gbx)

    # ---------------------------------------------------------------------------------------------
    def __create_gbx_gps(self):
        """
        create GPS groupBox
        """
        # create GPS feed
        self.__gps_feed = gpsfd.CGPSFeed(self.__control, self.__monitor)
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
    def __create_gbx_thr(self):
        """
        create thermometer groupBox
        """
        # create thermometer feed
        self.__thr_feed = thrfd.CThermometerFeed(self.__control, self.__monitor)
        assert self.__thr_feed

        # create thermometer widget
        lwid_thermometer = wthr.CWidgetThermometer(self.__thr_feed, self)
        assert lwid_thermometer

        # setup
        lwid_thermometer.setFixedHeight(280)

        # create horizontal layout
        llay_gbx = QtGui.QHBoxLayout()
        assert llay_gbx is not None
        
        # put thermometer on layout 
        llay_gbx.addWidget(lwid_thermometer)

        # create groupBox thermometer
        self.__gbx_thr = QtGui.QGroupBox(u"Termômetro", self)
        assert self.__gbx_thr

        # setup
        self.__gbx_thr.setStyleSheet(gdefs.D_GBX_STYLE)

        # set groupBox layout 
        self.__gbx_thr.setLayout(llay_gbx)

# < the end >--------------------------------------------------------------------------------------
        