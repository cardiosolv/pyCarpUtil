#!/usr/bin/env python

import sys

class ParameterFile:
    """
    Class for the CARP parameter file
    
    Bernardo M. Rocha
    """
    def __init__(self, ionicModel=None, ionicInitial=None, ionicPlugins=None, baseFile=None, carp_ver=None):
        
        if baseFile is None:                        
            self.params = {
                    'num_regions'    : 1 ,
                    'region[0].name' : "simulation",
                    'tend'           : 100.0,
                    'timedt'         : 1.0,
                    'dt'             : 5.0,
                    'spacedt'        : 3.0,
                    'readmesh'       : 2,
                    'bidomain'       : 0,
#                    'solnmethod'     : 2,
                    'parab_solve'    : 0,
                    'cg_tol_parab'   : 1.0e-3,
                    'experiment'     : 0,
                    'gridout_i'      : 0,
                    #'num_LATs'       : 1,                         # deprecated
                    #'lats[0].ID'     : 'activation',              # deprecated
                    'gil'            : 0.174,
                    'gel'            : 0.625,
                    'surfvolrat'     : 0.14
                    }
            if carp_ver is 'carpm':
                self.params['num_imp_regions'] = 1
                self.params['imp_region[0].name'] = self.params['region[0].name']
                self.params['num_gregions'] = 1
                self.params['gregion[0].g_il'] = self.params['gil'] 
                self.params['gregion[0].g_el'] = self.params['gel']
                self.params['imp_region[0].cellSurfVolRatio'] = 0.14

               # delete all useless CARPpe parameters
                del self.params['surfvolrat']
                del self.params['num_regions']
                del self.params['region[0].name']
                del self.params['gil']
                del self.params['gel']
                del self.params['readmesh']
                if ionicModel is not None:
                    self.params['imp_region[0].im'] = ionicModel  
                if ionicInitial is not None:
                    self.params['imp_region[0].im_sv_init'] = ionicInitial
                if ionicPlugins is not None:
                    self.params['imp_region[0].plugins'] = ionicPlugins  
            else:
                if ionicModel is not None:
                    self.params['region[0].im'] = ionicModel
                if ionicInitial is not None:
                    self.params['region[0].im_sv_init'] = ionicInitial
                if ionicPlugins is not None:
                    self.params['region[0].plugins'] = ionicPlugins
                    
            self.num_stim = 0
            self.num_LATs = 0
            self.stimulus = []
            self.LATs     = []

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
    
    def add_LAT(self, id, measurand=None, all=None, threshold=None, method=None):
        """
        Local activation measurements - CARP array parameter
        """
        self.num_LATs = self.num_LATs + 1
        dic_LAT = {'ID' : id}
        if measurand is not None: dic_LAT['measurand'] = measurand
        if all       is not None: dic_LAT['all'] = all
        if threshold is not None: dic_LAT['threshold'] = threshold
        if method    is not None: dic_LAT['method'] = method
        self.LATs.append(dic_LAT)
    
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
       
    def write_to_file(self, carp_ver, filename='par_file.par'):
         
        if carp_ver is 'carpe':
          nregions = self.params['num_regions']
          reg0name = self.params['region[0].name']
          reg0im   = self.params['region[0].im']
        if carp_ver is 'carpm':
          nregions = self.params['num_imp_regions']
          reg0name = self.params['imp_region[0].name']
          reg0im   = self.params['imp_region[0].im']
        
        f = open(filename, 'w')
        
        f.write("# ............................................ #\n")
        f.write("# CARP parameter file generated by par_file.py #\n")
        f.write("# ............................................ #\n\n")
        
        f.write("# General settings\n\n")
        
        # this is ugly, there must be a better fix for this
        #f.write("num_LATs = 1\n")
        
        sortedKeys  = sorted(self.params.keys())        
        for key in sortedKeys:
            val = self.params[key]
            if type(val) is str:
                f.write("%s = \"%s\"\n" % (key, val))
            else:
                f.write("%s = %s\n" % (key, val))
    
        f.write("\n# Stimulus\n\n")
        f.write("num_stim = %s\n" % self.num_stim)
        stim_cont = 0
        for stim in self.stimulus:
            stim_str = "stimulus[%1d]." % stim_cont
            for key, val in stim.items():
                f.write("%s%s = %s\n" % (stim_str, key, val))
        
        if len(self.LATs) > 0:
            f.write("\n# LATs\n\n")
            f.write("num_LATs = %s\n" % self.num_LATs)
            lats_cont = 0
            for lats in self.LATs:
                lats_str = "lats[%1d]." % lats_cont
                for key, val in lats.items():
                    f.write("%s%s = %s\n" % (lats_str, key, val))

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
    mypar.set_parameter('gil',0.178077495)
    
    # depends on the simulation
    mypar.set_parameter('tend',200)
    
    # add stimulus and LATs
    mypar.add_stimulus (0, 0, 5e-3, 1, 1100, 1100, 100, -550, -550, -10099)    
    mypar.add_LAT ('activation')
    
    # write
    mypar.write_to_file('example_lr2f_simulation.par')    
    
