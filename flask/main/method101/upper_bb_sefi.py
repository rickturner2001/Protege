import sys
from pathlib import Path

CURRENT_DIR = str(Path(__file__).resolve().parent.parent / 'utilities')

sys.path.append(CURRENT_DIR)
sys.path.insert(0, CURRENT_DIR)

    
from talib_related import db_historical_to_df
from functions import do_db_connection
from config import DB_PATH
import matplotlib.pyplot as plt
from sefi100 import get_sefi100, sefi_backtest
import tulipy as tp
import pandas as pd

sefi = get_sefi100()
result_sef_backtest = sefi_backtest(sefi)

connection = do_db_connection(DB_PATH)
cursor = connection.cursor()

positive_sefi = sefi[sefi['Entry'] == 1]

total_returns = []
no_exit_point_counter = 0

for i in positive_sefi.index:
    symbols = result_sef_backtest[i]
    exit_bool = False

    for symbol in symbols:
        df = db_historical_to_df(symbol, cursor)

        df.dropna(inplace=True)

        lower_bb, _, upper_bb = tp.bbands(df['Close'].values, 20, 2)


        df = df[::-1]
        df['lower_bb'] = pd.Series(lower_bb[::-1], index=df.index[:len(lower_bb)])
        df['upper_bb'] = pd.Series(upper_bb[::-1], index=df.index[:len(upper_bb)])
        df = df[::-1]

        df = df.loc[i:df.index[-1]]

        print(symbol," ", len(df))

        for n, date in enumerate(df.index):
            if df.loc[date]['Close'] >= df.loc[date]['upper_bb']:

                buy_price = df.iloc[0]['Close']
                sell_price = df.loc[date]['Close']

                total_return = round(((sell_price - buy_price) / sell_price) * 100, 2)
                total_returns.append(total_return)
                exit_bool = True
                
                break
            
        if not exit_bool:
            no_exit_point_counter += 1

import numpy as np
best_return = max(total_returns)
worst_return = min(total_returns)
mean_return = np.array(total_returns).mean()
positivity_range = len([i for i in total_returns if i > 0]) / len(total_returns) * 100
postive_mean_return = np.array([i for i in total_returns if i > 0]).mean()
negative_mean_return = np.array([i for i in total_returns if i < 0]).mean()