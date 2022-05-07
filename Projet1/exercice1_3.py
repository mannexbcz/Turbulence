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

def Energy_k(df,index,L,k,Umean):
    #x = df.iloc[0:index,1]
    u = df.iloc[0:100000,0]-Umean
    #dx= Umean*timestep
    x = df.iloc[0:100000,1]
    #L=x[-1]
    Ek1 = 0.5*np.abs(1/np.sqrt(2*np.pi*L)*integrate.trapz(u*np.exp(-1j*k*x),dx=-Umean*timestep))**2
    Ek2 = 0.5*np.abs(1/np.sqrt(2*np.pi*L)*integrate.trapz(u*np.exp(1j*k*x),dx=-Umean*timestep))**2   
    
    return Ek1+Ek2


def Energy(data,Ls,indexes,Umeans):
    Energies = []
    ks = np.logspace(-2,4,100)
    for j, (df,L,index,Umean) in enumerate(zip(data,Ls,indexes,Umeans)):
        Energy = np.zeros_like(ks)
        print(j)
        for i,k in enumerate(ks):
            #print(i)
            Energy[i] = Energy_k(df,index,L,k,Umean)
            #Energy[i] = E(k,df.iloc[0:index,0]-Umean,Umean,freq)
        Energies.append(Energy)
    return ks, Energies


def plotC(ks, Energies):
    fig, ax = plt.subplots(figsize=(7, 5))
    for i, Energy in enumerate(Energies):
        Energy_smooth = savgol_filter(Energy, 7, 1) # local linear smoothing with Savitzky-Golay filter
        #Energy_smooth = gaussian_filter1d(Energy,50)
        ax.loglog(ks,Energy_smooth,label=r'$A_'+str(i+1)+'$')
    ax.loglog(ks,ks**(-5/3),color="black",linestyle="--",label=r'5/3-law')
    ax.vlines(x=[0.4], color='black',ymin=1e-10, ymax=5e3,ls=(0, (3, 1, 1, 1, 1, 1)),label=r'$L_\mathrm{int,E}$')
    ax.vlines(x=[800], color='black',ymin=1e-10, ymax=5e3,ls=(0, (3, 1, 1, 1)),label=r'$\eta_\mathrm{E}$')

    #plt.axvline(x=0.4, color='black')
    ax.legend()
    ax.set_xlabel(r'$k$')
    ax.set_ylabel(r'$E(k)$')
    ax.grid()
            

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