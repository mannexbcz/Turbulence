# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 16:12:04 2022

@author: manon
"""

import pandas as pd
import os

#%%

def read_data():
    '''Read the data files and returns a list of dataframes, 
    1 for each anemometer'''
    path = 'C:/Users/manon/Desktop/Turbulences/Projet/data/'
    data = []
    for i in range(6):
        df = pd.read_csv(path+str(i+1)+'.txt',sep=' ', header=None, names =['Velocity'])
        data.append(df)
    return tuple(data)

#data = read_data()
