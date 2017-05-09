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
import math
import sys

# PyQt4
from PyQt4 import QtCore
from PyQt4 import QtGui

# numPy
import numpy as np

# matplotlib
import matplotlib.pyplot as plt
import matplotlib.text as mtext
import matplotlib.lines as lines
import matplotlib.transforms as mtransforms
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

        # distância em metros
        self.__f_dst = 300.
        
        # altitude em metros
        self.__f_alt = 20.

        # setup user interface
        self.__setup_ui(self)

        lf_alt = 8.5 

        l_x = [0., self.__f_dst]  
        l_y = [0., lf_alt] 
        llbl_gr = u"{:4.3f}°".format(math.degrees(math.atan2(lf_alt, self.__f_dst)))

        line = CPlotLine(l_x, l_y, mfc='red', ms=12, label=llbl_gr)
        #line.text.set_text('line label')
        line.text.set_color('red')
        line.text.set_fontsize(8)

        self.__drawing.add_line(line)


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
        # escalas dos eixos
        self.__drawing.set_xlim(0, self.__f_dst)
        self.__drawing.set_ylim(0, self.__f_alt)

        # label dos eixos
        self.__drawing.set_ylabel(u"Altitude")
        self.__drawing.set_xlabel(u"Distância")

        # desenha o canvas
        self.__canvas.draw()

    # ---------------------------------------------------------------------------------------------
    def __set_cos(self, v):
        self.cos = v / 100.

    # ---------------------------------------------------------------------------------------------
    def __set_sin(self, v):
        self.sin = v / 100.

    # ---------------------------------------------------------------------------------------------
    def __setup_ui(self, f_parent=None):
        """
        setup user interface
        """
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
        self.__canvas.setFixedHeight(270)
        self.__canvas.setFixedWidth(480)

        ###
        # sliders

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

        ###
        # frame

        # create font
        l_font = QtGui.QFont()
        assert l_font

        # setup
        l_font.setBold(True)
        l_font.setWeight(75)

        # label distância
        llbl_dst = QtGui.QLabel(u"Distância")
        assert llbl_dst
        
        # setup
        llbl_dst.setFont(l_font)

        # spinBox distância
        self.__dsb_dst = QtGui.QDoubleSpinBox()
        assert self.__dsb_dst

        # label pto zero 
        llbl_zero = QtGui.QLabel(u"Pto.Zero")
        assert llbl_zero

        # setup
        llbl_zero.setFont(l_font)

        # labels lat/lng/alt
        self.__lbl_lat = QtGui.QLabel("X:")
        assert self.__lbl_lat

        self.__lbl_lng = QtGui.QLabel("Y:")
        assert self.__lbl_lng

        self.__lbl_alt = QtGui.QLabel("Z:")
        assert self.__lbl_alt

        # clear screen button
        self.__btn_clear = QtGui.QPushButton("clear plot")
        assert self.__btn_clear

        # connect clear screen button        
        # self.__btn_clear.clicked.connect(lwid_ppt.clear_screen)

        # frame
        l_frm = QtGui.QFrame()
        assert l_frm
        
        # setup
        l_frm.setGeometry(QtCore.QRect(60, 120, 91, 171))
        l_frm.setFrameShape(QtGui.QFrame.StyledPanel)
        l_frm.setFrameShadow(QtGui.QFrame.Raised)

        # frame layout
        llay_frm = QtGui.QVBoxLayout(l_frm)
        assert llay_frm is not None

        llay_frm.addWidget(llbl_dst)
        llay_frm.addWidget(self.__dsb_dst)
        llay_frm.addWidget(llbl_zero)
        llay_frm.addWidget(self.__lbl_lat)
        llay_frm.addWidget(self.__lbl_lng)
        llay_frm.addWidget(self.__lbl_alt)
        llay_frm.addWidget(self.__btn_clear)

        # create plot layout
        llay_plt = QtGui.QHBoxLayout(f_parent)
        assert llay_plt is not None

        # setup
        llay_plt.addWidget(self.__canvas)
        llay_plt.addWidget(l_frm)

# < CPlotLine >------------------------------------------------------------------------------------

class CPlotLine(lines.Line2D):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        # we'll update the position when the line data is set
        self.text = mtext.Text(0, 0, '')
        lines.Line2D.__init__(self, *args, **kwargs)

        # we can't access the label attr until *after* the line is
        # inited
        self.text.set_text(self.get_label())

    # ---------------------------------------------------------------------------------------------
    def draw(self, renderer):
        # draw my label at the end of the line with 2 pixel offset
        lines.Line2D.draw(self, renderer)
        self.text.draw(renderer)

    # ---------------------------------------------------------------------------------------------
    def set_axes(self, axes):
        self.text.set_axes(axes)
        lines.Line2D.set_axes(self, axes)

    # ---------------------------------------------------------------------------------------------
    def set_data(self, x, y):
        if len(x):
            self.text.set_position((x[-1], y[-1]))

        lines.Line2D.set_data(self, x, y)

    # ---------------------------------------------------------------------------------------------
    def set_figure(self, figure):
        self.text.set_figure(figure)
        lines.Line2D.set_figure(self, figure)

    # ---------------------------------------------------------------------------------------------
    def set_transform(self, transform):
        # 2 pixel offset
        texttrans = transform + mtransforms.Affine2D().translate(2, 2)
        self.text.set_transform(texttrans)
        lines.Line2D.set_transform(self, transform)

# < the end >--------------------------------------------------------------------------------------
