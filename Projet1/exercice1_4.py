# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 21:56:35 2022

@author: manon
"""

import numpy as np

nu=14.88e-6

def epsilon(data,Ls):
    epsilons = []
    for i, (df,L) in enumerate(zip(data,Ls)):
        epsilon = np.sqrt(df['Velocity'].var()**3)/(2*L)
        epsilons.append(epsilon)
    return epsilons

def Taylor_Reynolds(data,epsilons):
    Reynolds = []
    for i, (df,epsilon) in enumerate(zip(data,epsilons)):
        lmda = np.sqrt(15*nu*df['Velocity'].var()/epsilon)
        Reynold = np.sqrt(df['Velocity'].var())*lmda/nu
        Reynolds.append(Reynold)
    return Reynolds

def Outer_Reynolds(Ls,Umeans):
    Reynolds = []#Pk L?
    for i, (L,Umean) in enumerate(zip(Ls,Umeans)):
        Reynold = Umean*L/nu
        Reynolds.append(Reynold)
    return Reynolds


