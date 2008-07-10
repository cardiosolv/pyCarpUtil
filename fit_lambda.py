#!/usr/bin/env python

from pylab import *
from scipy.optimize import leastsq
from read_array_pts import *
from igb.read_igb_file import read_igb_slice

def fit_lambda(igb_file, pts_file, resolution=100):
    """
    Function to fit the space constant lambda
    Input: igb_file   - with Vm at each time slice
           pts_file   - file describing the mesh
           resolution - of the mesh
    """

    [vm, hd] = read_igb_slice(igb_file)    
    Vm = vm.squeeze()
       
    xyz  = read_array_pts(pts_file)
    ytmp = xyz[:,1]
    ztmp = xyz[:,2]
    size = len(xyz[:,1])

    # list with the nodes' indexes of the line
    aux = -resolution/2
    lindx = [i for i in xrange(size) if ytmp[i] == aux and ztmp[i] == aux]

    value1 = Vm[:,100]
    
    x     = zeros((len(lindx))) # space
    data  = zeros((len(lindx))) # vm at t=100ms    
    
    for i in lindx:
        x[i]     = xyz[i,0]
        data[i] = value1[i]
    
    def dbexpl(x,p):
        """
        Example of curve fitting for
        a*exp(-x/p1)
        """
        return( p[0]*exp(-(x+25000)/p[1]) + data[-1] )
    
    def residuals(p,data,x):
        err = data - dbexpl(x,p)
        return err
        
    ### vm curve fitting ###
    p0         = [10,1000]                                          # initial guesses
    guessfit   = dbexpl(x,p0)                                       # data evaluated with p0
    pbest      = leastsq(residuals,p0,args=(data,x),full_output=1)  # minimize the sum of squares of a set of equations
    bestparams = pbest[0]                                           # solution (estimated parameters)
    cov_x      = pbest[1]                                           # estimate of the covariance matrix of the solution
    
    print ' best fit parameters ',bestparams
    #print cov_x
    
    datafit = dbexpl(x,bestparams)
    plot(x,data,'b',x,datafit,'r')
    legend(['Vm(x,t=100ms)','fitting'], 'upper right')
    xlabel('Time')
    title('Space constant ''$\lambda$'' fitting')
    grid(True)
    show()

def main():
    
    #igb_file = '/data/sim/space_constant/sc_ucla_long_0100um/vm.igb'
    #pts_file = '/data/sim/space_constant/sc_ucla_long_0100um/sc_ucla_long_t0100um_i.pts'
    
    #igb_file = '/data/sim/space_constant/sc_ucla_trans_0100um/vm.igb'
    #pts_file = '/data/sim/space_constant/sc_ucla_trans_0100um/sc_ucla_trans_t0100um_i.pts'
    
    igb_file = '/data/sim/space_constant/sc_ucla_slow_0100um/vm.igb'
    pts_file = '/data/sim/space_constant/sc_ucla_slow_0100um/sc_ucla_slow_t0100um_i.pts'
    
    fit_lambda(igb_file, pts_file, resolution=100)
    
if __name__ == "__main__":
    main()
    