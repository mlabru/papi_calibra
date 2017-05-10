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
import serial
import socket
import threading

# papi_calibra
import sns_altimeter as salt

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
M_SER_BAUD = 9600

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

    # create and start serial read thread
    threading.Thread(target=ser_read, args=(l_queue,)).start()

    # create and start net sender thread
    lthr_net = threading.Thread(target=net_sender, args=(l_queue,)).start()

    # aguarda as threads
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

    # while keep running...
    while G_KEEP_RUN:
        # block until get message
        ls_msg = f_queue.get()
 
        # split message
        llst_msg = ls_msg.split('#')
        M_LOG.debug("llst_msg: {}".format(llst_msg))

        # mensagem de altímetro ?
        if "!@ALT" == llst_msg[0]:
            # send altimeter message
            l_altimeter.send_data(float(llst_msg[1]), float(llst_msg[2]), float(llst_msg[3]))

        # mensagem de barômetro ?
        #elif "!@PRS" == llst_msg[0]:
            # send barometer message
            #l_barometer.send_data(llst_msg[1], llst_msg[2], llst_msg[3])

        # mensagem de termômetro ?
        #elif "!@TMP" == llst_msg[0]:
            # send termometer message
            #l_termometer.send_data(llst_msg[1], llst_msg[2], llst_msg[3])

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

    M_LOG.debug("l_ser: {}".format(l_ser))

    # while keep running...
    while G_KEEP_RUN:
        # read serial line        
        ls_line = l_ser.readline()
        M_LOG.debug("ls_line: {}".format(ls_line))

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
