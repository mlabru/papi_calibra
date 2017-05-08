#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
kalman

implements a multi-variable linear Kalman filter

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
import math
import random
import socket
import time

# numPy
import numpy as np

# kalman
import kalman_filter_linear as kfl

# < module data >----------------------------------------------------------------------------------

# symbolic name meaning all available interfaces
UDP_HOST = "192.168.12.1"

# arbitrary non-privileged port
UDP_PORT = 1961

# tupla
UDP_ADDR = (UDP_HOST, UDP_PORT)

# biases
BIAS1 = +1.
BIAS2 = -1.

# -------------------------------------------------------------------------------------------------
def main():
    """
    REAL PROGRAM START
    """
    # how many sensors ?
    li_sensors = 2
    
    # how many iterations should the simulation run for ?
    # (notice that the full journey takes 14.416 seconds, so 145 iterations will
    # cover the whole thing when timeslice = 0.10)
    # li_iterations = 1000

    # these are arrays to store the data points we want to plot at the end

    # sensors
    llst_ns1 = []
    llst_ns2 = []

    # kalman state
    llst_ks = []

    # state transition model
    l_A = np.matrix([[1.]])

    # control matrix
    l_B = np.matrix([[0.]])

    # control vector
    l_u = np.matrix([[0.]])

    # observation matrix is the identity matrix, since we can get direct
    # measurements of all values in our example
    l_H = np.ones((li_sensors, 1))
    # print "l_H:", l_H, l_H.shape

    # initial covariance estimate
    l_P = np.ones(1)
    
    # process noise covariance (estimated error in process)
    l_Q = np.matrix([[0.005]])

    # measurement noise covariances (estimated error in measurements)
    l_R = np.eye(li_sensors) * 0.64
    # print "l_R:", l_R, l_R.shape

    # initial guess
    l_x = [[0.]]

    # create Kalman filter
    l_kf = kfl.CKalmanFilterLinear(l_A, l_B, l_H, l_x, l_P, l_Q, l_R)
    assert l_kf

    # cria o soket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    assert sock

    # get initial time
    lf_ini = time.time()

    # iterate through the simulation
    while True:
        # measurements
        lf_alt1 = BIAS1 + 20 + math.sqrt(0.64) * np.random.randn()
        lf_alt2 = BIAS2 + 20 + math.sqrt(0.64) * np.random.randn()

        # save kalman state
        l_ks = l_kf.get_current_state()

        # list ?
        if list == type(l_ks):
            lf_ks = l_ks[0][0]

        # senão, matrix
        else:
            lf_ks = l_ks[0, 0]            

        # get time stamp
        lf_ts = time.time() - lf_ini

        # build string data
        ls_data = "{}#{}#{}#{}".format(lf_ts, lf_alt1, lf_alt2, lf_ks)

        # envia a string
        sock.sendto("101#114#{}".format(ls_data), UDP_ADDR)

        # step. control vector, measurement_vector
        l_kf.step(l_u, np.matrix([[lf_alt1], 
                                  [lf_alt2]]))

        time.sleep(1)

    # fecha o socket
    sock.close()

# -------------------------------------------------------------------------------------------------
# this is the bootstrap process

if "__main__" == __name__:

    # logger
    logging.basicConfig()

    # multiprocessing logger
    # multiprocessing.log_to_stderr()

    # run application
    main()

# < the end >--------------------------------------------------------------------------------------
