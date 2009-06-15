#!/usr/bin/env python

import sys, gzip, pdb, time
import numpy as np
from pyUtils.sctools import read_array_pts, read_array_elem

def carp2vtk (carpMesh, outputMesh):

    ptsFile  = carpMesh + '.pts'
    elemFile = carpMesh + '.elem'
    
    pts  = read_array_pts (ptsFile)
    elem = read_array_elem (elemFile)

    numPts  = np.shape(pts)[0]
    numElem = np.shape(elem)[0]

    outputFile = file(outputMesh, 'w')
    outputFile.write('# vtk DataFile Version 2.0\n')
    outputFile.write('CT scan data of human heart, courtesy by Henk Mastenbroek RuG\n')
    outputFile.write('ASCII\n')

    outputFile.write('UNSTRUCTURED_GRID\n')

    outputFile.write('POINT_DATA %d\n' % numPts)
    for i in xrange(numPts):
        outputFile.write('%f %f %f\n' % (pts[i,0],pts[i,1],pts[i,2]))

    outputFile.close()

if __name__ == "__main__":

    np.set_printoptions(precision=5)

    carp2vtk(sys.argv[1], sys.argv[2])    


# end of main
