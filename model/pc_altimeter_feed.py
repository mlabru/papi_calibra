#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pc_altimeter_feed

altimeter feed

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
import model.pc_sensor_feed as snsf

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CAltimeterFeed >-------------------------------------------------------------------------------

class CAltimeterFeed(snsf.CSensorFeed):
    """
    altimeter feed
    """
    # signal
    C_SGN_DATA_ALT = QtCore.pyqtSignal(list)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control, f_monitor=None):
        """
        constructor

        @param f_control: control
        """ 
        # check input
        assert f_control

        # network interface
        lt_ifc = f_control.config.dct_config["net.ifc"]
        # network address
        ls_addr = f_control.config.dct_config["net.adr"]
        # port
        li_port = int(f_control.config.dct_config["net.alt"])

        # init super class
        super(CAltimeterFeed, self).__init__(lt_ifc, ls_addr, li_port, f_monitor)

        # from CSensorFeed
        # sck_rcv     # receive socket
        # monitor     # data monitor
        # v_paused    # flag paused (bool)

        # make connections
        self.C_SGN_NEW_MSG_SNS.connect(self.trata_msg)

        # cria o processo de recebimento de dados
        l_prc = threading.Thread(target=self.query_data)
        assert l_prc

        # inicia o processo
        l_prc.start()

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(str)
    def trata_msg(self, fs_msg):
        """
        trata mensagem recebida

        @param fs_msg: received message
        """ 
        # check input
        assert fs_msg

        # existe monitor ?
        if self.monitor:
            # envia mensagem ao monitor
            self.monitor.C_SGN_NEW_MSG_SNS.emit(str(fs_msg))

        # split message
        llst_msg = str(fs_msg).split('#')
        
        # mensagem válida de altímetro ?
        if (gdefs.D_MSG_VRS == int(llst_msg[0])) and (gdefs.D_MSG_ALT == int(llst_msg[1])):
            # emit new altimeter data signal
            self.C_SGN_DATA_ALT.emit(llst_msg[2:])

# < the end >--------------------------------------------------------------------------------------
