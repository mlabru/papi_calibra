#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
gbx_camera

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

# numPy
import numpy as np

# openCV
import cv2.cv as cv

# pyQT4
from PyQt4 import QtCore
from PyQt4 import QtGui

# view
import view.img_opencv as imocv
import view.wid_image_camera as wimc

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CCameraWidget >--------------------------------------------------------------------------------

class CCameraWidget(QtGui.QGroupBox):
    """
    QImage for openCV
    """
    # signals
    # C_SGN_DATA_FRAME = QtCore.pyqtSignal(cv.iplimage)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_title, f_camera_feed, f_parent=None):
        """
        constructor

        @param fs_title: groupBox title
        @param f_camera_feed: image source
        @param f_parent: parent widget
        """
        # check input
        assert f_camera_feed

        # init super class
        super(CCameraWidget, self).__init__(fs_title, f_parent)

        # camera image
        lwid_cam = wimc.CImageCameraWidget(f_camera_feed, self)
        assert lwid_cam

        # rec chart button
        lbtn_rec = QtGui.QPushButton("REC")
        assert lbtn_rec

        # connect rec chart button
        # lbtn_rec.clicked.connect(self.__rec_cam)

        # create grid layout
        llay_wid = QtGui.QVBoxLayout()
        assert llay_wid is not None

        llay_wid.addWidget(lwid_cam)
        llay_wid.addWidget(lbtn_rec)

        self.setLayout(llay_wid)

        # make connections
        # self.C_SGN_DATA_FRAME.connect(self.__on_new_frame)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(cv.iplimage)
    def __on_new_frame(self, f_frame):
        """
        callback new frame arrived
        """
        # it emits a signal with the saved frame
        # (to process the frame is not responsibility of the widget)
        # self.C_SGN_DATA_FRAME.emit(self.__frame)

# < the end >--------------------------------------------------------------------------------------
        