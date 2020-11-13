"""
/hw4/code/genes.py

Written by Owen Morehead

Using sequence data to plot codon histogram and base pair density.

"""

import numpy as np
import matplotlib.pyplot as plt


def codonHistogram(geneString):
    """Function that traverses genome data as string and creates dictionary of each codon and its count
    """    
    histo = dict()  #create empty dictionary to hold codon pairs
        
    for i in range(0,(len(geneString)-3)): #final range value len(geneString) - 3 because we want to stop at  
                                           #the third from last character in string since last character is /n.
        char_threes = geneString[i] + geneString[i+1] + geneString[i+2]  #adding characters to make codon
        if char_threes not in histo:
            histo[char_threes] = 1   #append codon to dictionary 
        else:
            histo[char_threes] += 1 #if codon already in dictionary, add 1 to its value
    return histo
        
def plotHistogram(hist):
    """Functoin that plots the frequency of each codon in the SARS-CoV-2 sequence data
    """
    plt.figure(figsize=(12,6))
    plt.bar(range(len(hist)), hist.values())
    plt.xticks(range(len(hist)),labels=list(hist),rotation='vertical')
    plt.xlabel('Codon',fontSize = 12)
    plt.ylabel('Frequency',fontSize = 12)
    plt.title('Codon Frequency in SARS-CoV-2',fontSize = 15)
    plt.grid(True)
    plt.xlim([-1,len(hist)])
    #plt.show()
    plt.savefig('histogram.png')


def baseDensity(geneString,nWind=200):
    """Function that takes gene sequence as string and counts fraction of each base pair in window of width nWind.
    """
    a = np.zeros((len(geneString) - nWind))  #empty NumPy array for each base pair
    t = np.zeros((len(geneString) - nWind))
    c = np.zeros((len(geneString) - nWind))
    g = np.zeros((len(geneString) - nWind))
    for n in range(0,len(geneString) - nWind):
        a[n] = (geneString[n:n+nWind].count('a') / len(geneString[n:n+nWind]))  #count of base pair in window divided
        t[n] = (geneString[n:n+nWind].count('t') / len(geneString[n:n+nWind]))  #by length of the window
        c[n] = (geneString[n:n+nWind].count('c') / len(geneString[n:n+nWind]))
        g[n] = (geneString[n:n+nWind].count('g') / len(geneString[n:n+nWind]))
    return a,t,c,g

def densityPlot(da,dt,dc,dg):
    """Function that plots the density of the four base pairs in the gene sequence
    """
    plt.figure(figsize=(12,6))
    plt.plot(np.arange(0,len(da)),da[:])
    plt.plot(np.arange(0,len(dt)),dt[:])
    plt.plot(np.arange(0,len(dc)),dc[:])
    plt.plot(np.arange(0,len(dg)),dg[:])
    plt.title('Density of base pairs through gene sequence',fontSize = 15)
    plt.xlabel('Sequence position',fontSize = 12)
    plt.ylabel('Fraction per window',fontSize = 12)
    plt.grid(True)
    plt.legend(labels = ["A","T","C","G"])
    plt.savefig('density.png')
    

if __name__=="__main__":
    # Open genome
    with open('sarsCov2Sequence.txt','r') as geneFile:
        geneStr = geneFile.readline()
    #Generate codon histogram
    histo = codonHistogram(geneStr)
    #Plot histogram
    plotHistogram(histo)
    #Find base-pair density
    dA,dT,dC,dG = baseDensity(geneStr,nWind=500)
    # Or supply a different window width
    # dA,dT,dC,dG = baseDensity(geneStr, nWind=200)
    densityPlot(dA,dT,dC,dG)  #Plot density of base pairs
