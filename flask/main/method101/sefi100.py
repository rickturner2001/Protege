
import pandas as pd
import tulipy as tp
import sqlite3
from text_functions import succesfull_action, failed_action, warning_message, cyan_message

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR.parent / 'database' / 'pre_watchlist.sqlite3'


def db_historical_to_df(symbol: str, cursor):
    cursor.execute("select * from historical_data where symbol = ? order by Date", (symbol,))
    data = cursor.fetchall()
    data = [[val['Date'], val['Open'], val['High'], val['Low'], val['Close'], val['Volume']] for val in data]
    data = pd.DataFrame(data, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    data.index = pd.to_datetime(data['Date'])
    data = data.drop('Date', axis=1)
    data.index.name = 'Date'

    return data

def do_db_connection(db_path: str, row_factory=True):
    connection = sqlite3.connect(db_path, check_same_thread=False)
    if row_factory:
        connection.row_factory = sqlite3.Row
    return connection

def get_sefi100(verbose: bool = False, df_return=False):
    exception_symbol = 0
    connection = do_db_connection(DB_PATH)
    cursor = connection.cursor()
    if verbose: print("Initializing Conneciton to database")
    symbols = cursor.execute('SELECT distinct symbol from historical_data').fetchall()
    symbols = [symbol['Symbol'] for symbol in symbols]
    good_signals = []
    temp = {}
    if verbose: succesfull_action("Connection to database was successful")
    for j, symbol in enumerate(symbols):
            try:
                if verbose: print(f"Creating DataFrame for {symbol}\t= {round(j / len(symbols) * 100, 2)}% =")
                df = db_historical_to_df(symbol, cursor)
                df['MA20'] = df['Close'].rolling(window=20).mean()
                df.dropna(inplace=True)
                df['SEFI'] = [1 if df.loc[i]['Close'] < df.loc[i]['MA20'] else 0 for i in df.index]
                if df.iloc[-1]['SEFI'] == 1:
                    good_signals.append(symbol)
                for i in df[df['SEFI'] > 0].index:
                    i = str(i)[:-9]
                    if not i in temp.keys():
                        temp[i] = 0
                    else:
                        temp[i] += 1
            except Exception:
                exception_symbol += 1
                warning_message(f"Couldn't Create a Database for {symbol}")
                

    for key in temp:
        temp[key] = round(temp[key] / (len(symbols) - exception_symbol) * 100, 2)

    sefi = pd.DataFrame(data=[temp[key] for key in temp], columns=['Value'], index=[key for key in temp])
    if verbose: succesfull_action("S5FI was successfully created")
    
    # if df_return : return sefi

    lower_bb, _, upper_bb = tp.bbands(sefi['Value'].values, 20, 2)


    sefi = sefi[::-1]
    sefi['Lower_BB'] = pd.Series(lower_bb[::-1], index=sefi.index[:len(lower_bb)])
    sefi['Upper_BB'] = pd.Series(upper_bb[::-1], index=sefi.index[:len(upper_bb)])
    sefi = sefi[::-1]
    sefi = sefi.sort_index()

    sefi['Entry'] = [
        -1 if sefi.loc[i]['Value'] < 50 and sefi.loc[i]['Value'] < sefi.loc[i]['Lower_BB']
        else 1 if sefi.loc[i]['Value'] > 50 and sefi.loc[i]['Value'] > sefi.loc[i]['Upper_BB']
        else 0  
        for i in sefi.index]

    if verbose: print("Looking for good entries")
    # return sefi
    if sefi.iloc[-1]['Entry'] == 1:
        if good_signals:
            succesfull_action("Entries were found")
            for signal in good_signals:
                print("signal")
            return good_signals
        
    cyan_message("No signals were found")

    sefi.to_csv("sefi.csv")

    return sefi


# What we need
    # date : x; sefi_value: x; and stocks with a positive value for date x


def sefi_backtest(sefi):
    connection = do_db_connection(DB_PATH)
    cursor = connection.cursor()

    symbols = cursor.execute('SELECT distinct symbol from historical_data').fetchall()
    symbols = [symbol['Symbol'] for symbol in symbols]
    good_signals = []
    temp = {}
    symbols_data = {}


    for symbol in symbols:
            df = db_historical_to_df(symbol, cursor)
            df['MA20'] = df['Close'].rolling(window=20).mean()
            df.dropna(inplace=True)
            df['SEFI'] = [1 if df.loc[i]['Close'] < df.loc[i]['MA20'] else 0 for i in df.index]

            for i in df[df['SEFI'] == 1].index:
                i = str(i)[:-9]
                if not i in symbols_data.keys():
                    symbols_data[i] = [symbol]
                else:
                    symbols_data[i].append(symbol)

                if not i in temp.keys():
                    temp[i] = 0
                else:
                    temp[i] += 1
    for key in temp:
        temp[key] = round(temp[key] / len(symbols) * 100, 2)

    sefi = pd.DataFrame(data=[temp[key] for key in temp], columns=['Value'], index=[key for key in temp])

    
    return symbols_data

if __name__ == "__main__":
    sefi = get_sefi100()

    # lower_bb, _, upper_bb = tp.bbands(sefi['Value'].values, 20, 2)


    # sefi = sefi[::-1]
    # sefi['Lower_BB'] = pd.Series(lower_bb[::-1], index=sefi.index[:len(lower_bb)])
    # sefi['Upper_BB'] = pd.Series(upper_bb[::-1], index=sefi.index[:len(upper_bb)])
    # sefi = sefi[::-1]
    # sefi = sefi.sort_index()

    # sefi['Entry'] = [
    #     -1 if sefi.loc[i]['Value'] < 50 and sefi.loc[i]['Value'] < sefi.loc[i]['Lower_BB']
    #     else 1 if sefi.loc[i]['Value'] > 50 and sefi.loc[i]['Value'] > sefi.loc[i]['Upper_BB']
    #     else 0  
    #     for i in sefi.index]

    # if sefi.iloc[-1]['Entry'] == 1:
    #     if good_signals:
    #         return good_signals

    # return sefi

