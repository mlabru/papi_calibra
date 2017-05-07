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
import sys

# pyQt4
from PyQt4 import QtCore
from PyQt4 import QtGui

# openCV
import cv

# papi_alibra
import CameraDevice as cd
import CameraWidget as cw

# -------------------------------------------------------------------------------------------------
def _main():

    @QtCore.pyqtSlot(cv.iplimage)
    def onNewFrame(frame):
        cv.CvtColor(frame, frame, cv.CV_RGB2BGR)
        msg = "processed frame"
        font = cv.InitFont(cv.CV_FONT_HERSHEY_DUPLEX, 1.0, 1.0)
        tsize, baseline = cv.GetTextSize(msg, font)
        w, h = cv.GetSize(frame)
        tpt = (w - tsize[0]) / 2, (h - tsize[1]) / 2
        cv.PutText(frame, msg, tpt, font, cv.RGB(255, 0, 0))

    app = QtGui.QApplication(sys.argv)

    cameraDevice = cd.CameraDevice(mirrored=True)
    assert cameraDevice

    cameraWidget1 = cw.CameraWidget(cameraDevice)
    assert cameraWidget1

    cameraWidget1.newFrame.connect(onNewFrame)
    cameraWidget1.show()

    cameraWidget2 = cw.CameraWidget(cameraDevice)
    assert cameraWidget2

    cameraWidget2.show()

    sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------
# this is the bootstrap process

if "__main__" == __name__:

    _main()

# < the end >--------------------------------------------------------------------------------------    
    