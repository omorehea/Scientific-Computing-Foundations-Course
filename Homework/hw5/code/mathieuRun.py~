#am129/hw5/code/mathieuRun.py
#Python script that calls the Mathieu Functions code and generates the eigenvalue plot
#Written by Owen Morehead

import os
import numpy as np
import matplotlib.pyplot as plt

def rebuild():
    #change into mathieu
    os.chdir('mathieu')
    #call make clean mathieu
    cmd1 = 'make clean mathieu'
    os.system(cmd1)
    #change back to code directory
    os.chdir('../')

def build():
    #Same as rebuild() except no clean in the make call
    os.chdir('mathieu')
    os.system('make mathieu')
    os.chdir('../')

def generate_input(N,q):
    #Backup and write init file
    if 'mathieu.init' in os.listdir('mathieu'):
        os.rename('mathieu/mathieu.init','mathieu/mathieu.init.bak')
    fp = open('mathieu/mathieu.init','w')
    fp.write('num_points ' + str(N) + '\n')
    fp.write('q_index ' + str(q) + '\n')
    fp.write('run_name Mathieu_' + str(N) +'_' + str(q))
    fp.close()

def run_mathieu(N,q):
    #Setup and run mathieu program
    build()
    generate_input(N,q)
    os.chdir('mathieu')
    os.system('./mathieu')
    os.chdir('../')

def parsweep_mathieu(N):
    #Range of q values to test
    qRange = np.arange(0,42,2)
    for q in qRange:
        run_mathieu(N,q)

def plot_parsweep(N,nPlot):
    #Set range and space to store data
    qRange = np.arange(0,42,2)
    evals = np.zeros([len(qRange),nPlot])
    #Open files and extract relevant data
    for idx,q in enumerate(qRange):
        fname = 'mathieu/data/Mathieu_' + str(N) + '_' + str(q) + '.dat'
        data = np.loadtxt(fname)
        evals[idx,:] = np.sort(data[:,1])[0:nPlot]
    #Generate a plot of eigenvalues as a function of parameter q
    plt.figure(figsize=(12,8))
    plt.plot(qRange,evals,'-k')
    a = lambda: [1 + q - (1/8)*q**2 - (1/64)*q**3 for q in range(0,42,2)]
    b = lambda: [4 - (1/12)*q**2 + (5/13824)*q**4 for q in range(0,42,2)]
    plt.plot(qRange,a(),'b-.',label='a(q)')
    plt.plot(qRange,b(),'b--',label='b(q)')
    plt.grid(True)
    plt.title('Eigenvalues as a funciton of q',fontsize=18)
    plt.xlabel('q',fontsize=14)
    plt.ylabel('Eigenvalues',fontsize=14)
    plt.legend()
    plt.show()

if __name__=="__main__":
   
    N = 101
    rebuild()
    parsweep_mathieu(N)
    plot_parsweep(N,7)


