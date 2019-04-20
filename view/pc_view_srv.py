#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
papi calibrate
                        
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

revision 0.1  2017/abr  mlabru
initial release (Linux/Python)
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/04"

# < imports >--------------------------------------------------------------------------------------

# PyQt4
from PyQt4 import QtCore
from PyQt4 import QtGui

# view
import view.pc_wnd_main_srv as wmain

# < CPAPICalViewSrv >------------------------------------------------------------------------------

class CPAPICalViewSrv(object):
    """
    PAPI Calibra view
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control, f_model):
        """
        constructor
        """
        # init super class
        super(CPAPICalViewSrv, self).__init__()

        # control
        self.__control = f_control
        assert self.__control

        # model
        self.__model = f_model
        assert self.__model

        # show message
        self.__control.splash.showMessage("loading colour table...", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)

    # ---------------------------------------------------------------------------------------------
    def run(self):
        """
        exec gui
        """
        # clear to go
        assert self.__control
        assert self.__control.app

        # create main window
        l_wmain = wmain.CPAPICalWndMainSrv(self.__control)
        assert l_wmain

        # show main window
        l_wmain.show()

        # dismiss splash screen
        self.__control.splash.finish(l_wmain)

        # exec application
        self.__control.app.exec_()

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def app(self):
        return self.__control.app

    # ---------------------------------------------------------------------------------------------
    @property
    def control(self):
        return self.__control

    # ---------------------------------------------------------------------------------------------
    @property
    def model(self):
        return self.__model

# < the end >--------------------------------------------------------------------------------------
