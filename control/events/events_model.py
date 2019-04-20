#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
events_model

generic event super class

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial version (Linux/Python)
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < class CEventsModel >---------------------------------------------------------------------------

class CEventsModel(object):
    """
    generic event super class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # init super class
        super(CEventsModel, self).__init__()

        # event name
        self.__s_name = "Generic Event"

    # ---------------------------------------------------------------------------------------------
    def __str__(self):
        """
        DOCUMENT ME!
        """
        return "<%s %s>" % (self.__class__.__name__, id(self))

    # ---------------------------------------------------------------------------------------------
    @property
    def s_name(self):
        """
        get event name
        """
        return self.__s_name

    @s_name.setter
    def s_name(self, f_val):
        """
        set event name
        """
        self.__s_name = f_val

# < the end >--------------------------------------------------------------------------------------
