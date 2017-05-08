#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wid_papi_plot

papi calibrate

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
import sys

# PyQt4
from PyQt4 import QtCore
from PyQt4 import QtGui

# numPy
import numpy as np

# matplotlib
import matplotlib.pyplot as plt
import matplotlib.backends.backend_qt4agg as qt4agg

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CWidgetPAPIPlot >------------------------------------------------------------------------------

class CWidgetPAPIPlot(QtGui.QWidget):
    """
    QImage for openCV
    """
    # signals
    x = np.arange(0, 10, 0.1)
    cos = 0
    sin = 0

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_camera_feed, f_parent=None):
        """
        constructor

        @param f_camera_feed: image source
        @param f_parent: parent widget
        """
        # check input
        # assert f_camera_feed

        # init super class
        super(CWidgetPAPIPlot, self).__init__(f_parent)

        # figure
        l_figure = plt.figure()
        assert l_figure

        # drawing
        self.__drawing = l_figure.add_subplot(111)
        assert self.__drawing

        # canvas
        self.__canvas = qt4agg.FigureCanvasQTAgg(l_figure)
        assert self.__canvas

        # setup
        self.__canvas.setFixedHeight(230)
        self.__canvas.setFixedWidth(500)

        # clear screen button
        # lbtn_clear = QtGui.QPushButton("clear plot")
        # assert lbtn_clear

        # connect clear screen button        
        # lbtn_clear.clicked.connect(lwid_ppt.clear_screen)

        # create slider for cos
        l_sld_cos = self.__create_slider(self.__set_cos, self.__plot)

        # create slider for sin
        l_sld_sin = self.__create_slider(self.__set_sin, self.__plot)

        # create layout for sliders 
        llay_sld = QtGui.QGridLayout()
        assert llay_sld is not None

        # put sliders on layout
        llay_sld.addWidget(l_sld_cos, 0, 0)
        llay_sld.addWidget(l_sld_sin, 0, 1)

        # create groupBox for sliders
        lgbx_sld = QtGui.QGroupBox("Values")
        assert lgbx_sld
        
        # put sliders widgets on groupBox
        lgbx_sld.setLayout(llay_sld)

        # setup
        lgbx_sld.setFixedWidth(70)

        # create layout
        llay_plt = QtGui.QHBoxLayout(self)
        assert llay_plt is not None

        # setup
        llay_plt.addWidget(self.__canvas)
        llay_plt.addWidget(lgbx_sld)

        # do plot 
        self.__plot()

    # ---------------------------------------------------------------------------------------------
    def __create_slider(self, f_func, f_plot, f_parent=None):
        """
        create slider
        """
        # create slider
        l_sld = QtGui.QSlider(QtCore.Qt.Vertical, f_parent)
        assert l_sld

        # setup
        l_sld.setFocusPolicy(QtCore.Qt.NoFocus)
        l_sld.valueChanged[int].connect(f_func)
        l_sld.valueChanged.connect(f_plot)

        # return
        return l_sld
        
    # ---------------------------------------------------------------------------------------------
    def __plot(self):
        """
        do plot
        """
        s = np.sin(self.x + self.sin)
        c = np.cos(self.x + self.cos)

        self.__drawing.plot(self.x, s, 'r', self.x, c, 'r', self.x, s +c, 'b')
        self.__drawing.set_ylim(-2, 2)

        self.__canvas.draw()

    # ---------------------------------------------------------------------------------------------
    def __set_cos(self, v):
        self.cos = v / float(100)

    # ---------------------------------------------------------------------------------------------
    def __set_sin(self, v):
        self.sin = v / float(100)

# < the end >--------------------------------------------------------------------------------------