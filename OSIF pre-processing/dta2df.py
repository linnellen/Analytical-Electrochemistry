# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 11:58:53 2022

@author: lkelley
"""
import pandas as pd
# dta

def dta(file,num):
    '''

    Parameters
    ----------
    file : dta file 
    num : number of header lines before column labels (check by opening in Notepad)
    Returns
    -------
    df : dataframe of dta file

    '''
    df = pd.read_table(file,skiprows=num,delimiter='\t',header=0,encoding='ISO-8859-1')
    df = df.drop(columns='Unnamed: 0')
    if 'Over' in df:
        df = df.drop(columns='Over')
    df = df.drop(labels=0, axis=0)
    df = df.reset_index(drop=True)
    inds = []
    for i in range(len(df['Pt'])):
        if df['Pt'][i]=='TABLE':
            inds.append(i)
            inds.append(i+1)
            inds.append(i+2)
    df = df.drop(df.index[inds])
    
    df = df.reset_index()
    del df['index']
    
    df = df.astype(float)
    return df