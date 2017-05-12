#!/usr/bin/env python
# -*- coding: utf-8 -*-

# < imports >--------------------------------------------------------------------------------------

# python library
import socket

# numPy
import numpy

# openCV
import cv2
import cv2.cv as cv

# < module data >----------------------------------------------------------------------------------

# symbolic name meaning all available interfaces
UDP_HOST = "192.168.12.1"

# arbitrary non-privileged port
UDP_PORT = 1970

# tupla
UDP_ADDR = (UDP_HOST, UDP_PORT)

# -------------------------------------------------------------------------------------------------

# cria o soket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
assert sock

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
    
    # envia o tamanho da string 
    sock.sendto("101#111#{}".format(len(stringData) + 8), UDP_ADDR)
    # envia a string
    sock.sendto("101#112#{}".format(stringData), UDP_ADDR)

    # converte de string para imagem
    # data = numpy.fromstring(stringData, dtype="uint8")
        
    # decimg = cv2.imdecode(data, 1)
    # cv2.imshow("SEND...", decimg)

    # press q to quit
    # if cv2.waitKey(1) & 0xFF == ord('q'):
        # break
    
# fecha o socket
sock.close()

#cv2.waitKey(0)
#cv2.destroyAllWindows()

# <the end>----------------------------------------------------------------------------------------
