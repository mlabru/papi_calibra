#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
CameraWidget

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
import cv

# pyQT4
from PyQt4 import QtCore
from PyQt4 import QtGui

# papi_calibrate
import OpenCVQImage as ocvimg

# < CameraWidget >---------------------------------------------------------------------------------

class CameraWidget(QtGui.QWidget):
    """
    QImage for openCV
    """
    newFrame = QtCore.pyqtSignal(cv.iplimage)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, cameraDevice, parent=None):

        super(CameraWidget, self).__init__(parent)

        self._frame = None

        self._cameraDevice = cameraDevice
        self._cameraDevice.newFrame.connect(self._onNewFrame)

        w, h = self._cameraDevice.frameSize

        self.setMinimumSize(w, h)
        self.setMaximumSize(w, h)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(cv.iplimage)
    def _onNewFrame(self, frame):

        # saves its own version of the frame
        self._frame = cv.CloneImage(frame)

        # it emits a signal with the saved frame (to process the frame is not responsibility of the widget)
        self.newFrame.emit(self._frame)

        # forces a schedule of a paint event
        self.update()

    # ---------------------------------------------------------------------------------------------
    def changeEvent(self, e):

        if e.type() == QtCore.QEvent.EnabledChange:
            if self.isEnabled():
                self._cameraDevice.newFrame.connect(self._onNewFrame)

            else:
                self._cameraDevice.newFrame.disconnect(self._onNewFrame)

    # ---------------------------------------------------------------------------------------------
    def paintEvent(self, e):

        if self._frame is None:
            return

        painter = QtGui.QPainter(self)
        assert painter

        # effectively draws it when a paint event occurs
        painter.drawImage(QtCore.QPoint(0, 0), ocvimg.OpenCVQImage(self._frame))

# < the end >--------------------------------------------------------------------------------------
        