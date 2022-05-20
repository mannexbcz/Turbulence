# -*- coding: utf-8 -*-
"""
Created on Sat May  7 10:46:18 2022

@author: manon
"""

import numpy as np
import matplotlib.pyplot as plt
from rich.table import Table
from rich.console import Console
from cycler import cycler

from exercice3_1 import *

    
def fractal_dim_numerical(points,nb, fig = True):
    Ns = []
    rs = []
    vals = np.logspace(0,4,nb)
    vals = vals.astype(int)
    for i,val in enumerate(vals):
        rs.append(val)
        H, _ = np.histogramdd(points,val)
        Ns.append(np.sum(H>0))
    rs_inv = np.array(rs)
    Ns = np.array(Ns)
    D0s,_,_,_,_ = np.polyfit(np.log(rs_inv),np.log(Ns),1, full=True)
    D0 = D0s[0]
    if fig:
        fig, ax = plt.subplots(figsize=(5,4))
        ax.loglog(rs_inv,Ns, marker = '+', ls = 'dashed', markerfacecolor='k')
        ax.set_xlabel(r'$1/r$')
        ax.set_ylabel(r'$N(r)$')
            
    return D0,rs_inv,Ns

def fractal_dim_analytical(alpha):
    return 1-np.log(2)/np.log(alpha)



def compare_dims_different_alphas(npoints,nsteps,nbfit):
    alphas = [0.1,0.2,0.3,0.4,0.5]
    #alphas = [0.1,0.2]
    dims_an = []
    dims_num = []
    errs = []
    
    points =  initialize_map(npoints=npoints)
    
    table = Table(title="Fractal dimensions")
    table.add_column("alpha", justify="center")
    table.add_column("analytical value", justify="center")
    table.add_column("numerical value", justify="center")
    table.add_column("relative difference (%)", justify="center")
    custom_cycler = (cycler(color=['tab:blue', 'tab:orange', 'tab:green', 'tab:red','tab:purple']))
    fig, ax = plt.subplots(figsize=(7,4))
    ax.set_prop_cycle(custom_cycler)
    for i, alpha in enumerate(alphas):
        points_nsteps = do_n_steps(nsteps,points,beta=0.4,alpha1=alpha,alpha2=alpha,fig=False)
        dim_an = fractal_dim_analytical(alpha)
        dim_num,rs_inv,Ns = fractal_dim_numerical(points_nsteps,nbfit, fig = False)
        dims_num.append(dim_num)
        dims_an.append(dim_an)
        errs.append((np.abs(dim_num-dim_an)/dim_an)*100)
        ax.semilogx(rs_inv,np.log(Ns)/np.log(rs_inv),label=rf" $\alpha =$ {alpha:.1f}")
        
    
    #fig.gca().set_color_cycle(None)
    for i, alpha in enumerate(alphas):
        dim_an = fractal_dim_analytical(alpha)
        ax.semilogx(rs_inv,np.ones_like(rs_inv)*dim_an, ls='dashed',label=rf" $\alpha =$ {alpha:.1f}, analytical")
    ax.set_xlabel(r'$1/r$')
    ax.set_ylabel(r'$log(N(r))/log(1/r)$')
    
    #ax.legend(loc='upper right',ncol=2)  
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig('plot_fractal_dims.eps', bbox_inches='tight', format='eps')
    plt.tight_layout()    
    for i, (alpha, dim_an, dim_num, err) in enumerate(zip(alphas, dims_an, dims_num, errs)):
        table.add_row(f"{alpha:.1f}", f"{dim_an:.2f}", f"{dim_num:.2f}", f"{err:.2f}")
    
    console = Console()
    console.print(table)
    
    return dims_an, dims_num

  
    
