#Import proprer packages
import numpy as np
import pandas as pd
import datetime as dt
from pylab import mpl, plt

plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'
%config InlineBackend.figure_format = 'svg'

#Set up the directory for opening the file in the IDE
raw = pd.read_csv('C:\\Users\\LJone\\Fin510\\Stocks\\yf_eod_data.csv',
                  index_col=0, parse_dates=True)
raw.info()

symbol = 'AAPL'

data = (
    pd.DataFrame(raw[symbol])
    .dropna()
)

#Now lets implement the Simple moving Trading Strategy
#SMA1 = calcs the values for shorter SMA   SMA2 = calcs the values for longer SMA

SMA1 = 42  
SMA2 = 252
data['SMA1'] = data[symbol].rolling(SMA1).mean()  
data['SMA2'] = data[symbol].rolling(SMA2).mean()
data.plot(figsize=(10, 6));
data.dropna(inplace=True)
# This next line evaluates the condition cond element and places a when Truw AND b otherwise. Tells us when to short
data['Position'] = np.where(data['SMA1'] > data['SMA2'], 1, -1)
data.tail()
ax = data.plot(secondary_y='Position', figsize=(10, 6))
ax.get_legend().set_bbox_to_anchor((0.25, 0.85))

#How to interpret the plot
# Go long aka buy (=+1) when SMA1 is above than the SMA2
# Go short aka sell(=-1) when the SMA1 is lower than the SMA2

#Calculates the log returns of the stock (benchmark investment)
data['Returns'] = np.log(data[symbol] / data[symbol].shift(1))

#Multiplies the position values, shifted by 1 day by log returns of stock, shift is required to avoid foresight bias, can only predict tomorrow's return
data['Strategy'] = data['Position'].shift(1) * data['Returns']
data.round(4).head()
data.dropna(inplace=True)

#Sums the log returns for the strategy and the benchmark investment and calculates exponent value to arrive at absolute performance
np.exp(data[['Returns', 'Strategy']].sum())

#Calcs the annualized volatility for the strategy and benchmark investment  
data[['Returns', 'Strategy']].std() * 252 ** 0.5  

#Plots the performance of Stock and SMA-based trading strategy overtime (If you were to hold stock = returns / SMA Strategy = strategy)
ax = data[['Returns', 'Strategy']].cumsum(
        ).apply(np.exp).plot(figsize=(10, 6))
data['Position'].plot(ax=ax, secondary_y='Position', style='--')
ax.get_legend().set_bbox_to_anchor((0.25, 0.85)); 




 

 