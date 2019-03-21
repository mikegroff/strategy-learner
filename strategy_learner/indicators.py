"""
Student Name: Michael Groff
GT User ID: mgroff3 (replace with your User ID)
GT ID: 902772277 (replace with your GT ID)
"""

import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import os
from util import get_data, plot_data

def author():
    return 'mgroff3' # replace tb34 with your Georgia Tech username.

def testPolicy(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31)):
    n = 20
    syms = [symbol]
    sdn = sd - dt.timedelta(days = n*2)
    datesn = pd.date_range(sdn, ed)
    dates = pd.date_range(sd, ed)
    df = get_data(syms,dates)
    dfn = get_data(syms,datesn)
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
    dfn['SMAI'] = prices/dfn['SMA']
    dfn['BBU'] = dfn['SMA']+2*prices.rolling(n).std()
    dfn['BBL'] = dfn['SMA']-2*prices.rolling(n).std()
    dfn = dfn.drop([symbol],axis = 1)
    dfn = dfn.drop(['SPY'],axis = 1)
    df = df.join(dfn,how='left')

    ax = df.plot(y = [symbol,'MOM'])
    plt.grid(linestyle='--')
    plt.title("Price and Momentum")
    plt.figure(1)
    ax = df.plot(y = [symbol,'BBU','BBL'])
    plt.grid(linestyle='--')
    plt.title("Price & Bollinger Bands")
    plt.figure(2)
    ax = df.plot(y = [symbol,'FB236','FB382','FB50','FB618','FB100'])
    plt.grid(linestyle='--')
    plt.title("Price & Fibonacci Retracement")
    plt.figure(3)
    ax = df.plot(y = [symbol,'SMA'])
    plt.grid(linestyle='--')
    plt.title("Price & SMA")
    plt.figure(4)


    #plt.savefig('compare.png', bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    testPolicy()
