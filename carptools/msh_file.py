#!/usr/bin/env python

import pdb

class MeshFile:
    """
    Class for the mesh parameter file used as input in CARP
    
    Units:
        size      : cm
        resolution: um
    
    Bernardo M. Rocha
    """
  
    def __init__(self, size0=1.0, size1=1.0, size2=1.0, element=0, resolution=100, tri2d=False):
        self.params = {
                'mesh'         : 't%04dum' % resolution,
                'size[0]'      : size0,
                'size[1]'      : size1,
                'size[2]'      : size2,
                'Elem3D'       : element,
                'tri2D'        : tri2d,
                'resolution[0]': resolution,
                'resolution[1]': resolution,
                'resolution[2]': resolution
                } 
    
    def write_to_file(self, filename='msh_file.par'):
        name,  element, res = self.params['mesh'],    self.params['Elem3D'],  self.params['resolution[0]']
        size0, size1, size2 = self.params['size[0]'], self.params['size[1]'], self.params['size[2]']
        
        f = open(filename, 'w')
        
        f.write("# ................................. #\n")
        f.write("# Mesh file generated by mshfile.py #\n")
        f.write("# ................................. #\n\n")
        
        f.write("# mesh name\n")
        f.write("mesh = %s\n" % name)
        
        f.write("\n# mesh geometry\n")
        f.write("size[0] = %.3f\n" % size0)
        f.write("size[1] = %.3f\n" % size1)
        f.write("size[2] = %.3f\n" % size2)
        
        f.write("\n# element type\n")
        f.write("Elem3D = %1d\n" % element)

        f.write("\n# mesh resolution\n")
        f.write("resolution[0] = %04d\n" % res)
        f.write("resolution[1] = %04d\n" % res)
        f.write("resolution[2] = %04d\n" % res)
        f.write("\n")
        
        f.close()
   
if __name__ == "__main__":
    
    mymesh = MeshFile(size0=2.0, size1=0.075, size2=0.075, element=1, resolution=10)
    mymesh.write_to_file()
    
    