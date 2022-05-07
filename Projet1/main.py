# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 07:25:00 2022

@author: manon
"""

from read_data import read_data
import pandas as pd

from exercice1_1 import *
from exercice1_2 import *
from exercice1_3 import *
from exercice1_4 import *
from exercice1_5 import *
from exercice1_6 import *
from exercice1_7 import *

#%% Load data
data = read_data()

#%% Exercise 1.1

Umeans,Is = U_means(data)
data_x=x_from_time(data,Umeans)
plotA(data_x)

#%% Exercise 1.2

data = read_data()
corrs =  autocorrelation(data,Umeans,lags=10000000)
Ls, indexes = compute_corr_length(corrs,Umeans)
PlotB(corrs,Umeans)
Lins = compute_Lin(corrs,Umeans)

#%% Exercise 1.3

ks, Energies = Energy(data_x,Ls,indexes,Umeans)
plotC(ks,Energies)
P1,P2,err=Parseval(data,Energies,ks)

#%% Exercise 1.4

dissip_rates = epsilon(data,Ls)
TReynolds = Taylor_Reynolds(data,dissip_rates) 
OReynolds = Outer_Reynolds(Ls,Umeans)

#%% Exercise 1.5

KEnergies = kinetic_energy(data)

# First Method
d0_opt, h_opt = Energy_fitting(KEnergies,Umeans)

#Second Method
ds = [1.0,2.0,3.0,4.0,5.0,6.0]
d0s = np.linspace(0, 0.99, 100)
q_est,resids = plotD(KEnergies,ds,d0s)

idx = np.argmin(resids)
d0_opt_2 = d0s[idx] #for 100 values between 0 and 1 : d0_opt_2 = 0.64
q_opt_2 = q_est[idx] #for 100 values between 0 and 1 : q_opt_2 = -1.20
h_opt_2 = q_opt_2/(q_opt_2+2) #h_opt_2 = -1.50

# Final plot, with optimal fit
d0s = np.linspace(0, 0.99, 7)
plotD_opt(KEnergies,ds,d0s,d0_opt_2,q_opt_2)                  

#Third Method

h_opt_3 = plotE(KEnergies,np.array(Ls))
q_opt_3 = 2*h_opt_3/(1-h_opt_3)
d0s = np.linspace(0, 0.99, 100)
d0_opt_3 = plotED(KEnergies,ds,d0s,q_opt_3) #0.64

#Final plot, with optimal d0
d0s = np.linspace(0, 0.99, 7)
plotED_opt(KEnergies,ds,d0s,q_opt_3,d0_opt_3)

plotF(ks, Energies,h_opt,h_opt_2,h_opt_3)

#%% Exercise 1.6

plotG(data_x,Umeans)
ls = np.logspace(-3,3,50)
plotH(data_x,Umeans,ls)

#%% Exercise 1.7

plotI(data_x, Umeans,ls)
#%%
plotJ(data_x, Umeans,ls,KEnergies)
