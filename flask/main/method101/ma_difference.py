

import numpy as np
from peakdetect import peakdetect
from functions import normalize
import tulipy as tp
import pandas as pd
from functions import do_db_connection
from config import DB_PATH
from scipy.signal import find_peaks
from text_functions import succesfull_action, failed_action, cyan_message, warning_message
# NSDMA = Normalized Squared Difference Moving Averages

def db_historical_to_df(symbol: str, cursor, limit=0):
    if limit:
        cursor.execute("select * from historical_data where symbol = ? order by Date desc limit ?", (symbol, limit))
    else:
        cursor.execute("select * from historical_data where symbol = ? order by Date", (symbol,))
    data = cursor.fetchall()
    data = [[val['Date'], val['Open'], val['High'], val['Low'], val['Close'], val['Volume']] for val in data]
    data = pd.DataFrame(data, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    data.index = pd.to_datetime(data['Date'])
    data = data.drop('Date', axis=1)
    data.index.name = 'Date'

    return data


def do_analysis(df, ticker:str):

    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df.dropna(inplace=True)
    df['Fast Over Slow'] = [True if df['MA20'].loc[i] >
                        df['MA50'].loc[i] else False for i in df.index]
    df['NSDMA'] = [
        (df.loc[i]['MA20'] - df.loc[i]['MA50']) ** 2 for i in df.index]
    df['NSDMA'] = np.vectorize(normalize)(
    df['NSDMA'],
    df['NSDMA'].max(),
    df['NSDMA'].min())


    stoch_k, _ = tp.stoch(df['High'].values, df['Low'].values, df['Close'].values, 14, 1, 3)
    rsi = tp.rsi(df['Close'].values, period=14)

    df = df[::-1]
    df['stoch_k'] = pd.Series(
        stoch_k[::-1], index=df.index[:len(stoch_k)])
    df['RSI'] = pd.Series(
        rsi[::-1], index=df.index[:len(rsi)])
    df = df[::-1]

    range_starts = []
    for i, date in enumerate(df.index):
        if not df.iloc[i]['Fast Over Slow'] and df.iloc[i - 1]['Fast Over Slow']:
            range_starts.append(date)

    range_ends = []
    for i, date in enumerate(df.index):
        if df.iloc[i]['Fast Over Slow'] and not df.iloc[i - 1]['Fast Over Slow']:
            range_ends.append(date)

    # max_peaks, _ = peakdetect(df['NSDMA'].values, lookahead=21)
    # max_peaks_index = [i for i, _ in max_peaks]
    # max_peaks_values = [i for _, i in max_peaks]
    peaks = find_peaks(df['NSDMA'].values, height=0.1, threshold=0.0001, distance=10)
    peaks = peaks[0]
    max_peaks_values_mean = np.array([df.iloc[i]['NSDMA'] for i in peaks]).mean() * 0.60

    # max_peaks_values_mean = np.array(max_peaks_values).mean() * 0.80
    if range_ends[0] < range_starts[0]: range_ends.pop(0)
    if range_starts[-1] > range_ends[-1]: range_starts.pop()

    range_strategy = list(zip(range_starts, range_ends))

    highest_nsdma_values = []
    for range_ in range_strategy:
        start, end = range_

        max_nsdma = df.loc[start:end]['NSDMA'].max()
        highest_nsdma_values.append(max_nsdma)

    ideal_nsdma_value = min(highest_nsdma_values)

    entries = []
    exits = []
    for n, range_ in enumerate(range_strategy):
        entry = False
        exit_ = False
        start, end = range_
        for i in df[start:end].index:

                if df.loc[i]['NSDMA'] >= ideal_nsdma_value:
                    # We Account for the entry so that we know if we should look for an exit point
                    entry = True
                    entries.append(i)
                    break

        # Check if we can get the next entry (not in the last detected range bacause there wouldn't be a next start)
        if not n == len(range_strategy) - 1:
                # The dataframe will now be from the end of the interception to the beginning of the NEXT one
                # range_strategy[n + 1] is the next range, this is why make sure we are not on the last range_strategy
                # or else this will throw an error
                current_df = df.loc[end: range_strategy[n + 1][0]]
                

                for i in current_df.index:

                    if current_df.loc[i]['NSDMA'] >= max_peaks_values_mean:
                        exit_ = True
                        exits.append(i)
                        break
                    elif current_df.loc[i]['RSI'] >= 70:
                        exit_ = True
                        exits.append(i)
                        break
                    elif current_df.loc[i]['stoch_k'] >= 85:
                        exit_ = True
                        exits.append(i)
                        break

                # In the event that we cant find a suitable exit point we sell at the end of the range regardless
                if not exit_:
                    print("No exit")
                    # We use i since the last i came from the for loop above (last iteration = last date)
                    exits.append(i)
        else:
            # If we are on our last range then the dataframe will be from the
            # end of the selling_df to the end of the main dataframe
            current_df = df.loc[end:]
            
            for i in current_df.index:

                if current_df.loc[i]['NSDMA'] >= max_peaks_values_mean:
                    exit_ = True
                    exits.append(i)
                    break
                elif current_df.loc[i]['RSI'] >= 70:
                    exit_ = True
                    exits.append(i)
                    break
                elif current_df.loc[i]['stoch_k'] >= 85:
                    exit_ = True
                    exits.append(i)
                    break
               
                
            
            # If we didn't find an exit point on out last position then we don't want to consider our entry position
            if not exit_:
                entries.pop()

    positions = list(zip(entries, exits))

    # Check for the Total returns of each position (entry-exit)

    returns = []

    for position in positions:
        start, end = position

        df_position = df.loc[start:end]

        buy_price = df_position.iloc[0]['Close']
        sell_price = df_position.iloc[-1]['Close']

        total_return = round(
            ((sell_price - buy_price) / sell_price) * 100, 2)
        returns.append(total_return)
        if total_return <= -20:
            print(f"{ticker}... start->{start}...end->{end}")
    return returns


def get_nsdma_signals(df_return=False,verbose:bool=False ):
    symbol_exceptions = 0
    connection = do_db_connection(DB_PATH)
    cursor = connection.cursor()
    symbols = cursor.execute("select distinct symbol from historical_data").fetchall()
    symbols = [symbol['Symbol'] for symbol in symbols]
    if verbose: succesfull_action("Succesfully connected to the database")
    for j, symbol in enumerate(symbols):
        # try:
            if verbose: print(f"Creating DataFrame for {symbol}\t{round(j / len(symbols) * 100, 2)}%")

            signals = []
            df = db_historical_to_df(symbol, cursor)
        
            if len(df) < 50: return None

            df['MA20'] = df['Close'].rolling(window=20).mean()
            df['MA50'] = df['Close'].rolling(window=50).mean()
            df.dropna(inplace=True)
            df['Fast Over Slow'] = [True if df['MA20'].loc[i] >
                                df['MA50'].loc[i] else False for i in df.index]
            df['NSDMA'] = [
                (df.loc[i]['MA20'] - df.loc[i]['MA50']) ** 2 for i in df.index]
            if len(df['NSDMA'] > 0):
                df['NSDMA'] = np.vectorize(normalize)(
                df['NSDMA'],
                df['NSDMA'].max(),
                df['NSDMA'].min())
        

            range_starts = []
            for i, date in enumerate(df.index):
                if not df.iloc[i]['Fast Over Slow'] and df.iloc[i - 1]['Fast Over Slow']:
                    range_starts.append(date)

            range_ends = []
            for i, date in enumerate(df.index):
                if df.iloc[i]['Fast Over Slow'] and not df.iloc[i - 1]['Fast Over Slow']:
                    range_ends.append(date)

            max_peaks, _ = peakdetect(df['NSDMA'].values, lookahead=21)
            max_peaks_index = [i for i, _ in max_peaks]
            max_peaks_values = [i for _, i in max_peaks]

            max_peaks_values_mean = np.array(max_peaks_values).mean() * 0.80

            if range_ends[0] < range_starts[0]: range_ends.pop(0)
            if range_starts[-1] > range_ends[-1]: range_starts.pop()

            range_strategy = list(zip(range_starts, range_ends))

            highest_nsdma_values = []
            for range_ in range_strategy:
                start, end = range_

                max_nsdma = df.loc[start:end]['NSDMA'].max()
                highest_nsdma_values.append(max_nsdma)

            ideal_nsdma_value = min(highest_nsdma_values)

            if df['NSDMA'].iloc[-1] >= ideal_nsdma_value and not df.iloc[-1]['Fast Over Slow']:
                signals.append(symbol)
        # except Exception:
        #     warning_message(f"Could not create a Dataframe for {symbol}")
        #     symbol_exceptions += 1
    
    if verbose: succesfull_action("NSMA Analysis was succesfully finalized...")
    if signals:
        for signal in signals:
            print(signal)
    else:
        cyan_message("No signals were found")
            
    return signals