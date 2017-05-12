#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
papi calibrate

revision 0.1  2017/abr  mlabru
initial version (Linux/Python)
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/04"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import multiprocessing
import sys
import time

# PyQt
from PyQt4 import QtCore
from PyQt4 import QtGui

# model
import model.pc_data as gdata
import model.pc_model_cli as mdcli
import model.pc_model_srv as mdsrv

# view
import view.pc_view_cli as vcli
import view.pc_view_srv as vsrv

# control
import control.pc_config as config
import control.pc_net_sender as sender
import control.pc_net_listener as listener
import control.pc_net_sock_in as sockin

# events
import control.events.events_manager as evtmgr
import control.events.events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CPAPICalControl >------------------------------------------------------------------------------

class CPAPICalControl(object):
    """
    PAPI Calibra control
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # init super class
        super(CPAPICalControl, self).__init__()

        # instancia o event manager
        self.__event = evtmgr.CEventsManager()
        assert self.__event

        # registra a sí próprio como recebedor de eventos
        self.__event.register_listener(self)

        # carrega o arquivo com as opções de configuração
        self.__config = config.CPAPICalConfig("papical.cfg")
        assert self.__config

        # create application
        self.create_app("papi_calibra")

        # interface e endereço de rede
        lt_ifc = self.__config.dct_config["net.ifc"]
        ls_adr = self.__config.dct_config["net.adr"]

        # portas
        li_ccc = int(self.__config.dct_config["net.ccc"])
        li_img = int(self.__config.dct_config["net.img"])
        li_sns = int(self.__config.dct_config["net.sns"])

        # server mode ?
        if self.__config.dct_config["glb.server"]:
            # create connections
            self.create_connections_server(lt_ifc, ls_adr, li_ccc, li_img, li_sns)

            # instancia o modelo
            self.__model = mdsrv.CPAPICalModelSrv(self)
            assert self.__model

            # create view
            self.__view = vsrv.CPAPICalViewSrv(self, self.__model)
            assert self.__view

        # senão, client mode
        else:
            # create connections
            self.create_connections_client(lt_ifc, ls_adr, li_ccc, li_img, li_sns)        
        
            # instancia o modelo
            self.__model = mdcli.CPAPICalModelCli(self)
            assert self.__model

            # create view
            self.__view = vcli.CPAPICalViewCli(self, self.__model)
            assert self.__view

        # inicia
        gdata.G_KEEP_RUN = True

    # ---------------------------------------------------------------------------------------------
    def create_app(self, fs_name):
        """
        create application
        """
        # create application
        self.__app = QtGui.QApplication(sys.argv)
        assert self.__app

        # setup application parameters
        self.__app.setOrganizationName("sophosoft")
        self.__app.setOrganizationDomain("sophosoft.com.br")
        self.__app.setApplicationName(fs_name)
        
        # load logo
        l_pix_logo = QtGui.QPixmap(":/images/logos/logo.png")
        assert l_pix_logo
        
        # create splash screen
        self.__splash = QtGui.QSplashScreen(l_pix_logo, QtCore.Qt.WindowStaysOnTopHint)
        assert self.__splash

        self.__splash.setMask(l_pix_logo.mask())
        
        # show splash screen
        self.__splash.show()

        # process events (before main loop)
        self.__app.processEvents()

    # ---------------------------------------------------------------------------------------------
    def create_connections_client(self, ft_ifc, fs_adr, fi_ccc, fi_img, fi_sns):
        """
        create connections
        """
        # cria a queue de envio de comando/controle/configuração
        self.__q_snd_ccc = multiprocessing.Queue()
        assert self.__q_snd_ccc

        # cria o socket de envio de comando/controle/configuração
        self.__sck_snd_ccc = sender.CNetSender(ft_ifc, fs_adr, fi_ccc, self.__q_snd_ccc)
        assert self.__sck_snd_ccc

        # cria a queue de recebimento de comando/controle/configuração
        self.__q_rcv_ccc = multiprocessing.Queue()
        assert self.__q_rcv_ccc

        # cria o socket de recebimento de comando/controle/configuração
        self.__sck_rcv_ccc = listener.CNetListener(ft_ifc, fs_adr, fi_ccc, self.__q_rcv_ccc)
        assert self.__sck_rcv_ccc

        # cria o socket de recebimento de imagens
        self.__sck_rcv_img = sockin.CNetSockIn(ft_ifc, fs_adr, fi_img)
        assert self.__sck_rcv_img

        # cria o socket de recebimento de dados de sensores
        self.__sck_rcv_sns = sockin.CNetSockIn(ft_ifc, fs_adr, fi_sns)
        assert self.__sck_rcv_sns

    # ---------------------------------------------------------------------------------------------
    def create_connections_server(self, ft_ifc, fs_adr, fi_ccc, fi_img, fi_sns):
        """
        create connections
        """
        pass

    # ---------------------------------------------------------------------------------------------
    # @staticmethod
    def notify(self, f_evt):
        """
        event handling callback

        @param f_event: received event
        """
        # check input
        assert f_evt
        
        M_LOG.debug("pc_control: recebeu notificacao...")
        
        # received quit event ?
        if isinstance(f_evt, events.CQuit):
            M_LOG.debug("pc_control:...de FIM")

            # para todos os processos
            gdata.G_KEEP_RUN = False

            # wait all tasks terminate
            time.sleep(1)

            # ends application
            sys.exit()

    # =============================================================================================
    # dados     
    # =============================================================================================
        
    # ---------------------------------------------------------------------------------------------
    @property
    def app(self):
        return self.__app

    # ---------------------------------------------------------------------------------------------
    @property
    def config(self):
        return self.__config
        
    # ---------------------------------------------------------------------------------------------
    @property
    def dct_config(self):
        return self.__config.dct_config
        
    # ---------------------------------------------------------------------------------------------
    @property
    def event(self):
        return self.__event
        
    # ---------------------------------------------------------------------------------------------
    @property
    def model(self):
        return self.__model

    # ---------------------------------------------------------------------------------------------
    @property
    def q_rcv_ccc(self):
        return self.__q_rcv_ccc

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_rcv_ccc(self):
        return self.__sck_rcv_ccc

    # ---------------------------------------------------------------------------------------------
    @property
    def q_rcv_img(self):
        return self.__q_rcv_img

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_rcv_img(self):
        return self.__sck_rcv_img

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_rcv_sns(self):
        return self.__sck_rcv_sns

    # ---------------------------------------------------------------------------------------------
    @property
    def q_snd_ccc(self):
        return self.__q_snd_ccc

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_snd_ccc(self):
        return self.__sck_snd_ccc

    # ---------------------------------------------------------------------------------------------
    @property
    def splash(self):
        return self.__splash

    # ---------------------------------------------------------------------------------------------
    @property
    def view(self):
        return self.__view

# < the end >--------------------------------------------------------------------------------------
