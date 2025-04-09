#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm
import numpy as np
import fredpy as fp
import subprocess
import os

plt.style.use('classic')
plt.rcParams['figure.facecolor'] = 'white'


# In[2]:


# Dimensions and ratios
main_width = 16
main_height = 9
ratio = main_height/main_width

# Dowload data
u = fp.series('LNS14000028')
p = fp.series('CPIAUCSL')

# Construct the inflation series
p = p.pc(annualized=True)
p = p.ma(length=6,center=True)

# Make sure that the data inflation and unemployment series cover the same time interval
p,u = fp.window_equalize([p,u])

# Filter the data
p = p.bp_filter(low=24,high=84,K=84)[0].data
u = u.bp_filter(low=24,high=84,K=84)[0].data

# Set data for animation
years = u.index.year.astype(str)
n=len(u)


# In[3]:


# Plot setup
font = {'weight' : 'bold',
        'size'   : 15}
plt.rc('font', **font)
plt.rcParams['xtick.major.pad']='8'
plt.rcParams['ytick.major.pad']='8'

# colormap
cmap = plt.get_cmap('rainbow', len(u))
colors = [cmap(i) for i in range(len(u))]

# Initialize figure
fig = plt.figure(figsize=(12, 12*ratio))
ax = fig.add_subplot(1,1,1)
ax.grid()
xdata, ydata = [], []
ax.set_ylim(-4, 5)
ax.set_xlim(-2, 2)
ax.set_xlabel('Unemployment rate (%)')
ax.set_ylabel('Inflation rate (%)')
ax.set_title('US inflation and unemployment: BP-filtered data',fontsize=20)

text = ax.text(1.95, 4.35, '',fontsize=18,horizontalalignment='right')
ax.text(1.125,-3.75, 'Created by Brian C. Jenkins',fontsize=11, color='black',alpha=0.5)

fig.tight_layout()


# In[4]:


def update_plot(i):

    scatter = ax.plot(u.iloc[i],p.iloc[i],'o',fillstyle='none',alpha=0.9,markeredgecolor=colors[i], markeredgewidth=2,markersize=13)
    text.set_text(years[i])

    return scatter, text


# In[5]:


# Make directories for output if they don't exist
if not os.path.isdir('../video'):
    os.mkdir('../video')

if not os.path.isdir('../image'):
    os.mkdir('../image')


# In[6]:


# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=10, metadata=dict(artist='Brian C Jenkins'), bitrate=5000)

# Make the animation
ani = animation.FuncAnimation(fig, update_plot, frames = n,fargs = (), blit=False,repeat=False,interval=20)

# Save the animation as .mp4
# ani.save('../video/US_Inflation_Unemployment_Monthly_BP_Filtered.ogv',fps=10,codec='libtheora')
ani.save('../video/us_inflation_unemployment_monthly_bp_filtered.mp4',writer=writer)

# Save the final image of the animation to use as the still image placeholder
plt.savefig('../image/us_inflation_unemployment_monthly_bp_filtered.png',bbox_inches='tight',dpi=120)


# In[7]:


# # Convert the mp4 video to ogg format
# makeOgg = 'ffmpeg -i ../video/US_Inflation_Unemployment_Monthly_BP_Filtered.mp4 -acodec libvorbis -ac 2 -ab 128k -ar 44100 -b:v 1800k  ../video/US_Inflation_Unemployment_Monthly_BP_Filtered.ogv'
# subprocess.call(makeOgg,shell=True)

