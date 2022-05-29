import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "pre_watchlist.sqlite3"

connection = sqlite3.connect(DB_PATH)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

# cursor.execute("Select * from historical_data")
# data = cursor.fetchall()



# print(data)

