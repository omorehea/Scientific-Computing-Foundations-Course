#AM129 Final Project
#am129/Project/code/pyRun/fputRun.py
#Written by Owen Morehead
#Python script that calls the fput fortran code and generates plots

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import math

def rebuild():
    #change into fortran directory, currently in pyRun directory
    os.chdir('../')
    os.chdir('fortran')
    #call make clean fput
    os.system('make clean fput')
    #change back to code directory
    os.chdir('../')
    os.chdir('pyRun')
    print("done rebuilding")

def build():
    #Same as rebuild() except no clean in the make call
    os.chdir('../')
    os.chdir('fortran')
    os.system('make fput')
    os.chdir('../')
    os.chdir('pyRun')

def generate_input(N,alpha,C):
    #Backup and write init file
    os.chdir('../')  #Change back to code directory
    if 'fput.init' in os.listdir('fortran'):
        os.rename('fortran/fput.init','fortran/fput.init.bak')
    fp = open('fortran/fput.init','w')
    fp.write('num_masses '+ str(N) + '\n')
    fp.write('nonlinear_factor ' + str(alpha) + '\n')
    fp.write('correction_factor ' + str(C) + '\n')
    fp.write('run_name fput_' + str(N) + '_' + str(alpha) + '_' + str(C))
    fp.close()
    os.chdir('pyRun')

def run_fput(N,alpha,C):
    #Setup and run fput program
    build()
    generate_input(N,alpha,C)
    os.chdir('../')
    os.chdir('fortran')
    os.system('./fput')
    os.chdir('../')
    os.chdir('pyRun')

def n_1_plot_pta(C):
    #Plot for part a: exact and numerical solutions in time
    from scipy.interpolate import make_interp_spline, BSpline
    alpha = 0
    n1 = 1
    run_fput(n1,alpha,C)
    #Open file to extract relevant data
    os.chdir('../')
    fname = 'fortran/data/fput_' + str(n1) + '_' + str(alpha) + '_' + str(C) + '.dat'
    data = np.loadtxt(fname)
    n1valz = data[1,:]  #extracting 2nd row of data (first row holds dummy mass solutions)
    n1valzt = n1valz.reshape(1,len(data[1,:]))  #transpose data so all time solutions are in one row
   # timerange = np.arange(0,10*np.pi,(10*np.pi)/len(n1valzt[0,:]))
    timespace = np.linspace(0,10*np.pi,len(n1valzt[0,:]))
    f,ax = plt.subplots(figsize=(12,8))
    timerangenew = np.linspace(timespace.min(),timespace.max(),1500) #these three lines utilize scipy to plot
                                                                     #data as a smoother line
    spl = make_interp_spline(timespace, n1valzt[0,:],k=3)  
    power_smooth = spl(timerangenew)
    plt.plot(timerangenew, power_smooth,'r',label='numerical leapfrog solution')
   # plt.plot(timerange,n1valzt[0,:],'r',label='numerical leapfrog solution')
    timerange2new = np.linspace(0,10*np.pi,600)             #Same timerange but with more steps
    one_mass_soln = lambda: [(1/np.sqrt(32))*np.sin(np.sqrt(32)*t) for t in timerange2new]
    plt.plot(timerange2new,one_mass_soln(),'b-.',label='analytical solution')
    #Plotting construction and labels below
    plt.grid(True)
    plt.title('Numerical vs Analytical Solution for N = 1, C = 0.1',fontsize=18)
    plt.xlabel('t',fontsize=14)
    plt.ylabel('Amplitude',fontsize=14)
    plt.legend(loc='upper right')
    xtick = np.linspace(0,10*np.pi,11)   #11 steps in linspace because we include both end values
    xlabels = ['0',r'$\pi$',r'$2\pi$',r'$3\pi$',r'$4\pi$',r'$5\pi$',\
                   r'$6\pi$',r'$7\pi$',r'$8\pi$',r'$9\pi$',r'$10\pi$']
    plt.xticks(xtick,xlabels)
   # plt.xlim(0,20)  #uncomment to zoom in 
    plt.show()
    os.chdir('pyRun')

def n_sweep_fput_alpha_zero(C):
   #Range of N values to test
    alpha = 0
    Nrange = np.array([8,16,32])
    for n in Nrange:
        run_fput(n,alpha,C)      #Running the fortran code which generates the data file
#    print("Done running for all N values: ",Nrange)

