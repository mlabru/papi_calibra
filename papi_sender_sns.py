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
import time

# model
import model.pc_data as gdata

import model.pc_sns_altimeter as salt
import model.pc_sns_barometer as sbar
import model.pc_sns_gps as sgps
import model.pc_sns_thermometer as sthr

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# degug mode
M_DEBUG = True

# -------------------------------------------------------------------------------------------------
def main():
    """
    REAL PROGRAM MAIN
    """
    # create read queue
    l_queue = Queue.Queue()
    assert l_queue

    # start application
    gdata.G_KEEP_RUN = True

    # debug mode ?
    if M_DEBUG:
        # fake client address 
        gdefs.D_NET_CLI = "192.168.11.151"

        # create serial read thread
        lthr_ser = threading.Thread(target=ser_fake, args=(l_queue,))
        assert lthr_ser

    # senão, real mode...
    else:    
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
    # create altimeter
    l_altimeter = salt.CAltimeter(None, gdefs.D_NET_CLI, gdefs.D_NET_PORT_ALT)
    assert l_altimeter

    # create barometer
    l_barometer = sbar.CBarometer(None, gdefs.D_NET_CLI, gdefs.D_NET_PORT_BAR)
    assert l_barometer

    # create gps
    l_gps = sgps.CGPS(None, gdefs.D_NET_CLI, gdefs.D_NET_PORT_GPS)
    assert l_gps

    # create thermometer
    l_termometer = sthr.CThermometer(None, gdefs.D_NET_CLI, gdefs.D_NET_PORT_THR)
    assert l_termometer

    # while keep running...
    while gdata.G_KEEP_RUN:
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
            if len(llst_msg) > 3:
                # send altimeter message (alt1, alt2, ts)
                l_altimeter.send_data(float(llst_msg[1]), float(llst_msg[2]), float(llst_msg[3]))

            # send gps message (lat, lng, alt, sats, hdop, ts) (SJC: 23.2237° S, 45.9009° W)
            l_gps.send_data(-23.22 - random.random(), -45.90 - random.random(), 540 + random.random(), 0, 0, float(llst_msg[3]))

        # mensagem de GPS ?
        elif "!@GPS" == llst_msg[0]:
            if len(llst_msg) > 5:
                # send gps message (lat, lng, sats, hdop, ts)
                l_gps.send_data(float(llst_msg[1]), float(llst_msg[2]), int(llst_msg[3]), int(llst_msg[4]), float(llst_msg[5]))

        # mensagem de barômetro ?
        elif "!@BAR" == llst_msg[0]:
            if len(llst_msg) > 3:
                # send barometer message (bar1, bar2, ts)
                l_barometer.send_data(float(llst_msg[1]), float(llst_msg[2]), float(llst_msg[3]))

        # mensagem de termômetro ?
        elif "!@THR" == llst_msg[0]:
            if len(llst_msg) > 3:
                # send thermometer message (tmp1, tmp2, ts)
                l_termometer.send_data(float(llst_msg[1]), float(llst_msg[2]), float(llst_msg[3]))

# -------------------------------------------------------------------------------------------------
def ser_fake(f_queue):
    """
    serial reader thread
    """
    # tempo ini
    ll_init = time.time()

    # altitude
    lf_alt = 0.

    # while keep running...
    while gdata.G_KEEP_RUN:
        # altitude
        lf_alt += 0.05

        # read serial line        
        ls_line = "!@ALT#{}#{}#{}".format(lf_alt + random.random(), lf_alt - random.random(), time.time() - ll_init)
        # M_LOG.debug("ls_line: {}".format(ls_line))

        # queue message
        f_queue.put(ls_line)

        # sleep
        time.sleep(0.5)

# -------------------------------------------------------------------------------------------------
def ser_read(f_queue):
    """
    serial reader thread
    """
    # open serial port
    l_ser = serial.Serial(gdefs.D_SER_PORT, gdefs.D_SER_BAUD)
    assert l_ser

    # M_LOG.debug("l_ser: {}".format(l_ser))

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
