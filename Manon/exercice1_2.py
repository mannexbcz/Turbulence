# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 07:40:10 2022

@author: manon
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
from statsmodels.graphics import tsaplots
from scipy import integrate

freq = 20e3  # Sampling frequency = 20kHz
timestep = 1/freq 

#%%

def autocorrelation(data,Umeans,lags):
    corrs = []
    for i, (df,Umean) in enumerate(zip(data,Umeans)):
        corr = sm.tsa.acf(df-Umean,nlags=lags,fft=True,adjusted=True)
        corrs.append(corr)
    return corrs
   
def compute_corr_length(corrs,Umeans):
    Ls = []
    indexes = []
    for i, (corr, Umean) in enumerate(zip(corrs,Umeans)):
        index = (corr < 1/np.exp(1)).argmax()
        L = index*Umean/freq 
        Ls.append(L)
        indexes.append(index)
    return Ls, indexes

def PlotB(corrs,Umeans):
    fig, ax = plt.subplots(figsize=(7, 5))
    for i, (corr,Umean) in enumerate(zip(corrs,Umeans)):
        deltal = Umean * timestep
        n = corr.size
        l = np.linspace(0,n*deltal,n)
        ax.plot(l[0:5000],corr[0:5000],label=r'$A_'+str(i+1)+'$')
    ax.plot(l[0:5000], np.ones_like(l[0:5000])/np.exp(1), color="gray", linestyle="--",label=r'$e^{-1}$')
    ax.legend()
    ax.set_xlabel(r'$l$ [m]')
    ax.set_ylabel(r'$C_l$')
    ax.grid()
    
def compute_Lin(corrs,Umeans):
    Lins=[]
    for i, (corr, Umean) in enumerate(zip(corrs,Umeans)):     
        L = integrate.trapz(corr[0:5000], dx = Umean*timestep)
        Lins.append(L)
    return Lins
        
        
        
        