#!/usr/bin/env python
# -*- coding: utf-8 -*-

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import socket

# numPy
import numpy

# openCV
import cv2
import cv2.cv as cv

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# tupla
M_UDP_ADDR = (gdefs.D_NET_GCS, gdefs.D_NET_PORT_IMG)

# -------------------------------------------------------------------------------------------------

# logger
logging.basicConfig()
        
# cria o soket
l_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
assert l_sock

# inicia a captura do vídeo
l_capture = cv2.VideoCapture(0)
l_capture.set(cv.CV_CAP_PROP_FRAME_WIDTH, gdefs.D_VID_HORZ)
l_capture.set(cv.CV_CAP_PROP_FRAME_HEIGHT, gdefs.D_VID_VERT)

# para todo o sempre...
while True:
    # obtém um frame
    l_ret, l_frame = l_capture.read()

    # encode em jpeg
    l_encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    # faz o encode
    l_result, l_img_encode = cv2.imencode(".jpg", l_frame, l_encode_param)

    # converte em um array
    l_data = numpy.array(l_img_encode)

    # converte em string
    l_stringData = l_data.tostring()

    # tamanho da imagem excede o tamanho máximo de UDP ?
    if len(l_stringData) > 65507:
        # logger
        l_log = logging.getLogger("papi_sender_cam::main")
        l_log.setLevel(logging.WARNING)
        l_log.warning(u"<E01: image too long: {}. Droping.".format(len(l_stringData)))
                                                        
        # descarta a mensagem 
        continue
    
    # header
    ls_header = "{}#{}#".format(gdefs.D_MSG_VRS, gdefs.D_MSG_IMG)

    # envia o tamanho da string 
    l_sock.sendto("{}#{}#{}".format(gdefs.D_MSG_VRS, gdefs.D_MSG_SIZ, len(ls_header) + len(l_stringData)), M_UDP_ADDR)
    # envia a string
    l_sock.sendto("{}{}".format(ls_header, l_stringData), M_UDP_ADDR)

# fecha o socket
l_sock.close()

# <the end>----------------------------------------------------------------------------------------
