# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 22:33:14 2022

@author: manon
"""

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

freq = 20e3  # Sampling frequency = 20kHz
timestep = 1/freq 


def kinetic_energy(data):
    Es=[]
    for i, df in enumerate(data):
        E = 1.5*df['Velocity'].var()
        Es.append(E)
    return Es

def Energy_fitting(KEnergies,Umeans):
    Efct = lambda d,C,d0,q: C*(d - d0)**q #(2*h/(1-h))
    ds = [1.0,2.0,3.0,4.0,5.0,6.0]
    
    # Bounds for d0 and h
    bounds=([-np.inf,-np.inf,-np.inf],[np.inf,1,np.inf])
    
    [C_opt,d0_opt,q_opt], _ = curve_fit(Efct,ds,KEnergies, bounds=bounds)
    
    #d0_opt = opt_vals[0]
    #q_opt = opt_vals[1]
    h_opt = q_opt/(q_opt+2)
    #h_opt = opt_vals[1]
    return d0_opt, h_opt


def plotD(KEnergies,ds,d0s):
    fig, ax = plt.subplots(figsize=(4.5, 3.5))
    q_est = []
    resids = []
    for d0 in d0s:
        ax.loglog(ds-d0,KEnergies,label=f'$d_0=${d0:.3f}')
        q,res,_,_,_ = np.polyfit(np.log(ds-d0),np.log(KEnergies),1, full=True)
        q_est.append(q[0])
        resids.append(res[0])
    #ax.legend()
    ax.set_xlabel(r"$d - d_0$")
    ax.set_ylabel(r"$\mathcal{E}$")
    ax.grid()
    plt.tight_layout()

    #print(resids)
    return q_est,resids

def plotD_opt(KEnergies,ds,d0s,d0_opt,q_opt):
    fig, ax = plt.subplots(figsize=(4.5, 3.5))
    q_est = []
    resids = []
    for d0 in d0s:
        ax.loglog(ds-d0,KEnergies,alpha=0.7,label=f'$d_0=${d0:.3f}')
        q,res,_,_,_ = np.polyfit(np.log(ds-d0),np.log(KEnergies),1, full=True)
        q_est.append(q[0])
        resids.append(res[0])
    ax.loglog(ds-d0_opt,KEnergies,color='black',alpha=1,label=f'$d_0=${d0_opt:.3f}')
    ax.loglog(ds-d0_opt,(ds-d0_opt)**q_opt,alpha=1,color='black', ls='--',label=r'$(d-d_0)^{-1.20}$')
    ax.legend()
    ax.set_xlabel(r"$d - d_0$ [m]")
    ax.set_ylabel(r"$\mathcal{E}$ [m$^2$s$^{-2}$]")
    ax.grid()
    plt.ylim([0.1, 2])
    plt.tight_layout()
    plt.savefig('plotD.eps', bbox_inches='tight', format='eps')
    
    #print(resids)
    return q_est,resids 
    

def plotE(KEnergies,Ls):
    fig, ax = plt.subplots(figsize=(4.5, 3.5))
    ax.loglog(Ls,KEnergies,color='black',label=r'$\mathcal{E}$')
    H = np.polyfit(np.log(Ls),np.log(KEnergies),1)
    ax.loglog(Ls,Ls**-3, label = r'Saffman’s decay')
    ax.loglog(Ls,Ls**-5, label = r'Loitsyanskii’s decay')
    ax.loglog(Ls,Ls**-2, label = r'Self-similar decay')
    ax.loglog(Ls,Ls**H[0],color='black', ls='--', label=r'$L_c^{-2.984}$')
    ax.legend()
    ax.set_xlabel(r"$L_c$ [m]")
    ax.set_ylabel(r"$\mathcal{E}$ [m$^2$s$^{-2}$]")
    ax.grid()
    #plt.ylim([0.1, 2])
    plt.tight_layout()
    plt.savefig('plotE.eps', bbox_inches='tight', format='eps')
    
    return H[0]/2
 
def plotED(KEnergies,ds,d0s,qth):
    fig, ax = plt.subplots()
    resids = []
    for d0 in d0s:
        ax.plot((ds-d0)**qth,KEnergies,label=f'$d_0=${d0:.3f}')
        # to find optimal d0, one minimizes the residual of linar fit between 
        # log(Kenergies) and log(ds-d0)**qth)
        _,res,_,_,_ = np.polyfit((ds-d0)**qth,KEnergies,1, full=True)
        resids.append(res)
    ax.legend()
    ax.set_xlabel(r"$(d - d_0)^\mathrm{q_{th}}$ [m$^{q_{th}}$]")
    ax.set_ylabel(r"$\mathcal{E}$ [m$^2$s$^{-2}$]")
    idx = np.argmin(resids)
    d0_opt = d0s[idx]
    return d0_opt

def plotED_opt(KEnergies,ds,d0s,qth,d0_opt):
    fig, ax = plt.subplots(figsize=(4.5, 3.5))
    for d0 in d0s:
        ax.plot((ds-d0)**qth,KEnergies,alpha=0.7,label=f'$d_0=${d0:.3f}')
    ax.plot((ds-d0_opt)**qth,KEnergies,color='black',alpha=1,label=f'$d_0=${d0_opt:.3f}')
    ax.legend()
    ax.set_xlabel(r"$(d - d_0)^\mathrm{q_{th}}$ [m$^{q_{th}}$]")
    ax.set_ylabel(r"$\mathcal{E}$ [m$^2$s$^{-2}$]")
    ax.grid()
    #plt.ylim([0.1, 2])
    plt.tight_layout()
    plt.savefig('plotED.eps', bbox_inches='tight', format='eps')
    


def plotF(ks, Energies,h_opt1,h_opt2,h_opt3):
    fig, ax = plt.subplots(figsize=(5, 4))
    
    for i, Energy in enumerate(Energies):
        Energy_smooth = savgol_filter(Energy, 11, 1) # local linear smoothing with Savitzky-Golay filter
        #Energy_smooth = gaussian_filter1d(Energy,50)
        ax.loglog(ks,Energy_smooth,label=r'$A_'+str(i+1)+'$')
    ax.loglog(ks, ks**-(1+2*h_opt1),color='black',ls='dashed',label=r'$k^{-(1+2h_\mathrm{opt})}$')
    #ax.loglog(ks, ks**-(1+2*h_opt2),label=r'Method 2')
    #ax.loglog(ks, ks**-(1+2*h_opt3),label=r'Method 3')
    #plt.axvline(x=0.4, color='black')
    ax.legend(ncol=2,loc='upper left')
    ax.set_xlabel(r'$k$ [m$^{-1}$]')
    ax.set_ylabel(r'$E(k)$ [m$^3$s$^{-2}$]')
    ax.grid()
    plt.tight_layout()
    plt.savefig('plotF.eps', bbox_inches='tight', format='eps')
    