def plot_n_sweep_ptb(C):
    #Plots for part b. This functions format is very similar to n_1_plot_pta(). 
    alpha = 0
    os.chdir('../')
    Nrange = np.array([8,16,32])                   #three values of N to test
    fig, axs = plt.subplots(3,2,figsize=(45,20)) 
    plt.subplots_adjust(hspace=0.4,wspace=0.4)
    fig.suptitle(r"Pt B,  $\alpha = 0$",fontsize='18')

    for idx, n in enumerate(Nrange):

        fname = 'fortran/data/fput_' + str(n) + '_' + str(alpha) + '_' + str(C) + '.dat'
        data = np.loadtxt(fname)
        print("Shape of data for N = %.2f is : "%n)
        print(data.shape)   #Data has dummy mass at each end which is why matrix row size is N+2
        timesolns = np.zeros(len(data[0,:]))
        ndiv2 = int(n/2)
        timesolns = data[ndiv2,:]
        timesolns = timesolns.reshape(1,len(timesolns))
        timerange = np.arange(0,10*np.pi,(10*np.pi)/len(timesolns[0,:]))
       # print(len(timesolns[0,:]))
        
        timesnaps = np.array([math.ceil(len(timesolns[0,:])/4),math.ceil(len(timesolns[0,:])/2), \
                                  math.ceil(len(timesolns[0,:])*3/4), math.ceil(len(timesolns[0,:])-1)])
        timelabels = np.array([r'$T_f/4$',r'$T_f/2$',r'$3T_f/4$',r'$T_f$'])
        for m,l in zip(timesnaps,timelabels):   #Running through each time snapshot and extracting data
            mass_ydata = data[1:-1,m]           #Dont want to use the ends of the column solutions (dummy masses)
            mass_ydata = mass_ydata.reshape(1,len(mass_ydata))
            mass_xdata = np.arange(1, n+1)
           # print(mass_ydata.shape)
           # print(mass_xdata.shape)
            axs[idx,0].plot(mass_xdata,mass_ydata[0,:],label=l) #subplots of mass data. Plotting for each timesnapshot.

        xtick = np.linspace(0,10*np.pi,11)   #11 steps in linspace because we include both end values           
        xlabels = ['0',r'$\pi$',r'$2\pi$',r'$3\pi$',r'$4\pi$',r'$5\pi$',\
                       r'$6\pi$',r'$7\pi$',r'$8\pi$',r'$9\pi$',r'$10\pi$']
        axs[idx,0].set_title('Snapshot of solution at specified time values for N = %.2f'%(n))
        axs[idx,0].set(xlabel='ith mass',ylabel='Displacement')
        axs[idx,0].legend(fontsize='medium',loc='upper right')
        axs[idx,1].plot(timerange,timesolns[0,:])               #subplots of time solution data for mass N/2
        axs[idx,1].set_title('Time solutions for the mass i = %.2f for N = %.2f'%(n/2,n))
        axs[idx,1].set(xlabel='t',ylabel='Amplitude')
        axs[idx,1].set_xticks(xtick)
        axs[idx,1].set_xticklabels(xlabels)
    plt.show()
    os.chdir('pyRun') #change back to pyRun directory after this funciton call is complete

def n_sweep_fput_alpha_nonzero(C):
   #Range of N values to test  
   #In change from the function n_sweep_fput_alpha_zero(), this function now generates alpha for each N.
    Nrange = np.array([8,16,32])
    for n in Nrange:
        alpha = n/10
        run_fput(n,alpha,C)

