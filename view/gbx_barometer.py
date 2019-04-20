#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
gbx_barometer

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

revision 0.1  2017/abr  mlabru
initial release (Linux/Python)
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/04"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging

# pyQT4
from PyQt4 import QtCore
from PyQt4 import QtGui

# view
import wid_chart_model as wplt

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# barometer chart widget
M_BAR_YMAX = 1080
M_BAR_YMIN =  950

# < CBarometerWidget >-----------------------------------------------------------------------------

class CBarometerWidget(wplt.CChartModelWidget):
    """
    widget for barometer
    """
    # signals
    C_SGN_DATA_BAR = QtCore.pyqtSignal(list)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_sensor_feed, f_parent=None):
        """
        constructor

        @param f_sensor_feed: image source
        @param f_parent: parent widget
        """
        # check input
        assert f_sensor_feed

        # init super class
        super(CBarometerWidget, self).__init__(f_sensor_feed, f_parent)

        # image source
        self.__sensor_feed = f_sensor_feed
        self.__sensor_feed.C_SGN_DATA_BAR.connect(self.__on_new_data)

        # create the chart and curves
        self._create_chart(u"Pressão (hPa)", M_BAR_YMIN, M_BAR_YMAX)

        # curves checkBoxes
        self.lst_checkboxes = [self._create_checkbox("Barm 1(G)", QtCore.Qt.green,  self._activate_curve, 0),
                               self._create_checkbox("Barm 2(R)", QtCore.Qt.red,    self._activate_curve, 1),
                               self._create_checkbox("Kalman(Y)", QtCore.Qt.yellow, self._activate_curve, 2)]

        # clear chart button
        lbtn_clear = QtGui.QPushButton("clear chart")
        assert lbtn_clear

        # connect clear chart button
        lbtn_clear.clicked.connect(self._clear_chart)

        # create grid layout
        llay_wid = QtGui.QGridLayout()
        assert llay_wid is not None

        llay_wid.addWidget(self.chart, 0, 0, 8, 7)
        llay_wid.addWidget(self.lst_checkboxes[0], 0, 8)
        llay_wid.addWidget(self.lst_checkboxes[1], 1, 8)
        llay_wid.addWidget(self.lst_checkboxes[2], 2, 8)
        llay_wid.addWidget(lbtn_clear, 3, 8)

        self.setLayout(llay_wid)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(list)
    def __on_new_data(self, flst_data):
        """
        callback new data arrived
        """
        # update chart
        self._update_chart(flst_data)

        # it emits a signal with the data
        # (to process the data is not responsibility of the widget)
        self.C_SGN_DATA_BAR.emit(flst_data)

# < the end >--------------------------------------------------------------------------------------
        