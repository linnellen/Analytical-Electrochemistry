# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 12:41:10 2022

@author: lkelley
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog
from scipy.signal import argrelextrema

path = 'ST8C5_Ca03_U550N2_LK_BOT/txt files/'
files = os.listdir(path)
#ecsa = []
df_ecsa = []
for filename in files:
    if 'HAD' in filename:
        #ecsa.append(filename)
        df_ecsa.append(pd.read_csv(path+filename,delimiter='\t',header=14))
        
ecsa = df_ecsa[0]
        

#%%
        
def addtime(df,nu):
    time = []
    for i in range(len(df)):
        t=i*nu
        time.append(t)
    df['Time']=time 
    return time
        
t= addtime(ecsa,0.01)
        
#%%

def ECSA_edit(df,path,rng,pos_l,title,cell_area,CL):
    a_u = []
    a_l = []
    ma_u = []
    ma_l = []
    
    g_pt = CL*cell_area/1000

    x_ecsa = np.array(df_ecsa[0]['Volts'][rng].tolist()) # x,y,time for range of last full CV cycle
    y_ecsa = np.array(df_ecsa[0]['Amps'][rng].tolist())*(1000/cell_area) # (mA/cm^2)
    t_ecsa = np.array(df_ecsa[0]['Time'][rng].tolist())
            
    mins = np.array(argrelextrema(y_ecsa, np.less)).T # finding minimums in the data
    maxs = np.array(argrelextrema(y_ecsa, np.greater)).T # finding maximums in the data
    
    plt.plot(x_ecsa,y_ecsa)
    pts = plt.ginput(n=-1,timeout=-1,mouse_add=None,mouse_pop=None,mouse_stop=None)
    
    ind = []
    
    points = list(zip(x_ecsa,y_ecsa))
    def distance(a,b):
        return(sum([(k[0]-k[1])**2 for k in zip(a,b)])**0.5)
    for i,pt in enumerate(pts):
        dists = [distance([pt[0], pt[1]],k) for k in points]
        ind.append(dists.index(min(dists)))
        
    ROOT = tk.Tk()
    ROOT.withdraw()
    A = simpledialog.askstring(title="Test",prompt="Set left integration bound at a specified voltage or edge of first peak? (v/e)")
    if A=='v':
        ROOT = tk.Tk()
        ROOT.withdraw()
        v_up = simpledialog.askfloat(title="Test",prompt="Specify voltage for upper integration (V, do not add units)")
        v_down = simpledialog.askfloat(title="Test",prompt="Specify voltage for lower integration (V, do not add units)")
        up_d = np.where(np.abs(np.subtract(x_ecsa[ind[0]:ind[1]],v_up))==min(np.abs(np.subtract(x_ecsa[ind[0]:ind[1]],v_up))))[0][0]+ind[0]
        d_d = np.where(np.abs(np.subtract(x_ecsa[ind[2]:ind[3]],v_down))==min(np.abs(np.subtract(x_ecsa[ind[2]:ind[3]],v_down))))[0][0]+ind[2]
    if A=='e':
        up_d = int(mins[0])
        d_d = int(maxs[-1])
           
    up_l = np.where(y_ecsa==min(y_ecsa[ind[0]:ind[1]]))[0][0]
    d_l = np.where(y_ecsa==max(y_ecsa[ind[2]:ind[3]]))[0][0]

    upx = [x_ecsa[up_d],x_ecsa[up_l]] # xmin and xmax for the interp function drawing the upper horizontal line
    upy = [y_ecsa[up_l],y_ecsa[up_l]] # y-values for the interp function are the same 

    dx = [x_ecsa[d_l],x_ecsa[d_d]] # for the lower horizontal line
    dy = [y_ecsa[d_l],y_ecsa[d_l]]

    x_up = x_ecsa[up_d:up_l+1] # shared x-values for upper integration 
    y_up = y_ecsa[up_d:up_l+1] # y-values of the original data
    t_up = t_ecsa[up_d:up_l+1] # time values for upper integration 

    x_d = x_ecsa[d_l:d_d+1] # shared x-values for lower integration 
    y_d = y_ecsa[d_l:d_d+1]
    t_d = t_ecsa[d_l:d_d+1]

    line_up = np.interp(x_up,upx,upy) # creating an array of y-values for shared x-values (upper line)
    line_d = np.interp(x_d,dx,dy) # lower line

    # plotting
    
    plt.figure()
    plt.plot(x_ecsa,y_ecsa,'dodgerblue')

    plt.fill_between(x_up,line_up,y_up,color='firebrick')
    plt.fill_between(x_d,line_d,y_d,color='gold')

    plt.plot(x_up,line_up,'k')
    plt.plot(x_d,line_d,'k')

    plt.vlines(upx[0],upy[0],y_ecsa[up_d],'k')
    plt.vlines(dx[1],dy[0],y_ecsa[d_d],'k')

    plt.plot(x_up,y_up,'k')
    plt.plot(x_d,y_d,'k')
    
    ROOT = tk.Tk()
    ROOT.withdraw()
    a = simpledialog.askstring(title="Test",prompt="Do you want to plot guidelines? (Yes/No):")
    
    if (a=='Yes') or (a=='yes'):
        plt.plot(x_ecsa[ind[0]],y_ecsa[ind[0]],'*',color='k')
        plt.plot(x_ecsa[ind[1]],y_ecsa[ind[1]],'*',color='k')
        plt.plot(x_ecsa[ind[2]],y_ecsa[ind[2]],'*',color='k')
        plt.plot(x_ecsa[ind[3]],y_ecsa[ind[3]],'*',color='k')
        if A=='v':
            plt.axvline(x=v_up)
            plt.axvline(x=v_down)
    
    plt.plot(x_ecsa[up_d],y_ecsa[up_d],'x',color='mediumblue')
    plt.plot(x_ecsa[up_l],y_ecsa[up_l],'x',color='mediumblue')

    plt.plot(x_ecsa[d_d],y_ecsa[d_d],'x',color='mediumblue')
    plt.plot(x_ecsa[d_l],y_ecsa[d_l],'x',color='mediumblue')

    plt.xlabel('Potential (V vs SHE)')
    plt.ylabel('Current Density (mA/cm$^2$)')
    plt.title(title)
    
    # calculations
    
    a_upper = (np.trapz(y_up,t_up) - np.trapz(line_up,t_up))/(1000*210E-6) # cm^2 Pt/cm^2
    a_lower = np.abs((np.trapz(y_d,t_d) - np.trapz(line_d,t_d))/(1000*210E-6))
    a_u.append(a_upper)
    a_l.append(a_lower)
    
    ma_upper = a_upper*cell_area/(10000*g_pt)# m^2 Pt/g Pt
    ma_lower = a_lower*cell_area/(10000*g_pt)
    ma_u.append(ma_upper)
    ma_l.append(ma_lower)
    
    plt.text(0.2,pos_l,'ECSA upper: ' + str(round(ma_upper,2)) + ' m$^2_{Pt}$/g$_{Pt}$ \nECSA upper: ' + str(round(a_upper,2)) + ' cm$^2_{Pt}$/cm$^2$ \nECSA lower: ' + str(round(ma_lower,2)) + ' m$^2_{Pt}$/g$_{Pt}$ \nECSA lower: ' + str(round(a_lower,2)) + ' cm$^2_{Pt}$/cm$^2$')
    
    plt.savefig(path+title+'.svg',format='svg')
    
#%%
ECSA_edit(ecsa,'Miscellaneous Python/',list(range(13801,18400)),-28,'test',50,0.253)