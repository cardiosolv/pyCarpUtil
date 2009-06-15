#!/usr/bin/env python

import sys, pdb, os
import numpy as np
from pylab import *
from pyUtils.igb.igb_read import *

def calc_map_rrms(ve_name, vh_name, map_name):
	
  ve, vh = load_data(ve_name, vh_name)

  if(np.shape(ve)[0] != np.shape(vh)[0]):
    print " Error: time dimensions do not match."
    sys.exit(1)

  time_steps = np.int(np.shape(ve)[0])

  # read map
  map = np.loadtxt(map_name)	
  map_size = np.int(map[0,0])
  map = np.array(map[1:], dtype=int)

  # compute RRMS norm - call Cython module
  try:
    from rrms import rrms_map as calc_rrms
    calc_rrms(time_steps, ve, vh, map_size, map)
  except ImportError:
    print " Cython module rrms could not be found."
    sys.exit(1)

# end of calc_map_rrms

def calc_rrms (ve_name, vh_name):

  ve, vh = load_data(ve_name, vh_name)
  
  # reshape arrays to 1d arrays
  veshp = np.shape(ve)
  ve = ve.reshape((veshp[0], veshp[1]*veshp[2]))	

  vhshp = np.shape(vh)
  vh = vh.reshape((vhshp[0], vhshp[1]*vhshp[2]))	
	
  shp = np.shape(ve)
  time_steps = shp[0]

  # compute RRMS norm - call external module
  try:
    from rrms import rrms as calc_rrms
    calc_rrms(time_steps, ve, vh)
  except ImportError:
    print " Cython module rrms could not be found."
    sys.exit(1)

# end of calc_rrms

def load_data(ve_name, vh_name):

  # open exact Vm IGB
  if os.path.isfile(ve_name):
    [ve, veh] = read_igb_slice(ve_name, is_gzipped=True)
    ve = ve.squeeze()

  # open aprox Vm IGB
  if os.path.isfile(vh_name):
    [vh, vhh] = read_igb_slice(vh_name, is_gzipped=True)
    vh = vh.squeeze()

  # show information
  print np.shape(ve)
  print np.shape(vh)

  return ve, vh

# end of load_data

if __name__ == "__main__":
	
  if len(sys.argv) < 3:
    print "\n Usage: calcRRMS.py <EXATA> <APROX> <MAP>"; exit(1);

  ven = sys.argv[1] # nome da solucao exata
  vhn = sys.argv[2] # nome da solucao aprox

  # compute RRMS with map file 
  if len(sys.argv) > 3:
    map_name = sys.argv[3]
    calc_map_rrms(ven, vhn, map_name)
  else:
    calc_rrms (ven, vhn)  

# end of main
