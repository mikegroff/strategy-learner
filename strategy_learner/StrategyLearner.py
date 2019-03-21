"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch

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

import datetime as dt
import pandas as pd
import util as ut
import QLearner as ql
import marketsimcode as ma
import ManualStrategy as ms
import random
import numpy as np

class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        self.Q = None
        self.dyna = 0
        self.epochs = 500
        self.binsize = 10
        self.fbi = None
        self.b1 = None
        self.b2 = None
        self.b3 = None
        self.b4 = None

    def author(self):
        return 'mgroff3'

    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000):
        cash = sv
        shares = 0
        eval = sv
        n = 20
        syms = [symbol]
        sdn = sd - dt.timedelta(days = n*2)
        datesn = pd.date_range(sdn, ed)
        dates = pd.date_range(sd, ed)
        df = ut.get_data(syms,dates)
        dfn = ut.get_data(syms,datesn)
        prices = dfn[symbol]
        mom = prices/np.roll(prices,n) -1
        sma = (prices/prices.rolling(n).mean()) -1
        bb = (prices - sma)/2*prices.rolling(n).std()
        vd = prices.max() - prices.min()
        dfn['FB236'] = prices.min()+0.236*vd
        dfn['FB382'] = prices.min()+0.382*vd
        dfn['FB50'] = prices.min()+0.5*vd
        dfn['FB618'] = prices.min()+0.618*vd
        dfn['FB100'] = prices.min()+vd
        dfn['MOM'] = prices+mom*prices
        dfn['SMA'] = prices.rolling(n).mean()
        dfn['BBU'] = dfn['SMA']+2*prices.rolling(n).std()
        dfn['BBL'] = dfn['SMA']-2*prices.rolling(n).std()
        dfn = dfn.drop([symbol],axis = 1)
        dfn = dfn.drop(['SPY'],axis = 1)
        df = df.join(dfn,how='left')
        prices = df[symbol]
        sin = np.ones(len(prices))

        self.fbi = prices.min()+0.618*vd
        df['FBI'] = df[symbol] - df['FB618']
        dbi = df['FBI'].values
        ss = self.binsize
        r = np.array(range(0,ss))
        rat = (dbi.max()-dbi.min())/(ss-1)
        bins = dbi.min()*np.ones(len(r))+rat*r
        df['FBI'] = np.digitize(dbi,bins)-sin
        self.b1 = bins

        df['MOI'] = df[symbol] - df['MOM']
        dbi = df['MOI'].values
        rat = (dbi.max()-dbi.min())/(ss-1)
        bins = dbi.min()*np.ones(len(r))+rat*r
        df['MOI'] = np.digitize(dbi,bins)-sin
        self.b2 = bins

        df['SMI'] = df[symbol] - df['SMA']
        dbi = df['MOI'].values
        rat = (dbi.max()-dbi.min())/(ss-1)
        bins = dbi.min()*np.ones(len(r))+rat*r
        df['SMI'] = np.digitize(dbi,bins)-sin
        self.b3 = bins

        df['BBI'] = df[symbol] - df['BBU']
        dbi = df['BBI'].values
        rat = (dbi.max()-dbi.min())/(ss-1)
        bins = dbi.min()*np.ones(len(r))+rat*r
        df['BBI'] = np.digitize(dbi,bins)-sin
        self.b4 = bins



        df = df[[symbol,'FBI','MOI','SMI','BBI']]

        #print(df.to_string())

        self.Q = ql.QLearner(num_states=ss**4,\
            num_actions = 3, \
            alpha = 0.2, \
            gamma = 0.9, \
            rar = 0.98, \
            radr = 0.999, \
            dyna = self.dyna, \
            verbose=False)

        for epoch in range(1,self.epochs+1):
            i = 0
            dd = 1
            for row in df.itertuples():
                a,b,c,d = row[2],row[3],row[4],row[5]

                p = row[1]
                nstate = int(a+b*ss+c*ss**2+d*ss**3)

                if (i==0):
                    action = self.Q.querysetstate(nstate)
                    act = action-dd
                    if (act < 0):
                        p = p*(1-self.impact)
                        cash -= p*1000*act
                        cash -= 9.95
                        shares += act
                    elif (act > 0):
                        p = p*(1+self.impact)
                        cash -= p*1000*act
                        cash -= 9.95
                        shares += act
                    i+=1
                    dd = action
                    continue

                r = p*1000*shares + cash - eval
                #print(act,shares,cash)

                action = self.Q.query(nstate, r)
                act = action -dd
                if (act < 0):
                    p = p*(1-self.impact)
                    cash -= p*1000*act
                    shares += act
                elif (act > 0):
                    p = p*(1+self.impact)
                    cash -= p*1000*act
                    shares += act

                eval = r+eval
                dd = action

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        cash = sv
        shares = 0
        eval = sv
        n = 20
        syms = [symbol]
        sdn = sd - dt.timedelta(days = n*2)
        datesn = pd.date_range(sdn, ed)
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        df = ut.get_data(syms,dates)
        dfn = ut.get_data(syms,datesn)
        prices = dfn[symbol]
        mom = prices/np.roll(prices,n) -1
        sma = (prices/prices.rolling(n).mean()) -1
        bb = (prices - sma)/2*prices.rolling(n).std()
        vd = prices.max() - prices.min()
        dfn['FB236'] = prices.min()+0.236*vd
        dfn['FB382'] = prices.min()+0.382*vd
        dfn['FB50'] = prices.min()+0.5*vd
        dfn['FB618'] = self.fbi
        dfn['FB100'] = prices.min()+vd
        dfn['MOM'] = prices+mom*prices
        dfn['SMA'] = prices.rolling(n).mean()
        dfn['BBU'] = dfn['SMA']+2*prices.rolling(n).std()
        dfn['BBL'] = dfn['SMA']-2*prices.rolling(n).std()
        dfn = dfn.drop([symbol],axis = 1)
        dfn = dfn.drop(['SPY'],axis = 1)
        df = df.join(dfn,how='left')
        prices = df[symbol]
        sin = np.ones(len(prices))

        df['FBI'] = df[symbol] - df['FB618']
        dbi = df['FBI'].values
        ss = self.binsize
        df['FBI'] = np.digitize(dbi,self.b1)-sin

        df['MOI'] = df[symbol] - df['MOM']
        dbi = df['MOI'].values
        df['MOI'] = np.digitize(dbi,self.b2)-sin

        df['SMI'] = df[symbol] - df['SMA']
        dbi = df['MOI'].values
        df['SMI'] = np.digitize(dbi,self.b3)-sin

        df['BBI'] = df[symbol] - df['BBU']
        dbi = df['BBI'].values
        df['BBI'] = np.digitize(dbi,self.b4)-sin

        df = df[[symbol,'FBI','MOI','SMI','BBI']]
        act = np.zeros(len(prices))
        i=0
        d=1
        for row in df.itertuples():
            a,b,c,d = row[2],row[3],row[4],row[5]
            p = row[1]
            nstate = (int)(a+b*ss+c*ss**2+d*ss**3)
            action = self.Q.querysetstate(nstate)
            act[i] = action -1
            i+=1
        df["Act"] = pd.Series(act, index = df.index)
        df['Symbol'] = symbol
        df = df[['Symbol','Act']]
        trades = ms.gen_trade(df=df,ind =-1)

        if self.verbose: print type(trades) # it better be a DataFrame!
        if self.verbose: print trades
        if self.verbose: print prices_all
        return trades

if __name__=="__main__":
    print "One does not simply think up a strategy"
