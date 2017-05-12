#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pc_config

configuration manager

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/12"

# < import >---------------------------------------------------------------------------------------

# python library
import ConfigParser
import argparse
import os

# model 
import model.pc_data as gdata
import model.pc_utils as util

# control
import control.pc_defs as gdefs

# < class CPAPICalConfig >-------------------------------------------------------------------------

class CPAPICalConfig(object):
    """
    mantém as informações de configuração
    """
    # informações comuns de configuração
    __CFG_PAPICAL = {"dir.dat": gdefs.D_DIR_DAT,          # diretório de dados
                     "dir.img": gdefs.D_DIR_IMG,          # diretório de imagens
                     "dir.tab": gdefs.D_DIR_TAB,          # diretório de tabelas
 
                     "glb.canal": gdata.G_CANAL,          # canal de comunicação
                     "glb.server": gdata.G_SERVER,        # modo de execução (cliente(F)/servidor(T))

                     "msg.vrs": gdefs.D_MSG_VRS,          # versão do protocolo

                     "net.adr": "",                       # symbolic name meaning all available interfaces
                     "net.ifc": gdefs.D_NET_IFC,          # interface de rede
                     "net.cli": gdefs.D_NET_CLI,          # endereço cliente
                     "net.srv": gdefs.D_NET_SRV,          # endereço server

                     "net.ccc": gdefs.D_NET_PORT_CCC,     # porta de comando/controle/comunicação
                     "net.img": gdefs.D_NET_PORT_IMG,     # porta de imagens
                     "net.alt": gdefs.D_NET_PORT_ALT,     # porta de altímetro
                     "net.bar": gdefs.D_NET_PORT_BAR,     # porta de barômetro
                     "net.gps": gdefs.D_NET_PORT_GPS,     # porta de GPS
                     "net.thr": gdefs.D_NET_PORT_THR,     # porta de termômetro

                     "ser.baud": gdefs.D_SER_PORT,        # porta serial default
                     "ser.port": gdefs.D_SER_BAUD,        # baudrate default
                     
                     "tab.aer": gdefs.D_TBL_AER,          # tabela de aeródromos

                     "tim.evnt": gdefs.D_TIM_EVNT,        # tratador de eventos (10Hz)
                     "tim.rrbn": gdefs.D_TIM_RRBN,        # round-robin time (10Hz)
                     "tim.wait": gdefs.D_TIM_WAIT,        # tempo de espera de eventos (2Hz)
                    }  # __CFG_PAPICAL

    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_cnfg):
        """
        constructor

        @param fs_cnfg: full path do arquivo de configuração
        """
        # inicia a super class
        super(CPAPICalConfig, self).__init__()

        # load default values in dictionary
        self.__dct_config = self.__CFG_PAPICAL.copy()
        assert self.__dct_config is not None

        # cria o parser para o arquivo de configuração
        l_cp = ConfigParser.SafeConfigParser()
        assert l_cp

        # arquivo de configuração existe ?
        if os.path.exists(os.path.expanduser(fs_cnfg)):
            # abre o arquivo de configuração
            l_cp.readfp(open(fs_cnfg))

            # load entire config file in dictionary
            for l_section in l_cp.sections():
                for l_option in l_cp.options(l_section):
                    self.__dct_config[str(l_section.lower() + '.' + l_option.lower())] = l_cp.get(l_section, l_option)

        # modo de execução
        self.__dct_config["glb.server"] = self.__get_server_mode()

        # cria um parser para os argumentos
        l_parser = argparse.ArgumentParser(description="PAPI Calibra (C) 2017.")
        assert l_parser

        # argumento: canal de comunicação
        l_parser.add_argument("-c", "--canal", type=int, dest="canal",
                              default=self.__dct_config["glb.canal"],
                              help=u"Communications channel (default: {})".format(self.__dct_config["glb.canal"]))

        # argumento: modo servidor
        l_parser.add_argument("-s", "--server", action="store_true",
                              default=self.__dct_config["glb.server"], 
                              help=u"Server Mode (default: {})".format(self.__dct_config["glb.server"]))

        # argumento: version
        l_parser.add_argument("-v", "--version", action="version", version=__version__)

        # faz o parser da linha de argumentos
        l_args = l_parser.parse_args()
        assert l_args

        # salva os argumentos no dicionário
        self.__dct_config["glb.canal"] = abs(int(l_args.canal))
        self.__dct_config["glb.server"] = l_args.server

        # endereço da contra-parte
        self.__dct_config["net.adr"] = self.__dct_config["net.srv"] if l_args.server else self.__dct_config["net.cli"] 

        # load dirs section
        self.__load_dirs()

    # ---------------------------------------------------------------------------------------------
    def __get_server_mode(self):
        """
        modo de execução
        """
        # return platform data
        return os.uname()[4].startswith("arm")

    # ---------------------------------------------------------------------------------------------
    def __load_dirs(self):
        """
        carrega as configurações de diretórios
        """
        # monta o diretório de imagens
        self.__dct_config["dir.img"] = util.filepath(os.path.join(self.__dct_config["dir.dat"],
                                                                  self.__dct_config["dir.img"]))

        # monta o diretório de tabelas
        self.__dct_config["dir.tab"] = util.filepath(os.path.join(self.__dct_config["dir.dat"],
                                                                  self.__dct_config["dir.tab"]))

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_config(self):
        """
        config manager data dictionary
        """
        return self.__dct_config

    @dct_config.setter
    def dct_config(self, f_val):
        """
        config manager data dictionary
        """
        # save a shallow copy
        self.__dct_config = dict(f_val)

# < the end >--------------------------------------------------------------------------------------
