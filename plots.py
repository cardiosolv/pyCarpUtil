#!/usr/bin/env python

import os, sys
import numpy, scipy
from pylab import *
from fit_lambda import fit_lambda
from condVelocity import condVelocity

if __name__ == "__main__":
    
    # declarations
    space_const = (894.42214823, 312.15803892, 79.11666987)
    resArray    = (10,25,50,100,200,250,500,750,1000)    
    dirs = ('cgtol_1e-6/experiment_ucla_long/cable-hexa/',
            'cgtol_1e-6/experiment_ucla_trans/cable-hexa/',
            'cgtol_1e-6/experiment_ucla_slow/cable-hexa/')
    
    # filling cvArray
    arrSize = len(resArray)
    cvArray = numpy.zeros((arrSize,len(dirs)+1))
    for i in xrange(arrSize):
        cvArray[i][0] = resArray[i]

    # main loop
    i = 1
    for d in dirs:
        os.chdir(d)
        print " >> %s " % d
        j = 0
        for r in resArray:
            sim    = "t%04dum" % r
            simPts = sim + "/" + sim + "_i.pts"
            simAct = sim + "/" + "activation-thresh.dat"
                        
            if (os.path.isfile(simPts) != True):
                print " error calculateCV: file %s not found" + simPts
                exit(-1)
            
            if (os.path.isfile(simAct) != True):
                print " error calculateCV: file %s not found" + simAct
                exit(-1)
            
            ## calculate
            cv = condVelocity(simPts, simAct)
            cvArray[j][i] = cv
            j = j + 1           
        os.chdir("../../../")
        i = i + 1
       
    x1 = cvArray[:,0]/space_const[0]
    x2 = cvArray[:,0]/space_const[1]
    x3 = cvArray[:,0]/space_const[2]

    y1 = cvArray[:,1]/cvArray[0,1]
    y2 = cvArray[:,2]/cvArray[0,2]
    y3 = cvArray[:,3]/cvArray[0,3]
                    
    plot(x1, y1, linewidth=1.0)
    plot(x2, y2, linewidth=1.0)
    plot(x3, y3, linewidth=1.0)
        
    legend(('longitudinal', 'transverse', 'slow decremental'), 'upper right')
    xlabel('dx(um)')
    ylabel('velocity (m/s)')   
    title('teste')
    grid(True)
    show()

    

