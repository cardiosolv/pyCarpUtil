#!/usr/bin/env python

import os, sys, popen2, subprocess
from numpy import arange, loadtxt
from scipy.io import write_array
from scipy.io import read_array

def iseq(start=0, stop=None, inc=1):
    """
    Purpose: Generate integer from start to (and including) stop
    with increment of inc. Alternative to range/xrange.
    """
    if stop == None:
        stop = start; start = 0; inc = 1
    return xrange(start, stop+inc, inc)

def sequence(start, stop, inc):
    """
    Purpose: Generate float sequence from start to (and including) stop
    with increment of inc. Alternative to arange.
    """
    return arange(start, stop+inc, inc)

def read_array_pts(ptsFile):
    """
    Purpose: Function to read a .pts file from CARP simulator, where the first line contains
    the number of nodes and the remaining file contains the array of nodes
    
    Example:
    from sctools import read_array_pts
    nn, narray = read_array_pts("t0010um_i.pts")
    print nn
    print narray[:,0]
    print narray[:,1]
    print narray[:,2]
    
    Bernardo M. Rocha, 2008
    """
    try:
        f = open(ptsFile)
        lines = f.readlines()
        f.close()
    except IOError:
        print "IOError: File %s not found." % ptsFile
        sys.exit(-1)
    
    # number of nodes
    numNodes = int(lines[0]); del lines[0]
    nodesTmp = "mytemp.txt"

    try:
        fnew = open(nodesTmp,"w")
        for i in lines:
            fnew.write(i)
        fnew.close()
    except IOError:
        print "IOError: File %s not found." % ptsFile
        exit(-1)

    # numpy array of nodes
    nodes = loadtxt(nodesTmp)
    
    if(numNodes != len(nodes)):
        print " error read_array_pts(): the size of the array doesn't match"
        exit(-2)
    
    os.remove(nodesTmp)
            
    return nodes

# end of read_array_pts

def run_command_line (command, output=False):
    """
    Purpose: Run a command line and capture the stdout and stderr
    """   
    proc = subprocess.Popen(command,shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT
                        )
    stdout_value, stderr_value = proc.communicate()
    if output: print '\tcombined output:', repr(stdout_value)

# end of run_command_line

def run_command_line_old(command, output=False):
    """
    Purpose: Run a command line and capture the stdout and stderr
    Deprecated: the use of popen2.popen4 will not be supported in Python 3
    """
    r,w = popen2.popen4(command)
    out = r.readlines()
    if output: print out
    r.close()
    w.close()

# end of run_command_line

def check_path(prog_name):
    """
    Purpose: find if the user has the prog_name in his $PATH
    """
    prog = False    
    pathList = os.environ.get('PATH').split(':')
    for path in pathList:
        if not os.access(path,os.X_OK):
            continue
        binaryList = os.listdir(path)
        binaryList.sort()
        if prog_name in binaryList:
            prog = True
            #if DEBUG: print "%s path=%s" % (prog_name, os.path.join(path,carpBinary))
    if not prog:
        print "Error: %s was not found in your $PATH" % (prog_name)
        exit(-1)
        
# end of check_path