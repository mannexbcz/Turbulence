# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 15:47:44 2022

@author: manon
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from exercice1_6 import velocity_increment


def nth_structure_fct(n,delta):
    '''Computes the nth order structure function of delta'''
    Sn =  np.mean(delta**n)
    return Sn

def plotI(data, Umeans,ls):
    S2s = []
    for i, l in enumerate(ls):
        delta, x = velocity_increment(data[0], Umeans[0], l)
        S2 = nth_structure_fct(2,delta)
        S2s.append(S2)
    fig,ax = plt.subplots(figsize=(4.5, 3.5))
    ax.loglog(ls,S2s,color='blueviolet',label = r'$S_2(l)$')
    ax.loglog(ls[0:35],ls[0:35]**(2/3), color='k',ls='--', label=r'$l^{2/3}$')
    ax.legend()
    ax.set_xlabel(r'$l$ [m]')
    ax.set_ylabel(r'$S_2(l)$ [m$^2$]')
    ax.grid()
    plt.savefig('plotI.eps', bbox_inches='tight', format='eps')
    
def plotJ(data, Umeans,ls,KEnergies):
    S3s = []
    for i, l in enumerate(ls):
        delta, x = velocity_increment(data[0], Umeans[0], l)
        delta = -delta
        S3 = nth_structure_fct(3,delta)
        S3s.append(S3)
    fig,ax = plt.subplots(figsize=(4.5, 3.5))
    ax.semilogx(ls,S3s,color='limegreen',label = r'$S_3(l)$')
    ax.semilogx(ls[0:25],(-4/5)*KEnergies[0]*ls[0:25],color='k',ls='--', label=r'4/5-law')
    ax.legend()
    ax.set_xlabel(r'$l$ [m]')
    ax.set_ylabel(r'$S_3(l)$ [m$^3$]')
    ax.grid()
    plt.savefig('plotJ.eps', bbox_inches='tight', format='eps')


    
def plot_dissipation(data,Umeans,ls):
    epss=[]
    epss2=[]
    C2=2.2
    for i, l in enumerate(ls):
        delta, x = velocity_increment(data[0], Umeans[0], l)
        S2 = nth_structure_fct(2,delta)
        delta = -delta
        S3 = nth_structure_fct(3,delta) 
        eps = (1/l)*(S2/C2)**(3/2)
        eps2 = -(5/4)*(S3/l)
        epss.append(eps)
        epss2.append(eps2)
    fig,ax = plt.subplots(figsize=(5.5, 4))
    ax.semilogx(ls,epss,color='orange',label = r'$(1/l)(S_2(l)/C_2)^{3/2}$')
    ax.semilogx(ls,epss2,color='royalblue',label = r'$-(5/4)(S_3(l)/l)$')
    ax.semilogx(ls, np.ones_like(ls)*2.87, color='k', ls='dashed',label = r'Value from integral scale')
    ax.legend(loc='upper right')
    ax.set_xlabel(r'$l$ [m]')
    ax.set_ylabel(r'$\epsilon$ [m$^2$s$^{-3}$]')
    ax.grid()
    plt.savefig('plotdissipation.eps', bbox_inches='tight', format='eps')
    
    idx1 = np.argmin(np.abs(ls-np.ones_like(ls)*1e-2))
    idx2 = np.argmin(np.abs(ls-np.ones_like(ls)))
    
    meaneps = np.mean(epss[idx1:idx2])
    meaneps2 = np.mean(epss2[idx1:idx2])
    
    return meaneps,meaneps2


def compute_Sn(n,data,Umeans,ls):
    Sns = []
    for i, l in enumerate(ls):
        delta, x = velocity_increment(data[0], Umeans[0], l)
        delta = -delta
        Sn = nth_structure_fct(n,delta) 
        Sns.append(Sn)
        
    return Sns

def fitting_S2(data,Umeans,ls):
    S2fct = lambda l,eps: 2.2*(eps*l)**(2/3)
    
    S2vals = compute_Sn(2,data,Umeans,ls)

    bounds=([0],[np.inf])
    p0 = [0, 0]
    [epsS2], _ = curve_fit(S2fct,ls,S2vals, bounds=bounds)
    
    return epsS2

def fitting_S3(data,Umeans,ls):
    S3fct = lambda l,eps: -(4/5)*(eps*l)
    
    S3vals = compute_Sn(3,data,Umeans,ls)
    p0 = [0, 0]
    bounds=([0],[np.inf])
    
    [epsS3], _ = curve_fit(S3fct,ls,S3vals, bounds=bounds)
    
    return epsS3


    
    
    