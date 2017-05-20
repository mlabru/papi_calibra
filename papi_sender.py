#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
papi_sender

PAPI sender

revision 0.1  2017/abr  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/04"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import Queue
import random
import serial
import socket
import threading
import time

# numPy
import numpy

# openCV
import cv2
import cv2.cv as cv

# model
import model.pc_data as gdata

import model.pc_sns_altimeter as salt
import model.pc_sns_barometer as sbar
import model.pc_sns_gps as sgps
import model.pc_sns_thermometer as sthr

# control
import control.pc_defs as gdefs
import control.pc_setup as gcfg

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------
def main():
    """
    REAL PROGRAM MAIN
    """
    # load config
    gcfg.load_setup("papical.cfg")

    # create read queue
    l_queue = Queue.Queue()
    assert l_queue

    # start application
    gdata.G_KEEP_RUN = True

    # create sender camera thread
    lthr_cam = threading.Thread(target=send_cam, args=(l_queue,))
    assert lthr_cam

    # start sender camera thread
    lthr_cam.start()

    # debug mode ?
    if gdata.G_DCT_CONFIG["glb.debug"]:
        # import fake serial
        import ser_fake as sfk

        # fake gcs address 
        gdata.G_DCT_CONFIG["net.gcs"] = "192.168.11.101"

        # create serial read thread
        lthr_ser = threading.Thread(target=sfk.ser_fake, args=(l_queue,))
        assert lthr_ser

    # senão, real mode...
    else:    
        # create serial read thread
        lthr_ser = threading.Thread(target=ser_read, args=(l_queue,))
        assert lthr_ser
    
    # start serial read thread
    lthr_ser.start()

    # create sender sensors thread
    lthr_sns = threading.Thread(target=send_sensors, args=(l_queue,))
    assert lthr_sns

    # start sender sensors thread
    lthr_sns.start()

    # aguarda as threads
    lthr_cam.join()
    lthr_ser.join()
    lthr_sns.join()

# -------------------------------------------------------------------------------------------------
def send_cam(f_queue):
    """
    sender camera thread
    """
    # tupla network address
    lt_udp_addr = (gdata.G_DCT_CONFIG["net.gcs"], gdata.G_DCT_CONFIG["net.img"])

    # cria o soket
    l_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    assert l_sock

    # inicia a captura do vídeo
    l_capture = cv2.VideoCapture(0)
    assert l_capture

    l_capture.set(cv.CV_CAP_PROP_FRAME_WIDTH, gdefs.D_VID_HORZ)
    l_capture.set(cv.CV_CAP_PROP_FRAME_HEIGHT, gdefs.D_VID_VERT)

    # para todo o sempre...
    while gdata.G_KEEP_RUN:
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
        # print len(l_stringData)

        # tamanho da imagem excede o tamanho máximo de UDP ?
        if len(l_stringData) > 65507:
            # logger
            l_log = logging.getLogger("papi_sender::send_cam")
            l_log.setLevel(logging.WARNING)
            l_log.warning(u"<E01: message too long: {}".format(len(l_stringData))

            # descarta a mensagem 
            continue
        
        # header
        ls_header = "{}#{}#".format(gdefs.D_MSG_VRS, gdefs.D_MSG_IMG)

        # envia o tamanho da string 
        l_sock.sendto("{}#{}#{}".format(gdefs.D_MSG_VRS, gdefs.D_MSG_SIZ, len(ls_header) + len(l_stringData)), lt_udp_addr)
        # envia a string
        l_sock.sendto("{}{}".format(ls_header, l_stringData), lt_udp_addr)

    # fecha o socket
    l_sock.close()

# -------------------------------------------------------------------------------------------------
def send_sensors(f_queue):
    """
    sender sensors thread
    """
    # create altimeter
    l_alt = salt.CAltimeter(None, gdata.G_DCT_CONFIG["net.gcs"], gdata.G_DCT_CONFIG["net.alt"])
    assert l_alt

    # create barometer
    l_bar = sbar.CBarometer(None, gdata.G_DCT_CONFIG["net.gcs"], gdata.G_DCT_CONFIG["net.bar"])
    assert l_bar

    # create gps
    l_gps = sgps.CGPS(None, gdata.G_DCT_CONFIG["net.gcs"], gdata.G_DCT_CONFIG["net.gps"])
    assert l_gps

    # create thermometer
    l_thr = sthr.CThermometer(None, gdata.G_DCT_CONFIG["net.gcs"], gdata.G_DCT_CONFIG["net.thr"])
    assert l_thr

    # while keep running...
    while gdata.G_KEEP_RUN:
        # block until get message
        ls_msg = f_queue.get()

        # invalid ?
        if not ls_msg:
            # logger
            l_log = logging.getLogger("papi_sender::send_sensors")
            l_log.setLevel(logging.WARNING)
            l_log.warning(u"<E01: queue empty.")

            # next message
            continue
 
        # split message
        llst_msg = ls_msg.split('#')
        # M_LOG.debug("llst_msg: {}".format(llst_msg))

        try:
            # mensagem de altímetro ?
            if "!@ALT" == llst_msg[0]:
                if len(llst_msg) > 3:
                    # send altimeter message (alt1, alt2, ts)
                    l_alt.send_data(float(llst_msg[1]), float(llst_msg[2]), float(llst_msg[3]))

            # mensagem de GPS ?
            elif "!@GPS" == llst_msg[0]:
                if len(llst_msg) > 5:
                    # send gps message (lat, lng, sats, hdop, ts)
                    l_gps.send_data(float(llst_msg[1]), float(llst_msg[2]), int(llst_msg[3]), int(llst_msg[4]), float(llst_msg[5]))

            # mensagem de barômetro ?
            elif "!@BAR" == llst_msg[0]:
                if len(llst_msg) > 3:
                    # send barometer message (bar1, bar2, ts)
                    l_bar.send_data(float(llst_msg[1]), float(llst_msg[2]), float(llst_msg[3]))

            # mensagem de termômetro ?
            elif "!@THR" == llst_msg[0]:
                if len(llst_msg) > 3:
                    # send thermometer message (tmp1, tmp2, ts)
                    l_thr.send_data(float(llst_msg[1]), float(llst_msg[2]), float(llst_msg[3]))

        # em caso de erro...
        except Exception as l_err:
            # logger
            l_log = logging.getLogger("papi_sender::send_sensors")
            l_log.setLevel(logging.WARNING)
            l_log.warning(u"<E02: send data error: {}".format(l_err))
             
# -------------------------------------------------------------------------------------------------
def ser_read(f_queue):
    """
    serial reader thread
    """
    # open serial port
    l_ser = serial.Serial(gdata.G_DCT_CONFIG["ser.port"], gdata.G_DCT_CONFIG["ser.baud"])
    assert l_ser

    # while keep running...
    while gdata.G_KEEP_RUN:
        # read serial line        
        ls_line = l_ser.readline()
        # M_LOG.debug("ls_line: {}".format(ls_line))

        # queue message
        f_queue.put(ls_line[:-2])

# -------------------------------------------------------------------------------------------------
# this is the bootstrap process

if "__main__" == __name__:

    # logger
    logging.basicConfig()

    # run application
    main()

# < the end >--------------------------------------------------------------------------------------
