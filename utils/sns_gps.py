#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
sns_gps

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

# numPy
# import numpy as np

# kalman
# import kalman_filter_linear as kfl

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------
class CGPS(object):
    """
    gps class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_sock, ft_client):
        """
        constructor
        """
        # check input
        assert f_sock
        assert ft_client

        # save socket
        self.__sock = f_sock
        
        # save client tuple
        self.__t_client = ft_client
        '''
        # how many sensors ?
        li_sensors = 2
        
        # state transition model
        l_A = np.matrix([[1.]])

        # control matrix
        l_B = np.matrix([[0.]])

        # control vector
        self.__u = np.matrix([[0.]])

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
        self.__kf = kfl.CKalmanFilterLinear(l_A, l_B, l_H, l_x, l_P, l_Q, l_R)
        assert self.__kf
        '''
    # ---------------------------------------------------------------------------------------------
    def send_data(self, lf_lat, lf_lng, li_sats, li_hdop, lf_ts):
        """
        send gps data
        """
        # build string data
        ls_data = "{}#{}#{}#{}#{}".format(lf_ts, lf_lat, lf_lng, li_sats, li_hdop)

        # envia a string
        self.__sock.sendto("101#115#{}".format(ls_data), self.__t_client)

    # ---------------------------------------------------------------------------------------------
    def send_kf(self, lf_lat, lf_lng, lf_ts):
        """
        send gps data
        """
        '''
        # save kalman state
        l_ks = self.__kf.get_current_state()

        # list ?
        if list == type(l_ks):
            lf_ks = l_ks[0][0]

        # senão, matrix
        else:
            lf_ks = l_ks[0, 0]            

        # build string data
        ls_data = "{}#{}#{}#{}".format(lf_ts, lf_lat, lf_lng, lf_ks)

        # envia a string
        self.__sock.sendto("101#114#{}".format(ls_data), self.__t_client)

        # step. control vector, measurement_vector
        self.__kf.step(self.__u, np.matrix([[lf_lat], 
                                            [lf_lng]]))
        '''
# < the end >--------------------------------------------------------------------------------------
