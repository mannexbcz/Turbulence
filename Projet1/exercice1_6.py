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
    ls = [1e-3, 1e-2, 1e-1, 10]
    fig, ax = plt.subplots(4, 1,sharey=True,sharex=True,figsize=(5, 10))
    for i, l in enumerate(ls):
        delta, x = velocity_increment(data[0], Umeans[0], l)
        ax[i].plot(x, delta, label=f"l = {l:.2e}m")
        ax[i].legend()
        ax[i].set_xlabel("$x$ [m]")
        ax[i].set_ylabel("$\delta u_{||}(x, l)$")
        

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
    fig,ax = plt.subplots()
    ax.semilogx(ls,fs,color='tomato',label = r'$f(l)$')
    #flatness of a Gaussian = 3 (à revérifier)
    ax.semilogx(ls,3*np.ones_like(ls),color='k', ls='--',label=r'$f_\mathrm{gauss}=3$')
    ax.legend()
    ax.set_xlabel(r'$l$ [m]')
    ax.set_ylabel(r'$f$')