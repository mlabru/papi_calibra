#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pc_defs

defines e constantes válidas globalmente

revision 0.1  2017/may  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/05"

# < camera >---------------------------------------------------------------------------------------

# configuração da camera
D_CAM_WIDTH = 320
D_CAM_HEIGHT = 240

# < config >---------------------------------------------------------------------------------------

# arquivo de configuração
D_CFG_FILE = "papical.cfg"

# < diretórios >-----------------------------------------------------------------------------------

# diretório de dados
D_DIR_DAT = "data"
# diretório de imagens
D_DIR_IMG = "images"
# diretório de tabelas
D_DIR_TAB = "tabs"

# < mensagens >------------------------------------------------------------------------------------

# versão do conjunto de mensagens
D_MSG_VRS = 101

# códigos das mensagens

D_MSG_SIZ = 111    # mensagens de imagens
D_MSG_IMG = 112    # mensagens de imagens
D_MSG_SNS = 113    # mensagens de sensores
D_MSG_ALT = 114    # mensagens de altímetro

# separador de campos na mensagem
D_MSG_SEP = '#'

# mensagens válidas
SET_MSG_VALIDAS = [D_MSG_IMG, D_MSG_SNS]

# < rede >-----------------------------------------------------------------------------------------

# interface de rede
D_NET_IFC = (None, None)  # ("wlan0", "wlan0")

# endereço do cliente
D_NET_CLI = "192.168.12.1"
# endereço do servidor
D_NET_SRV = "192.168.12.2"

# arbitrary non-privileged ports

# comnado/controle/configuração
D_NET_PORT_CCC = 1923
# imagens
D_NET_PORT_IMG = 1970
# sensores
D_NET_PORT_SNS = 1961

# < serial >---------------------------------------------------------------------------------------

# porta
D_SER_PORT = "/dev/ttyACM0"
# velocidade
D_SER_BAUD = 115000

# < stylesheet >-----------------------------------------------------------------------------------

D_GBX_STYLE = """QGroupBox { color: white;
                             background-color: rgb(150, 150, 150);
                             border-style: solid;
                             border: 2px solid white;
                             border-radius: 5px;
                             margin-top: 4ex; }

                 QGroupBox::title { background-color: transparent;
                                    subcontrol-origin: margin;
                                    subcontrol-position: top left;
                                    padding: 3 13px;
                                    font-size: 18px;
                                    font-weight: bold; }

                 QGroupBox:focus { border: 2px solid 
                                   QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a); }
"""
# D_GBX_STYLE = ""

D_PTE_STYLE = """QPlainTextEdit { color: white;
                                  background-color: rgb(0, 0, 0);
                                  border: 1px solid rgb(200, 200, 200);
                                  border-style: solid;
                                  border-radius: 5px;}
"""
# D_PTE_STYLE = ""

D_XXX_STYLE = """
                                  margin-top: 4ex; }

                 QPlainTextEdit::title { background-color: transparent;
                                         subcontrol-origin: margin;
                                         subcontrol-position: top left;
                                         padding: 3 13px;
                                         font-size: 18px;
                                         font-weight: bold; }

                 QPlainTextEdit:focus { border: 2px solid 
                                        QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a); }
"""
# < tables >---------------------------------------------------------------------------------------

# tabela de aeródromos
D_TBL_AER = "tabAer"

# < temporização >---------------------------------------------------------------------------------

# tratador de eventos (10Hz) (float)
D_TIM_EVNT = .1
# round-robin (10Hz) (float)
D_TIM_RRBN = .1
# espera de eventos (2Hz) (float)
D_TIM_WAIT = .5

# < the end >--------------------------------------------------------------------------------------
