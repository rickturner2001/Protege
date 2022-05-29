import sys
sys.path.append('.')

import concurrent.futures
from utilities.functions import do_db_connection
from utilities.config import DB_PATH
from utilities.patterns import Pattern
import datetime
from utilities.fundamental import FundamentalAnalysis

analysis = FundamentalAnalysis()
def do_analysis(ticker):
    analysis.finalize_result(ticker)

connection = do_db_connection(DB_PATH)
cursor = connection.cursor()
cursor.execute("select distinct Symbol from historical_data")
symbols = cursor.fetchall()
symbols = [symbol['Symbol'] if '.' not in symbol['Symbol'] 
            else symbol['Symbol'].replace('.', '-') for symbol in symbols]

with concurrent.futures.ThreadPoolExecutor (max_workers=50) as executor:
    analysis_result = executor.map(do_analysis, symbols)

    results = analysis.get_results()
def delete_missing():
    symbols = []
    for symbol in results:
        if "Score" not in list(results[symbol].keys()):
            symbols.append(symbol)

    return symbols

to_remove = delete_missing()

for i in to_remove:
    del results[i]

    filtered_results = analysis.filter_results(threshold=10)


CURRENT_DATE = str(datetime.date.today())

pattern = Pattern(list(filtered_results.keys()))
pattern.download_data()
interceptions = pattern.intercepitons()


for i, symbol in enumerate(filtered_results):
    
    cursor.execute(
        """
        INSERT or IGNORE INTO to_analyze
        (symbol, PEG, ROE, PB, GrossMargin, QuickRatio, CurrentRatio, PS, ForwardPE, Recom, Score,
        Interception, CurrentDate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (symbol,
        filtered_results[symbol]['PEG'][0],
        filtered_results[symbol]['ROE'][0],
        filtered_results[symbol]['P/B'][0],
        filtered_results[symbol]['Gross Margin'][0],
        filtered_results[symbol]['Quick Ratio'][0],
        filtered_results[symbol]['Current Ratio'][0],
        filtered_results[symbol]['P/S'][0],
        filtered_results[symbol]['Forward P/E'][0],
        filtered_results[symbol]['Recom'][0],
        filtered_results[symbol]['Score'],
        str(interceptions[i]),
        str(CURRENT_DATE)))

connection.commit()