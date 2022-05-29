import sys

sys.path.append('.')

from utilities.config import DB_PATH
import yfinance as yf
import sqlite3

connection = sqlite3.connect(DB_PATH)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("select distinct symbol from historical_data")
symbols = cursor.fetchall()

symbols = [symbol['Symbol'] if '.' not in symbol['Symbol']
            else symbol['Symbol'].replace('.', '-') for symbol in symbols]

data = yf.download(
        tickers=symbols,
        period='1d',
        interval='1d',
        group_by='ticker',
        auto_adjust=False,
        prepost=False,
        threads=True,
        proxy=None
    )

data = data.T


for i, symbol in enumerate(symbols):

    df = data.loc[symbol].T
    print(f"{round(i / len(symbols) * 100, 2)}%")

    cursor.execute("select * from historical_data where symbol = ? limit 1", (symbol,))
    date = cursor.fetchall()
    
    date = date[0]['Date']
    print(date)
    cursor.execute(
        """
        DELETE FROM historical_data WHERE Symbol = ? and Date = ?
        """, (symbol, str(date)))
    
    cursor.execute(
        """
        INSERT INTO historical_data (Date, Symbol, Open, High, Low, Close, Volume)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (str(df.index[0]),
              symbol,
              df.iloc[0]['Open'],
              df.iloc[0]['High'],
              df.iloc[0]['Low'],
              df.iloc[0]['Close'],
              df.iloc[0]['Volume'],
              ))
connection.commit()
