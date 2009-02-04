#!/usr/bin/env python

import os, sys, getopt
import subprocess
import glob 

ext = 'png'
pos = ('NW','N','NE','W','C','E','SW','S','SE')
imp = ('NorthWest', 'North', 'NorthEast', 'West', 'Center', 'East', 'SouthWest', 'South', 'SouthEast')

"""
A simple script to make a movie with a brand/logo

Bernardo M. Rocha, Gernot Plank
January 2009
"""

def brand_movie(base_name, logo_name, position):
  
  # create error and output log file
  outFile = os.path.join(os.curdir, "output.log")
  outptr = file(outFile, "w")
  
  errFile = os.path.join(os.curdir, "error.log")
  errptr = file(errFile, "w")
  
  # check position
  if position not in pos:
    print 'Error: the position %s is undefined.' % position
    sys.exit(1)
  
  for i in xrange(len(pos)):
    if position == pos[i]:
      imp_index = i
  
  im_position = imp[imp_index]
  
  # figure out list of files that match pattern 
  pattern = '%s*' % (base_name)
  file_list = glob.glob(pattern)
  file_list.sort()

  i = 0
  for f in file_list:
    print ' processing image %05d...' % (i)
   
    # use_composite (ImageMagick)
    dirname  = os.path.dirname(f)
    filename = os.path.basename(f) 
      
    if (dirname != ''):
      o = '%s/b_%s' % (dirname,filename)
    else:
      o = 'b_%s' % f

    cmd = ["composite", "-gravity", im_position, logo_name, f, o]
    retval = subprocess.call(cmd)      

    # convert to jpg first to strip alpha channel in pngs
    fnoext = filename.split('.')
    fnoext = fnoext[0]
    
    if (dirname != ''):
      ifile = '%s/b_%s' % (dirname,filename)
      ofile = '%s/b_%s.jpg' % (dirname,fnoext)
    else:
      ifile = 'b_%s' % (filename)
      ofile = 'b_%s.jpg' % (fnoext)

    cmd = ["convert", ifile, ofile]
    retval = subprocess.call(cmd)

    cmd = ["convert", ofile, ifile]
    retval = subprocess.call(cmd)
  
    i = i + 1
    
  # end of image range loop
    
  # write temporary file with filenames to convert into a movie
  temp_name = 'list.txt'
  fptr = open(temp_name,'w')
  for f in file_list:
    fptr.write('%s\n' % f)
  fptr.close()
  
  # execute mencoder
  cmd = ["mencoder", \
          "mf://@%s" % temp_name,\
          "-mf", "w=800:h=600:fps=25:type=png",\
          "-ovc" ,"lavc",\
          "-oac", "copy",\
          "-o", "output.avi"]
  retval = subprocess.call(cmd, 0, None, None, outptr, errptr)
   
  # check the process exit code
  if not retval == 0:
    errptr = file(errFile, "r")
    errData = errptr.read()
    errptr.close()
    raise Exception("Error executing command: " + repr(errData))
  else:
    os.remove(outFile)
    os.remove(errFile)

  # remove temporary list
  os.remove(temp_name)
  
# end of brand_movie

def check_retval(retval, errFile):
  if not retval == 0:
    errptr = file(errFile, "r")
    errData = errptr.read()
    errptr.close()
    raise Exception("Error executing command: " + repr(errData))
  
def print_help():
  print "\n Usage: brand_movie.py -b base_files -w logo_file -p watermark_position \n"
  print "\t positions: NW, N, NE, W, C, E, SW, S, SE\n"
 
def main(args):
  # default values
  logo_name = 'CARP_TextLogo_104x54.png'
  position  = 'SW'
  
  if len(args) == 1:
    print_help()
    sys.exit(1)
  
  # command line parsing with getopt
  try:
    opts, args = getopt.getopt(sys.argv[1:], "hb:w:p:",["help", "base=", "logo=","pos="])
  except getopt.GetoptError, err:
    print str(err)
    print_help()
    sys.exit(-1)
  
  for o, a in opts:
    if o in ("-h", "--help"):
      print_help()
      sys.exit()
    elif o in ("-b", "--base="):
      base_name = str(a)
    elif o in ("-w","--logo="):
      logo_name = str(a)
    elif o in ("-p","--pos="):
      position = str(a)
    else:
        assert False, "unhandled option"
        sys.exit(-1)
  # end of command line parsing  
  
  # call our fancy function
  brand_movie(base_name, logo_name, position)

if __name__ == "__main__":
  main(sys.argv)
