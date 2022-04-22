# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 16:42:35 2022

@author: manon
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from read_data import read_data

freq = 20e3  # Sampling frequency = 20kHz
timestep = 1/freq 

#%%
def U_means(data):
    Umeans = []
    Is = []
    for i, df in enumerate(data):
        Umean = df['Velocity'].mean()
        Ustd = np.std(df['Velocity'] - Umean)
        I = Ustd/Umean
        
        Umeans.append(Umean)
        Is.append(I)
    return Umeans, Is

def x_from_time(data,Umeans):
    xs = []
    data_x = data
    for i, (df, Umean) in enumerate(zip(data_x, Umeans)):
        n = len(df)
        time = np.linspace(0,n*timestep,n)
        df['x'] = -Umean * time + i+1
        #i+1 : ajoute le décalage spatial des sondes
    return data_x

def plotA(data_x): 
    fig, ax = plt.subplots(2,3,sharey=True,figsize=(10, 8))
    
    for i, df in enumerate(data_x):
        I = i % 2
        J = i % 3
        ax[I,J].plot(df['x'],df['Velocity'])
        ax[I,J].set_title(r'$A_'+str(i+1)+'$')
        ax[I,J].set_xlabel(r'$x$ [m]')
        ax[I,J].set_ylabel(r'$u_{\mathrm{tot}}$ [m/s]')
        ax[I,J].grid()
    #fig.savefig('')
    
