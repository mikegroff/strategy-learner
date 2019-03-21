"""
Student Name: Michael Groff (replace with your name)
GT User ID: mgroff3 (replace with your User ID)
GT ID: 902772277 (replace with your GT ID)
"""

import datetime as dt
import pandas as pd
from util import get_data, plot_data
import QLearner as ql
import marketsimcode as ma
import random
import ManualStrategy as ms
import StrategyLearner as sl
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

def author():
    return 'mgroff3' # replace tb34 with your Georgia Tech username.

if __name__=="__main__":
    symbol = "JPM"
    sd=dt.datetime(2008,1,1)
    ed=dt.datetime(2009,12,31)
    sv = 100000
    syms = [symbol]
    dates = pd.date_range(sd, ed)
    df = get_data(syms,dates)
    prices = df[symbol]
    sp = prices.iloc[0]
    ep = prices.iloc[-1]
    bm = prices*1000 + (sv - sp*1000)

    learner = sl.StrategyLearner(verbose = False, impact = 0.005) # constructor
    learner.addEvidence(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000) # training phase
    df_trades = learner.testPolicy(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000) # testing phase
    df_trades = ms.con_trades(df_trades,symbol)
    pv = ma.compute_portvals(df_trades, start_val = sv, commission=9.95, impact=0.005)
    buy = df_trades.index[df_trades['Order'] == 'BUY'].tolist()
    sell = df_trades.index[df_trades['Order'] == 'SELL'].tolist()
    pv['PortVal'] /=sv
    pv['Bench'] = bm/sv

    ax = pv.plot(y = ['PortVal','Bench'],colormap = colors.ListedColormap(['k','b']))
    for xc in buy:
        ax.axvline(x=pd.to_datetime(xc),color = 'green',linestyle='-')
    for xc in sell:
        ax.axvline(x=pd.to_datetime(xc),color = 'red',linestyle='-')
    plt.grid(linestyle='--')
    plt.title("Portfolio Value(Q) and Benchmark")
    plt.figure(1)

    norm = pv['PortVal']
    normb = pv['Bench']
    cum_ret = norm.iloc[-1]/norm.iloc[0]-1
    cum_ret_b = normb.iloc[-1]/normb.iloc[0]-1

    dret = (norm / np.roll(norm, 1)) - 1
    dret = dret[1:]
    dretb = (normb / np.roll(normb, 1)) - 1
    dretb =dretb[1:]
    std_daily_ret=dret.std()
    std_daily_ret_b=dretb.std()
    avg_daily_ret=dret.mean()
    avg_daily_ret_b=dretb.mean()


    print "In-sample"
    print
    print "Date Range: {} to {}".format(sd, ed)
    print
    print "Cumulative Return of Portfolio(Q): {}".format(cum_ret)
    print "Cumulative Return of Benchmark : {}".format(cum_ret_b)
    print
    print "Standard Deviation of Portfolio(Q): {}".format(std_daily_ret)
    print "Standard Deviation of Benchmark : {}".format(std_daily_ret_b)
    print
    print "Average Daily Return of Portfolio(Q): {}".format(avg_daily_ret)
    print "Average Daily Return of Benchmark : {}".format(avg_daily_ret_b)
    print

    ms.testPolicy(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)

    sd=dt.datetime(2010,1,1)
    ed=dt.datetime(2011,12,31)
    sv = 100000
    syms = [symbol]
    dates = pd.date_range(sd, ed)
    df = get_data(syms,dates)
    prices = df[symbol]
    sp = prices.iloc[0]
    ep = prices.iloc[-1]
    bm = prices*1000 + (sv - sp*1000)

    learner = sl.StrategyLearner(verbose = False, impact = 0.005) # constructor
    learner.addEvidence(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000) # training phase
    df_trades = learner.testPolicy(symbol = "JPM", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000) # testing phase
    df_trades = ms.con_trades(df_trades,symbol)
    pv = ma.compute_portvals(df_trades, start_val = sv, commission=9.95, impact=0.005)
    buy = df_trades.index[df_trades['Order'] == 'BUY'].tolist()
    sell = df_trades.index[df_trades['Order'] == 'SELL'].tolist()
    pv['PortVal'] /=sv
    pv['Bench'] = bm/sv

    ax = pv.plot(y = ['PortVal','Bench'],colormap = colors.ListedColormap(['k','b']))
    for xc in buy:
        ax.axvline(x=pd.to_datetime(xc),color = 'green',linestyle='-')
    for xc in sell:
        ax.axvline(x=pd.to_datetime(xc),color = 'red',linestyle='-')
    plt.grid(linestyle='--')
    plt.title("Portfolio Value(Q) and Benchmark")
    plt.figure(1)

    norm = pv['PortVal']
    normb = pv['Bench']
    cum_ret = norm.iloc[-1]/norm.iloc[0]-1
    cum_ret_b = normb.iloc[-1]/normb.iloc[0]-1

    dret = (norm / np.roll(norm, 1)) - 1
    dret = dret[1:]
    dretb = (normb / np.roll(normb, 1)) - 1
    dretb =dretb[1:]
    std_daily_ret=dret.std()
    std_daily_ret_b=dretb.std()
    avg_daily_ret=dret.mean()
    avg_daily_ret_b=dretb.mean()


    print "Out-sample"
    print
    print "Date Range: {} to {}".format(sd, ed)
    print
    print "Cumulative Return of Portfolio(Q): {}".format(cum_ret)
    print "Cumulative Return of Benchmark : {}".format(cum_ret_b)
    print
    print "Standard Deviation of Portfolio(Q): {}".format(std_daily_ret)
    print "Standard Deviation of Benchmark : {}".format(std_daily_ret_b)
    print
    print "Average Daily Return of Portfolio(Q): {}".format(avg_daily_ret)
    print "Average Daily Return of Benchmark : {}".format(avg_daily_ret_b)
    print

    ms.testPolicy(symbol = "JPM", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000)

    plt.show()
