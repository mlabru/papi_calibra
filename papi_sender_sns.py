#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
papi_sender_sns

PAPI sender sensors

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

# model
import model.sns_altimeter as salt
import model.sns_barometer as sbar
import model.sns_gps as sgps
import model.sns_thermometer as sthr

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# symbolic name meaning all available interfaces
M_UDP_HOST = "192.168.12.1"

# arbitrary non-privileged port
M_UDP_PORT = 1961

# tupla
M_UDP_ADDR = (M_UDP_HOST, M_UDP_PORT)

# serial port
M_SER_PORT = "/dev/ttyUSB0"

# serial baudrate
M_SER_BAUD = 115200

# keep running
G_KEEP_RUN = True

# -------------------------------------------------------------------------------------------------
def main():
    """
    REAL PROGRAM MAIN
    """
    # create read queue
    l_queue = Queue.Queue()
    assert l_queue

    # create serial read thread
    lthr_ser = threading.Thread(target=ser_read, args=(l_queue,))
    assert lthr_ser
    
    # start serial read thread
    lthr_ser.start()

    # create net sender thread
    lthr_net = threading.Thread(target=net_sender, args=(l_queue,))
    assert lthr_net

    # start net sender thread
    lthr_net.start()

    # aguarda as threads
    lthr_ser.join()
    lthr_net.join()

# -------------------------------------------------------------------------------------------------
def net_sender(f_queue):
    """
    net sender thread
    """
    # cria o soket
    l_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    assert l_sock

    # create altimeter
    l_altimeter = salt.CAltimeter(l_sock, M_UDP_ADDR)
    assert l_altimeter

    # create barometer
    l_barometer = sbar.CBarometer(l_sock, M_UDP_ADDR)
    assert l_barometer

    # create gps
    l_gps = sgps.CGPS(l_sock, M_UDP_ADDR)
    assert l_gps

    # create thermometer
    l_termometer = sthr.CThermometer(l_sock, M_UDP_ADDR)
    assert l_termometer

    # while keep running...
    while G_KEEP_RUN:
        # block until get message
        ls_msg = f_queue.get()

        # invalid ?
        if not ls_msg:
            # next message
            continue
 
        # split message
        llst_msg = ls_msg.split('#')
        # M_LOG.debug("llst_msg: {}".format(llst_msg))

        # mensagem de altímetro ?
        if "!@ALT" == llst_msg[0]:
            # send altimeter message (alt1, alt2, ts)
            l_altimeter.send_data(float(llst_msg[1]), float(llst_msg[2]), float(llst_msg[3]))

            # send gps message (lat, lng, alt, sats, hdop, ts) (SJC: 23.2237° S, 45.9009° W)
            l_gps.send_data(-23.22 - random.random(), -45.90 - random.random(), 540 + random.random(), 0, 0, float(llst_msg[3]))

        # mensagem de GPS ?
        elif "!@GPS" == llst_msg[0]:
            # send gps message (lat, lng, sats, hdop, ts)
            l_gps.send_data(float(llst_msg[1]), float(llst_msg[2]), int(llst_msg[3]), int(llst_msg[4]), float(llst_msg[5]))

        # mensagem de barômetro ?
        elif "!@BAR" == llst_msg[0]:
            # send barometer message (bar1, bar2, ts)
            l_barometer.send_data(float(llst_msg[1]), float(llst_msg[2]), float(llst_msg[3]))

        # mensagem de termômetro ?
        elif "!@THR" == llst_msg[0]:
            # send thermometer message (tmp1, tmp2, ts)
            l_termometer.send_data(float(llst_msg[1]), float(llst_msg[2]), float(llst_msg[3]))

    # fecha o socket
    l_sock.close()

# -------------------------------------------------------------------------------------------------
def ser_read(f_queue):
    """
    serial reader thread
    """
    # open serial port
    l_ser = serial.Serial(M_SER_PORT, M_SER_BAUD)
    assert l_ser

    # M_LOG.debug("l_ser: {}".format(l_ser))

    # while keep running...
    while G_KEEP_RUN:
        # read serial line        
        ls_line = l_ser.readline()
        # M_LOG.debug("ls_line: {}".format(ls_line))

        # read serial line and queue message
        f_queue.put(ls_line[:-2])

# -------------------------------------------------------------------------------------------------
# this is the bootstrap process

if "__main__" == __name__:

    # logger
    logging.basicConfig()

    # run application
    main()

# < the end >--------------------------------------------------------------------------------------