def plot_n_sweep_ptc(C):
    #Plots for part d      
    #Same function as for pt b but with minor changes to adjust for a nonzero value of alpha
    os.chdir('../')
    Nrange = np.array([8,16,32])
    fig, axs = plt.subplots(3,2,figsize=(45,20))
    plt.subplots_adjust(hspace=0.4,wspace=0.4)
    fig.suptitle(r"Pt C,  $\alpha = N/10$,  C = %.2f"%(C),fontsize='18')
    xtick = np.linspace(0,10*np.pi,11)   #11 steps in linspace because we include both end values                           
    xlabels = ['0',r'$\pi$',r'$2\pi$',r'$3\pi$',r'$4\pi$',r'$5\pi$',\
                   r'$6\pi$',r'$7\pi$',r'$8\pi$',r'$9\pi$',r'$10\pi$'] #x axis labels for time plots

    for idx, n in enumerate(Nrange):
        alpha = n/10
        fname = 'fortran/data/fput_' + str(n) + '_' + str(alpha) + '_' + str(C) + '.dat'
        data = np.loadtxt(fname)
        timesolns = np.zeros(len(data[0,:]))
        ndiv2 = int(n/2)
        timesolns = data[ndiv2,:]
        timesolns = timesolns.reshape(1,len(timesolns))
        timerange = np.arange(0,10*np.pi,(10*np.pi)/len(timesolns[0,:]))

        timesnaps = np.array([math.ceil(len(timesolns[0,:])/4),math.ceil(len(timesolns[0,:])/2), \
                                  math.ceil(len(timesolns[0,:])*3/4), math.ceil(len(timesolns[0,:])-1)])
        timelabels = np.array([r'$T_f/4$',r'$T_f/2$',r'$3T_f/4$',r'$T_f$'])
        for m,l in zip(timesnaps,timelabels):  #Running through each time snapshot and extracting relevant data
            mass_ydata = data[1:-1,m]          #Dont want to use the ends of the column solutions (dummy masses)           
            mass_ydata = mass_ydata.reshape(1,len(mass_ydata))
            mass_xdata = np.arange(1, n+1)
           # print(mass_ydata.shape)
           # print(mass_xdata.shape)
            axs[idx,0].plot(mass_xdata,mass_ydata[0,:],label=l)

        axs[idx,0].set_title('Snapshot of solution at specified time values for N = %.2f'%(n))
        axs[idx,0].set(xlabel='ith mass',ylabel='Displacement')
        axs[idx,0].legend(fontsize='medium',loc='upper right')
        axs[idx,1].plot(timerange,timesolns[0,:])
        axs[idx,1].set_title('Time solutions for the mass i = %.2f for N = %.2f'%(n/2,n))
        axs[idx,1].set(xlabel='t',ylabel='Amplitude')
        axs[idx,1].set_xticks(xtick)
        axs[idx,1].set_xticklabels(xlabels)

    plt.show()
    os.chdir('pyRun')

def n_sweep_fput_alpha_negative(C):
   #Range of N values to test                                                               
   #Now alpha is negative
    Nrange = np.array([8,16,32])
    for n in Nrange:
        alpha = -n/10
        run_fput(n,alpha,C)

def plot_n_sweep_pte(C):
    #Plots for part e                                                                                
    #Same function as for pt b and c but with minor changes to account for negative alpha(label changes and such)
    #This function and the one above are not quite necessary as the task of computing for negative alpha
    #can be done with much less code. I just copied the function above so that every question
    #(pt a, b, d, e) can be compiled and plots made all at once.
    os.chdir('../')
    Nrange = np.array([8,16,32])
    fig, axs = plt.subplots(3,2,figsize=(45,20))
    plt.subplots_adjust(hspace=0.4,wspace=0.4)
    fig.suptitle(r"Pt E,  $\alpha = -N/10$,  C = %.2f"%(C),fontsize='18')
    xtick = np.linspace(0,10*np.pi,11)   #11 steps in linspace because we include both end values                   
    xlabels = ['0',r'$\pi$',r'$2\pi$',r'$3\pi$',r'$4\pi$',r'$5\pi$',\
                   r'$6\pi$',r'$7\pi$',r'$8\pi$',r'$9\pi$',r'$10\pi$'] #x axis labels for time plots                    
    for idx, n in enumerate(Nrange):
        alpha = -n/10
        fname = 'fortran/data/fput_' + str(n) + '_' + str(alpha) + '_' + str(C) + '.dat'
        data = np.loadtxt(fname)
        timesolns = np.zeros(len(data[0,:]))
        ndiv2 = int(n/2)
        timesolns = data[ndiv2,:]
        timesolns = timesolns.reshape(1,len(timesolns))
        timerange = np.arange(0,10*np.pi,(10*np.pi)/len(timesolns[0,:]))
        timesnaps = np.array([math.ceil(len(timesolns[0,:])/4),math.ceil(len(timesolns[0,:])/2), \
                                  math.ceil(len(timesolns[0,:])*3/4), math.ceil(len(timesolns[0,:])-1)])
        timelabels = np.array([r'$T_f/4$',r'$T_f/2$',r'$3T_f/4$',r'$T_f$'])
        for m,l in zip(timesnaps,timelabels):
            mass_ydata = data[1:-1,m]   #Dont want to use the ends of the column solutions (dummy masses)                                                                                                       
            mass_ydata = mass_ydata.reshape(1,len(mass_ydata))
            mass_xdata = np.arange(1, n+1)
           # print(mass_ydata.shape)
           # print(mass_xdata.shape)
            axs[idx,0].plot(mass_xdata,mass_ydata[0,:],label=l)

        axs[idx,0].set_title('Snapshot of solution at specified time values for N = %.2f'%(n))
        axs[idx,0].set(xlabel='ith mass',ylabel='Displacement')
        axs[idx,0].legend(fontsize='medium',loc='upper right')
        axs[idx,1].plot(timerange,timesolns[0,:])
        axs[idx,1].set_title('Time solutions for the mass i = %.2f for N = %.2f'%(n/2,n))
        axs[idx,1].set(xlabel='t',ylabel='Amplitude')
        axs[idx,1].set_xticks(xtick)
        axs[idx,1].set_xticklabels(xlabels)
    plt.show()
    os.chdir('pyRun')

