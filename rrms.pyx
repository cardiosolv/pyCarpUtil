"""
Cython module for RRMS norm calculation of IGB files

Compilation steps:
  1. To generate .c file:
     cython yourmod.pyx

  2. To generate the module:
     gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing
         -I/usr/include/python2.5 -o yourmod.so yourmod.c

http://docs.cython.org/docs/numpy_tutorial.html

Bernardo M. Rocha, 2009
"""

import sys, os
import numpy as np
from pylab import *
from pyUtils.igb.igb_read import *

# 'cimport' is used to import special compile-time information
# about the numpy module (in numpy.pxd) 
cimport numpy as np

# fix the datatype for our arrays
DTYPE = np.float32

# ctypedef assigns a corresponding compile-time type to DTYPE_t.
# for every type in numpy module there's a corresponding compile-time
# type with a _t suffix
ctypedef np.float32_t DTYPE_t

def rrms_map(int time_steps,
         np.ndarray[DTYPE_t, ndim=2] ve,
         np.ndarray[DTYPE_t, ndim=2] vh,
         int map_size,
         np.ndarray[np.int_t, ndim=2] map):

    cdef float aux1 = np.float32(0.0)
    cdef float aux2 = np.float32(0.0)
    cdef float erro
    cdef unsigned int t, j, index1, index2 # avoids negative index checking

    cdef np.ndarray[DTYPE_t, ndim=1] se = np.zeros([map_size], dtype=DTYPE)
    cdef np.ndarray[DTYPE_t, ndim=1] sh = np.zeros([map_size], dtype=DTYPE)

    for t in xrange(time_steps):

        # slice in time t
        se = ve[t,:]
        sh = vh[t,:]

        # extracts the matching nodes
        for j in xrange(map_size):
            index1 = <unsigned int> map[j,0]
            index2 = <unsigned int> map[j,1]
            aux1 += (se[index1]-sh[index2])*(se[index1]-sh[index2])
            aux2 += (se[index1]*se[index1])
    
        erro = 100.0 * ( sqrt(aux1) / sqrt(aux2) )
        print "error at time %f is %f " % (t,erro)


def rrms(time_steps, ve, vh):
  aux1 = 0.0
  aux2 = 0.0

  for t in xrange(time_steps):
    se = ve[t,:] # slice in time t
    sh = vh[t,:] # slice in time t
	
    aux1 += np.sum( (se-sh)*(se-sh) )
    aux2 += np.sum( se*se )
    
  err = 100.0 * ( np.sqrt(aux1) / np.sqrt(aux2)	)
  print err
    
