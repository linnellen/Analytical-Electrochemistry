# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 14:28:11 2022

@author: lkelley
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

from matplotlib.lines import Line2D
from scipy.optimize import curve_fit

class Cell(object):
    def __init__(self,cell_id,area,loading,colors,save_folder):
        self.cell_id = cell_id
        self.area = area
        self.loading = loading
        self.colors = colors
        self.save_folder = save_folder
        self.g_pt = self.loading*self.area/1000 # grams Pt
        self.ma = []
        
    def custlegend(self,labels,colors,location):
        lines = [Line2D([0], [0], color=c, linewidth=2) for c in colors]
        plt.legend(lines,labels,loc='upper right',facecolor='white',framealpha=1)
        
class Cycle(object):
    def __init__(self,cycle_num,cell):
        self.cycle_num = cycle_num
        self.path = cell.cell_id+'/data_'+self.cycle_num
        self.files = os.listdir(self.path)
        
        for filename in self.files:
            if '.xlsx' in filename:
                self.pol = pd.read_excel(self.path+filename,sheet_name='BauerAverage')
            if 'h2x' in filename:
                self.h2x = pd.read_csv(self.path+filename,delimiter='\t',header=14)
        
    def pol_curve_o2(self,c,m,cell):
        # Find indices of anodic and cathodic O2 curves.
        o2 = []
        for i in range(len(self.pol['Sub Protocol'])):
            if 'O2' in self.pol['Sub Protocol'][i]:
                o2.append(i)
        rng_o2_a = o2[-20:-10]
        rng_o2_c = o2[-10:]
        self.rng = [rng_o2_a,rng_o2_c]
        
        # Create arrays of voltage and current density. 
        j_a = (self.pol['Current Density FB (A/cm2)'][self.rng[0]]*1000).tolist()
        j_c = (self.pol['Current Density FB (A/cm2)'][self.rng[1]].sort_values()*1000).tolist() 
        v_a = (self.pol['Load Bank Voltage (V)'][self.rng[0]]).tolist()
        v_c = (self.pol['Load Bank Voltage (V)'][self.rng[1]].sort_values(ascending=False)).tolist()
        self.j_ma = j_a[0:-1]
        
        # Plot O2 polarization curves.
        plt.figure(1)
        plt.plot(j_a,v_a,color=c,marker='o')
        plt.plot(j_c,v_c,color=c,marker='>',markerfacecolor='none',linestyle=':')
        plt.xlabel('Current Density (mA/cm$^2$)')
        plt.ylabel('Cell Voltage (V)')
        plt.ylim([0.74,1.03])
        plt.title('O$_2$, 1.5 atm, 80$^o$C, 100%RH')
        plt.legend(['BOT, An', 'BOT, Ca','30K, An', '30K, Ca',
                    '60K, An', '60K, Ca', '90K, An', '90K, Ca'])
        plt.savefig(cell.save_folder+'pol_curve_o2.svg',format='svg',dpi=150)
        
    def linear(self,x,m,b):
        y = m*x+b
        return y
        
    def massact(self,r_proton,color,voltage_cut,cell):
        # Calculate steady-state hydrogen crossover current.
        end_count = len(self.h2x['Amps']) 
        start_count = len(self.h2x['Amps'])-100 
        j_h2x = (self.h2x['Amps'][start_count:end_count].mean())*1000/cell.area 
        self.j_h2x = j_h2x
        
        # Correct voltage data for HFR and proton transport resistance.
        # Correct current density data for hydrogen crossover current. 
        self.pol['HFR corrected voltage (V)'] = \
            self.pol['Load Bank Voltage (V)'] \
            + self.pol['Current Density FB (A/cm2)']*self.pol['HFR (Ohm-cm2)'] 
        v_a_hfr = (self.pol['HFR corrected voltage (V)'][self.rng[0]][0:-1]).tolist() 
        j_h2x_tafel = np.log10([x+self.j_h2x for x in self.j_ma]) 
        v_a_ir = v_a_hfr + np.divide(np.multiply(self.j_ma,r_proton),1000) 
        
        # Use data only above specified cut-off voltage for linear fit.
        df = pd.DataFrame()
        df['V-iR free'] = v_a_ir
        df['i-h2x cor'] = j_h2x_tafel
        df_cut = df[df['V-iR free']>voltage_cut]
        
        # Perform linear fit and solve for x-intercept at 0.9 V.
        popt_ma, pcov_ma = curve_fit(self.linear,df_cut['i-h2x cor'],df_cut['V-iR free'])
        yp_ma = self.linear(j_h2x_tafel, *popt_ma)
        x_0p9 = (0.9-popt_ma[1])/popt_ma[0] 
        
        # Create Tafel plot and mark current density at 0.9 V. 
        plt.figure(1)
        plt.axhline(y=0.9,color='k',zorder=0,linewidth=0.5)
        plt.plot(10**j_h2x_tafel,v_a_ir,color=color,marker='o',markerfacecolor='none')
        plt.plot(10**j_h2x_tafel,yp_ma,color=color,linestyle=':')
        plt.plot(10**x_0p9,self.linear(x_0p9, *popt_ma),'*',markersize=5,color='k')
        plt.ylabel('V$_{iR-free}$ (V)')
        plt.xlabel('Current Density, H$_2$ Crossover Corrected (mA/cm$^2$)')
        
        # Store values. 
        self.i_0p9 = round(10**x_0p9,2)
        cell.ma.append(round(self.i_0p9*cell.area/(cell.g_pt*1000),2))
        
        
        
        
