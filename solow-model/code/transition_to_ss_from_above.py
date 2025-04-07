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
T = 125
t0 = 10
model = solow(alpha=0.35,s=0.5)
model.eval(k0=45)
model.transpath(T=T,t0=t0)
kx_max = np.max(model.ktil_trans)+4
kx = np.arange(0,55,0.001)
dk = (model.delta+model.n+model.g)*kx
f  = model.A*kx**model.alpha
sf = model.s*f

##########################################

# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=6, metadata=dict(artist='Brian C. Jenkins'), bitrate=1000)

fig = plt.figure(figsize=(16,9))
ax1 = fig.add_subplot(1, 1, 1)
ax1.grid()
plt.plot(kx,f,lw=6)
plt.plot(kx,sf,lw=4)
plt.plot(kx,dk,lw=2)
line11, = ax1.plot([], [],'o--k', lw=3)
time_text = ax1.text(45.5,0.25, '',fontsize=20)
ax1.set_xlim(0, 55)
ax1.text(45.5, 0.125, 'Created by Brian C. Jenkins',fontsize=11, color='black',alpha=0.5)
# plt.legend(['$Ak^{\\alpha}$','$sAk^{\\alpha}$','$dep$'],loc='upper left',fontsize=20)
plt.legend(['Production','Investment','Depreciation'],loc='upper left',fontsize=20)
ax1.set_title('Transition to the Steady State from Above',fontsize=20)

tme = []
k = model.ktil_trans
i = model.itil_trans
y = model.ytil_trans
depk= [(model.n+model.delta+model.g)*a for a in k]

#############
z,n=10000,0

def run(*args):
    global z,n,T,y,k,i,tme,depk
    tme=n
    model.ktil_trans[n]
    model.ytil_trans[n]
    model.ctil_trans[n]
    model.itil_trans[n]
    Y =[depk[n],i[n],y[n]]
    X =[k[n],k[n],k[n]]
    ax1.set_xticks([k[n]])
    ax1.set_yticks([depk[n],i[n],y[n]])
    xlabel  = '$k_{%d}$' % n
    ylabel1 = '$dep_{%d}$       ' % n
    ylabel2 = '$i_{%d}$' % n
    ylabel3 = '$y_{%d}$' % n
    ax1.set_xticklabels([xlabel],fontsize=20)
    ax1.set_yticklabels([ylabel1,ylabel2,ylabel3],fontsize=20)
    text ='t=%d' % n
    time_text.set_text(text)
    line11.set_data(X,Y)

    # fig.savefig("%d.png"%z)
    z+=1
    if n==T:
        n=0
        model.ktil_trans[n]
        model.ytil_trans[n]
        model.ctil_trans[n]
        model.itil_trans[n]
        Y =[depk[n],i[n],y[n]]
        X =[k[n],k[n],k[n]]
        tme=[n]
    else:
        n+=1
    return line11, time_text

ani = animation.FuncAnimation(fig, run, T, blit=False,repeat=True,interval=1)
ani.save('../video/transition_to_ss_from_above.mp4',writer=writer)
