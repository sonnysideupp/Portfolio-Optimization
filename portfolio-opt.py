import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style 
import pandas as pd
import pandas_datareader.data as web
import fix_yahoo_finance as yf
from pandas.plotting import lag_plot
from pandas.plotting import autocorrelation_plot
from pandas import DataFrame
from pandas import concat
import numpy as np


start = dt.datetime(2018,1,1)
end = dt.datetime(2019,1,31)

AAPL = yf.download('AAPL',start,end)
WTW = yf.download('WTW',start,end)
WB = yf.download('WB',start,end)

AAPL['Return'] = np.array([0]*len(AAPL))
WTW['Return'] =  np.array([0]*len(WTW))
WB['Return'] =  np.array([0]*len(WTW)) 

for i in range(1,len(AAPL.Return)):
    AAPL.loc[AAPL.index[i],['Return']] = (AAPL['Adj Close'][i]/AAPL['Adj Close'][i-1]) - 1
    WTW.loc[WTW.index[i],['Return']] = (WTW['Adj Close'][i]/WTW['Adj Close'][i-1]) - 1
    WB.loc[WB.index[i],['Return']] = (WB['Adj Close'][i]/WB['Adj Close'][i-1]) - 1

MeanAAPL = np.mean(AAPL['Return'])
MeanWTW = np.mean(WTW['Return'])
MeanWB = np.mean(WB['Return'])

VarAAPL = np.var(AAPL['Return'])
VarWTW = np.var(WTW['Return'])
VarWB = np.var(WB['Return'])

AAPLreturn = pd.Series.as_matrix(AAPL['Return'])
WTWreturn = pd.Series.as_matrix(WTW['Return'])
WBreturn = pd.Series.as_matrix(WB['Return'])
x = []
x.append(AAPLreturn)
x.append(WTWreturn)
x.append(WBreturn)
covariancematrix = np.cov(x)


def lagrangian(w,lamda1,lamda2,sigma,a0,mean):
    part1 = (1/2)* np.matmul(np.matmul(w.transpose(),sigma),w)
    part2 = lamda1*(a0-np.matmul(w.transpose(),mean) )
    ones = np.array([1]*len(w))
    part3 = lamda2*(1- np.matmul(w.transpose(),ones) )
    return part1 + part2 + part3


