from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / 'results'
REPORTS_DIR = BASE_DIR / 'reports_dir'
EXCEL_DIR = RESULTS_DIR / 'excel'
DB_DIR = BASE_DIR.parent / 'watchlist.db'

DB_PATH = BASE_DIR.parent / 'database' / 'pre_watchlist.sqlite3'
MODELS_DIR = BASE_DIR / 'models'


# Define your watchlist, note that it could be a list of tickers as well as symbols from an external source. 
# Example of use: 

# With .csv or .txt file
# SYMBOLS = pd.read_csv(mysymbols.csv)
# WATCHLIST = [symbol for symbol in symbols[Symbol] -> symbol['Symbol']
# refers to the specific column containing the symbols

# Simple list
# SYMBOLS = ['AAPL', "MSFT", "TSLA"...]
# WATCHLIST = SYMBOLS

# LEAVE EMPTY TO SCAN ALL S&P500 SECURITIES (RECOMMENDED)

WATCHLIST = []


# Choose a querying parameter (get the alpha and beta values based on x parameter)

# QUERY PARAMS ->  ['1d', "7d", "1mo", "6mo", '1y', "2y", "5y", "10y"]

QUERY_PARAM = '1mo'

# Define the frequency of your trading schedule

# The options are : 

# Trading Frequencies ->  ['1d', "7d", "1mo", "6mo"]

# "day" for daily trading -> trade on a daily basis 
# "week" for weekly trading  -> trade on a weekly basis
# "month" for monthly trading -> trade on a montlhy basis

TRADING_FREQ = '7d'

# Declare a threshold for the total score (scale 1-10)
THRESHOLD = 7 # Only get results that have 7+ total score on the fundamental analysis evaluation
