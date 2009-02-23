#!/usr/bin/env python

import sys, gzip, pdb, time
import numpy as np
from sctools import read_array_pts

def intersect_nodes(fpts1, fpts2, fout):
    a = read_array_pts(fpts1)
    b = read_array_pts(fpts2)
    
    ia = np.logical_or.reduce(np.logical_and.reduce(a == b[:,None], axis=2))
    ib = np.logical_or.reduce(np.logical_and.reduce(b == a[:,None], axis=2))
    index_ia = np.array(np.nonzero(ia), dtype=np.int).squeeze()
    index_ib = np.array(np.nonzero(ib), dtype=np.int).squeeze()
    
    f = open(fout, 'w')
    f.write('%d\n' % (np.shape(index_ia)[0]))
    for i in xrange(len(index_ia)):
        print index_ia[i], index_ib[i]
        f.write('%d %d\n' % (index_ia[i], index_ib[i]))
    f.close()
    
# end of intersect_nodes

if __name__ == "__main__":
    
    if len(sys.argv) < 4:
        print "\n Usage: map_nodes [pts_file_1] [pts_file_2] [outfile] \n"
        exit(-1)
    
    c1 = time.clock()
    
    #map_nodes(sys.argv[1], sys.argv[2], sys.argv[3])
    
    intersect_nodes(sys.argv[1], sys.argv[2], sys.argv[3])
    
    print " Time: %f" % (time.clock()-c1)
