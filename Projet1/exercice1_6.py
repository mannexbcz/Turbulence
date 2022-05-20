# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 13:46:03 2022

@author: manon
"""
import numpy as np
import matplotlib.pyplot as plt

freq = 20e3  # Sampling frequency = 20kHz
timestep = 1/freq


def velocity_increment(data, Umean, l):
    dl = Umean * timestep
    idx = round(l/dl)
    d = data['Velocity'].to_numpy()
    delta = d[idx:] - d[:-idx]
    x = data['x'].to_numpy()
    x = x[:-idx]
    return delta, x


def plotG(data, Umeans):
    means = []
    ls = [1e-3, 1e-2, 1e-1, 10]
    fig, ax = plt.subplots(4, 1,sharey=True,sharex=True,figsize=(5, 10))
    for i, l in enumerate(ls):
        delta, x = velocity_increment(data[0], Umeans[0], l)
        mean_delta = delta.mean()
        means.append(mean_delta)
        ax[i].plot(x[::100], delta[::100], label=f"l = {l:.2e}m")
        ax[i].plot(x[::100], np.ones_like(x[::100])*mean_delta, color = 'black', linestyle='--', label='$<\delta u_{||}> $')
        ax[i].legend(loc='upper right')
        #ax[i].set_title(r'$<\delta u_{||}> $')
        ax[i].set_xlabel("$x$ [m]")
        ax[i].set_ylabel("$\delta u_{||}(x, l)$")
        ax[i].grid()
    plt.savefig('plotG.eps', bbox_inches='tight', format='eps')
    plt.tight_layout()
    return means

def plot_distributions(data,Umeans):
    means=[]
    ls = [1e-3, 1e-2, 1e-1, 10]
    fig,ax = plt.subplots(2,2,sharex=True,figsize=(6, 5))
    for i, l in enumerate(ls):
        delta, x = velocity_increment(data[0], Umeans[0], l)
        mean_delta = delta.mean()
        means.append(mean_delta)
        if i == 0:
            I=J=0
        if i == 2:
            I = 1
            J = 0
        if i == 3:
            I=J=1
        if i == 1:
            I = 0
            J = 1
        ax[I,J].hist(delta,bins=200,label=f"l = {l:.2e}m")
        ax[I,J].legend()
        ax[I,J].set_xlabel("$\delta u_{||}$ [m]")
        ax[I,J].set_ylabel("Frequency")
        ax[I,J].grid()
    plt.tight_layout()
    plt.savefig('plotdistribution.eps', bbox_inches='tight', format='eps')
    
def flatness(delta):
    v4 = np.mean(delta**4)
    v2 = np.mean(delta**2)
    return v4/v2**2


def plotH(data,Umeans,ls):
    fs = []
    for i, l in enumerate(ls):
        delta, x = velocity_increment(data[0], Umeans[0], l)
        f = flatness(delta)
        fs.append(f)
    fig,ax = plt.subplots(figsize=(4.5, 3.5))
    ax.semilogx(ls,fs,color='tomato',label = r'$f(l)$')
    #flatness of a Gaussian = 3 (à revérifier)
    ax.semilogx(ls,3*np.ones_like(ls),color='k', ls='--',label=r'$f_\mathrm{gauss}=3$')
    ax.legend()
    ax.set_xlabel(r'$l$ [m]')
    ax.set_ylabel(r'$f$')
    ax.grid()
    plt.tight_layout()
    plt.savefig('plotH.eps', bbox_inches='tight', format='eps')
    