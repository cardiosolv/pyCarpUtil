#!/usr/bin/env python

import sys, gzip, pdb, time
import numpy as np
from pyUtils.sctools import read_array_pts, read_array_elem

def carp2Gmsh (carpMesh, outputMesh):

    ptsFile  = carpMesh + '.pts'
    elemFile = carpMesh + '.elem'
    
    pts  = read_array_pts (ptsFile)
    elem = read_array_elem (elemFile)

    numPts  = np.shape(pts)[0]
    numElem = np.shape(elem)[0]

    pdb.set_trace()

    outputFile = file(outputMesh, 'w')
    outputFile.write('$MeshFormat\n2.0 0 8\n$EndMeshFormat\n')
    outputFile.write('$Nodes\n')
    outputFile.write('%d\n' % numPts)
    for i in xrange(numPts):
        outputFile.write('%d %f %f %f\n' % (i+1,pts[i,0],pts[i,1],pts[i,2]))
    outputFile.write('$EndNodes\n')
    outputFile.write('$Elements\n')
    outputFile.write('%d\n' % numElem)

#    print elem

    # triangles only
    for i in xrange(numElem):
        outputFile.write('%d 2 2 99 2 %d %d %d\n' % (i+1, int(elem[i][1])+1, int(elem[i][2])+1, int(elem[i][3])+1 ) )

    outputFile.write('$EndElements\n')
    outputFile.close()

if __name__ == "__main__":

    np.set_printoptions(precision=5)

    carp2Gmsh(sys.argv[1], sys.argv[2])    


# end of main
