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
    fig, ax = plt.subplots(figsize=(5, 4))
    for i, (corr,Umean) in enumerate(zip(corrs,Umeans)):
        deltal = Umean * timestep
        n = corr.size
        l = np.linspace(0,n*deltal,n)
        ax.plot(l[0:5000],corr[0:5000],label=r'$A_'+str(i+1)+'$')
    ax.plot(l[0:5000], np.ones_like(l[0:5000])/np.exp(1), color="dimgray", linestyle="--",label=r'$e^{-1}$')
    plt.vlines(x = 0.3666998544410602,ymin=-0.1, ymax=1/np.exp(1), color = "dimgray", linestyle=":", label = "$L_{C}$")
    plt.vlines(x = 0.6344775543132096,ymin=-0.1, ymax=1/np.exp(1), color = "dimgray", linestyle=":")
    plt.vlines(x = 0.7733063368560684,ymin=-0.1, ymax=1/np.exp(1), color = "dimgray", linestyle=":")
    plt.vlines(x = 0.9038678770166491,ymin=-0.1, ymax=1/np.exp(1), color = "dimgray", linestyle=":")
    plt.vlines(x = 1.0090931773879106,ymin=-0.1, ymax=1/np.exp(1), color = "dimgray", linestyle=":")
    plt.vlines(x = 1.0853295716563338,ymin=-0.1, ymax=1/np.exp(1), color = "dimgray", linestyle=":")
    plt.ylim([-0.1, 1.05])
    ax.legend()
    ax.set_xlabel(r'$l$ [m]')
    ax.set_ylabel(r'$C_l$')
    ax.grid()
    plt.savefig('plotB.eps', format='eps')
    
def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

def compute_Lin(corrs,Umeans):
    Lins=[]
    for i, (corr, Umean) in enumerate(zip(corrs,Umeans)): 
        means = moving_average(corr,2000)
        #meansequal0 = np.isclose(means,np.zeros_like(meantest), atol=1e-2)
        idx =  np.argmax(means<0, axis=0)
        #idx = np.argmax(corr<0, axis=0)
        L = integrate.trapz(corr[0:idx], dx = Umean*timestep)
        Lins.append(L)
    return Lins
        
        
        
        