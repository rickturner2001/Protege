import sys
from pathlib import Path

CURRENT_DIR = str(Path(__file__).resolve().parent.parent / 'utilities')

sys.path.append(CURRENT_DIR)
sys.path.insert(0, CURRENT_DIR)



from functions import do_db_connection
from talib_related import db_historical_to_df
import tulipy as tp
import pandas as pd
import datetime
from config import DB_PATH

CURRENT_DATE = datetime.date.today()

connection = do_db_connection(DB_PATH)
cursor = connection.cursor()

symbols = cursor.execute("select * from to_be_scanned").fetchall()
if symbols:
    symbols = [symbol['Symbol'] for symbol in symbols]
    for symbol in symbols:
        df = db_historical_to_df(symbol, cursor)
        rsi = tp.rsi(df['Close'].values, 14)
        _, _, macd = tp.macd(df['Close'].values, 12, 26, 9)
        lower_bb, _, upper_bb = tp.bbands(df['Close'].values, 20, 2)

        df = df[::-1]
        df['RSI'] = pd.Series(rsi[::-1], index=df.index[:len(rsi)])
        df['MACD'] = pd.Series(macd[::-1], index=df.index[:len(macd)])
        df['Lower_BB'] = pd.Series(lower_bb[::-1], index=df.index[:len(lower_bb)])
        df['Upper_BB'] = pd.Series(upper_bb[::-1], index=df.index[:len(upper_bb)])
        df = df[::-1]

        df['Entry'] = [1 if df.loc[i]['RSI'] < 25 and df.loc[i]['Close'] < df.loc[i]['Lower_BB']
                        and df.loc[i]['MACD'] < 0 else 0 for i in df.index]

        if df.iloc[-1]['Entry'] == 1:
            print(f"{symbol} Has a good entry point -- {CURRENT_DATE}")
            cursor.execute("Insert into bullish_signals (Symbol, Date) Values (?, ?)", (symbol, str(CURRENT_DATE)))

else:
    print(F"Database is empty at this time {CURRENT_DATE}")