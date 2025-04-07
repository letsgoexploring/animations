#!/usr/bin/env python
# coding: utf-8

# # Python program for replicating Figure 1.5 from *The Conquest of American Inflation* by Thomas Sargent.
# 
# In Figure 1.5, Sargent compares the business cycle componenets of monthly inflation and unemployment data for the US from 1960-1982. This program produces a replication of Figure 1.5 (among other things) by using the fredpy package to import data from inflation and unemployment data from Federeal Reserve Economic Data (FRED), manage the data, and then plot the results.

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import fredpy as fp
plt.style.use('classic')
plt.rcParams['figure.facecolor'] = 'white'


# ## Data
# 
# ### Importing the data
# 
# As his measure of the unemployment rate, Sargent uses the unemployment rate for white men age 20 and over (FRED code: LNS14000028). The results are essentially identical if the unemployment rate of the over 16 non-institutional population (FRED code: UNRATE) is used. His measure of the inflation rate is a 13-month two-sided moving average of the annualized monthly percentage change in the CPI. The unemployment and inflation rate data are monthly.
# 
# ### Detrending procedures
# 
# Sargent isolates the business cycle components of the data using the bandpass filter of Baxter and King (1995). Since the data are monthly, the minimum frequency is set to 24 months, the maximum is set to 84 months, and the lag-lead truncation to 84. Additionally, I also detrend the data using the Hodrick-Prescott filter (1997). The striking loops in Sargent's Figure 1.5 *are sensitive* to the filtering procedure used.

# In[2]:


# Dowload data
u = fp.series('LNS14000028')
p = fp.series('CPIAUCSL')

# Construct the inflation series
p = p.pc(annualized=True)
p = p.ma(length=6,center=True)

# Make sure that the data inflation and unemployment series cover the same time interval
p,u = fp.window_equalize([p,u])

# Filter the data
p_bp = p.bp_filter(low=24,high=84,K=84)[0]
p_hp = p.hp_filter(lamb=129600)[0]
u_bp = u.bp_filter(low=24,high=84,K=84)[0]
u_hp = u.hp_filter(lamb=129600)[0]


# ## Plots

# In[3]:


# Scatter plot of BP-filtered inflation and unemployment data (Sargent's Figure 1.5)
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

cmap = plt.get_cmap('jet', len(u_bp.data))
colors = [cmap(i) for i in range(len(u_bp.data))]

ax.scatter(u_bp.data,p_bp.data,facecolors='none',alpha=0.7,s=50,edgecolors=colors,linewidths=2)
ax.set_xlabel('Unemployment rate (%)')
ax.set_ylabel('Inflation rate (%)')
ax.set_title('Inflation and unemployment: BP-filtered data')
ax.grid(True)


# In[4]:


# Scatter plot of HP-filtered inflation and unemployment data
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

cmap = plt.get_cmap('jet', len(u_hp.data))
colors = [cmap(i) for i in range(len(u_hp.data))]

ax.scatter(u_hp.data,p_hp.data,facecolors='none',alpha=0.7,s=50,edgecolors=colors,linewidths=2)
ax.set_xlabel('Unemployment rate (%)')
ax.set_ylabel('Inflation rate (%)')
ax.set_title('Inflation and unemployment: HP-filtered data')
ax.grid(True)


# ## Remarks
# 
# There is a visible downward-sloping relationship between the inflation rate and the rate of unemployment over the business cycle. The relationship is less-pronounced under HP filtering relative to the relationship revealed by BP filtering. The so-called Phillips loops are not apparent in the HP-filtered data.
