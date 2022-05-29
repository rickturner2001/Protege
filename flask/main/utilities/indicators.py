import sys

sys.path.append('.')

import pandas as pd
import numpy as np
import tulipy as tp
from talib_related import db_historical_to_df

# Classes
class DataFrame_constructor(object):
    def __init__(self, symbol, cursor):
        self.symbol = symbol
        self.cursor = cursor
        self.df = db_historical_to_df(self.symbol, self.cursor)
        self.df.dropna(inplace=True)

    def populate_df(
        self, rsi_val=14,
        macd_val=(12, 26, 9),
        ema_val=20, tema_val=50,
        stoch_val=(14,1,3),
        bollinger_val=(20, 2),
        psar_val=(2, 20)):

        closes = self.df['Close'].values
        highs = self.df['High'].values
        lows = self.df['Low'].values
        opens = self.df['Open'].values
        rsi = tp.rsi(closes, rsi_val)
        ema = tp.ema(closes[1:], ema_val)  
        _, _, macd = np.array(tp.macd(closes, macd_val[0], macd_val[1], macd_val[2]))
        
        lower, middle, upper = np.array(tp.bbands(closes, bollinger_val[0], bollinger_val[1]))
        tema = np.array(tp.tema(closes, tema_val))
        stoch_k, stoch_d = np.array(tp.stoch(highs, lows, closes, stoch_val[0], stoch_val[1], stoch_val[2]))
        psar = np.array(tp.psar(highs, lows, psar_val[0], psar_val[1]))
        self.df = self.df[::-1]
        self.df['MACD'] = pd.Series(macd[::-1], index=list(self.df.index)[:len(macd)])
        self.df['EMA'] = pd.Series(ema[::-1], index=list(self.df.index)[:len(ema)])
        self.df['RSI'] = pd.Series(rsi[::-1], index=list(self.df.index)[:len(rsi)])
        self.df['lower_bollinger'] = pd.Series(lower[::-1], index=list(self.df.index)[:len(lower)])
        self.df['middle_bollinger'] = pd.Series(middle[::-1], index=list(self.df.index)[:len(middle)])
        self.df['upper_bollinger'] = pd.Series(upper[::-1], index=list(self.df.index)[:len(upper)])
        self.df['TEMA'] = pd.Series(tema[::-1], index=list(self.df.index)[:len(tema)])
        self.df['stochastic_k'] = pd.Series(stoch_k[::-1], index=list(self.df.index)[:len(stoch_k)])
        self.df['stochastic_d'] = pd.Series(stoch_d[::-1], index=list(self.df.index)[:len(stoch_d)])
        self.df['PSAR'] = pd.Series(psar[::-1], index=list(self.df.index)[:len(psar)])
        self.df = self.df[::-1]

        return self.df


# Utility Functions
def get_percent_change(df):
    change = ((df.iloc[-1]['Close'] - df.iloc[0]['Close']) / abs(df.iloc[-1]['Close'])) * 100
    return change


def test_best_range(df, strategy):
    day_to_check = -1
    position_return = 0
    while not position_return > 0:
        if day_to_check == -50:
            df_copy = df.copy().iloc[day_to_check:]
            position_return = get_percent_change(df_copy)
            return (day_to_check, round(position_return, 2))

        if strategy(df, day_to_check):
            df_copy = df.copy().iloc[day_to_check:]
            position_return = get_percent_change(df_copy)
        day_to_check -= 1   

    return (day_to_check, round(position_return, 2))
    

# Strategies
def rsi_macd_oversold(df, index):
    if df.iloc[index]['RSI'] < 40 and df.iloc[index]['MACD'] < 0: return True


def close_below_lower_band(df, index):
    if df.iloc[index]['Close'] < df.iloc[index]['lower_bollinger']: return True