#!/usr/bin/env python

from numpy import *
from scipy.io import write_array
from scipy.io import read_array
from read_array_pts import read_array_pts

def condVelocity(ptsFile, actFile):
    """
    Function to calculate the conduction velocity in a cable slab
    Input: ptsFile - description of the nodes
           actFile - file with activation time of the nodes
    Example:
            0 1 2 3 4 5 6 7 8
                A       B
    
    @author Bernardo Martins Rocha
    """
   
    xyz = read_array_pts(ptsFile)
    act = read_array(actFile)
    actTeste = act
       
    distA =   max(xyz[:,0]/4)
    distB = 3*max(xyz[:,0]/4)

    # node A
    tmp   = abs(xyz[:,0] - distA)
    tmpID = where(tmp == tmp.min())    # where return tuple
    aux   = tmpID[0][0] + 1
    nodeA = xyz[aux]
    actTI = where(act[:,0] == aux)     # activation time index

    if size(actTI) == 0:
        print " NodeA was not activated. CV is unknown!"
        return
    else:
        actTI = actTI[0][0]            # from tuple to scalar
        actTA = act[actTI , 1]         # activation time for node A
    
    # node B
    tmp   = abs(xyz[:,0] - distB)
    tmpID = where(tmp == tmp.min())    # where return tuple
    aux   = tmpID[0][0] + 1
    nodeB = xyz[aux]
    actTI = where(act[:,0] == aux)     # activation time index

    if size(actTI) == 0:
        print " NodeB was not activated. CV is unknown!"
        return
    else:
        actTI = actTI[0][0]            # from tuple to scalar
        actTB = act[actTI , 1]         # activation time for node B

    distAB = sqrt(sum(pow(nodeB - nodeA,2)))
    condve = distAB / (actTB - actTA)
        
    print " CV = %.3f m/s" % (condve/1000)
    return (condve/1000)
