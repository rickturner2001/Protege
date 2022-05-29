import sys

sys.path.append('.')

from utilities.talib_related import get_talib_patterns, db_historical_to_df
from utilities.functions import do_db_connection
from utilities.config import DB_PATH
import datetime

CURRENT_DATE = str(datetime.date.today())

connection = do_db_connection(DB_PATH)
cursor = connection.cursor()

cursor.execute('SELECT DISTINCT Symbol from historical_data')
symbols = cursor.fetchall()
symbols = [symbol['Symbol'] for symbol in symbols]

for symbol in symbols:
    data = db_historical_to_df(symbol, cursor)
    patterns = get_talib_patterns(data=data, bullish=True)
    
    for pattern in patterns:
        data = data[-5:]
        data[pattern] = patterns[pattern][-1]
        if data.iloc[-1][pattern] > 0:        
            print(f"Adding: {symbol} -> {pattern[3:]}")
    
            cursor.execute(
                    """
                    INSERT INTO candlestick_patterns (Symbol, Pattern, Date)
                    VALUES (?, ?, ?)
                    """, (symbol, pattern[3:], CURRENT_DATE))

connection.commit()