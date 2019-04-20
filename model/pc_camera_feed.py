#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
pc_camera_feed

camera feed

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

revision 0.1  2017/abr  mlabru
initial release (Linux/Python)
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/05"

# < imports >--------------------------------------------------------------------------------------

# python library
import base64
import errno
import logging
import socket
import threading
import time

# numPy
import numpy as np

# openCV
import cv2

# pyQt4
from PyQt4 import QtCore

# model
import model.pc_data as gdata
import model.pc_sensor_feed as snsf

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < CCameraFeed >----------------------------------------------------------------------------------

class CCameraFeed(snsf.CSensorFeed):
    """
    camera feed
    """
    # signal
    C_SGN_NEW_MSG_CAM = QtCore.pyqtSignal(str)
    C_SGN_DATA_FRAME  = QtCore.pyqtSignal(np.ndarray)  # cv.iplimage)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_monitor=None):
        """
        constructor

        @param f_monitor: data monitor
        """ 
        # logger
        # M_LOG.info("CCameraFeed constructor >>")

        # check input
        # assert f_monitor

        # network interface
        lt_ifc = gdata.G_DCT_CONFIG["net.ifc"]
        # network address
        ls_addr = gdata.G_DCT_CONFIG["net.adr"]
        # port
        li_port = int(gdata.G_DCT_CONFIG["net.img"])

        # init super class
        super(CCameraFeed, self).__init__(lt_ifc, ls_addr, li_port, f_monitor)

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
    @QtCore.pyqtSlot(str)
    def dispatch_msg(self, fs_msg):
        """
        dispatch de imagens
        """
        # logger
        # M_LOG.info("dispatch_msg >>")

        # existe monitor ?
        if self.monitor:
            # envia mensagem ao monitor
            self.monitor.C_SGN_NEW_MSG_CAM.emit(fs_msg)

    # ---------------------------------------------------------------------------------------------
    def __receive_all(self, f_sock, fi_len):
        """
        receive a message in packets
        
        @param f_sock:
        @param fi_
        """
        # logger
        # M_LOG.info(">> receive all")

        # data
        ls_str_data = ""

        # para todos os packets...
        while 1:
            # recebe a imagem
            lv_ok, llst_msg, l_msg = self.__receive_msg(f_sock, fi_len)
            # M_LOG.debug("l_msg len: {}".format(len(l_msg)))

            # split message
            llst_msg = l_msg.split('#')
            # M_LOG.debug("llst_msg: {}".format(llst_msg))

            # mensagem ?
            if gdefs.D_MSG_I00 == int(llst_msg[1]):
                # próxima mensagem
                ls_str_data += l_msg[gdefs.D_HDR_SIZ:]

            # fim de mensagem ?
            elif gdefs.D_MSG_I99 == int(llst_msg[1]):
                # próxima mensagem
                ls_str_data += l_msg[gdefs.D_HDR_SIZ:]

                # quit
                break

            # senão,...
            else:
                # quit
                break

        # log 
        # M_LOG.debug("msg len: {}".format(len(ls_str_data)))

        # return
        return True, ls_str_data    

    # ---------------------------------------------------------------------------------------------
    def __receive_msg(self, f_sock, fi_size, fi_type=None):
        """
        receive a message
        """
        # logger
        # M_LOG.info("__receive_msg >>")

        try:
            # receive image size
            l_msg, l_addr = f_sock.recvfrom(fi_size)

        # em caso de erro...
        except socket.error, l_err:
            # ger error code
            li_err = l_err.args[0]

            # no data available ?
            if (errno.EAGAIN == li_err) or (errno.EWOULDBLOCK == li_err):
                # no data available
                return False, None, None

            # senão,...
            else:
                # logger
                l_log = logging.getLogger("CCameraFeed::__receive_msg")
                l_log.setLevel(logging.CRITICAL)
                l_log.critical(u"<E01: error: {}".format(l_err))

                # a "real" error occurred
                sys.exit(1)

        # zero len message ?
        if 0 == len(l_msg):
            # logger
            l_log = logging.getLogger("CCameraFeed::__receive_msg")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E02: error: zero length message.")

            # continue
            return False, None, None

        # emit new message signal
        self.C_SGN_NEW_MSG_CAM.emit(l_msg)

        # split message
        llst_msg = l_msg.split('#')
        
        # versão ou tipo inválidos ?
        if (gdefs.D_MSG_VRS != int(llst_msg[0])) or ((fi_type is not None) and (fi_type != int(llst_msg[1]))):
            # return error
            return False, None, None

        # return message
        return True, llst_msg, l_msg

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def query_frame(self):
        """
        processo de recebimento de imagens
        """
        # logger
        # M_LOG.info("query_frame >>")

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

            # non-blocking socket
            self.sck_rcv.settimeout(0.)
            self.sck_rcv.setblocking(0)

            # receive image size
            lv_ok, llst_msg, _ = self.__receive_msg(self.sck_rcv, 32, gdefs.D_MSG_SIZ)
            
            # invalid message ?
            if not lv_ok:
                # next message 
                continue

            # log 
            # M_LOG.debug("llst_msg(1): {}/{}/len: {}".format(llst_msg[0], llst_msg[1], llst_msg[2]))
            
            # tamanho da mensagem
            li_len = int(llst_msg[2])

            # change to blocking socket
            self.sck_rcv.setblocking(1)

            # receive image
            lv_ok, l_msg = self.__receive_all(self.sck_rcv, li_len + gdefs.D_HDR_SIZ)

            # invalid message ?
            if not lv_ok:
                # next message 
                continue

            # encoded ? 
            if gdefs.D_B64:
                # converte de string para imagem
                l_data = np.fromstring(base64.b64decode(l_msg), dtype="uint8")

            # senão,...
            else:
                # converte de string para imagem
                l_data = np.fromstring(l_msg, dtype="uint8")

            # decodifica a imagem
            l_frame = cv2.imdecode(l_data, 1)

            # emit new frame signal
            self.C_SGN_DATA_FRAME.emit(l_frame)

        # fecha a conexão
        self.sck_rcv.close()

# < the end >--------------------------------------------------------------------------------------
