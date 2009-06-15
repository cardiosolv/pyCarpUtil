#!/usr/bin/env python

import os, sys,pdb
import numpy as np
from math import *
from pylab import *
from pyUtils.carptools.Solution import Solution

class DataSet():
    """
    This class holds the set of refined solutions to compute the convergence.
    File format example:
    2 5 
    hex /data/resultsHex
    tet /data/resultsTet
    10 20 30 40 50
    """
    def __init__(self, filename, size=1, levels=1):

        self.size = size
        self.levels = levels

        self.dofs = [] # degrees of freedom 
        self.lbls = [] # labels
        self.dirs = [] # data directories
        
        self.readDataSetFile(filename)

    def __str__(self):
        tstr  = "\n objsize=%d lvls=%d\n" % (self.size, self.levels)
        tstr += "lbls=%s\n" % (self.lbls)
        tstr += "dirs=%s\n" % (self.dirs)
        tstr += "dofs=%s\n" % (self.dofs)
        return tstr

    def readDataSetFile(self, filename):
        f = open(filename,"r")
        t = f.readline().split()
        
        self.size = int(t[0])
        self.levels = int(t[1])

        for i in xrange(self.size):
            l = f.readline().split()
            self.lbls.append(l[0])
            self.dirs.append(l[1])

        for i in xrange(self.levels):
            l = f.readline().split()
            self.dofs.append(int(l[0]))

        f.close()               

# end of class DataSet

def evalExactSolution(exactStr, x, y, z):
    """
    Compute exact solution u(x,y,z) of the problem -a \nabla u = f(x,y)
    where f(x,y) = a*sin(pi*x)*sin(pi*y) given an string to evaluate
    the exact solution using eval.
    
    Note: use numpy arrays for vectorized operations
    Example: exactStr = 'np.sin(pi*x)' 
    """
    result = eval(exactStr)
    return result

# end of evalExactSolution

def calcPoissonError (solname, outputdir, exactsol):

    # get aproximated solution at each node
    sol = Solution(solname, outdir=outputdir)
    uh = sol.getPhie()[0,:] 

    # compute exact solution at each node
    ue = np.zeros((np.shape(uh)[0]),dtype='float32') # exact u
    lM = sol.getLumpedMassMatrixE()                  # lumped Mass
    mesh = sol.getNodes()   
    X = mesh[:,0]
    Y = mesh[:,1]
    Z = mesh[:,2]
    ue = evalExactSolution(exactsol, X, Y, Z)   

    # compute nodal error
    err = ue - uh

    # compute the L2 norm of the error
    normeu = sol.calcL2NormError(err, lM)
    return normeu

def plotSolution(ue, uh):
    ueshp = np.shape(ue)[0]
    numNodesX = int( sqrt(ueshp) )
    numNodesY = int( sqrt(ueshp) )
    uenew = np.reshape(ue, (numNodesX,numNodesY))
    uhnew = np.reshape(uh, (numNodesX,numNodesY))

    ax = subplot(211)
    im = imshow(uenew, cmap=cm.jet)
    im.set_interpolation('bilinear')
    title('Exact solution')
    colorbar()

    ax = subplot(212)
    im = imshow(uhnew, cmap=cm.jet)
    im.set_interpolation('bilinear')
    title('Aproximated solution')
    colorbar()
    
    show()

def calcConvergence(dataset, exactstr):

    m = len(dataset.dofs)
    E = np.zeros(m)
    H = np.zeros(m)
    N = np.array(dataset.dofs)

    # for quadrangles - gambiarra
    T = np.array([25.0,100.0,400.0,1600.0,6400.0,25600.0])

    for l in xrange(len(dataset.lbls)):
        label = dataset.lbls[l]
        for i in xrange(m):
            solname = '%s%s' % (dataset.dirs[l], dataset.dofs[i])
            outputd = os.path.basename(dataset.dirs[l]) + str(dataset.dofs[i])
       
            E[i] = calcPoissonError(solname, outputd, exactstr)
        
            if label == 'Triangles':
                H[i] = sqrt(1.0/T[i]) * sqrt(2)
            else:
                H[i] = sqrt(1.0/T[i])               

        plotConvergenceResults (H, E, label)
        printConvergenceResults(N, H, E)

    title('Convergence for Poisson problem')
    grid()
    show()

# end of calcConvergence2D
 
def printConvergenceResults(N, H, E):
    print '\n'
    print ' NDOFs\t  h\t\t ||u-uh||\t ||u-uh||/h*h\n'
    for i in xrange(len(N)):
        print '%5d\t %8.3e\t %8.3e\t %8.3e ' % (N[i],H[i],E[i],(E[i]/(H[i]*H[i])) )

    print ''
  
# end of printConvergenceResults

def plotConvergenceResults(H, E, elabel):
    xlabel('$\log{h}$')
    ylabel('$-\log{||e||_{0}}$')

    if elabel == 'Triangles' or elabel == 'Tetrahedra':
        plot(np.log(H), -np.log(E), '-^', label= elabel)
        #plot(H, E, '-^', label= elabel)
    else:
        plot(np.log(H), -np.log(E), '-s', label= elabel)
        #plot(H, E, '-^', label= elabel)
    legend(loc='upper right')

# end of plotConvergenceResults

def main(args):

    # setup data
    d = DataSet(args[0])

    # print some known exact functions
    print "Exact solutions:"
    print " \"1.0/(2.0*pi*pi)*np.sin(pi*x)*np.sin(pi*y)\""
    print " \"1.0/(3.0*pi*pi)*np.sin(pi*x)*np.sin(pi*y)*np.sin(pi*z)\""
    print ""

    # read exact solution from input
    try:
        exact = input("Enter the exact solution (enclosed in quotes): ")
    except:
        print " Error during the input of exact solution."; sys.exit(1);
    
    calcConvergence(d, exact)  

# end of main

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "\n Usage: python calcPoissonError <DATA_SET_FILE> \n"
        sys.exit(1)

    main(sys.argv[1:])

    
            
