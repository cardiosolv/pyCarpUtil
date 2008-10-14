#!/usr/bin/env python
import os, sys, popen2, getopt
from carptools.msh_file import MeshFile
from carptools.par_file import ParameterFile
from condVelocity import condVelocity

import pdb

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

def calculate_g(v1,v0,g0):
    """
    Input:  v1 - desired conduction velocity
            v0 - computed conduction velocity
            g0 - bulk conductivity to obtain v0
    Output: g1 - bulk conductivity to obtain v1
    Description: g1 = g0 * ((v1/v0)**2)
    """
    return g0 * ((v1/v0)*(v1/v0))

def checkCARP(carpBinary, mesherBinary):
    """
    Purpose: find if the user has the specified/default
    carp and mesher binaries in order to run the simulations
    """
    carp   = False
    mesher = False
    
    pathList = os.environ.get('PATH').split(':')
    for path in pathList:
        if not os.access(path,os.X_OK):
            continue
        binaryList = os.listdir(path)
        binaryList.sort()        
        if carpBinary in binaryList:
            carp = True
            #print os.path.join(path,carpBinary)
        if mesherBinary in binaryList:
            mesher = True
            #print os.path.join(path,mesherBinary)

    if not carp:   print "carp.linux.petsc was NOT found in $PATH"; exit(-1)
    if not mesher: print "mesher was NOT found in $PATH"; exit(-1)

def find_CV(avg_dx, gil, gel, beta, model, carpBinary, mesherBinary, carp_ver):
    """
    Input: avg_dx - mesh resolution as a scalar or list (list - Not implemented yet)
           gil    - intracellular conductivity along the cable
           gel    - intracellular conductivity along the cable
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
        #cmd = 'mesher +F %s' % mesh_file
        cmd = '%s +F %s' % (mesherBinary, mesh_file)
        print 'running %s' % cmd
        runCommandLine(cmd)        
        # run CARP
        #cmd = 'carp.linux.petsc +F %s -meshname %s -simID OUTPUT_DIR'  % (carp_file, mesh_name)
        cmd = '%s +F %s -meshname %s -simID OUTPUT_DIR'  % (carpBinary, carp_file, mesh_name)
        print 'running %s' % cmd
        runCommandLine(cmd)
        
        # calculate CV
        sim_pts = "OUTPUT_DIR/%s_i.pts" % mesh_name
        sim_act = "OUTPUT_DIR/activation-thresh.dat"    
        cvList.append( condVelocity(sim_pts, sim_act, output=False) )
    
    # print information
    print "\n S i m u l a t i o n   d e t a i l s\n"
    if len(resList) == 1:
        print "    mesh resolution  :  %d um" % resList[0]
        print "    ionic model      :  %s" % model
        print "    gil              : %8.5f" % gil
        print "    gel              : %8.5f" % gel
        print "    gl_bulk          : %8.5f" % (gil*gel/(gil+gel))
        print "    CV measured      : %8.5f m/s" % cvList[0]
        return cvList[0]
    else:
        print "    mesh resolution  : ", resList
        print "    gil              : %8.5f" % gil
        print "    gel              : %8.5f" % gel
        print "    gl_bulk          : %8.5f" % gil*gel/(gil*gel)
        print "    CV measured      : ", cvList, " m/s\n"
        return cvList

def run_simulation():
    # try to implement and then use map
    pass

def runCommandLine(command):
    """
    Run a command line and capture the stdout and stderr and print if
    print_output is True.
    """
    r,w = popen2.popen4(command)
    out = r.readlines()    
    r.close()
    w.close()   
   
def printHelp():
    usage    = "  >> Usage       : python -d <dx> -g <initial conductivity> -v <desired_velocity>\n"
    help_de  = "  >> Description : script for tuning bulk conductivities\n  >> Parameters  :\n"
    help_dx  = "\t -d <value>   --resolution=<value>   \t avg resolution of mesh in um (default=100um)\n"
    help_vel = "\t -v <value>   --velocity=<value>     \t desired conduction velocity in m/s\n"
    help_md  = "\t -m <model>   --model=<model         \t name of ionic model to test\n"
    help_g   = "\t -g <value>   --glbulk=<value>       \t start value for bulk conductivity\n"
    help_wc  = "\t --with-carp=<path_to_carp_binary>   \t specify your carp binary version\n"
    help_wm  = "\t --with-mesher=<path_to_mesher_binary> \t specify your mesher binary version\n"
    
    print "%s%s%s%s%s%s%s%s" % (usage, help_de, help_dx, help_vel, help_md, help_g, help_wc, help_wm)
 
def main(argv):

    # default values 
    model   = "MBRDR"
    avgdx   = 100
    gil     = 0.174
    gel     = 0.625
    beta    = 0.14
    
    while len(argv) == 1:
        printHelp(); sys.exit(1)
    
    # command lind parsing with getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:v:i:e:m:",
                    ["help", "resolution=","velocity=","gi=","ge=","model=","with-carp=","with-mesher="])
    except getopt.GetoptError, err:
        print str(err) # option -a not recognized"
        printHelp()
        sys.exit(-1)
    
    # default options
    carpBinary   = 'carpm.linux.petsc'
    mesherBinary = 'mesher'
    
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
        elif o in ("-m","--model"):
            model = str(a)
        elif o == "--with-carp":
            carpBinary = str(a)
        elif o == "--with-mesher":
            mesherBinary = str(a)
        else:
            assert False, "unhandled option"
            sys.exit(-1)
    # end of command line parsing

    
    checkCARP(carpBinary, mesherBinary)
    carp_ver = 'carpm'
    CV_measured = find_CV (avgdx, gil, gel, beta, model, carpBinary, mesherBinary, carp_ver)
    gl_bulk     = gil*gel/(gil+gel)
    gl_bulk     = calculate_g (vel, CV_measured, gl_bulk)

    print "    CV desired       : %8.5f m/s" % (vel)
    print "    bulk conductivity: %8.5f \n" % (gl_bulk)
    print "    use gi/ge        : %8.5f %8.5f \n" % (gel*gl_bulk/(gel-gl_bulk), gel)

if __name__ == "__main__":
    main(sys.argv)
 
