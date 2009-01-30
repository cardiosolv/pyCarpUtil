#!/usr/bin/env python

import os, sys, getopt
import subprocess
import glob 

ext = 'png'
pos = ('NW','N','NE','W','C','E','SW','S','SE')
imp = ('NorthWest', 'North', 'NorthEast', 'West', 'Center', 'East', 'SouthWest', 'South', 'SouthEast')

"""
A simple script to make a movie with a brand/logo
"""

def brand_movie(base_name, logo_name, position):
  
  # extract file name and directory
  dirname  = os.path.dirname(base_name)
  filename = os.path.basename(base_name) 
  
  # create error and output log file
  outFile = os.path.join(os.curdir, "output.log")
  outptr = file(outFile, "w")
  
  errFile = os.path.join(os.curdir, "error.log")
  errptr = file(errFile, "w")
  
  # NorthWest, North, NorthEast, West, Center, East, SouthWest, South, SouthEast
  # NW, N, NE, W, C, E, SW, S, SE
  if position not in pos:
    print 'Error: the position %s is undefined.' % position
    sys.exit(1)
  
  for i in xrange(len(pos)):
    if position == pos[i]:
      imp_index = i
  
  im_position = imp[imp_index]
  
  # figure out list of files that match pattern 
  pat = '%s*' % (base_name)
  lst = glob.glob(pat);
  inc = 2
  images_range = xrange(0,len(lst),inc)
  
  list_name = 'list.txt'
  file_list = open(list_name,'w')
   
  for i in images_range:
    print ' processing image %05d...' % (i)
    
    # use_composite (ImageMagick)
    if (dirname != ''):
      f = '%s/%s%05d.%s'   % (dirname,filename,i,ext)
      o = '%s/b_%s%05d.%s' % (dirname,filename,i,ext)
    else:
      f = '%s%05d.%s' % (filename,i,ext)
      o = 'b_%s' % f
   
    cmd = ["composite", "-gravity", im_position, logo_name, f, o]
    retval = subprocess.call(cmd)      
    
    # convert to jpg first to strip alpha channel in pngs
    if (dirname != ''):
      ifile = '%s/b_%s%05d.png' % (dirname,filename,i)
      ofile = '%s/b_%s%05d.jpg' % (dirname,filename,i)
    else:
      ifile = 'b_%s%05d.png' % (filename,i)
      ofile = 'b_%s%05d.jpg' % (filename,i)

    cmd = ["convert", ifile, ofile]
    retval = subprocess.call(cmd)
    
    cmd = ["convert", ofile, ifile]
    retval = subprocess.call(cmd)
    
    file_list.write('%s\n' % (ifile))
    
  # end of image range loop
    
  # finally convert to a movie  
  file_list.close()
  
  # execute mencoder
  cmd = ["mencoder", \
          "mf://@%s" % list_name,\
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
  os.remove(list_name)
  
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
