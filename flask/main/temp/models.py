import sys
sys.path.append('..')
import tulipy as tp
import pandas as pd
import numpy as np
from peakdetect import peakdetect
from functions import do_db_connection
from config import DB_PATH
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from config import DB_PATH

connection = do_db_connection(DB_PATH)
cursor = connection.cursor()
symbols = cursor.execute('select distinct Symbol from historical_data').fetchall()
symbols = [symbol['Symbol'] for symbol in symbols]

for i, symbol in enumerate(symbols):

    cursor.execute('select * from historical_data where symbol = ?', (symbol,))
    print(f"{round(i / len(symbols) * 100, 2)}%")
    data = cursor.fetchall()
    closes = [c['Close'] for c in data]
    highs = [h['High'] for h in data]
    lows = [l['Low'] for l in data]
    df = pd.DataFrame(index=[d['Date'] for d in data],
                      columns=['Close', 'High', 'Low'],
                      data=list(zip(closes, highs, lows)))
    df.dropna(inplace=True)
    rsi = tp.rsi(df['Close'].values, period=14)
    _, _, macd = tp.macd(df['Close'].values, 12, 26, 9)
    stoch_k, stoch_d = tp.stoch(df['High'].values, df['Low'].values, df['Close'].values, 14, 1 , 3)
    df = df[::-1]
    df['RSI'] = pd.Series(rsi[::-1], index=df.index[:len(rsi)])
    df['MACD'] = pd.Series(macd[::-1], index=df.index[:len(macd)])
    df['stoch_k'] = pd.Series(stoch_k[::-1], index=df.index[:len(stoch_k)])
    df = df[::-1]
    from statsmodels.tsa.statespace.tools import diff
    df['d1'] = diff(df['Close'],k_diff=1)
    df = df.drop(['High', 'Low'], axis=1)
    df.dropna(inplace=True)
    peaks = peakdetect(df['Close'].values, lookahead=22) 
    lowerPeaks = np.array(peaks[1])
    index_entries = []
    for val in lowerPeaks:
        index_entries.append(df.index[int(val[0])])
    df['class'] = [0 for i in df.index]
    for i in index_entries:
        df.at[i, 'class'] = 1
    X = df.drop(['class', 'Close'], axis=1)
    y = df['class']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
    scaler = StandardScaler()
    scaled_X_train = scaler.fit_transform(X_train)
    scaled_X_test = scaler.transform(X_test)
    log_model = LogisticRegression(class_weight='balanced')
    log_model.fit(scaled_X_train, y_train)
    y_pred = log_model.predict(scaled_X_test)
    accuracy = accuracy_score(y_test, y_pred) * 100
    scaler = StandardScaler()
    scaled_X = scaler.fit_transform(X)
    log_model = LogisticRegression(class_weight='balanced')
    log_model.fit(scaled_X, y)
    
    results = log_model.predict(X)
    print()
    break