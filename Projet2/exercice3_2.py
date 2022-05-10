# -*- coding: utf-8 -*-
"""
Created on Sat May  7 10:46:18 2022

@author: manon
"""

import numpy as np
import matplotlib.pyplot as plt
from rich.table import Table
from rich.console import Console

from exercice3_1 import *

    
def fractal_dim_numerical(points,nb, fig = True):
    Ns = []
    rs = []
    vals = np.logspace(0,2,nb)
    vals = vals.astype(int)
    for i,val in enumerate(vals):
        rs.append(val)
        H, _ = np.histogramdd(points,val)
        Ns.append(np.sum(H>0))
    rs_inv = np.array(rs)
    Ns = np.array(Ns)
    if fig:
        fig, ax = plt.subplots(figsize=(5,4))
        ax.loglog(rs_inv,Ns)
        ax.set_xlabel(r'$1/r$')
        ax.set_ylabel(r'$N(r)$')
    D0s,_,_,_,_ = np.polyfit(np.log(rs_inv),np.log(Ns),1, full=True)
    D0 = D0s[0]
    return D0

def fractal_dim_analytical(alpha):
    return 1-np.log(2)/np.log(alpha)

def compare_dims_different_alphas(npoints,nsteps,nbfit):
    alphas = [0.1,0.2,0.3,0.4,0.5]
    dims_an = []
    dims_num = []
    errs = []
    
    points =  initialize_map(npoints=npoints)
    
    table = Table(title="Fractal dimensions")
    table.add_column("alpha", justify="center")
    table.add_column("analytical value", justify="center")
    table.add_column("numerical value", justify="center")
    table.add_column("relative difference (%)", justify="center")
    
    for i, alpha in enumerate(alphas):
        points_nsteps = do_n_steps(nsteps,points,beta=0.4,alpha1=alpha,alpha2=alpha,fig=False)
        dim_an = fractal_dim_analytical(alpha)
        dim_num = fractal_dim_numerical(points_nsteps,nbfit, fig = False)
        dims_num.append(dim_num)
        dims_an.append(dim_an)
        errs.append((np.abs(dim_num-dim_an)/dim_an)*100)
    for i, (alpha, dim_an, dim_num, err) in enumerate(zip(alphas, dims_an, dims_num, errs)):
        table.add_row(f"{alpha:.1f}", f"{dim_an:.2f}", f"{dim_num:.2f}", f"{err:.2f}")
    
    console = Console()
    console.print(table)
    
    return dims_an, dims_num

  
    
