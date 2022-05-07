# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 15:47:44 2022

@author: manon
"""

import numpy as np
import matplotlib.pyplot as plt
from exercice1_6 import velocity_increment


def nth_structure_fct(n,delta):
    Sn =  np.mean(delta**n)
    return Sn

def plotI(data, Umeans,ls):
    S2s = []
    for i, l in enumerate(ls):
        delta, x = velocity_increment(data[0], Umeans[0], l)
        S2 = nth_structure_fct(2,delta)
        S2s.append(S2)
    fig,ax = plt.subplots()
    ax.semilogx(ls,S2s,color='blueviolet',label = r'$S_2(l)$')
    ax.semilogx(ls[0:25],ls[0:25]**(2/3), color='k',ls='--', label=r'$l^{2/3}$')
    ax.legend()
    ax.set_xlabel(r'$l$ [m]')
    ax.set_ylabel(r'$f$')
    
def plotJ(data, Umeans,ls,KEnergies):
    S3s = []
    for i, l in enumerate(ls):
        delta, x = velocity_increment(data[0], Umeans[0], l)
        S3 = nth_structure_fct(3,delta)
        S3s.append(S3)
    fig,ax = plt.subplots()
    ax.semilogx(ls,S3s,color='limegreen',label = r'$S_3(l)$')
    ax.semilogx(ls[0:25],(-4/5)*KEnergies[0]*ls[0:25],color='k',ls='--', label=r'4/5-law')
    ax.legend()
    ax.set_xlabel(r'$l$ [m]')
    ax.set_ylabel(r'$f$')