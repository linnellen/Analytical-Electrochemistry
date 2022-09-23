# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 14:32:17 2022

@author: lkelley
"""

import seaborn as sns
import matplotlib.pyplot as plt
from mass_activity import Cell,Cycle

plt.rcParams.update({'font.size': 20})
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams["figure.figsize"] = (9,7)

#%%
cell = Cell('Sample data',50,0.253,sns.color_palette('colorblind'),'Saved images/')

#%%
c_BOT = Cycle('BOT/',cell)
c_30K = Cycle('30K/',cell)
c_60K = Cycle('60K/',cell)
c_90K = Cycle('90K/',cell)

#%%
c_BOT.pol_curve_o2(cell.colors[0],'o',cell)
c_30K.pol_curve_o2(cell.colors[1],'s',cell)
c_60K.pol_curve_o2(cell.colors[2],'*',cell)
c_90K.pol_curve_o2(cell.colors[3],'>',cell)

#%%
cell.ma.clear()
c_BOT.massact(0.036186,cell.colors[0],0.85,cell)
c_30K.massact(0.033869,cell.colors[1],0.85,cell)
c_60K.massact(0.038103,cell.colors[2],0.85,cell)
c_90K.massact(0.035323,cell.colors[3],0.85,cell)

plt.text(50,0.84,'i at 0.9 V \nBOT: ' 
         + str(c_BOT.i_0p9) + ' mA/cm$^2$ \n30K: ' 
         + str(c_30K.i_0p9) + ' mA/cm$^2$ \n60K: ' 
         + str(c_60K.i_0p9)+ ' mA/cm$^2$ \n90K: ' 
         + str(c_90K.i_0p9) + ' mA/cm$^2$')
plt.text(2.1,0.91,'O$_2$, 1.5 atm, 80$^o$C, 100%RH, An')
cell.custlegend(['BOT','30K','60K','90K'],cell.colors,[0.02,0.4])
plt.xscale('log',base=10)
plt.title('PtCo/HSC H$_2$/N$_2$ AST, Mass Activity at 0.9 V')
plt.savefig(cell.save_folder+'ma.svg',format='svg',dpi=150)

plt.figure(2)
a = plt.bar(['BOT','30K','60K','90K'],cell.ma,width=0.6,color=cell.colors[0])
plt.ylabel('Mass Activity (mA/mg$_{Pt}$ at 0.9 V)')
plt.xlabel('AST Cycles')
plt.title('PtCo/HSC H$_2$/N$_2$ AST, Mass Activity at 0.9 V')
plt.bar_label(a)
plt.bar_label(a,labels=['','-14 %','-26 %','-38 %'],color=cell.colors[1],\
              label_type='center',fontsize=20,fontweight='bold')
plt.savefig(cell.save_folder+'ma bar.svg',format='svg',dpi=150)
print(cell.ma)