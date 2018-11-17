#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wid_thermometer

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

# pyQT4
from PyQt4 import QtCore
from PyQt4 import QtGui

# view
import wid_plot_model as wplt

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# thermometer plot widget
M_THR_YMAX = 50
M_THR_YMIN = 10

# < CWidgetThermometer >---------------------------------------------------------------------------

class CWidgetThermometer(wplt.CWidgetPlotModel):
    """
    widget for thermometer
    """
    # signals
    C_SGN_DATA_THR = QtCore.pyqtSignal(list)

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
        super(CWidgetThermometer, self).__init__(f_sensor_feed, f_parent)

        # image source
        self.__sensor_feed = f_sensor_feed
        self.__sensor_feed.C_SGN_DATA_THR.connect(self.on_new_data)

        # create the plot and curves
        self._create_plot(u"Temperatura (°C)", M_THR_YMIN, M_THR_YMAX)

        # curves checkBoxes
        self.lst_checkboxes = [self._create_checkbox("Thrm 1(G)", QtCore.Qt.green,  self._activate_curve, 0),
                               self._create_checkbox("Thrm 2(R)", QtCore.Qt.red,    self._activate_curve, 1),
                               self._create_checkbox("Fusion(Y)", QtCore.Qt.yellow, self._activate_curve, 2)]

        # clear plot button
        lbtn_clear = QtGui.QPushButton("clear plot")
        assert lbtn_clear

        # connect clear plot button
        lbtn_clear.clicked.connect(self._clear_plot)

        # create grid layout
        llay_wid = QtGui.QGridLayout()
        assert llay_wid is not None

        llay_wid.addWidget(self.plot, 0, 0, 8, 7)
        llay_wid.addWidget(self.lst_checkboxes[0], 0, 8)
        llay_wid.addWidget(self.lst_checkboxes[1], 1, 8)
        llay_wid.addWidget(self.lst_checkboxes[2], 2, 8)
        llay_wid.addWidget(lbtn_clear, 3, 8)

        self.setLayout(llay_wid)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(list)
    def on_new_data(self, flst_data):
        """
        callback new data arrived
        """
        # update plot
        self._update_plot(flst_data)

        # it emits a signal with the data
        # (to process the data is not responsibility of the widget)
        self.C_SGN_DATA_THR.emit(flst_data)

# < the end >--------------------------------------------------------------------------------------
        