from sefi100 import get_sefi100
import datetime
import sqlite3
from pathlib import Path




def main():
    def do_db_connection(db_path: str, row_factory=True):
        connection = sqlite3.connect(db_path, check_same_thread=False)
        if row_factory:
            connection.row_factory = sqlite3.Row
        return connection

    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_PATH = BASE_DIR.parent / 'database' / 'pre_watchlist.sqlite3'
    CURRENT_DATE = datetime.date.today()
    FIVE_DAYS_INCREMENT = CURRENT_DATE + datetime.timedelta(days=7)
    connection = do_db_connection(DB_PATH)

    cursor = connection.cursor()



    symbols_in_db = cursor.execute("select Symbol from to_be_scanned").fetchall()
    symbols_in_db = [symbol['Symbol'] for symbol in symbols_in_db]

    symbols = get_sefi100()
    #
    if symbols:
        for symbol in symbols:
            if not symbol in symbols_in_db:

                print(f"Adding {symbol}...")
                cursor.execute(
                    """
                    INSERT INTO to_be_scanned (Symbol, Date, FinalDate) VALUES (?, ?, ?) 
                    """, (symbol, str(CURRENT_DATE), str(FIVE_DAYS_INCREMENT)))
            else:
                cursor.execute(
                    """
                    DELETE FROM to_be_scanned WHERE Symbol = "?"
                    """, (symbol,))
                cursor.execute(
                    """
                    INSERT INTO to_be_scanned (Symbol, Date, FinalDate) VALUES (?, ?, ?)
                    """, (symbol, str(CURRENT_DATE), str(FIVE_DAYS_INCREMENT)))
    else:
        print("No symbols were found")


if __name__ == '__main__':
    main()