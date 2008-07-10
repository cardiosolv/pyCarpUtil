#!/usr/bin/env python

"""
Function to read a .pts file from CARP simulator, where the first line contains
the number of nodes and the remaining file contains the array of nodes

@author Bernardo Martins Rocha
"""

from numpy import *
from scipy.io import write_array
from scipy.io import read_array
  
#from read_array_pts import read_array_pts
#nn, narray = read_array_pts("t0010um_i.pts")
#print nn
#print narray[:,0]
#print narray[:,1]
#print narray[:,2]    

def read_array_pts(ptsFile):
    try:
        f = open(ptsFile)
        lines = f.readlines()
        f.close()
    except IOError:
        print "IOError: File %s not found." % ptsFile
        exit(-1)
    
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
        print " error read_array_pts(): the size of the arrays doesn't match"
        exit(-2)
    
    from os import remove
    remove(nodesTmp)
            
    return nodes
