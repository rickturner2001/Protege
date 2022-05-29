import sys


sys.path.append('..')

import pandas as pd
import tulipy as tp
from utilities.config import DB_PATH
from utilities.indicators import rsi_macd_oversold
from utilities.functions import do_db_connection
import numpy as np
from pathlib import Path

csv_file = Path(__file__).resolve().parent / 'sp100.csv'
symbols = pd.read_csv(csv_file)
symbols = [symbol  if "." not in symbol else symbol.replace('.', '-') for symbol in symbols['Symbol']]

connection = do_db_connection(DB_PATH)
cursor = connection.cursor()
df_length = 10

for symbol in symbols:
    cursor.execute("select * from historical_data where symbol = ?", (symbol,))
    data = cursor.fetchall()
    closes = [d['Close'] for d in data]
    rsi = tp.rsi(np.array(closes).astype('float64'), period=14)
    index = [d['Date'] for d in data]
    _, _,macd = tp.macd(np.array(closes).astype('float64'), 12, 26, 9)
    df = pd.DataFrame(list(zip(closes[-(df_length):], rsi[-(df_length):], macd[-(df_length):])),
                        columns=['Close', 'RSI', 'MACD'], index=index[-(df_length):])
    df['pct_change'] = df['Close'].pct_change()
    if rsi_macd_oversold(df):
        print(df['pct_change']) 
        

