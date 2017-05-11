#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pc_sensor_feed

sensors feed

revision 0.1  2017/abr  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/05"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import threading
import time

# pyQt4
from PyQt4 import QtCore

# model
import model.pc_data as gdata

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CSensorFeed >----------------------------------------------------------------------------------

class CSensorFeed(QtCore.QObject):
    """
    sensors feed
    """
    # signal new message received
    C_SGN_NEW_MSG_SNS = QtCore.pyqtSignal(str)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_sock, f_monitor=None):
        """
        constructor

        @param f_sock: receive socket
        """ 
        # check input
        assert f_sock

        # init super class
        super(CSensorFeed, self).__init__()

        # receive socket
        self.__sck_rcv = f_sock

        # data monitor
        self.__monitor = f_monitor

        # flag paused
        self.__v_paused = False

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def query_data(self):
        """
        processo de recebimento de dados
        """
        # clear to go
        assert self.__sck_rcv

        # application wait
        while not gdata.G_KEEP_RUN:
            # aguarda
            time.sleep(1)

        # application loop
        while gdata.G_KEEP_RUN:
            # paused ?
            if self.__v_paused:
                # aguarda
                time.sleep(1)
                # continua
                continue

            # recebe uma mensagem
            l_msg, l_addr = self.__sck_rcv.recvfrom(1024)

            # emit new message signal
            self.C_SGN_NEW_MSG_SNS.emit(l_msg)

        # fecha a conexão
        self.__sck_rcv.close()

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def monitor(self):
        return self.__monitor

    @monitor.setter
    def monitor(self, f_val):
        self.__monitor = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def v_paused(self):
        return self.__v_paused

    @v_paused.setter
    def v_paused(self, f_val):
        self.__v_paused = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_rcv(self):
        return self.__sck_rcv

    @sck_rcv.setter
    def sck_rcv(self, f_val):
        self.__sck_rcv = f_val

# < the end >--------------------------------------------------------------------------------------
