#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import subprocess
import os

plt.style.use('classic')
plt.rcParams['figure.facecolor'] = 'white'


# In[2]:


data = pd.read_csv('https://raw.githubusercontent.com/letsgoexploring/economic-data/refs/heads/main/dmp/csv/beveridge_curve_data.csv',index_col=0,parse_dates=True)

data = data.loc['1947':]
u_rate = data['Unemployment [Thousands of persons]']/data['Labor force [Thousands of persons]']*100
theta = data['Vacancies [Thousands of vacancies]']/data['Labor force [Thousands of persons]']*100

# Set data for animation
years = data.index.year.astype(str)
n=len(data.index)


# In[3]:


# Plot setup
font = {'weight' : 'bold',
        'size'   : 15}
plt.rc('font', **font)
plt.rcParams['xtick.major.pad']='8'
plt.rcParams['ytick.major.pad']='8'

# Setup colormap
cmap = plt.get_cmap('rainbow', n)
colors = [cmap(i) for i in range(n)]

# Initialize figure
fig = plt.figure(figsize=(16,9))
ax = fig.add_subplot(1,1,1)
ax.grid()
xdata, ydata = [], []
ax.set_ylim(0, 3.5)
ax.set_xlim(0, 16)
ax.set_xlabel('Unemployment rate (%)')
ax.set_ylabel('Vacancy rate (%)')
ax.set_title('US Beveridge Curve',fontsize=20)

# Placeholder for year text
text = ax.text(13.5, 3.125, '',fontsize=18,horizontalalignment='right')

# Watermark
ax.text(12.125,0.25, 'Created by Brian C. Jenkins',fontsize=11, color='black',alpha=0.5)

fig.tight_layout()

# Function for updating the plot with new data points
def update_plot(i):

    scatter = ax.plot(u_rate.iloc[i],theta.iloc[i],'o',fillstyle='none',alpha=0.9,markeredgecolor=colors[i], markeredgewidth=2,markersize=13)
    text.set_text(years[i])

    return scatter, text


# In[4]:


# Make directories for output if they don't exist
if not os.path.isdir('../video'):
    os.mkdir('../video')

if not os.path.isdir('../image'):
    os.mkdir('../image')


# In[5]:


# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=10, metadata=dict(artist='Brian C Jenkins'), bitrate=5000)

# Make the animation
ani = animation.FuncAnimation(fig, update_plot, frames = n,fargs = (), blit=False,repeat=False,interval=20)

# Save the animation as .mp4
# ani.save('../video/US_Inflation_Unemployment_Monthly_BP_Filtered.ogv',fps=10,codec='libtheora')
ani.save('../video/us_beveridge_curve.mp4',writer=writer)

# Save the final image of the animation to use as the still image placeholder
plt.savefig('../image/us_beveridge_curve.png',bbox_inches='tight',dpi=120)

# # Convert the mp4 video to ogg format
# makeOgg = 'ffmpeg -i ../video/US_Inflation_Unemployment_Monthly_BP_Filtered.mp4 -acodec libvorbis -ac 2 -ab 128k -ar 44100 -b:v 1800k  ../video/US_Inflation_Unemployment_Monthly_BP_Filtered.ogv'
# subprocess.call(makeOgg,shell=True)

