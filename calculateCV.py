#!/usr/bin/env python

import os, sys
from pylab import *
from numpy import zeros
from os import getcwd
from condVelocity import condVelocity
import pdb

def printUsage():
    usage  = "  >> Usage: python calculateCV.py <OPTIONS>\n"
    usage += "  >> Description:\n\n"
    usage += "\t -d <experiment_directory>\t directory containing the results of the experiments for different resolutions\n"
    usage += "\t -m <ionic_model>         \t name of the ionic model (ucla-long, ucla-slow, ucla-trans, tt2-long, ..., lr2f-long) \n"
    usage += "\t -r <one_value_resolution>\t the resolution you want to compute the conduction velocity\n"
    usage += "\t --save\t\t\t\t if you want to save a file with data\n"
    print usage

if __name__ == "__main__":
    
    # variables
    saveFile  = False
    directory = ""
    dirList   = ("cable-hexa","cable-tetra")
    resArray  = (10,25,50,100,200,250,500,750,1000)
    resValue  = -1

    lambDict  = {'ucla-long'  : 894.42214823,
                 'ucla-trans' : 312.15803892,
                 'ucla-slow'  : 79.11666987 ,
                 'tt2-long'   : 919.34206339,
                 'tt2-trans'  : 313.74227759,
                 'tt2-slow'   : 80.07370971 , 
                 'lr2f-long'  : 669.32099569,
                 'lr2f-trans' : 225.82278861,
                 'lr2f-slow'  : 59.50694777 }
    
    titleDict = {'ucla-long'  : 'Longitudinal (UCLA_RAB)',
                 'ucla-trans' : 'Transverse (UCLA_RAB)',
                 'ucla-slow'  : 'Slow decremental (UCLA_RAB)',
                 'tt2-long'   : 'Longitudinal (TT2)',
                 'tt2-trans'  : 'Transverse (TT2)',
                 'tt2-slow'   : 'Slow decremental (TT2)',
                 'lr2f-long'  : 'Longitudinal (LRII_F)',
                 'lr2f-trans' : 'Transverse (LRII_F)',
                 'lr2f-slow'  : 'Slow decremental (LRII_F)'}
    
    # usage
    while len(sys.argv) == 1:
        printUsage()
        sys.exit(1)

    # read variables from the command line
    while len(sys.argv) > 1:
        option = sys.argv[1];              del sys.argv[1]
        if   option == '-d':
            directory = sys.argv[1];       del sys.argv[1]
        elif option == '-r':
            resValue  = int(sys.argv[1]);  del sys.argv[1]
        elif option == '-m':
            model     = sys.argv[1];       del sys.argv[1]            
        elif option == '--save':
            saveFile  = True
        else:
            print sys.argv[0],': invalid option',option
            sys.exit(1)

    # change to experiment_directory
    os.chdir(directory)

    if resValue != -1:
        arrSize  = 1
        arrIndex = -1
        for i in xrange(len(resArray)):
            if resArray[i] == resValue:
                arrIndex = i
        if arrIndex == -1:
            print " error in resArray index"
            exit(-1)
    else:
        arrSize = len(resArray)

    # filling cvArray
    cvArray = zeros((arrSize,3))
    for i in xrange(arrSize):
        cvArray[i][0] = resArray[i]
        
    # main loop
    i = 1
    for dir in dirList:
        os.chdir(dir)
        print " >> %s " % dir
        j = 0
        if arrSize == 1:
            sim    = "t%04dum" % resArray[arrIndex]
            simPts = sim + "/" + sim + "_i.pts"
            simAct = sim + "/" + "activation-thresh.dat"
            cv = condVelocity(simPts, simAct)
            cvArray[0][i] = cv
        else:
            for res in resArray:
                sim    = "t%04dum" % res
                simPts = sim + "/" + sim + "_i.pts"
                simAct = sim + "/" + "activation-thresh.dat"
                
                if (os.path.isfile(simPts) != True):
                    print " error calculateCV: file %s not found" + simPts
                    exit(-1)
                
                if (os.path.isfile(simAct) != True):
                    print " error calculateCV: file %s not found" + simAct
                    exit(-1)
                
                # calculate
                cv = condVelocity(simPts, simAct)
                cvArray[j][i] = cv
                j = j + 1           
        os.chdir("..")
        i = i + 1

    # write cvArray on file
    if(saveFile):
        outName = "condVelocity.pld"
        print " saving to file " + outName + "..."
        outFile = open(outName, "w")
        for i in xrange(len(resArray)):
            outFile.write("%f \t %6.3f \t %6.3f\n" % (cvArray[i][0] , cvArray[i][1] , cvArray[i][2]))
        outFile.close()

    # matplotlib        
    x1 = cvArray[:,0]                   # not scaled
    #x1 = cvArray[:,0]/lambDict[model]  # scaled (dx/lambda)
    
    # try to avoid error with NaNs in the case where a Node was not activated
    x1 = x1; aux1 = cvArray[:,1]
    x2 = x1; aux2 = cvArray[:,2]
    
    for i in xrange(len(cvArray[:,1])):
        if(str(cvArray[:,1][i]) == 'nan'):
            x1   = x1[0:i]
            aux1 = cvArray[:,1][0:i]
            break
    
    for i in xrange(len(cvArray[:,2])):
        if(str(cvArray[:,2][i]) == 'nan'):
            x2   = x1[0:i]
            aux2 = cvArray[:,2][0:i]
            break    
    
    # plot
    if arrSize > 1:
        plot(x1[:], aux1, linewidth=1.0)
        plot(x2[:], aux2, 'r')
        
        legend(('hexa', 'tetra'), 'upper right')
        xlabel('dx(um)')
        ylabel('velocity (m/s)')
        
        title(titleDict[model])
        grid(True)
        show()

    
