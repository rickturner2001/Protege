import sys

sys.path.append('..')

from typing import Iterable
import yfinance as yf
from scipy.stats import linregress
import sqlite3
import warnings
import concurrent.futures

warnings.filterwarnings('ignore')


def threadpool_executor(func, args:list, workers:int) -> Iterable:
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        results = executor.map(func, args)
        return results

def normalize(n: int, x_max: int, x_min: int) -> float:
    """
    Normalize `n` to be between 0 and 1 
    """
    return (n - x_min) / (x_max - x_min)

        
def valuate(data, key: str, best_val: int, worst_val: int) -> tuple:
    """
    Return: (value, evaluation)
    Take a value form a given dictionary and normalize it to  0-1 range  between `worst_val` and `best_val`
    """
    value = data.loc[key]['Values']
    # Check if value is True
    if value:
        # Determine whether the best value is greater than the worst
        # so that we can give the correct evaluation once one of the values is out of bounds (worst_val, best_val)
        if best_val > worst_val:
            if not value > best_val and not value < worst_val: 
                valuation = normalize(n=value, x_max=best_val, x_min=worst_val)
            else:
                if value > best_val:
                    valuation = 1
                elif value < worst_val:
                    valuation = 0
        else:
            if not value < best_val and not value > worst_val:
                valuation = normalize(n=value, x_max=best_val, x_min=worst_val)
            else:
                if value < best_val:
                    valuation = 1
                elif value > worst_val:
                    valuation = 0
    else:
        valuation = 0
        
    return value, valuation


def do_db_connection(db_path: str, row_factory=True):
    connection = sqlite3.connect(db_path, check_same_thread=False)
    if row_factory:
        connection.row_factory = sqlite3.Row
    return connection
    

def beta_and_alpha(df, index_df) -> tuple:
    beta, alpha, _, _, _ = linregress(index_df[-len(df):]['Daily Returns'], df['Daily Returns'])
    return alpha, beta


# The S5FI is an index that tells what percentage of  stocks in the S&P 500 are Above the 50-Day Moving Average

def s5fi(self):
    """Function that returns the closes of the S5FI for the last 6 months, along
    with a matplotlib .png file displaying the plot of S5FI closes """
    dfs = self.df_symbols['long'].copy()
    for df in dfs:
        df['MA50'] = df['Adj Close'].rolling(window=50).mean()
    dfs = [df[df['MA50'] > 0] for df in dfs]
    dfs = [df[['Adj Close', 'MA50']] for df in dfs]
    for df in dfs:
        df['S5FI'] = [1 if df['Adj Close'].loc[i] > df['MA50'].loc[i] else 0 for i in df.index]
    for i, df in enumerate(dfs):
        if len(df) != len(dfs[0]):
            del dfs[i]
    apt = []
    for i, df in enumerate(dfs):
        counter = 0
        for _ in df.index:
            if df.iloc[counter]['S5FI'] > 0:
                apt.append((self.symbols[i], counter))
                counter += 1
            else:
                counter += 1
    sorted_apt = sorted(apt, key=lambda x: x[1])
    vals = {}
    for i in range(len(dfs[0])):
        vals[i] = 0 
        for e in sorted_apt:
            if e[1] == i:
                vals[i] += 1
    self.closes_S5FI = []
    for v in vals:
        self.closes_S5FI.append((vals[v] / len(dfs) * 100)) 
    return self.closes_S5FI


def get_spx(self):
    self.spx_data = {}
    """Function that returns the spx percent change and saves a .png file
    displaying the spx line plot along with MA50 and MA20"""
    spx = yf.download('^GSPC', period='1d', interval='1m')
    spx['MA50'] = spx['Adj Close'].rolling(window=50).mean()
    spx['MA20'] = spx['Adj Close'].rolling(window=20).mean()
    
    self.spx_data['spx_pct_change'] = (spx['Adj Close'].iloc[-1] - spx['Open'].iloc[0]) / spx['Adj Close'].iloc[0] * 100
    self.spx_data['last_close'] = spx.iloc[-1]['Close']
    return self.spx_data


# VIX is the ticker symbol and the popular name for the Chicago Board Options Exchange's CBOE Volatility Index,
# a popular measure of the stock market's expectation of volatility based on S&P 500 index options.
def get_vix(self):
    """Function that returns the last closing price of VIX and its supports and resistances, along
    with a matplotlib .png file displaying the plot of VIX closes and resistances/supports"""
    self.vix_data = {}
    data_week = yf.download('^VIX', period='6mo', interval='1wk')
    data_day = yf.download('^VIX', period='2y', interval='1d')
    
    lowest_low_index = data_week['Low'].idxmin()
    highest_high_index = data_week['High'].idxmax()
    last_close = data_week.iloc[-1]['Close']
    highest_high = data_week.loc[highest_high_index]['High']
    lowest_low = data_week.loc[lowest_low_index]['Low']
    pivot_point = (highest_high + lowest_low + last_close) / 3
    # Getting supports and resistances
    r_one = 2 * pivot_point - lowest_low
    s_one = 2 * pivot_point - highest_high
    r_two = pivot_point + (highest_high - lowest_low)
    s_two = pivot_point - (highest_high - lowest_low)
    r_three = highest_high + 2 * (pivot_point - lowest_low)
    s_three = lowest_low - 2 * (highest_high - pivot_point)
    supports = [s_one, s_two, s_three]
    resistances = [r_one, r_two, r_three]
    self.vix_data['supports'] = supports
    self.vix_data['resistances'] = resistances 
    self.vix_data['closes'] = data_day['Close']
    return self.vix_data

