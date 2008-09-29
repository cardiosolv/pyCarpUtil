#!/usr/bin/env python

import os, sys, popen2
from carptools.msh_file import *
from carptools.par_file import *
from condVelocity import condVelocity

"""
Bernardo M. Rocha, 2008
"""

class CableTest(ParameterFile):
    """
    Base class for the cable to run the tuning simulations
    """
    def __init__(self, im, gbulk):
        ParameterFile.__init__(self, ionicModel=im)

        self.set_parameter('readmesh',    3)
        self.set_parameter('solnmethod',  4)
        self.set_parameter('gridout_i',   2)
        self.set_parameter('dt',          10)
        self.set_parameter('timedt',      0.5)
        self.set_parameter('spacedt',     1)
        self.set_parameter('CN_parab',    1)
        self.set_parameter('cg_tol_parab',1.0e-06)
        self.set_parameter('num_LATs',    1)
        self.set_parameter('lats[0].ID',  'activation')
        self.set_parameter('gil',         gbulk)
        self.set_parameter('tend',        200)

        self.add_stimulus(0, 0, 5e-2, 1, 100, 1000, 1000, -5099, -500, -500)

def find_CV(avg_dx, g_bulk):
    """
    Input: avg_dx - mesh resolution as a scalar or list (list - Not implemented yet)
           g_bulk - conductivity for the cable
    Output:
           cv_measured in a 1cm long cable with avg_dx of resolution and using
           the value of g_bulk as conductivity
    """
    resList = []   # list of resolutions
    cvList  = []   # list of conduction velocities measured
    
    if isinstance(avg_dx,list):
        resList = avg_dx
    elif isinstance(avg_dx,int) or isinstance(avg_dx,float):
        resList.append(avg_dx)    

    # settings
    xsize = 1.0 # cm
    mesh_file = "expMesh.par"
    mesh_name = "mesh4exp"
    carp_file = "expParam.par"    

    for res in resList:
        
        yzsize = float(res/10000.)   # cm
           
        my_mesh = MeshFile(mesh_name, size0=xsize, size1=yzsize, size2=yzsize, element=1, resolution=res)
        my_mesh.write_to_file(mesh_file)

        my_cable = CableTest('UCLA_RAB', g_bulk)
        my_cable.write_to_file(carp_file)
           
        # run MESHER
        cmd = 'mesher +F %s' % mesh_file
        runCommandLine(cmd)        
        # run CARP
        cmd = 'carp.linux.petsc +F %s -meshname %s -simID OUTPUT_DIR'  % (carp_file, mesh_name)
        runCommandLine(cmd)
        
        # calculate CV
        sim_pts = "OUTPUT_DIR/%s_i.pts" % mesh_name
        sim_act = "OUTPUT_DIR/activation-thresh.dat"    
        cvList.append( condVelocity(sim_pts, sim_act, output=False) )
    
    # print information
    print "\n S i m u l a t i o n   d e t a i l s\n"
    if len(resList) == 1:
        print "    mesh resolution :  %d um" % resList[0]
        print "    conductivity    : %8.5f" % g_bulk
        print "    CV measured     : %8.5f m/s\n" % cvList[0]
        return cvList[0]
    else:
        print "    mesh resolution : ", resList
        print "    conductivity    : %8.5f" % g_bulk
        print "    CV measured     : ", cvList, " m/s\n"
        return cvList

def run_simulation():
    pass

def calculate_g(v1,v0,g0):
    """
    Input:  v1 - desired conduction velocity
            v0 - computed conduction velocity
            g0 - conductivity to obtain v0
    Output: g1 - conductivity to obtain v1
    Description: g1 = g0 * ((v1/v0)**2)
    """
    return g0 * ((v1/v0)*(v1/v0))

def runCommandLine(command):
    """
    Run a command line and capture the stdout and stderr and print if
    print_output is True.
    """
    r,w = popen2.popen4(command)
    out = r.readlines()    
    r.close()
    w.close()
    
if __name__ == "__main__":
       
    avgdx = 50
    gbulk = 0.178077495
    
    CV_measured = find_CV (avgdx, gbulk)
    
    print "    new g : %f\n" % (calculate_g (0.7 , CV_measured, gbulk))
    