def modal_decomp(C):
    #Extra credit part: Modal decomposition
    #Matrix T is generated and the product T*x^n is calculated for the first M = 4 modes
    #for the same 3 values of N used in the previous parts.
    
    os.chdir('../')
    Nrange = np.array([8,16,32])
    fig, axs = plt.subplots(1,3,figsize=(30,20))
    plt.subplots_adjust(hspace=0.4,wspace=0.4)
    fig.suptitle(r"Modal Decomposition Plots,  $\alpha = N/10$,  C = %.2f"%(C),fontsize='18')
    Mrange = np.array([1,2,3,4])
    xtick = np.linspace(0,10*np.pi,11) 
    xlabels = ['0',r'$\pi$',r'$2\pi$',r'$3\pi$',r'$4\pi$',r'$5\pi$',\
                   r'$6\pi$',r'$7\pi$',r'$8\pi$',r'$9\pi$',r'$10\pi$'] #x axis labels for time plots                    

    for idx, n in enumerate(Nrange):
        alpha = n/10
        T = np.zeros([len(Mrange),n])
        fname = 'fortran/data/fput_' + str(n) + '_' + str(alpha) + '_' + str(C) + '.dat'
        data = np.loadtxt(fname)   
       # print("Shape of data is:", data.shape)
        alltimesolns = np.zeros([n,len(data[0,:])])
        alltimesolns = data[1:-1,:]  #all the data excluding the two dummy mass time solutions
        alltimesolns = alltimesolns.reshape(n,len(alltimesolns[0,:]))
       # print("Python extracted data shape: ", alltimesolns.shape)
        js = np.arange(0,n,1)
        for i in Mrange:    #Filling the matrix T
            for j in js:
                T[i-1,j] = 2/(n + 2)*np.sin(i*np.pi*((j+1)/(n+1)))

        productmatrix = np.matmul(T,alltimesolns) 
        
       # print("Shape of Matrix product T*alltimesolns is: ",productmatrix.shape)
       # print("Shape of one row of productmatrix: ",productmatrix[0,:].shape)
       # timespace = np.arange(0,10*np.pi,(10*np.pi)/len(productmatrix[0,:]))
        timespace = np.linspace(0,10*np.pi,len(productmatrix[0,:]))
       # print("Size of timespace array: ", timespace.size)
        
        for ll,m in enumerate(Mrange):

           # productmatrix = productmatrix.reshape(len(Mrange),len(productmatrix[0,:]))
            axs[idx].plot(timespace,productmatrix[ll,:],label="Mode M = %.2f"%(m))
           # print(productmatrix[:,10:15])

        axs[idx].set_title('Amplitude of Modes over time for N = %.2f'%(n))
        axs[idx].set(xlabel='t',ylabel='Amplitude')
        axs[idx].legend(fontsize='medium',loc='upper right')
        axs[idx].set_xticks(xtick)
        axs[idx].set_xticklabels(xlabels)
       # axs[idx].set_xlim(0,20)
    plt.show()
    os.chdir('pyRun')
   
    
if __name__=="__main__":
    
    C = 1.0       
    rebuild()
    n_1_plot_pta(C)                 #Plot for part a
 
    C = 1.0
    n_sweep_fput_alpha_zero(C)
    plot_n_sweep_ptb(C)             #Plot for part b
 
    C = 0.5
    n_sweep_fput_alpha_nonzero(C)  
    plot_n_sweep_ptc(C)             #Plot for part c
    
    n_sweep_fput_alpha_negative(C)
    plot_n_sweep_pte(C)             #Plot for part e
   
    C = 0.5
    modal_decomp(C)                 #Modal Decomposition Plots            
 
