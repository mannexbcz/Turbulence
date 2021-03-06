# -*- coding: utf-8 -*-
"""
Created on Fri May  6 08:20:40 2022

@author: manon
"""

'''
This script is used to run all exercices. Each exercise can 
be run separately by simply running the corresponding cell
'''

from exercice3_1 import *
from exercice3_2 import *
from exercice3_3 import *

#%% Exercice 3.1
# Initial configuration
points =  initialize_map(npoints=50000)
idx1,idx2 = find_indx_beta(points,beta=0.4)
plot_map(points,beta=0.4,idx1=idx1,idx2=idx2)

# After 1 step
updated_points = step(points,beta=0.4,alpha1=0.2,alpha2=0.5)
plot_map(updated_points,beta=0.4)

# After n steps
points =  initialize_map(npoints=50000)
points_nsteps = do_n_steps(2000,points,beta=0.4,alpha1=0.4,alpha2=0.4)

# study two close points after niters
study_two_close_points(npoints=50000,niters=1000,dist=1e-4,beta=0.4,alpha1=0.4,alpha2=0.5)

#%% EXERCICE 3.2
#Fractal dimension
D0,_,_ = fractal_dim_numerical(points_nsteps,100)

# For different values of alpha
dims_an, dims_num = compare_dims_different_alphas(npoints=50000,nsteps=2000,nbfit=100)

#%% EXERCICE 3.3

comparison_lyapunov_exponents(ntrials=1000,nsteps=10,epsilon0=1e-5)
    