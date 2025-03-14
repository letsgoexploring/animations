import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import subprocess
import os
from solow_model import solow

plt.style.use('classic')
plt.rcParams['figure.facecolor'] = 'white'

# Make directories for output if they don't exist
if not os.path.isdir('../video'):
    os.mkdir('../video')
    
##########################################
T = 60
t0 = 10
model = solow(s=0.35)
model.eval()
model.transpath(T=T,s1=0.5,t0=t0)
##########################################


# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=6, metadata=dict(artist='Brian C. Jenkins'), bitrate=1000)

fig = plt.figure(figsize=(16,9))
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)
ax4 = fig.add_subplot(2, 2, 4)


line11, = ax1.plot([], [], lw=4)
line12, = ax1.plot([], [],'ob',lw=4)
ax1.grid()
ax1.set_ylim(np.min(model.ktil_trans)-0.25, np.max(model.ktil_trans)+0.25)
ax1.set_xlim(0, T)
ax1.set_title('Capital $k_t$',fontsize=20)

line21, = ax2.plot([], [], lw=4)
line22, = ax2.plot([], [],'ob',lw=4)
ax2.grid()
ax2.set_ylim(np.min(model.ytil_trans)-0.25, np.max(model.ytil_trans)+0.25)
ax2.set_xlim(0, T)
ax2.set_title('Output $y_t$',fontsize=20)

line31, = ax3.plot([], [], lw=4)
line32, = ax3.plot([], [],'ob',lw=4)
ax3.grid()
ax3.set_ylim(np.min(model.ctil_trans)-0.25, np.max(model.ctil_trans)+0.25)
ax3.set_xlim(0, T)
ax3.set_title('Consumption $c_t$',fontsize=20)

line41, = ax4.plot([], [], lw=4)
line42, = ax4.plot([], [],'ob',lw=4)
ax4.grid()
ax4.set_ylim(np.min(model.itil_trans)-0.25, np.max(model.itil_trans)+0.25)
#ax4.set_ylim(0.1,0.15)
ax4.set_xlim(0, T)
ax4.set_title('Investment $i_t$',fontsize=20)
ax4.text(T-22, np.min(np.min(model.itil_trans)-0.25,0)+0.05, 'Created by Brian C. Jenkins',fontsize=11, color='black',alpha=0.5)

tme,y,k,c,i= [],[],[],[],[]

#############
z,n=10000,0

def run(*args):
    global z,n,T,y,k,c,i,tme
    tme.append(n)
    k.append(model.ktil_trans[n])
    y.append(model.ytil_trans[n])
    c.append(model.ctil_trans[n])
    i.append(model.itil_trans[n])
    line11.set_data(tme,k)
    line12.set_data([tme[-1]],[k[-1]])
    line21.set_data(tme,y)
    line22.set_data([tme[-1]],[y[-1]])
    line31.set_data(tme,c)
    line32.set_data([tme[-1]],[c[-1]])
    line41.set_data(tme,i)
    line42.set_data([tme[-1]],[i[-1]])

    # fig.savefig("%d.png"%z)
    z+=1
    if n==T:
        n=0
        k=[model.ktil_trans[n]]
        y=[model.ytil_trans[n]]
        c=[model.ctil_trans[n]]
        i=[model.itil_trans[n]]
        tme=[n]
    else:
        n+=1
    return line11,line12 ,line21,line22,line31,line32,line41,line42

ani = animation.FuncAnimation(fig, run, T, blit=False,repeat=False,interval=1)#20)
ani.save('../video/increase_s_away_from_golden_rule.mp4',writer=writer)
