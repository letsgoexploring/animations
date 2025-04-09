#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from matplotlib.collections import LineCollection
import numpy as np
import fredpy as fp
import subprocess
import pandas as pd
import os


# In[2]:


# Make directories for output if they don't exist
if not os.path.isdir('../video'):
    os.mkdir('../video')

if not os.path.isdir('../image'):
    os.mkdir('../image')


# In[3]:


# Dimensions and ratios
main_width = 1920
main_height = 540
ratio = main_height/main_width


# In[4]:


# --- data prep ---
data = fp.series('PCEPI').data
data = data/data.shift() - 1
data = data.dropna()
scale = 0.05
data = (data - data.min())/(data.max()-data.min()) * ((1-scale)*main_height - (1+scale)*0) + (1+scale)*0
data.index = np.linspace(0,main_width,len(data.index))
data = data.reset_index()
data.columns = ['x','y']

length_of_data = len(data.index)

data


# In[5]:


n_pad = 200

# grab the constant y‑values
y0 = data.y.iloc[0]
yN = data.y.iloc[-1]

# grab the constant x‑values you want
x0 = 0               # for zeros_before
xN = data.x.iloc[-1] # e.g. 793

# make the before‐block: index -200…-1, x=0, y=y0
zeros_before = pd.DataFrame(
    {'x': x0, 'y': y0},
    index=range(-n_pad, 0)
)

# make the after‐block: index N…N+199, x=793, y=yN
zeros_after = pd.DataFrame(
    {'x': xN, 'y': yN},
    index=range(len(data), len(data) + n_pad)
)

# stitch them together
data = pd.concat([zeros_before, data, zeros_after])


# In[6]:


n_frames = 1200
fps = 60
first_frame = 60

# Initialize figure & axes
fig = plt.figure(figsize=(12, 12*ratio), facecolor='black')
# set the axes to cover the full figure and start with a black background
ax = fig.add_axes([0, 0, 1, 1], facecolor='black')

# initial static background plot (optional; update_plot will re‑draw it)
ax.plot(data.x,data.y, color='#1f77b4', linewidth=0.75, alpha=0.25)
ax.axis('off')

# Pre‐set the figure‐level rcParam so savefig uses black by default
plt.rcParams['savefig.facecolor'] = 'black'

def update_plot(i):
    ax.cla()                      # clear everything
    ax.set_facecolor('black')     # restore black background

    # re‑draw your data
    ax.plot(data.x,data.y, color='#1f77b4', linewidth=0.75, alpha=0.25)

    # fix your limits
    ax.set_xlim([0, main_width])
    ax.set_ylim([0, main_height])

    # remove ticks/labels/spines
    ax.axis('off')

    # print(i)

    if i>=first_frame:
        start = i + (200-first_frame)
        start=i-60
        length = 100
        segment = data.iloc[start:start+length]
        
        # correct 1-D x & y arrays
        x_seg = segment['x'].values
        y_seg = segment['y'].values
        
        # build and add the colored line
        pts  = np.stack([x_seg, y_seg], axis=1).reshape(-1,1,2)
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
        norm = Normalize(vmin=x_seg.min(), vmax=x_seg.max())
        lc   = LineCollection(segs, cmap='hot', norm=norm, linewidth=2)
        lc.set_array(x_seg)
        ax.add_collection(lc)

        if start==462+200:
            fig.savefig('../image/banner_thumbnail.png',dpi=526,transparent=False)

    # no need to return anything when blit=False
    return

# Set up the ffmpeg writer
Writer = animation.writers['ffmpeg']
writer = Writer(fps=fps, metadata=dict(artist='You'), bitrate=5000)

ani = animation.FuncAnimation(
    fig, update_plot, frames=n_frames, blit=False, repeat=False, interval=20
)

# When saving, the figure and axes are already black:
ani.save('../video/vimeo_banner_video.mp4', writer=writer)

