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
M_UDP_ADDR = (gdefs.D_NET_CLI, gdefs.D_NET_PORT_IMG)

# -------------------------------------------------------------------------------------------------

# cria o soket
l_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
assert l_sock

# inicia a captura do vídeo
capture = cv2.VideoCapture(0)
capture.set(cv.CV_CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

# para todo o sempre...
while True:
    # obtém um frame
    ret, frame = capture.read()
    # print ret

    # encode em jpeg
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    # faz o encode
    result, imgencode = cv2.imencode(".jpg", frame, encode_param)
    # print result

    # converte em um array
    data = numpy.array(imgencode)

    # converte em string
    stringData = data.tostring()
    # print len(stringData)

    # tamanho da imagem excede o tamanho máximo de UDP ?
    if len(stringData) > 65507:
        # descarta a mensagem 
        continue
    
    # header
    ls_header = "{}#{}#".format(gdefs.D_MSG_VRS, gdefs.D_MSG_IMG)

    # envia o tamanho da string 
    l_sock.sendto("{}#{}#{}".format(gdefs.D_MSG_VRS, gdefs.D_MSG_SIZ, len(ls_header) + len(stringData)), M_UDP_ADDR)
    # envia a string
    l_sock.sendto("{}{}".format(ls_header, stringData), M_UDP_ADDR)

# fecha o socket
l_sock.close()

# <the end>----------------------------------------------------------------------------------------
