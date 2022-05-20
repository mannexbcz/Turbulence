# -*- coding: utf-8 -*-
"""
Created on Tue May 10 14:41:26 2022

@author: manon
"""

import numpy as np
from numpy.linalg import norm
from rich.table import Table
from rich.console import Console

from exercice3_1 import *

def Jacobian(point1, point2, alpha1,alpha2,beta):
    xn = point1[0,0]
    yn = point1[0,1]
    xnplus1 = point2[0,0]
    ynplus1 = point2[0,1]
    
    F1 = step(np.array([[xnplus1,yn]]),beta,alpha1,alpha2) # j = x
    F2 = step(np.array([[xn,ynplus1]]),beta,alpha1,alpha2) # j = y
    F1 = np.squeeze(F1)
    F2 = np.squeeze(F2)
    delta_xn = xnplus1-xn
    delta_yn = ynplus1-yn
    
    J = np.zeros((2,2))
    #print(yn)
    J[0,0] = (F1[0]-xnplus1)/(xnplus1-xn)
    J[0,1] = (F2[0]-xnplus1)/(ynplus1-yn)
    J[1,0] = (F1[1]-ynplus1)/(xnplus1-xn)
    J[1,1] = (F2[1]-ynplus1)/(ynplus1-yn)
    
    return J


def lyapunov_exponents(nsteps, alpha1,alpha2,beta):
    eps1 = [[1],[0]]
    eps2 = [[0],[1]]
    point1 = initialize_map(npoints=1)
    #print(point1)
    ln_Jx = []
    ln_Jy = []
    
    for n in range(nsteps):
        point2 = step(point1,beta,alpha1,alpha2)
        
        J = Jacobian(point1, point2, alpha1,alpha2,beta)
        #print(J)
        ln_Jx.append(np.log(norm(J@eps1)))
        ln_Jy.append(np.log(norm(J@eps2)))
        
        point1 = np.copy(point2)
        
    lambda1 = np.array(ln_Jx).mean()
    lambda2 = np.array(ln_Jy).mean()
    
    return lambda1, lambda2

def lyapunov_exponents_averaged_ntrials(ntrials, nsteps, alpha1,alpha2,beta):
    lambda1s = []
    lambda2s = []
    
    for n in range(ntrials):
        lambda1, lambda2 = lyapunov_exponents(nsteps=nsteps, alpha1=alpha1,alpha2=alpha2,beta=beta)
        lambda1s.append(lambda1)
        lambda2s.append(lambda2)
    return np.array(lambda1s).mean(), np.array(lambda2s).mean()

    
def comparison_lyapunov_exponents(ntrials,nsteps,epsilon0)  :
    alphas = [0.1,0.2,0.3,0.4,0.5]
    beta = 0.5
    lambda1_an = []
    lambda1_num = []
    errs1 = []
    lambda2_an = []
    lambda2_num = []
    errs2 = []
    
    table = Table(title="Lyapunov exponents")
    table.add_column("alpha", justify="center")
    table.add_column("lambda1, ana.", justify="center")
    table.add_column("lambda1, num.", justify="center")
    table.add_column("lambda1, rel.diff (%)", justify="center")
    table.add_column("lambda2, ana.", justify="center")
    table.add_column("lambda2, num.", justify="center")
    table.add_column("lambda2, rel.diff (%)", justify="center")
    
    
    for i, alpha in enumerate(alphas):
        lambda1,_ = lyapunov_exponents_averaged_ntrials(ntrials=ntrials, nsteps=nsteps, alpha1=alpha,alpha2=alpha,beta=beta)
        lambda2 = compute_first_lyapunov(nsteps=nsteps,epsilon0=epsilon0,beta=beta,alpha1=alpha,alpha2=alpha)
   
        lambda1_num.append(lambda1)
        lambda2_num.append(lambda2)
        
        lambda1_an.append(np.log(alpha))
        lambda2_an.append(np.log(2))
        
        errs1.append((np.abs(lambda1-np.log(alpha))/np.log(alpha))*100)
        errs2.append((np.abs(lambda2-np.log(2))/np.log(2))*100)
    
    for i, (alpha, l1_an, l1_num, err1, l2_an, l2_num, err2) in enumerate(zip(alphas, lambda1_an, lambda1_num, errs1,lambda2_an, lambda2_num, errs2)):
        table.add_row(f"{alpha:.1f}", f"{l1_an:.3f}", f"{l1_num:.3f}", f"{err1:.3f}", f"{l2_an:.3f}", f"{l2_num:.3f}", f"{err2:.3f}")
    
    console = Console()
    console.print(table)
    

def compute_first_lyapunov(nsteps,epsilon0,beta,alpha1,alpha2):
    point1 = initialize_map(npoints=1)
    point2 = point1 + epsilon0
    epsilons = np.zeros(nsteps)
    #epsilons[0] = np.linalg.norm(point1-point2)
    for n in range(nsteps):
        point1 = step(point1,beta,alpha1,alpha2)
        point2 = step(point2,beta,alpha1,alpha2)
        
        epsilons[n] = np.linalg.norm(point1-point2)
    
   # fig,ax = plt.subplots(figsize=(5,4))
   # ax.semilogy(np.arange(nsteps), )
    
    
    lambdas,_,_,_,_ = np.polyfit(np.arange(nsteps)+1,np.abs(np.log(epsilons/epsilon0)),1, full=True)
    lambda1 = lambdas[0]
    return lambda1
    
    
    
    
    
    