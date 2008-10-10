#!/usr/bin/env python

from numpy import *
from scipy import *
from pylab import *

"""
Input     : file list - each file is a x y vectors as columns
Objective : plot a curve where the number of nodes where the error is bigger
            than the threshold value for each file in the file list 

Bernardo M. Rocha, 2008
"""

if __name__ == "__main__":

    in_args = sys.argv[1:]
    in_args_len = len(in_args)
    
    # read data
    xyData = []
    for file in in_args:
        xyData.append(loadtxt(file))
    
    # plot data
    for data in xyData:
        t = data[:,0]
        e = data[:,1]        
        plot(t, e, lw=2)


    legend(in_args, loc=2)
    xlabel('time (ms)')
    ylabel('L2 norm')
    #title('quad-tri at 50um - threshold 1 mV')
    grid(True)

    show()

