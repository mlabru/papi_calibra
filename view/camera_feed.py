#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
camera_feed

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

# numPy
import numpy as np

# openCV
import cv2
import cv2.cv as cv

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

# < CCameraFeed >----------------------------------------------------------------------------------

class CCameraFeed(QtCore.QObject):
    """
    QImage for openCV
    """
    # signal
    C_SIG_NEW_FRAME = QtCore.pyqtSignal(cv.iplimage)

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
        super(CCameraFeed, self).__init__()

        # receive socket
        self.__sck_rcv_img = f_sock

        # data monitor
        self.__monitor = f_monitor

        # flag paused
        self.__v_paused = False

        # cria o processo de recebimento de imagens
        l_prc = threading.Thread(target=self.__query_frame)
        assert l_prc

        # inicia o processo
        l_prc.start()

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __query_frame(self):
        """
        processo de recebimento de imagens
        """
        # clear to go
        assert self.__sck_rcv_img

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
            l_msg, l_addr = self.__sck_rcv_img.recvfrom(32)

            # monitor (emit new message signal)
            self.__monitor.C_SIG_MSG_CAM.emit(l_msg)

            # split message
            llst_msg = l_msg.split('#')
            
            # mensagem inválida ?
            if (gdefs.D_MSG_VRS != int(llst_msg[0])) or (gdefs.D_MSG_SIZ != int(llst_msg[1])):
                # próxima mensagem
                continue

            # tamanho da mensagem
            li_length = int(llst_msg[2])
                
            # recebe a imagem
            l_msg, l_addr = self.__sck_rcv_img.recvfrom(li_length)

            # monitor (emit new message signal)
            self.__monitor.C_SIG_MSG_CAM.emit(l_msg)

            # split message
            llst_msg = l_msg.split('#')

            # mensagem inválida ?
            if (gdefs.D_MSG_VRS != int(llst_msg[0])) or (gdefs.D_MSG_IMG != int(llst_msg[1])):
                # próxima mensagem
                continue

            # converte de string para imagem
            l_data = np.fromstring(l_msg[8:], dtype="uint8")

            # decodifica a imagem
            l_data = cv2.imdecode(l_data, 1)

            # converting from numPy to iplImage
            l_frame = cv.CreateImageHeader((l_data.shape[1], l_data.shape[0]), cv.IPL_DEPTH_8U, 3)
            assert l_frame
            
            cv.SetData(l_frame, l_data.tostring(), l_data.dtype.itemsize * 3 * l_data.shape[1])

            # emit new frame signal
            self.C_SIG_NEW_FRAME.emit(l_frame)

        # fecha a conexão
        self.__sck_rcv_img.close()

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
