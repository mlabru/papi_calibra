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
        ls_ifc = self.__config.dct_config["net.ifc"]
        ls_adr = self.__config.dct_config["net.adr"]

        # portas
        ls_ccc = self.__config.dct_config["net.ccc"]
        ls_img = self.__config.dct_config["net.img"]
        ls_sns = self.__config.dct_config["net.sns"]

        # server mode ?
        if self.__config.dct_config["glb.server"]:
            # create connections
            self.create_connections_server(ls_ifc, ls_adr, ls_ccc, ls_img, ls_sns)

            # instancia o modelo
            self.__model = mdsrv.CPAPICalModelSrv(self)
            assert self.__model

            # create view
            self.__view = vsrv.CPAPICalViewSrv(self, self.__model)
            assert self.__view

        # senão, client mode
        else:
            # create connections
            self.create_connections_client(ls_ifc, ls_adr, ls_ccc, ls_img, ls_sns)        
        
            # instancia o modelo
            self.__model = mdcli.CPAPICalModelCli(self)
            assert self.__model

            # create view
            self.__view = vcli.CPAPICalViewCli(self, self.__model)
            assert self.__view

        # inicia
        gdata.G_KEEP_RUN = True

    # ---------------------------------------------------------------------------------------------
    def cbk_termina(self):
        """
        termina a aplicação
        """
        # clear to go
        assert self.__event

        # cria um evento de quit
        l_evt = events.CQuit()
        assert l_evt

        # dissemina o evento
        self.__event.post(l_evt)
        '''
        print "threadings:", threading.enumerate()

        import traceback

        for thread_id, frame in sys._current_frames().iteritems():
            name = thread_id
            for thread in threading.enumerate():
                if thread.ident == thread_id:
                    name = thread.name

            traceback.print_stack(frame)
        '''
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
    def create_connections_client(self, ls_ifc, ls_adr, ls_ccc, ls_img, ls_sns):
        """
        create connections
        """
        # cria a queue de envio de comando/controle/configuração
        self.__q_snd_ccc = multiprocessing.Queue()
        assert self.__q_snd_ccc

        # cria o socket de envio de comando/controle/configuração
        self.__sck_snd_ccc = sender.CNetSender(ls_ifc, ls_adr, ls_ccc, self.__q_snd_ccc)
        assert self.__sck_snd_ccc

        # cria a queue de recebimento de comando/controle/configuração
        self.__q_rcv_ccc = multiprocessing.Queue()
        assert self.__q_rcv_ccc

        # cria o socket de recebimento de comando/controle/configuração
        self.__sck_rcv_ccc = listener.CNetListener(ls_ifc, ls_adr, ls_ccc, self.__q_rcv_ccc)
        assert self.__sck_rcv_ccc

        # cria o socket de recebimento de imagens
        self.__sck_rcv_img = sockin.CNetSockIn(ls_ifc, ls_adr, ls_img)
        assert self.__sck_rcv_img

        # cria o socket de recebimento de dados de sensores
        self.__sck_rcv_sns = sockin.CNetSockIn(ls_ifc, ls_adr, ls_sns)
        assert self.__sck_rcv_sns

    # ---------------------------------------------------------------------------------------------
    def create_connections_server(self, ls_ifc, ls_adr, ls_ccc, ls_img, ls_sns):
        """
        create connections
        """
        pass
        
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
