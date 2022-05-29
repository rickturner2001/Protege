import sys
from pathlib import Path
from functions import do_db_connection
import datetime
from ma_difference import get_nsdma_signals


def main():
    signals = get_nsdma_signals()
    if signals:

        BASE_DIR = Path(__file__).resolve().parent.parent
        DB_PATH = BASE_DIR.parent / 'database' / 'pre_watchlist.sqlite3'

        connection = do_db_connection(DB_PATH)
        cursor = connection.cursor()

        CURRENT_DATE = datetime.date.today()

        for symbol in signals:
            cursor.execute(
                """
                INSERT INTO nsma_signals (date, symbol) VALUES (?, ?)
                """, (CURRENT_DATE, symbol))

            print(f"Found entry point for {symbol}")

        connection.commit()

    else:
        print("No signals found")


if __name__ == '__main__':
    main()
