#!/usr/bin/env python
import os, sys, getopt
from carptools.msh_file import MeshFile
from carptools.par_file import ParameterFile
from condVelocity import condVelocity
from sctools import check_path, run_command_line

DEBUG = False

"""
Bernardo M. Rocha, 2008
"""

class CableTest(ParameterFile):
    """
    Base class for the cable to run the tuning simulations
    """
    def __init__(self, im, gil, gel, beta, vs):
        ParameterFile.__init__(self, ionicModel=im, carp_ver=vs)

        self.set_parameter('surfvolrat',  beta)
        self.set_parameter('solnmethod',  4)
        self.set_parameter('gridout_i',   2)
        self.set_parameter('dt',          10)
        self.set_parameter('timedt',      0.5)
        self.set_parameter('spacedt',     1)
        self.set_parameter('CN_parab',    1)
        self.set_parameter('cg_tol_parab',1.0e-06)
        self.set_parameter('num_LATs',    1)
        self.set_parameter('lats[0].ID',  'activation')
        self.set_parameter('tend',        200)

        # version specific settings
        if vs is 'carpe':
          self.set_parameter('readmesh',  3)
          self.set_parameter('gil',       gil)
          self.set_parameter('gel',       gil)

        if vs is 'carpm':
          self.set_parameter('gregion[0].g_il', gil)
          self.set_parameter('gregion[0].g_el', gel)

        self.add_stimulus(0, 0, 5e-2, 1, 100, 1000, 1000, -5099, -500, -500)

# end of CableTest

def calculate_g(v1,v0,g0):
    """
    Input:  v1 - desired conduction velocity
            v0 - computed conduction velocity
            g0 - bulk conductivity to obtain v0
    Output: g1 - bulk conductivity to obtain v1
    Description: g1 = g0 * ((v1/v0)**2)
    """
    return g0 * ((v1/v0)*(v1/v0))

def find_CV(avg_dx, gil, gel, beta, model, carpBinary, mesherBinary, carp_ver):
    """
    Input: avg_dx - mesh resolution as a scalar or list (list - Not implemented yet)
           gil    - intracellular conductivity along the cable
           gel    - extracellular conductivity along the cable
           beta   - surface-to-volume ratio
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

        my_cable = CableTest(model, gil, gel, beta, carp_ver)
        my_cable.write_to_file(carp_ver,carp_file)

        # run MESHER
        cmd = '%s +F %s' % (mesherBinary, mesh_file)
        if DEBUG: print 'running %s' % cmd
        run_command_line(cmd)        
        # run CARP
        cmd = '%s +F %s -meshname %s -simID OUTPUT_DIR'  % (carpBinary, carp_file, mesh_name)
        if DEBUG: print 'running %s' % cmd
        run_command_line(cmd)
        
        # calculate CV
        sim_pts = "OUTPUT_DIR/%s_i.pts" % mesh_name
        sim_act = "OUTPUT_DIR/activation-thresh.dat"    
        cvList.append( condVelocity(sim_pts, sim_act, output=False) )
    
    if len(resList) == 1: return cvList[0]
    return cvList

def run_simulation():
    # try to implement and then use map
    pass
  
def printHelp():
    print """
  >> Usage       : python -d <dx> -v <target velocity> -m <model> -i <gil> -e <gel> -b <beta>
  >> Description : script for tuning tissue conductivities\n  >> Parameters  :
  \t -d <value>   --resolution=<value>   \t avg resolution of mesh in um       \t (default=100um)
  \t -v <value>   --velocity=<value>     \t desired conduction velocity in m/s \t (default=0.6)
  \t -m <model>   --model=<model         \t name of ionic model to test        \t (default=MBRDR)
  \t -i <value>   --gil=<value>          \t initial value for gil              \t (default=0.174 S/m)
  \t -e <value>   --gel=<value>          \t initial value for gel              \t (default=0.625 S/m)
  \t -b <value>   --beta=<value>         \t surface-to-volume ratio            \t (default=0.14 cm^-1)
  \t -t <value>   --tol=<value>          \t tolerance - percentage of error    \t (default=0.05)
  \t --with-carp = <path_to_carp_binary>   \t specify your carp version
  \t --with-mesher=<path_to_mesher_binary> \t specify your mesher version
  """
 
def main(argv):

    # default values 
    model   = "MBRDR"
    avgdx   = 100
    gil     = 0.174
    gel     = 0.625
    beta    = 0.14
    tol     = 0.05
    
    checkBin     = True
    carpBinary   = 'carp.linux.petsc'
    mesherBinary = 'mesher'
    carp_version = 'carpm'
    
    if len(argv) == 1:
        printHelp(); sys.exit(1)
    
    # command lind parsing with getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:v:i:e:b:m:t:",
                    ["help", "resolution=","velocity=","gi=","ge=","beta=","model=","tol=","with-carp=","with-mesher="])
    except getopt.GetoptError, err:
        print str(err) # option -a not recognized"
        printHelp()
        sys.exit(-1)
    
    for o, a in opts:
        if o in ("-h", "--help"):
            printHelp()
            sys.exit()
        elif o in ("-d", "--resolution"):
            avgdx = int(a)
        elif o in ("-v","--velocity"):
            vel = float(a)
        elif o in ("-i","--gi"):
            gil = float(a)
        elif o in ("-e","--ge"):
            gel = float(a)
        elif o in ("-b","--beta"):
            beta = float(a)
        elif o in ("-t","--tol"):
            tol = float(a)
        elif o in ("-m","--model"):
            model = str(a)
        elif o == "--with-carp":
            carpBinary = str(a)
            checkBin   = False
        elif o == "--with-mesher":
            mesherBinary = str(a)
            checkBin     = False
        else:
            assert False, "unhandled option"
            sys.exit(-1)
    # end of command line parsing
    
    if (checkBin):
        check_path (carpBinary)
        check_path (mesherBinary)

    # settings    
    eps = vel * tol    
    its = 1
    CV_measured = 0.
    
    print "\n S i m u l a t i o n   s e t t i n g s\n"
    print "    ionic model      :  %s" % model
    print "    mesh resolution  :  %s" % avgdx
    print "    CV desired       : %8.5f m/s" % (vel)
    print "    tolerance        :  %.4f" % tol
    print "\n S i m u l a t i n g ...\n"
    
    while abs(vel - CV_measured) > eps:
        print "    Iteration  %d: gil =%8.5f, gel =%8.5f, gl_bulk =%8.5f" % (its,gil,gel,(gil*gel/gil+gel)),
        sys.stdout.flush()
        
        CV_measured = find_CV (avgdx, gil, gel, beta, model, carpBinary, mesherBinary, carp_version)
        print " --->  CV measured : %8.5f m/s" % CV_measured
        
        gl_bulk     = gil*gel/(gil+gel)
        gl_bulk     = calculate_g (vel, CV_measured, gl_bulk)
        gil         = gel*gl_bulk/(gel-gl_bulk)
        delta_abs   = vel-CV_measured
        delta_rel   = delta_abs/vel
        its        += 1
    
    print "\n S i m u l a t i o n   r e s u l t s\n"    
    print "    bulk conductivity: %8.5f"          % (gl_bulk)
    print "    use gi/ge        : %8.5f %8.5f \n" % (gel*gl_bulk/(gel-gl_bulk), gel)

if __name__ == "__main__":
    main(sys.argv)
 
