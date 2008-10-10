#!/usr/bin/env python

import sys
from os import remove
from numpy import arange, loadtxt
from scipy.io import write_array
from scipy.io import read_array

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

def read_array_pts(ptsFile):
    """
    Function to read a .pts file from CARP simulator, where the first line contains
    the number of nodes and the remaining file contains the array of nodes
    
    Example of usage:
    from sctools import read_array_pts
    nn, narray = read_array_pts("t0010um_i.pts")
    print nn
    print narray[:,0]
    print narray[:,1]
    print narray[:,2]
    
    Bernardo Martins Rocha, 2008
    """
    try:
        f = open(ptsFile)
        lines = f.readlines()
        f.close()
    except IOError:
        print "IOError: File %s not found." % ptsFile
        sys.exit(-1)
    
    # number of nodes
    numNodes = int(lines[0]); del lines[0]
    nodesTmp = "mytemp.txt"

    try:
        fnew = open(nodesTmp,"w")
        for i in lines:
            fnew.write(i)
        fnew.close()
    except IOError:
        print "IOError: File %s not found." % ptsFile
        exit(-1)

    # numpy array of nodes
    nodes = loadtxt(nodesTmp)
    
    if(numNodes != len(nodes)):
        print " error read_array_pts(): the size of the array doesn't match"
        exit(-2)
    
    remove(nodesTmp)
            
    return nodes