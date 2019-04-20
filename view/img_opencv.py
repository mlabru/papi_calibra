#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
img_opencv

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

# openCV
import cv2

# pyQt4
from PyQt4 import QtGui

# < CImageOpenCV >---------------------------------------------------------------------------------

class CImageOpenCV(QtGui.QImage):
    """
    QImage for openCV
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_opencv_bgr_img):
        """
        constructor

        @param f_opencv_bgr_img: BGR image
        """
        # get image size
        l_h, l_w, l_c = f_opencv_bgr_img.shape

        # converts the image from BGR to RGB format. it's assumed the image is in BGR format
        # cv2.CvtColor(f_opencv_bgr_img, l_opencv_rgb_img, cv2.cv.BGR2RGB)

        # saves a reference to the l_opencv_rgb_img byte-content to prevent the garbage
        # collector from deleting it when __init__ returns
        self.__img_data = f_opencv_bgr_img.tostring()

        # call the QImage base class constructor passing the byte-content, dimensions and format of the image
        super(CImageOpenCV, self).__init__(self.__img_data, l_w, l_h, QtGui.QImage.Format_RGB888)

# < the end >--------------------------------------------------------------------------------------
            