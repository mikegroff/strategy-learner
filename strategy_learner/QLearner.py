"""
Template for implementing QLearner  (c) 2015 Tucker Balch

Copyright 2018, Georgia Institute of Technology (Georgia Tech)
Atlanta, Georgia 30332
All Rights Reserved

Template code for CS 4646/7646

Georgia Tech asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. Students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including repositories
such as github and gitlab.  This copyright statement should not be removed
or edited.

We do grant permission to share solutions privately with non-students such
as potential employers. However, sharing with other current or future
students of CS 7646 is prohibited and subject to being investigated as a
GT honor code violation.

-----do not edit anything above this line---

Student Name: Michael Groff (replace with your name)
GT User ID: mgroff3 (replace with your User ID)
GT ID: 902772277 (replace with your GT ID)
"""

import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.num_states = num_states
        self.alpha = alpha
        self.gamma = gamma
        self.rar = radr
        self.radr = radr
        self.dyna = dyna
        self.s = 0
        self.a = 0

        self.Q = np.zeros((num_states,num_actions))
        if self.dyna != 0:
            self.E = np.array([[self.s,self.a,self.s,0]])

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        if rand.random() <= self.rar :
            action = rand.randint(0, self.num_actions-1)
        else:
            action = np.argmax(self.Q[s])
        if self.verbose: print "s =", s,"a =",action

        self.a = action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """
        act = np.argmax(self.Q[s_prime])
        self.Q[self.s,self.a] = self.Q[self.s,self.a] + self.alpha*(r + self.gamma*(self.Q[s_prime,act]) -self.Q[self.s,self.a])

        if rand.random() <= self.rar :
            action = rand.randint(0, self.num_actions-1)
        else:
            action = act

        a = action
        s = s_prime
        rr =r
        if self.dyna != 0:
            self.E = np.vstack((self.E, np.array([self.s,self.a,s,r])))
            es =  self.E.shape[0]
            if es <= 2:
                ind = np.ones(self.dyna, dtype = int)
            else:
                ind = np.random.randint(1,es-1,size = self.dyna)
            for i in ind:
                self.s,self.a,s_prime,r = self.E[i]
                self.s,self.a,s_prime = (int)(self.s),(int)(self.a),(int)(s_prime)
                self.Q[self.s,self.a] = self.Q[self.s,self.a] + self.alpha*(r + self.gamma*(np.amax(self.Q[s_prime,:])) -self.Q[self.s,self.a])


        if self.verbose: print "s =", s_prime,"a =",a,"r =",rr
        self.rar = self.rar*self.radr

        self.s = s
        self.a = a
        return action

    def author(self):
        return 'mgroff3'

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
