#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pc_camera_feed

camera feed

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
import model.pc_sensor_feed as snsf

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CCameraFeed >----------------------------------------------------------------------------------

class CCameraFeed(snsf.CSensorFeed):
    """
    camera feed
    """
    # signal
    C_SGN_NEW_MSG_CAM = QtCore.pyqtSignal(str)
    C_SGN_DATA_FRAME  = QtCore.pyqtSignal(cv.iplimage)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_sock, f_monitor=None):
        """
        constructor

        @param f_sock: receive socket
        """ 
        # check input
        assert f_sock

        # init super class
        super(CCameraFeed, self).__init__(f_sock, f_monitor)

        # from CSensorFeed
        # sck_rcv     # receive socket
        # monitor     # data monitor
        # v_paused    # flag paused (bool)

        # make connections
        self.C_SGN_NEW_MSG_CAM.connect(self.dispatch_msg)

        # cria o processo de recebimento de imagens
        l_prc = threading.Thread(target=self.query_frame)
        assert l_prc

        # inicia o processo
        l_prc.start()

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def dispatch_msg(self, fs_msg):
        """
        dispatch de imagens
        """
        # existe monitor ?
        if self.monitor:
            # envia mensagem ao monitor
            self.monitor.C_SGN_NEW_MSG_SNS.emit(fs_msg)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def query_frame(self):
        """
        processo de recebimento de imagens
        """
        # clear to go
        assert self.sck_rcv

        # application wait
        while not gdata.G_KEEP_RUN:
            # aguarda
            time.sleep(1)

        # application loop
        while gdata.G_KEEP_RUN:
            # paused ?
            if self.v_paused:
                # aguarda
                time.sleep(1)
                # continua
                continue

            # recebe o tamanho do buffer
            l_msg, l_addr = self.sck_rcv.recvfrom(32)

            # emit new message signal
            self.C_SGN_NEW_MSG_CAM.emit(l_msg)

            # split message
            llst_msg = l_msg.split('#')
            
            # mensagem inválida ?
            if (gdefs.D_MSG_VRS != int(llst_msg[0])) or (gdefs.D_MSG_SIZ != int(llst_msg[1])):
                # próxima mensagem
                continue

            # tamanho da mensagem
            li_length = int(llst_msg[2])
                
            # recebe a imagem
            l_msg, l_addr = self.sck_rcv.recvfrom(li_length)

            # emit new message signal
            self.C_SGN_NEW_MSG_CAM.emit(l_msg)

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
            self.C_SGN_DATA_FRAME.emit(l_frame)

        # fecha a conexão
        self.sck_rcv.close()

# < the end >--------------------------------------------------------------------------------------
