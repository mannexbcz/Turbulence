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
    '''Computes the mean velocity for each anemometer'''
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
    '''Using Taylor Flow hypothesis, computes the spatial upstream
    distance from the time series'''
    xs = []
    data_x = data
    for i, (df, Umean) in enumerate(zip(data_x, Umeans)):
        n = len(df)
        time = np.linspace(0,n*timestep,n)
        df['x'] = -Umean * time
    return data_x

def plotA(data_x,Umeans): 
    fig, ax = plt.subplots(2,3,sharey=True,figsize=(7, 6))
    
    for i, df in enumerate(data_x):
        if i == 0:
            I=J=0
        if i == 1:
            I=0
            J=1
        if i == 2:
            I=0
            J=2
        if i == 3:
            I=1
            J=0
        if i == 4:
            I=J=1
        if i == 5:
            I=1
            J=2
        ax[I,J].plot(df['x'],df['Velocity'], label = '$A_'+str(i+1)+'$')
        ax[I,J].plot(df['x'],np.ones_like(df['x'])*Umeans[i], color='black',linestyle='--', label='$\langle u \rangle$')
        #ax[I,J].set_title(r'$A_'+str(i+1)+'$')
        ax[I,J].legend( loc='upper right')
        ax[I,J].set_xlabel(r'$x$ [m]')
        ax[I,J].set_ylabel(r'$u_{\mathrm{tot}}$ [m/s]')
        ax[I,J].grid()
        
    plt.savefig('plotA.eps', format='eps')
    #fig.savefig('')
    
def plotA_zoom(data_x,Umeans):
    fig, ax = plt.subplots(figsize=(6, 4))
    for i, df in enumerate(data_x):
        ax.plot(df['x'].iloc[0:8000],df['Velocity'].iloc[0:8000], label = '$A_'+str(i+1)+'$')
    ax.legend( loc='upper left')
    ax.set_xlabel(r'Upstream distance $x$ [m]')
    ax.set_ylabel(r'$u_{\mathrm{tot}}$ [m/s]')
    ax.grid()
    plt.savefig('plotAZoom.eps', format='eps')
