import sys

sys.path.append('.')

from screener import Signals
from config import DB_PATH
from functions import do_db_connection

connection = do_db_connection(DB_PATH)

cursor = connection.cursor()


major_news = Signals()
major_news = major_news.major_news()['results']

symbols = [symbol for symbol in major_news['Ticker']]

for symbol in symbols:
    cursor.execute("""INSERT or IGNORE INTO pre_watchlist (symbol, signal) values (?, ?)""", (symbol, 'Major News'))
    

head_and_shoulders = Signals()
head_and_shoulders = head_and_shoulders.head_and_shoulders()['results']

symbols = [symbol for symbol in head_and_shoulders['Ticker']]

for symbol in symbols:
    cursor.execute(
        """
        INSERT or IGNORE INTO pre_watchlist (symbol, signal) values (?, ?)
        """, (symbol, 'Head and Shoulders'))

head_and_shoulders_inverse = Signals()
head_and_shoulders_inverse = head_and_shoulders_inverse.head_and_shoulders_inverse()['results']

symbols = [symbol for symbol in head_and_shoulders_inverse['Ticker']]

for symbol in symbols:
    cursor.execute(
        """INSERT or IGNORE INTO pre_watchlist (symbol, signal) values (?, ?)""",
        (symbol, 'Head and Shoulders Inverse'))

channel_up = Signals()
channel_up = channel_up.channel_up()['results']

symbols = [symbol for symbol in channel_up['Ticker']]

for symbol in symbols:
    cursor.execute(
        """INSERT or IGNORE INTO pre_watchlist (symbol, signal) values (?, ?)""",
        (symbol, 'Channel Up'))

channel_down = Signals()
channel_down = channel_down.channel_down()['results']

symbols = [symbol for symbol in channel_down['Ticker']]

for symbol in symbols:
    cursor.execute(
        """INSERT or IGNORE INTO pre_watchlist (symbol, signal) values (?, ?)""",
        (symbol, 'Channel Down'))

ascending_triangle = Signals()
ascending_triangle = ascending_triangle.ascending_triangle()['results']

symbols = [symbol for symbol in ascending_triangle['Ticker']]

for symbol in symbols:
    cursor.execute(
        """INSERT or IGNORE INTO pre_watchlist (symbol, signal) values (?, ?)""",
        (symbol, 'Ascending Triangle'))

double_bottom = Signals()
double_bottom = double_bottom.double_bottom()['results']

symbols = [symbol for symbol in double_bottom['Ticker']]

for symbol in symbols:
    cursor.execute(
        """INSERT or IGNORE INTO pre_watchlist (symbol, signal) values (?, ?)""",
        (symbol, 'Double Bottom'))

multiple_bottoms = Signals()
multiple_bottoms = multiple_bottoms.multiple_bottoms()['results']

symbols = [symbol for symbol in multiple_bottoms['Ticker']]

for symbol in symbols:
    cursor.execute(
        """INSERT or IGNORE INTO pre_watchlist (symbol, signal) values (?, ?)""",
        (symbol, 'Multiple Bottoms'))


connection.commit()

print("pre_watchlist has been updated")
