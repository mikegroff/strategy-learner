"""
Student Name: Michael Groff
GT User ID: mgroff3 (replace with your User ID)
GT ID: 902772277 (replace with your GT ID)
"""
from matplotlib import colors
import marketsimcode as ma
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def con_trades(df,sym):
    df_trades= df
    ord = ['NA']*len(df)
    shr = np.zeros(len(df))
    i = 0
    for row in df_trades.itertuples():
        i+=1
        act = row[-1]
        if act < 0:
            ord[i-1] = 'SELL'
            shr[i-1] = -act
        else:
            ord[i-1] = 'BUY'
            shr[i-1] = act

    df_trades['Symbol'] = sym
    df_trades["Order"] = pd.Series(ord, index = df.index)
    df_trades = df_trades.drop(['Shares'],axis = 1)
    df_trades["Shares"] = pd.Series(shr, index = df.index)
    df_trades = df_trades[['Symbol','Order','Shares']]
    return df_trades

def gen_trade(df,ind):
    df_trades = df
    pa = 0
    ord = ['NA']*len(df)
    shr = np.zeros(len(df))
    shr[:] = np.nan
    i = 0
    for row in df_trades.itertuples():
        i+=1
        if(i==1):
            ord[i-1] = 'BUY'
            shr[i-1] = 0
        if(i==len(df)):
            ord[i-1] = 'SELL'
            shr[i-1] = 0

        act = row[ind]
        if act == 1:
            if pa ==1:
                continue
            elif pa ==-1:
                ord[i-1] = 'BUY'
                shr[i-1] = 2000
            else:
                ord[i-1] = 'BUY'
                shr[i-1] = 1000
        elif act == -1:
            if pa == -1:
                continue
            elif pa ==1:
                ord[i-1] = 'SELL'
                shr[i-1] = -2000
            else:
                ord[i-1] = 'SELL'
                shr[i-1] = -1000
        else:
            if pa == 1:
                ord[i-1] = 'SELL'
                shr[i-1] = -1000
            elif pa == -1:
                ord[i-1] = 'BUY'
                shr[i-1] = 1000
            else:
                continue
        pa = act
    df_trades = df_trades.drop(['Act'],axis = 1)
    df_trades["Order"] = pd.Series(ord, index = df.index)
    df_trades["Shares"] = pd.Series(shr, index = df.index)
    df_trades = df_trades.dropna()
    df_trades = df_trades.drop(['Order'],axis = 1)
    df_trades = df_trades.drop(['Symbol'],axis = 1)

    return df_trades

def gen_trades(df,ind = -1):
    df_trades = df
    pa = 0
    ord = ['NA']*len(df)
    shr = np.zeros(len(df))
    shr[:] = np.nan
    i = 0
    for row in df_trades.itertuples():
        i+=1
        if(i==1):
            ord[i-1] = 'BUY'
            shr[i-1] = 0
        if(i==len(df)):
            ord[i-1] = 'SELL'
            shr[i-1] = 0
        act = row[ind]
        if act == 1:
            if pa ==1:
                continue
            elif pa ==-1:
                ord[i-1] = 'BUY'
                shr[i-1] = 2000
            else:
                ord[i-1] = 'BUY'
                shr[i-1] = 1000
        elif act == -1:
            if pa == -1:
                continue
            elif pa ==1:
                ord[i-1] = 'SELL'
                shr[i-1] = 2000
            else:
                ord[i-1] = 'SELL'
                shr[i-1] = 1000
        else:
            if pa == 1:
                ord[i-1] = 'SELL'
                shr[i-1] = 1000
            elif pa == -1:
                ord[i-1] = 'BUY'
                shr[i-1] = 1000
            else:
                continue
        pa = act
    df_trades = df_trades.drop(['Act'],axis = 1)
    df_trades["Order"] = pd.Series(ord, index = df.index)
    df_trades["Shares"] = pd.Series(shr, index = df.index)
    df_trades = df_trades.dropna()

    return df_trades

