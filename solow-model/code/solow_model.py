# Defines solow class and functions tfor simulating the Solow model

from __future__ import division
import pylab as py 
import numpy as np

class solow:

    def __init__(self,alpha=0.35,A=1,s=0.1,delta=.04,n=0.01,g=0.02):

        # Define parameters of the current instance of the Solow model
        self.A       = A
        self.alpha   = alpha
        self.s       = s
        self.delta   = delta
        self.n       = n
        self.g       = g

        # Compute the steady state values of endogenous variables in ``per effective worker terms''
        self.ktil_ss = (s*A/(n+g+delta))**(1/(1-alpha))
        self.ytil_ss = A*self.ktil_ss**alpha
        self.itil_ss = s*self.ytil_ss
        self.ctil_ss = (1-s)*self.ytil_ss
        self.dktil_ss= 0

    def eval(self,k0='FALSE',E0=1,L0=1):

        ''' Evaluates an instance of the Solow model given k0, E0, and L0.'''

        if k0=='FALSE':
            self.ktil = self.ktil_ss
        else:
            self.ktil = k0

        self.ytil = self.A*self.ktil**self.alpha
        self.ctil = (1-self.s)*self.ytil
        self.itil = self.s*self.ytil
        self.dktil= self.s*self.ytil - (self.delta+self.n+self.g)*self.ktil
        self.ktil1= self.ktil+self.dktil

        self.k    = self.ktil*E0
        self.y    = self.ytil*E0
        self.i    = self.itil*E0
        self.c    = self.ctil*E0

        self.K    = self.ktil*E0*L0
        self.Y    = self.ytil*E0*L0
        self.I    = self.itil*E0*L0
        self.C    = self.ctil*E0*L0

        self.gktil= self.s*self.A*self.ktil**(self.alpha-1)-(self.delta+self.n+self.g)
        self.gytil= self.alpha*self.gktil
        self.gctil= self.alpha*self.gktil
        self.gitil= self.alpha*self.gktil

        self.gk   = self.gktil+self.g
        self.gy   = self.alpha*self.gktil+self.g
        self.gc   = self.alpha*self.gktil+self.g
        self.gi   = self.alpha*self.gktil+self.g

        self.gK   = self.gktil+self.n+self.g
        self.gY   = self.alpha*self.gktil+self.n+self.g
        self.gC   = self.alpha*self.gktil+self.n+self.g
        self.gI   = self.alpha*self.gktil+self.n+self.g

        self.E0   = E0
        self.L0   = L0
        self.E1   = (1+self.g)*E0
        self.L1   = (1+self.n)*L0


    def transpath(self,t0=5,T=10,A1='FALSE',s1='FALSE',delta1='FALSE',n1='FALSE',g1='FALSE'):
        self.ktil_trans= [self.ktil]
        self.ytil_trans= [self.ytil]
        self.ctil_trans= [self.ctil]
        self.itil_trans= [self.itil]
        self.k_trans   = [self.k]
        self.y_trans   = [self.y]
        self.c_trans   = [self.c]
        self.i_trans   = [self.i]
        self.K_trans   = [self.K]
        self.Y_trans   = [self.Y]
        self.C_trans   = [self.C]
        self.I_trans   = [self.I]
        self.E_trans   = [self.E0]
        self.L_trans   = [self.L0]

        self.gktil_trans= [self.gktil]
        self.gytil_trans= [self.gytil]
        self.gctil_trans= [self.gctil]
        self.gitil_trans= [self.gitil]
        self.gk_trans   = [self.gk]
        self.gy_trans   = [self.gy]
        self.gc_trans   = [self.gc]
        self.gi_trans   = [self.gi]
        self.gK_trans   = [self.gK]
        self.gY_trans   = [self.gY]
        self.gC_trans   = [self.gC]
        self.gI_trans   = [self.gI]


        def trans():
            self.eval(k0=self.ktil1,E0=self.E1,L0=self.L1)
            self.ktil_trans.append(self.ktil)
            self.ytil_trans.append(self.ytil)
            self.ctil_trans.append(self.ctil)
            self.itil_trans.append(self.itil)

            self.k_trans.append(self.k)
            self.y_trans.append(self.y)
            self.c_trans.append(self.c)
            self.i_trans.append(self.i)

            self.K_trans.append(self.K)
            self.Y_trans.append(self.Y)
            self.C_trans.append(self.C)
            self.I_trans.append(self.I)

            self.gktil_trans.append(self.gktil)
            self.gytil_trans.append(self.gytil)
            self.gctil_trans.append(self.gctil)
            self.gitil_trans.append(self.gitil)

            self.gk_trans.append(self.gk)
            self.gy_trans.append(self.gy)
            self.gc_trans.append(self.gc)
            self.gi_trans.append(self.gi)

            self.gK_trans.append(self.gK)
            self.gY_trans.append(self.gY)
            self.gC_trans.append(self.gC)
            self.gI_trans.append(self.gI)

            self.E_trans.append(self.E0)
            self.L_trans.append(self.L0)

        if t0 == 'FALSE':
            for k in range(T):
                trans()

        else:

            for k in range(t0-1):
                trans()

            if A1 != 'FALSE':
                for k in range(t0-1,T):
                    self.A = A1
                    trans()

            elif s1 != 'FALSE':
                for k in range(t0-1,T):
                    self.s = s1
                    trans()

            elif delta1 != 'FALSE':
                for k in range(t0-1,T):
                    self.delta = delta1
                    trans()

            elif n1 != 'FALSE':
                for k in range(t0-1,T):
                    self.n = n1
                    trans()

            elif g1 != 'FALSE':
                for k in range(t0-1,T):
                    self.g = g1
                    trans()

            else:
                for k in range(t0-1,T):
                    trans()