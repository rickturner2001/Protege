import sqlite3
import yfinance as yf
import requests
import pandas as pd
import time
from config import DB_PATH
    

start = time.time()
# Connection to our SQLite3 db
connection = sqlite3.connect(DB_PATH)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()    

cursor.execute("delete from historical_data")
# Wikipedia GET request to retrieve all securities in the sp100
# html = requests.get('https://en.wikipedia.org/wiki/S%26P_100').text
html = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies').text

# symbols = pd.read_html(html)[2]['Symbol'].values
symbols = pd.read_html(html)[0]['Symbol'].values
symbols = list(map(lambda x: x.replace('.', '-'), symbols))

data = yf.download(
        tickers=symbols,
        period='6mo',
        interval='1d',
        group_by='ticker',
        auto_adjust=False,
        prepost=False,
        threads=True,
        proxy=None
    )

data = data.T


for j, symbol in enumerate(symbols):
    print(f"{round(j / len(symbols) * 100, 2)}%")
    df = data.loc[symbol].T
    for i, date in enumerate(df.index):
        cursor.execute(
            """
            INSERT INTO historical_data (Date, Symbol, Open, High, Low, Close, Volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (str(df.index[i]),
                  symbol,
                  df.loc[date]['Open'],
                  df.loc[date]['High'],
                  df.loc[date]['Low'],
                  df.loc[date]['Close'],
                  df.loc[date]['Volume']))

connection.commit()

print('It took', time.time()-start, 'seconds.')