#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
sensor_feed

papi calibrate

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
    # signal
    C_SIG_NEW_ALTM = QtCore.pyqtSignal(list)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_sock, f_monitor):
        """
        constructor

        @param f_sock: receive socket
        @param f_monitor: data monitor
        """ 
        # check input
        assert f_sock
        assert f_monitor

        # init super class
        super(CSensorFeed, self).__init__()

        # receive socket
        self.__sck_rcv_sns = f_sock

        # data monitor
        self.__monitor = f_monitor

        # flag paused
        self.__v_paused = False

        # cria o processo de recebimento de imagens
        l_prc = threading.Thread(target=self.__query_data)
        assert l_prc

        # inicia o processo
        l_prc.start()

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __query_data(self):
        """
        processo de recebimento de imagens
        """
        # clear to go
        assert self.__sck_rcv_sns

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

            # recebe o tamanho do buffer
            l_msg, l_addr = self.__sck_rcv_sns.recvfrom(1024)

            # monitor (emit new message signal)
            self.__monitor.C_SIG_MSG_SNS.emit(l_msg)

            # split message
            llst_msg = l_msg.split('#')
            
            # mensagem inválida ?
            if gdefs.D_MSG_VRS != int(llst_msg[0]):
                # próxima mensagem
                continue

            # mensagem de altímetro ?
            if gdefs.D_MSG_ALT == int(llst_msg[1]):
                # emit new altimeter data signal
                self.C_SIG_NEW_ALTM.emit(llst_msg[2:])

        # fecha a conexão
        self.__sck_rcv_sns.close()

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def paused(self):
        return self.__v_paused

    @paused.setter
    def paused(self, f_val):
        self.__v_paused = f_val

# < the end >--------------------------------------------------------------------------------------
