#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
OpenCVQImage

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

# pyQt4
from PyQt4 import QtGui

# < OpenCVQImage >---------------------------------------------------------------------------------

class OpenCVQImage(QtGui.QImage):
    """
    QImage for openCV
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, opencvBgrImg):
        """
        constructor
        """
        # get depth and channels
        depth, nChannels = opencvBgrImg.depth, opencvBgrImg.nChannels
        print "depth, channels:", depth, nChannels

        # valid image ?
        if (cv.IPL_DEPTH_8U != depth) or (3 != nChannels):
            raise ValueError("the input image must be 8-bit, 3-channel")

        # get image size
        w, h = cv.GetSize(opencvBgrImg)
        print "w, h:", w, h

        # create image
        opencvRgbImg = cv.CreateImage((w, h), depth, nChannels)
        assert opencvRgbImg

        # converts the image from BGR to RGB format. it's assumed the image is in BGR format
        cv.CvtColor(opencvBgrImg, opencvRgbImg, cv.CV_BGR2RGB)

        # saves a reference to the opencvRgbImg byte-content to prevent the garbage collector from deleting it when __init__ returns
        self._imgData = opencvRgbImg.tostring()

        # call the QImage base class constructor passing the byte-content, dimensions and format of the image
        super(OpenCVQImage, self).__init__(self._imgData, w, h, QtGui.QImage.Format_RGB888)

# < the end >--------------------------------------------------------------------------------------
            