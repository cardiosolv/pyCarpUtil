#!/usr/bin/env python

import os, sys, pdb
import numpy, scipy, pylab
from fit_lambda import fit_lambda
from condVelocity import condVelocity

def isnan(x):
    return str(x) == 'nan'

if __name__ == "__main__":
    
    # declarations
    use_pyx = True
    
    resArray    = (10,25,50,100,200,250,500,750,1000)
    space_const = (894.42214823, 312.15803892, 79.11666987,
                   919.34206339, 313.74227759, 80.07370971,
                   669.32099569, 225.82278861, 59.50694777)        
    dirs = ('/data/sim/benchAntzCGtol_1e-6/experiment_ucla_long/cable-hexa/',
            '/data/sim/benchAntzCGtol_1e-6/experiment_ucla_trans/cable-hexa/',
            '/data/sim/benchAntzCGtol_1e-6/experiment_ucla_slow/cable-hexa/',
            '/data/sim/benchAntzCGtol_1e-6/experiment_tt2_long/cable-hexa/',
            '/data/sim/benchAntzCGtol_1e-6/experiment_tt2_trans/cable-hexa/',
            '/data/sim/benchAntzCGtol_1e-6/experiment_tt2_slow/cable-hexa/',
            '/data/sim/benchAntzCGtol_1e-6/experiment_lr2f_long/cable-hexa/',
            '/data/sim/benchAntzCGtol_1e-6/experiment_lr2f_trans/cable-hexa/',
            '/data/sim/benchAntzCGtol_1e-6/experiment_lr2f_slow/cable-hexa/')
    
    # filling cvArray
    arrSize = len(resArray)
    cvArray = numpy.zeros((arrSize,len(dirs)+1))
    for i in xrange(arrSize):
        cvArray[i][0] = resArray[i]

    # main loop
    i = 1
    for d in dirs:
        os.chdir(d)
        print "%s " % d
        j = 0
        for r in resArray:
            sim    = "t%04dum" % r
            simPts = sim + "/" + sim + "_i.pts"
            simAct = sim + "/" + "activation-thresh.dat"
                        
            if (os.path.isfile(simPts) != True):
                print " error calculateCV: file %s not found" + simPts
                exit(-1)
            
            if (os.path.isfile(simAct) != True):
                print " error calculateCV: file %s not found" + simAct
                exit(-1)
            
            ## calculate
            cv = condVelocity(simPts, simAct, output=False)
            cvArray[j][i] = cv
            j = j + 1           
        os.chdir("../../../")
        i = i + 1
      
    # plot UCLA_RAB
    ax1 = pylab.subplot(311)
    for i in xrange(0,3):
        x = cvArray[:,0]/space_const[i]
        y = cvArray[:,i+1]/cvArray[0,i+1]
        pylab.plot(x,y,linewidth=1.0)
    ax1.xaxis.set_major_locator(pylab.NullLocator())
    pylab.legend(('longitudinal', 'transverse', 'slow decremental'), 'upper right')
    pylab.title('UCLA_RAB - Hexa')

    # plot LRII_F
    ax2 = pylab.subplot(312)
    for i in xrange(6,9):
        x = cvArray[:,0]/space_const[i]
        y = cvArray[:,i+1]/cvArray[0,i+1]
        pylab.plot(x,y,linewidth=1.0)
    ax2.xaxis.set_major_locator(pylab.NullLocator())
    pylab.legend(('longitudinal', 'transverse', 'slow decremental'), 'upper right')
    pylab.title('LRII_F - Hexa')

    # plot TT2
    ax3 = pylab.subplot(313)
    for i in xrange(3,6):
        x = cvArray[:,0]/space_const[i]
        y = cvArray[:,i+1]/cvArray[0,i+1]
        pylab.plot(x,y,linewidth=1.0)    
    pylab.legend(('longitudinal', 'transverse', 'slow decremental'), 'upper right')
    pylab.title('TT2 - Hexa')
    pylab.xlabel('dx(um)')
    pylab.ylabel('velocity (m/s)')

    pylab.show()
    
    if (use_pyx):
        from pyx import *
        c = canvas.canvas()
        
        # ajusta titulos
        c.text(4, 17.15, r"LR2F", [text.halign.boxcenter]) 
        c.text(4, 11.15, r"TT2", [text.halign.boxcenter])  
        c.text(4, 5.15,  r"UCLA", [text.halign.boxcenter])
        
        # plot UCLA
        g1 = c.insert(graph.graphxy(width=8, x=graph.axis.linear(min=0, max=0.9),
                                             y=graph.axis.linear(min=0, max=1.0),
                                             key=graph.key.key(pos="bl", dist=0.1)))
        mydata=[]
        for i in xrange(0,3):
            x = cvArray[:,0]/space_const[i]
            y = cvArray[:,i+1]/cvArray[0,i+1]
            mydata.append(numpy.transpose([x,y]))
            
        g1.plot([graph.data.points(mydata[0], x=1, y=2, title='longitudinal'),
                 graph.data.points(mydata[1], x=1, y=2, title='transverse'),
                 graph.data.points(mydata[2], x=1, y=2, title='slow decremental')],
                [graph.style.line([color.gradient.Rainbow, style.linewidth.Thin, style.linestyle.solid])])

        # plot TT2
        g2 = c.insert(graph.graphxy(width=8, ypos=g1.height+1.0,
                                             x=graph.axis.linkedaxis(g1.axes["x"]),
                                             y=graph.axis.linear(min=0, max=1.0),
                                             key=graph.key.key(pos="bl", dist=0.1)))
        mydata=[]
        for i in xrange(3,6):
            x = cvArray[:,0]/space_const[i]
            y = cvArray[:,i+1]/cvArray[0,i+1]
            mydata.append(numpy.transpose([x,y]))

        g2.plot([graph.data.points(mydata[0], x=1, y=2, title='longitudinal'),
                 graph.data.points(mydata[1], x=1, y=2, title='transverse'),
                 graph.data.points(mydata[2], x=1, y=2, title='slow decremental')],
                [graph.style.line([color.gradient.Rainbow, style.linewidth.Thin, style.linestyle.solid])])
        
        # plot LRII_F
        g3 = c.insert(graph.graphxy(width=8, ypos=g1.height+7.0,
                                             x=graph.axis.linkedaxis(g1.axes["x"]),
                                             y=graph.axis.linear(min=0, max=1.0),
                                             key=graph.key.key(pos="bl", dist=0.1)))
        mydata=[]
        for i in xrange(6,9):
            x = cvArray[:,0]/space_const[i]
            y = cvArray[:,i+1]/cvArray[0,i+1]
            mydata.append(numpy.transpose([x,y]))

        g3.plot([graph.data.points(mydata[0], x=1, y=2, title='longitudinal'),
                 graph.data.points(mydata[1], x=1, y=2, title='transverse'),
                 graph.data.points(mydata[2], x=1, y=2, title='slow decremental')],
                [graph.style.line([color.gradient.Rainbow, style.linewidth.Thin, style.linestyle.solid])])
        
        print 'writing EPS file'
        c.writeEPSfile("pyx_plots")
        print 'writing PDF file'
        c.writePDFfile("pyx_plots")
