#!/usr/bin/env python

import sys, gzip, pdb
from numpy import zeros
from igb.igb_header import igb_header
from igb.igb_read import *
from math import fabs

"""
File      : vm_diff
Input     : threshold value
Objective : plot the number of nodes where the error is bigger than the threshold value

Bernardo M. Rocha, 2008
"""

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print "\nUsage: vm_diff.py [thresholdValue]\n"
        exit(-1)
    
    threshold = float(sys.argv[1]) # in mV
    
    myIGBfile = "/home/rocha/src/data/vm_diff_200um.igb"
    [vm, hd] = read_igb_slice(myIGBfile)
    
    Vm = squeeze(vm)
    
    # sum up the number of nodes if the abs difference is greater than threshold    
    shp = shape(Vm)
    esum1 = zeros((shp[1]))
    esum2 = zeros((shp[1]))
    esum3 = zeros((shp[1]))
    esum4 = zeros((shp[1]))
    esum5 = zeros((shp[1]))
    threshold1 = 0.5
    threshold2 = 1.0
    threshold3 = 2.0
    threshold4 = 5.0
    threshold5 = 10.0
    
    
    for i in xrange(shp[1]):
        esum1[i] = 0
        esum2[i] = 0
        esum3[i] = 0
        esum4[i] = 0
        esum5[i] = 0
        for j in xrange(shp[0]):
            if (fabs(Vm[j,i]) > threshold1):
                esum1[i] += 1
            if (fabs(Vm[j,i]) > threshold2):
                esum2[i] += 1
            if (fabs(Vm[j,i]) > threshold3):
                esum3[i] += 1
            if (fabs(Vm[j,i]) > threshold4):
                esum4[i] += 1
            if (fabs(Vm[j,i]) > threshold5):
                esum5[i] += 1
    
    from pylab import *

    ft = float(shp[1])
    t  = arange(0.0, ft, 1.0)    
    plot(t, esum1, 'b-', t, esum2, 'r-', t, esum3, 'g-', t, esum4, 'y-',t, esum5, 'c-', lw=2)

    xlabel('time (ms)')
    ylabel('number of nodes')
    title('error as a function of time - threshold = 0.5 1 2 5 10 mV')
    grid(True)

    show()

