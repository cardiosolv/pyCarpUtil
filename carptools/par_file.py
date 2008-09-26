#!/usr/bin/env python

import sys

class ParameterFile():
    """
    Class for the CARP parameter file
    
    Bernardo M. Rocha
    """
    def __init__(self, ionicModel=None, baseFile=None):
        
        if baseFile is None:                        
            self.params = {
                    'num_regions'    : 1 ,
                    'region[0].name' : "simulation",
                    'tend'           : 100.0,
                    'timedt'         : 1.0,
                    'dt'             : 5.0,
                    'spacedt'        : 3.0,
                    'readmesh'       : 2,
                    'solnmethod'     : 2,
                    'CN_parab'       : 0,
                    'cg_tol_parab'   : 1.0e-3,
                    'experiment'     : 0,
                    'gridout_i'      : 0,
                    'num_LATs'       : 0,
                    'lats[0].ID'     : 'activation',
                    'gil'            : 0.174
                    }
            if ionicModel is not None:
                self.params['region[0].im'] = ionicModel
            self.num_stim = 0
            self.stimulus = []

        else:
            self.parseBaseFile(baseFile)
    
    def parseBaseFile(baseFile):
        pass
    
    def add_stimulus(self, stimtype, start, strength, duration, xd, yd, zd, x0, y0, z0):
        self.num_stim = self.num_stim + 1
        dic_stim = {
            'stimtype' : stimtype,
            'start'    : start,
            'strength' : strength,
            'duration' : duration,
            'xd'       : xd,
            'yd'       : yd,
            'zd'       : zd,
            'x0'       : x0,
            'y0'       : y0,
            'z0'       : z0
        }
        self.stimulus.append(dic_stim)
    
    def set_parameter(self, param_key, value):
        """
        Change param_key in the params dictionary to value
        """
        p = self.params
        if not p.has_key(param_key):
            print " Error in ParameterFile: self.params doesn't have the keyword %s" % (param_key)
            sys.exit(-1)
        else:
            p[param_key] = value
    
    def get_parameter(self, param_key):
        """
        Return param_key in the params dictionary
        """
        p = self.params
        if not p.has_key(param_key):
            print " Error in ParameterFile: self.params doesn't have the keyword %s" % (param_key)
            sys.exit(-1)
        else:
            return p[param_key]
       
    def write_to_file(self, filename='par_file.par'):
        
        nregions = self.params['num_regions']
        reg0name = self.params['region[0].name']
        reg0im   = self.params['region[0].im']
        
        f = open(filename, 'w')
        
        f.write("# ............................................ #\n")
        f.write("# CARP parameter file generated by par_file.py #\n")
        f.write("# ............................................ #\n\n")
        
        f.write("# General settings\n\n")
        for key, val in self.params.items():
            f.write("%s = %s\n" % (key, val))
    
        f.write("\n# Stimulus\n\n")
        f.write("num_stim = %s\n" % self.num_stim)
        stim_cont = 0
        for stim in self.stimulus:
            stim_str = "stimulus[%1d]." % stim_cont
            for key, val in stim.items():
                f.write("%s%s = %s\n" % (stim_str, key, val))

        f.close()

if __name__ == "__main__":
    
    ### Example of usage ###
    mypar = ParameterFile("LRDII_F")        

    # common setup
    mypar.set_parameter('readmesh',3)
    mypar.set_parameter('solnmethod',4)
    mypar.set_parameter('gridout_i',2)
    mypar.set_parameter('dt',10)
    mypar.set_parameter('timedt',0.5)
    mypar.set_parameter('spacedt',1)
    mypar.set_parameter('CN_parab',1)
    mypar.set_parameter('cg_tol_parab',1.0e-06)
    mypar.set_parameter('num_LATs',1)
    mypar.set_parameter('lats[0].ID', 'activation')
    mypar.set_parameter('gil',0.178077495)
    # depends on the simulation
    mypar.set_parameter('tend',200)
    # add stimulus    
    mypar.add_stimulus(0, 0, 5e-3, 1, 1100, 1100, 100, -550, -550, -10099)
    # write
    mypar.write_to_file('example_lr2f_simulation.par')
    