# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 07:33:16 2022

@author: manon
"""
'''
This script is used to run all exercices. Each exercise can 
be run separately by simply running the corresponding cell
'''
import pandas as pd

from read_data import *
from exercice1_1 import *
from exercice1_2 import *
from exercice1_3 import *
from exercice1_4 import *
from exercice1_5 import *
from exercice1_6 import *
from exercice1_7 import *

#%%

def save_energy_spectra(E_val, k_val):
    kname = "kvalues.dat"
    np.savetxt(kname, k_val)

    for i, e in enumerate(E_val):
        fname = f"Ek_A{i + 1}.dat"
        fpath = os.path.join(fname)
        np.savetxt(fpath, e)

def load_energy_spectra():
    kname = "kvalues.dat"
    #kpath = os.path.join(save_dir, kname)
    k_val = np.loadtxt(kname)

    E_val = []
    for i in range(6):
        
        fname = f"Ek_A{i + 1}.dat"
        fpath = os.path.join(fname)
        e = np.loadtxt(fname)
        E_val.append(e)

    return E_val, k_val


#%% Save Energy Spectra
save_energy_spectra(Energies, ks)
#%% Load Energy Spectra
Energies,ks = load_energy_spectra()

#%% Load data
data = read_data()

#%% Exercise 1.1

Umeans,Is = U_means(data)
data_x=x_from_time(data,Umeans)
plotA(data_x,Umeans)
plotA_zoom(data_x,Umeans)

#%% Exercise 1.2

data = read_data()
corrs =  autocorrelation(data,Umeans,lags=10000000)
Lcs, indexes = compute_corr_length(corrs,Umeans)
Lins_mean = compute_Lin(corrs,Umeans)
PlotB(corrs,Umeans)

#%% Exercise 1.3
ks100, Energies1500 = Energy(data_x,Lcs,indexes,Umeans)
plotC(ks,Energies)
P1,P2,err=Parseval(data,Energies500,ks500)

#%% Exercise 1.4

dissip_rates = epsilon(data,Ls)
TReynolds = Taylor_Reynolds(data,dissip_rates) 
OReynolds = Outer_Reynolds(Ls,Umeans)

#%% Exercise 1.5

KEnergies = kinetic_energy(data)
# First Method
d0_opt, h_opt = Energy_fitting(KEnergies,Umeans)

# Second Method
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
h_opt_3 = plotE(KEnergies,np.array(Lcs))
q_opt_3 = 2*h_opt_3/(1-h_opt_3)
d0s = np.linspace(0, 0.88, 100)
d0_opt_3 = plotED(KEnergies,ds,d0s,q_opt_3) #0.64

#Final plot, with optimal d0
d0s = np.linspace(0, 0.88, 7)
plotED_opt(KEnergies,ds,d0s,q_opt_3,d0_opt_3)

ks_smalls, Energies_smallk = Energy(data_x,Ls,indexes,Umeans)
plotF(ks100, Energies1500,h_opt,h_opt_2,h_opt_3)

#%% Exercise 1.6
means_deltas = plotG(data_x,Umeans)
plot_distributions(data_x,Umeans)
ls = np.logspace(-3,3,50)
plotH(data_x,Umeans,ls)

#%% Exercise 1.7
ls = np.logspace(-3,3,50)
plotI(data_x, Umeans,ls)
plotJ(data_x, Umeans,ls,KEnergies)
meanepsS2, meanepsS3 = plot_dissipation(data_x,Umeans,ls)

ls = np.logspace(-2,-1,50)
epsS2 = fitting_S2(data_x,Umeans,ls)
epsS3 = fitting_S3(data_x,Umeans,ls)