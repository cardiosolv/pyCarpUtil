#!/usr/bin/env python

import matplotlib.pyplot as plt
from scipy import sparse
from pyUtils.sctools import read_binary_array

# Read from binary file the CSR Matrix

file_Ax = 'testdata/csr_matrix_Ax.bin'
file_Aj = 'testdata/csr_matrix_Aj.bin'
file_Ap = 'testdata/csr_matrix_Ap.bin'

Ax = read_binary_array (file_Ax,'f')
Aj = read_binary_array (file_Aj,'i')
Ap = read_binary_array (file_Ap,'i')

A = sparse.csr_matrix ((Ax,Aj,Ap))

plt.spy(A,marker='.')
plt.show()




