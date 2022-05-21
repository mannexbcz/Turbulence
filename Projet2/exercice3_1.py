# -*- coding: utf-8 -*-
"""
Created on Fri May  6 07:58:32 2022

@author: manon
"""

import numpy as np
import matplotlib.pyplot as plt

def initialize_map(npoints=2000):
    points =  np.random.random_sample((npoints, 2))
    return points

def plot_map(points,beta,idx1,idx2, name=None):
    if name == None:
        name='plotmap_init'
    #idx1,idx2 = find_indx_beta(points,beta)
    points1 = points[idx1,:]
    points2 = points[idx2,:]
    fig, ax = plt.subplots(figsize=(4,4))
    ax.plot(points2[:,0],points2[:,1],color='blue', marker = '.',markersize=1,linestyle = 'None', label=r'$y_{n,\mathrm{init}}\geq\beta$')
    ax.plot(points1[:,0],points1[:,1],color='blue', marker = '.',markersize=1,linestyle = 'None',label=r'$y_{n,\mathrm{init}}<\beta$')
    ax.legend(loc='upper left')
    ax.axis('equal')
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')
    plt.savefig(name+'.eps', format='eps')
    
    
def find_indx_beta(points,beta):
    indexes1 = np.where(points[:,1]<beta)
    indexes2 = np.where(points[:,1]>=beta)
    return indexes1[0],indexes2[0]

def step(points,beta,alpha1,alpha2):
    updated_points = np.copy(points)
    idx1,idx2 = find_indx_beta(points,beta)
    #update xn
    updated_points[idx1,0] = points[idx1,0]*alpha1
    updated_points[idx2,0] = (1-alpha2)+points[idx2,0]*alpha2
    #update yn
    updated_points[idx1,1] = points[idx1,1]/beta
    updated_points[idx2,1] = (points[idx2,1]-beta)/(1-beta)
    
    return updated_points


def do_n_steps(n,points,beta,alpha1,alpha2,fig=True):
    idx1,idx2 = find_indx_beta(points,beta)
    if fig:
        plot_map(points,beta,idx1,idx2,'plot_init')
    for i in range(n):
        name = 'plot_step_'+str(i+1)+'_alpha1_'+str(alpha1)+'_alpha2_' +str(alpha2)
        points = step(points,beta,alpha1,alpha2)
        #plot_map(points,beta,idx1,idx2,name)
    if fig:
        plot_map(points,beta,idx1,idx2,'plot_nend_n_'+str(n)+'_alpha1_'+str(alpha1)+'_alpha2_' +str(alpha2))
    return points


def study_two_close_points(npoints,niters,dist,beta,alpha1,alpha2):
    points = initialize_map(npoints=npoints)
    points[1,0]=points[0,0]+dist
    points[1,1]=points[0,1]+dist
    # initial configuration
    points1 = points[[0,1],:]
    points2 = points
    fig, ax = plt.subplots(figsize=(4,4))
    ax.plot(points2[:,0],points2[:,1],color='dodgerblue', marker = '.',markersize=1,linestyle = 'None')
    ax.plot(points1[:,0],points1[:,1],color='hotpink', marker = '.',markersize=10,linestyle = 'None')
    ax.legend(loc='upper left')
    ax.grid()
    ax.axis('equal')
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')
    # do n steps
    points_niters = do_n_steps(niters,points,beta,alpha1,alpha2)
    # final configuration
    points1 = points_niters[[0,1],:]
    points2 = points_niters
    fig, ax = plt.subplots(figsize=(4,4))
    ax.plot(points2[:,0],points2[:,1],color='dodgerblue', marker = '.',markersize=1,linestyle = 'None')
    ax.plot(points1[:,0],points1[:,1],color='hotpink', marker = '.',markersize=10,linestyle = 'None')
    ax.axis('equal')
    ax.grid()
    ax.legend(loc='upper left')
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')
    #plt.savefig('twoclosepoints_end4.eps', format='eps')
    
    