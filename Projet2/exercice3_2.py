# -*- coding: utf-8 -*-
"""
Created on Sat May  7 10:46:18 2022

@author: manon
"""

import numpy as np
import matplotlib.pyplot as plt


def fractal_dim_img(points,nb):
    
    rs = np.linspace(1,0,nb)
    Nboxes=[]
    for r in rs[:-1]:
        Nbox = 0
        for i in range(int(1/r)+1):
            xmin = i*r
            xmax = (i+1)*r
            xok = np.logical_and((points[:,0]>=xmin), (points[:,0]<xmax))
            for j in range(int(1/r)+1):
                ymin = j*r
                ymax = (j+1)*r
                yok = np.logical_and((points[:,1]>=ymin), (points[:,1]<ymax))
                OK = np.logical_and(xok,yok)
                
                if np.any(OK):
                    Nbox = Nbox +1
        Nboxes.append(Nbox)
    
    fig,ax = plt.subplots(figsize=(5,4))
    ax.plot(np.log(Nboxes)/np.log(1/rs[:-1]))
    ax.set_xlabel(r'$1/r$')
    ax.set_ylabel(r'$N(r)$')
    