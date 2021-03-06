#!/usr/bin/env python

import numpy as np

def calculate_apd (data_file, perc=0.9):
    """
    APD90, ou seja, duracao do potencial de acao a 90% da fase de repolarizacao,
    calculado usando a diferenca entre o tempo de ativacao e o de repolarizacao.
    O tempo de ativacao e' o tempo de derivada maxima de um PA.
    O tempo de repolarizacao e' o instante em que o potencial da membrana atinge
    o nivel correspondente a 10% da amplitude do PA apos a ativacao.

    >>> filename='/home/rocha/src/pyUtils/testdata/test_apd.dat'
    >>> calculate_apd (filename)
    act_time: 001.0000 ms
    rep_time: 163.4500 ms
    APD     : 162.4500 ms
    162.44999999999999

    """
    data = np.loadtxt(data_file)            # format: %f %f \n (time voltage)
    tm = data[:,0]                          # time
    vm = data[:,1]                          # transmembrane potential
    
    ### find the activation time
    idmax = 0
    dvmax = 0.0
    dt = tm[1] - tm[0]
    size = len(vm)-1
    
    for i in xrange(size):
        dv = vm[i+1] - vm[i]
        if (dv > dvmax):
            dvmax = dv/dt
            idmax = i
            
    act_time = tm[idmax]
    
    amp = np.max(vm) - np.min(vm)           # find the AP amplitude
    
    #### find the repolarization time
    vchk = amp*(1.0-perc) + np.min(vm)
    stop = False
    for i in xrange(size):
        dv = vm[i+1] - vm[i]
        if ((dv<0.) and (vm[i] < vchk) and (not stop)):
            rep_time = tm[i]
            stop = True
    
    apd = np.abs(rep_time - act_time)       # calculate APD
    
    print 'act_time: %08.4f ms' % act_time
    print 'rep_time: %08.4f ms' % rep_time
    print 'APD     : %08.4f ms' % apd
    
    return apd
    
if __name__ == "__main__":
    
    import doctest
    doctest.testmod()

