#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ser_fake

serial fake

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

revision 0.1  2019/fev  mlabru
initial release (Linux/Python)
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2019/02"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import random
import time

# papi
import model.pc_data as gdata

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------
def ser_fake(f_queue):
    """
    serial reader thread
    """
    # tempo ini
    ll_init = time.time()

    # altitude
    lf_alt = 0.

    # posição
    lf_lat = 0.
    lf_lng = 0.

    # barômetro
    lf_bar = 0.

    # termômetro
    lf_thr = 0.

    # while keep running...
    while gdata.G_KEEP_RUN:
        # altitude
        lf_alt += 0.05

        # read serial line        
        ls_line = "!@ALT#{}#{}#{}".format(lf_alt + random.random(), lf_alt - random.random(), time.time() - ll_init)
        # M_LOG.debug("ls_line: {}".format(ls_line))

        # queue message
        f_queue.put(ls_line)

        # posição
        lf_lat += 0.05
        lf_lng += 0.05

        # read serial line        
        ls_line = "!@GPS#{}#{}#{}#{}#{}#{}".format(lf_lat + random.random(), lf_lng - random.random(), lf_alt + random.random(), 12, 55, time.time() - ll_init)
        # M_LOG.debug("ls_line: {}".format(ls_line))

        # queue message
        f_queue.put(ls_line)

        # barômetro
        lf_bar += 0.05

        # read serial line        
        ls_line = "!@BAR#{}#{}#{}".format(lf_bar + random.random(), lf_bar - random.random(), time.time() - ll_init)
        # M_LOG.debug("ls_line: {}".format(ls_line))

        # queue message
        f_queue.put(ls_line)

        # termômetro
        lf_thr += 0.05

        # read serial line        
        ls_line = "!@THR#{}#{}#{}".format(lf_thr + random.random(), lf_thr - random.random(), time.time() - ll_init)
        # M_LOG.debug("ls_line: {}".format(ls_line))

        # queue message
        f_queue.put(ls_line)

        # sleep
        time.sleep(0.5)

# < the end >--------------------------------------------------------------------------------------
