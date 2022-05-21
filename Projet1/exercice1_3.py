# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 20:09:40 2022

@author: manon
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import integrate
from scipy.signal import savgol_filter
from scipy.ndimage import gaussian_filter1d
freq = 20e3  # Sampling frequency = 20kHz
timestep = 1/freq 

def Energy_k(df,index,k,Umean):
    '''Comutes E(k)'''
    u = df.iloc[:,0]-Umean
    dx= Umean*timestep
    x = df.iloc[:,1]
    L=x[0]-x[-1:]
    Ek1 = 0.5*np.abs(1/np.sqrt(2*np.pi*L)*integrate.trapz(y=u*np.exp(-1j*k*x),x=x))**2 #dx=-Umean*timestep
    Ek2 = 0.5*np.abs(1/np.sqrt(2*np.pi*L)*integrate.trapz(y=u*np.exp(1j*k*x),x=x))**2   
    return Ek1+Ek2


def Energy(data,Ls,indexes,Umeans):
    '''Computes the Energy spectrum'''
    Energies = []
    ks = np.logspace(-7,-3,100)
    for j, (df,L,index,Umean) in enumerate(zip(data,Ls,indexes,Umeans)):
        Energy = np.zeros_like(ks)
        print(j) 
        
        for i,k in enumerate(ks):
                
            #print(i)
            Energy[i] = Energy_k(df,index,k,Umean)
            #Energy[i] = E(k,df.iloc[0:index,0]-Umean,Umean,freq)
        Energies.append(Energy)
    return ks, Energies

    

def plotC(ks, Energies):
    fig, ax = plt.subplots(figsize=(6, 4.5))
    for i, Energy in enumerate(Energies):
        Energy_smooth = savgol_filter(Energy, 11, 1) # local linear smoothing with Savitzky-Golay filter
        #Energy_smooth = gaussian_filter1d(Energy,50)
        ax.loglog(ks,Energy_smooth,label=r'$A_'+str(i+1)+'$')
    ax.loglog(ks,ks**(-5/3),color="black",linestyle="--",label=r'5/3-law')
    ax.vlines(x=[0.9], color='black',ymin=1e-12, ymax=2e5,ls='dotted',linewidth=2,label=r'$2\pi/L_\mathrm{int,E}$')
    ax.vlines(x=[600], color='black',ymin=1e-12, ymax=2e5,ls='dashdot',label=r'$2\pi/\eta_\mathrm{E}$')

    #plt.axvline(x=0.4, color='black')
    ax.legend(ncol=2,loc='upper right')
    ax.set_xlabel(r'$k$ [m$^{-1}$]')
    ax.set_ylabel(r'$E(k)$ [m$^3$s$^{-2}$]')
    ax.grid()
    plt.savefig('plotC.eps', format='eps')      

def Parseval(data,Energies,ks):
    P1s=[]
    P2s=[]
    errs=[]
    for i, (df, Energy) in enumerate(zip(data, Energies)):
        P1 = 0.5*df['Velocity'].var()
        P2 = integrate.trapz(Energy,ks)
        err=abs((P1-P2)/P1)
        P1s.append(P1)
        P2s.append(P2)
        errs.append(err)
        
        print(f"Anemometer {i}, P1={P1} P2={P2} relative error={err}")
    return P1s,P2s,errs