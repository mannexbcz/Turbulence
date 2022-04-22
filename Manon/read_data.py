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
    '''data1 = pd.read_csv(path+str(1)+'.txt',sep=' ', header=None, names =['1'])
    data2 = pd.read_csv(path+str(2)+'.txt',sep=' ', header=None, names =['2'])
    data3 = pd.read_csv(path+str(3)+'.txt',sep=' ', header=None, names =['3'])
    data4 = pd.read_csv(path+str(4)+'.txt',sep=' ', header=None, names =['4'])
    data5 = pd.read_csv(path+str(5)+'.txt',sep=' ', header=None, names =['5'])
    data6 = pd.read_csv(path+str(6)+'.txt',sep=' ', header=None, names =['6'])
    
    data = pd.concat([data1,data2,data3,data4,data5,data6],axis=1)

    return data'''

#data = read_data()
