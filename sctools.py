#!/usr/bin/env python

from numpy import arange

def iseq(start=0, stop=None, inc=1):
    """
    Generate integer from start to (and including) stop
    with increment of inc. Alternative to range/xrange.
    """
    if stop == None:
        stop = start; start = 0; inc = 1
    return xrange(start, stop+inc, inc)

def sequence(start, stop, inc):
    """
    Generate float sequence from start to (and including) stop
    with increment of inc. Alternative to arange.
    """
    return arange(start, stop+inc, inc)