#!/usr/bin/env python

import sys, pdb, os
import numpy as np
from pylab import *
from pyUtils.carptools.Solution import Solution

""" 
Attention:
This script depends on:
    - FiPY
    - pysparse
"""

if __name__ == "__main__":

    np.set_printoptions(precision=5)
    np.set_printoptions(threshold=100000)
    
    dataPrefix = '/data/sim/simulacao_3/'

    tr_name = ['tri_160um','tri_80um','tri_40um', 'tri_20um', 'tri_10um']
    qd_name = ['qua_160um','qua_80um','qua_40um', 'qua_20um', 'qua_10um']
    qb_name = ['qua_iso_160um','qua_iso_80um','qua_iso_40um', 'qua_iso_20um', 'qua_iso_10um']

    m    = len(tr_name) - 1
    h    = np.array([160,80,40,20])
    time = np.array([8])

    E2t = np.zeros(m)
    E2q = np.zeros(m)
    E2i = np.zeros(m)
    EM  = np.zeros(m)
    DOF = np.zeros(m)

    # reference solutions
    triRef = Solution('/data/sim/simulacao_3/tri_10um/tri_10um')
    quaRef = Solution('/data/sim/simulacao_3/qua_10um/qua_10um')
    quaisoRef = Solution('/data/sim/simulacao_3/qua_iso_10um/qua_iso_10um')

    # convergence for triangle
    for t in xrange(len(time)):
        for i in xrange(m):
            solname = os.path.join(dataPrefix + tr_name[i], tr_name[i])
            triSol  = Solution(solname)
            E2t[i]  = triSol.getL2NormError(triRef, time[t])
            DOF[i]  = triSol.getNumberOfNodes()

        print 'Tr ', E2t

    # convergence for quadrangle (hybrid approach)
    for t in xrange(len(time)):
        for i in xrange(m):
            solname = os.path.join(dataPrefix + qd_name[i], qd_name[i])
            quaSol  = Solution(solname)
            E2q[i]  = quaSol.getL2NormError(quaRef, time[t])
            DOF[i]  = quaSol.getNumberOfNodes()

        print 'Qd ', E2q

    # convergence for isoparametric quadrangle
    for t in xrange(len(time)):
        for i in xrange(m):
            solname = os.path.join(dataPrefix + qb_name[i], qb_name[i])
            quiSol  = Solution(solname)
            E2i[i]  = quiSol.getL2NormError(quaisoRef, time[t])
            DOF[i]  = quiSol.getNumberOfNodes()
            
        print 'Qb ', E2i


    # plot log|h| versus log||err||

    plot(np.log(h) , -np.log(E2t) , '-^', color='red')
    plot(np.log(h) , -np.log(E2q) , '-s', color='blue')
    plot(np.log(h) , -np.log(E2i) , '-s', color='green')

    xlabel('log(h)')
    ylabel('-log ||$err_{0}$||')

    legend(('triangles', 'quadrangles (Macro)', 'quadrangles (Isopar)'), loc='upper right')

    grid()

    # plot log|ndof| verus log||err||
    
    #plot(np.log(DOF) , -np.log(E2t) , '-^', color='red',  label='triangles')
    #plot(np.log(DOF) , -np.log(E2q) , '-s', color='blue', label='quadrangles (Hybrid)')
    #plot(np.log(DOF) , -np.log(E2i) , '-s', color='green', label='quadrangles (Isopar)')

    #xlabel('log NDofs')
    #ylabel('-log ||$err_{0}$||')

    #legend(('triangles', 'quadrangles (Macro)', 'quadrangles (Isopar)'), loc='upper left')

    ###
    
    title('CARP - Finite element discretization errors')
    show()
    
# end of main
