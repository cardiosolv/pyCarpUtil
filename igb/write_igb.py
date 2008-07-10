#!/usr/bin/env python

import sys, os, pdb, time
import numpy, stat, string

from numpy import *
from scipy.io.npfile import npfile
#from scipy.io.fopen import fopen
from igb_header import igb_header
from read_igb_file import *

"""
IGB write file - UNDER DEVELOPMENT

Bernardo M. Rocha
"""

def packFloatData(data):
    """
    pack binary data to be written in a binary file in 'little_endian' format
    data must has 2 dimensions (ndim=2)
    data(x,t) -> x node
              -> t time slice
    """
    import struct
    
    packedData=''
    size = shape(data)
    for j in xrange(size[1]):
        for i in xrange(size[0]):
            packedData+=struct.pack('<f',data[i,j])

    #packedData = ''.join([struct.pack('<f',data[i,j]) for j in xrange(size[1]) for i in xrange(size[0])])

    return packedData

def write_igb(data, hd, filename):

    # start time
    t0 = time.time()
    
    n_dims = data.ndim
    d_data = zeros((data.ndim))    
    for i in xrange(data.ndim):
        d_data[i] = data.shape[i]
        
    #if n_dims == 2:#
    #    d_data = zeros(d)
    #    array([d_data,1,1])
    
    #if n_dims == 3:
    #    d_data = array([d_data,1])
      
    t1 = time.time()
    pData = packFloatData(data.squeeze())
    t2 = time.time()

    print " packFloatData: %.5f seconds wall time" % (t2-t1)

    if d_data[0] == hd.x and d_data[1] == hd.y and d_data[2] == hd.z and d_data[3] == hd.t:        
        fh = npfile (filename,'w')       
        write_header(hd, fh)        
        fh.write_array(pData)       
        fh.close()
    else:
        print " ERROR: Header-Data mismatch\n"

    print " write_igb    : %.5f seconds wall time" % (time.time() - t0)

def write_header(hd, fh):
    """
    write the 1024 bytes IGB format header (hd) in file (fh)
    """    
    # header size in bytes
    hs = 1024

    # create write buffer
    buffer = [ ' ' for i in xrange(hs-1)]

    # create header substrings
    N  = 'x:%d y:%d z:%d t:%d \r\n' % (hd.x, hd.y,hd.z,hd.t)
    DT = 'type:%s \r\n' % (hd.type)
    D  = 'dim_x:%f dim_y:%f dim_z:%f dim_t:%f \r\n' % (hd.dim_x, hd.dim_y, hd.dim_z, hd.dim_t)
    U  = 'unites_x:%s unites_y:%s unites_z:%s unites_t:%s unites:%s \n' % (hd.unites_x, hd.unites_y, hd.unites_z, hd.unites_t, hd.unites)
    F  = 'facteur:%d \r\n' % (hd.facteur)
    Z  = 'zero:%d \r\n' % (hd.zero)
    SY = 'systeme:%s \r\n' % (hd.systeme)

    # concatenate header substrings
    hd_str = '%s %s %s %s %s %s %s' % (N, DT, D, U, F, Z, SY)
    
    # fill rest with empty lines, each line not longer than 80 chars
    lines = int(floor( (1023 - len(hd_str) ) / 78 ))
   
    ln = [' ' for i in xrange(75)]    
    ln_str = string.join(ln, '')
        
    for i in xrange(lines):
        hd_str = '%s %s \r\n' % (hd_str, ln_str)

    # convert to character array
    for i in xrange(len(hd_str)):
        buffer[i] = hd_str[i]
    buffer_str = string.join(buffer, '')

    # write buffer
    fh.write_array(buffer_str)
    #fh.write(buffer_str)

    # write header termination character
    # (seems to be 0x0C)
    hd_term = chr(12)
    fh.write_array(hd_term)
    #fh.write(hd_term)

if __name__ == "__main__":
       
    #hd = igb_header([18036,1,1,101],'float',[nan,nan,nan,100.0100],('cm', 'cm', '', 'mss', 'mV'),1,0)
    #data = zeros((18036*101)).reshape(18036,1,1,101)

    # resolution 100um - UCLA_RAB model
    igb_file = '/home/rocha/sim/experiment_gm_ucla/gm_t0100/vm.igb'
    pts_file = '/home/rocha/sim/experiment_gm_ucla/gm_t0100/gm_t0100um_i.pts'
    [vm, hd] = read_igb_slice(igb_file)
    Vm = vm.squeeze()

    write_igb (vm, hd, 'teste.igb')#
    
    #pdb.set_trace()
