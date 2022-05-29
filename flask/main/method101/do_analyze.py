import sys
from pathlib import Path

CURRENT_DIR = str(Path(__file__).resolve().parent.parent / 'utilities')

from talib_related import db_historical_to_df
from functions import do_db_connection
from config import DB_PATH
import pandas as pd
import tulipy as tp


def slope(x1, y1, x2, y2):
    x = (y2 - y1) / (x2 - x1)
    return x

def get_returns(symbol: str, cursor, iteration: int) -> float:

    total_return = 0
    df = db_historical_to_df(symbol, cursor)
    df['MA100'] = df['Close'].rolling(window=100).mean()

    df.dropna(inplace=True)
    lower_bb, _, upper_bb = tp.bbands(df['Close'].values, 20, 2)
    df = df[::-1]
    df['lower_bb'] = pd.Series(lower_bb[::-1], index=df.index[:len(lower_bb)])
    df['upper_bb'] = pd.Series(upper_bb[::-1], index=df.index[:len(upper_bb)])
    df = df[::-1]

    df['Slope'] = [slope(i - 1, df.iloc[i - 1]['MA100'], i, df.iloc[i]['MA100'])
               if not i == 0 else 0
               for i, _ in enumerate(df.index)]

    shortened_df = df.loc[iteration:df.index[-1]]

    for n, date in enumerate(shortened_df.index):
        if shortened_df.loc[date]['Close'] >= shortened_df.loc[date]['upper_bb']:
            buy_price = shortened_df.iloc[0]['Close']
            sell_price = shortened_df.loc[date]['Close']
            total_return = round(((sell_price - buy_price) / sell_price) * 100, 2)
            
            break
    if not total_return:
        return None


def do_analyze(sefi, result_sefi_backtest):
    print(sefi)   
    connection = do_db_connection(DB_PATH)
    cursor = connection.cursor()

    positive_sefi = sefi[sefi['Entry'] == 1]

    total_returns = []

    for n, i in enumerate(positive_sefi.index):
        symbols = result_sefi_backtest[i]
        exit_bool = False

        for j, symbol in enumerate(symbols):
            total_returns.append(get_returns(symbol, cursor, i))

        break