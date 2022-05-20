# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 16:12:04 2022

@author: manon
"""

import pandas as pd
import os

#%%

def read_data():
    path = 'C:/Users/manon/Desktop/Turbulences/Projet/data/'
    #path = os.path.join(os.path.dirname(os.getcwd()), 'data/' )
    data = []
    for i in range(6):
        df = pd.read_csv(path+str(i+1)+'.txt',sep=' ', header=None, names =['Velocity'])
        data.append(df)
    return tuple(data)

#data = read_data()