def testPolicy(symbol = "JPM", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000):
    n = 20
    syms = [symbol]
    sdn = sd - dt.timedelta(days = n*10)
    datesn = pd.date_range(sdn, ed)
    dates = pd.date_range(sd, ed)
    df = get_data(syms,dates)
    dfn = get_data(syms,datesn)
    prices = dfn[symbol]
    pmax = prices.max()
    pmin = prices.min()
    sp = prices.iloc[0]
    mom = prices/np.roll(prices,n) -1
    sma = (prices/prices.rolling(n).mean()) -1
    bb = (prices - prices.rolling(n).mean())/(2*prices.rolling(n).std())
    mom = prices/np.roll(prices,n) -1
    sma = (prices/prices.rolling(n).mean()) -1
    bb = (prices-prices.rolling(n).mean())/2.5*prices.rolling(n).std()
    fr = (prices.rolling(n*5).max()-prices.rolling(n*5).min())*0.618 + prices.rolling(n*5).min()
    dfn['MOM'] = mom
    dfn['SMA'] = sma
    dfn['BB'] = bb
    dfn['FR'] = fr
    dfn = dfn.drop([symbol],axis = 1)
    dfn = dfn.drop(['SPY'],axis = 1)
    df = df.join(dfn,how='left')

    prices = df[symbol]
    sp = prices.iloc[0]
    ep = prices.iloc[-1]
    bm = prices*1000 + (sv - sp*1000)
    act = np.zeros(len(prices))
    df = df.drop(['SPY'],axis = 1)
    df['Symbol'] = symbol
    bs = 0
    frs = 0
    i =0
    pp = sp
    pact = 0
    for row in df.itertuples():
        p = row[1]
        m = row[2]
        s = row[3]
        b = row[4]
        f = row[5]
        if p<pmin:
            pmin = p
        if p>pmax:
            pmax = p
        fr = (pmax - pmin)


        if (b < 1) and (bs>1):
            act[i] = -1
        elif (b > -1) and (bs<-1):
            act[i] = 1
        elif (m>0) and (p < f):
            act[i] = 1
        elif (m<0) and (p>f):
            act[i] = -1
        else:
            act[i] = pact

        pact = act[i]
        i+=1

        bs = b
        pp = p



    df["Act"] = pd.Series(act, index = df.index)
    df = df.drop([symbol],axis = 1)
    df = df.drop(['MOM'],axis = 1)
    df = df.drop(['SMA'],axis = 1)
    df = df.drop(['BB'],axis = 1)
    df = df.drop(['FR'],axis = 1)
    df_trades = gen_trades(df)
    buy = df_trades.index[df_trades['Order'] == 'BUY'].tolist()
    sell = df_trades.index[df_trades['Order'] == 'SELL'].tolist()
    pv = ma.compute_portvals(df_trades, start_val = sv, commission=9.95, impact=0.005)
    pv['PortVal'] /=sv
    pv['Bench'] = bm/sv
    print(len(pv['Bench']))

    ax = pv.plot(y = ['PortVal','Bench'],colormap = colors.ListedColormap(['k','b']))
    for xc in buy:
        ax.axvline(x=pd.to_datetime(xc),color = 'green',linestyle='-')
    for xc in sell:
        ax.axvline(x=pd.to_datetime(xc),color = 'red',linestyle='-')
    plt.grid(linestyle='--')
    plt.title("Portfolio Value(M) and Benchmark")
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


    print "Date Range: {} to {}".format(sd, ed)
    print
    print "Cumulative Return of Portfolio(M): {}".format(cum_ret)
    print "Cumulative Return of Benchmark : {}".format(cum_ret_b)
    print
    print "Standard Deviation of Portfolio(M): {}".format(std_daily_ret)
    print "Standard Deviation of Benchmark : {}".format(std_daily_ret_b)
    print
    print "Average Daily Return of Portfolio(M): {}".format(avg_daily_ret)
    print "Average Daily Return of Benchmark : {}".format(avg_daily_ret_b)


    plt.show()

    return df_trades
if __name__ == "__main__":
    testPolicy()
