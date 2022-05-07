# -*- coding: utf-8 -*-
"""
Created on Fri May  6 08:20:40 2022

@author: manon
"""

from exercice3_1 import *
from exercice3_2 import *

#%%
points =  initialize_map(npoints=10000)
idx1,idx2 = find_indx_beta(points,beta=0.4)
plot_map(points,beta=0.4,idx1=idx1,idx2=idx2)

#%%
updated_points = step(points,beta=0.4,alpha1=0.2,alpha2=0.5)

plot_map(updated_points,beta=0.4)

#%%

updated_points = step(updated_points,beta=0.4,alpha1=0.2,alpha2=0.5)

plot_map(updated_points,beta=0.4)

#%% do n steps
points =  initialize_map(npoints=50000)
points_nsteps = do_n_steps(6,points,beta=0.4,alpha1=0.3,alpha2=0.2)

#%% study two close points

study_two_close_points(npoints=50000,niters=1000,dist=1e-4,beta=0.4,alpha1=0.4,alpha2=0.5)



#%% EXERCICE 3.2

fractal_dim_img(points,10)