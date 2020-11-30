#Homework/hw6/code/dist.dat_plot.py
#Code written by Owen Morehead

#Extracting column data from file dist.dat and visualizing it in a plot.

import numpy as np
import matplotlib.pyplot as plt

gridpts = []
probs = []

with open('dist.dat','r') as f:
    d = f.readlines()
    for i in d:
        j,k = i.split()
        #print(j)
        #print(k)
        gridpts.append(float(j))
        probs.append(float(k))

def S(x):
    ps = 0.75*np.exp(-np.abs(x-0.25))
    return ps/np.sum(ps)

gridpts = np.array(gridpts)
probs = np.array(probs)

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
ax.plot(gridpts,probs,'k',label=r'$P_{part}(x)$')
ax.set_xlabel('x')
ax.set_ylabel('Probability')
ax.plot(gridpts,S(gridpts),'r--',label=r'$S(x)$')
ax.set_title(r'Stationary PMF of particle position (N=200, BIAS = 0.001)')
plt.grid(True)
plt.legend()
plt.show()


