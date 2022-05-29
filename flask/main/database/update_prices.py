import sys
from pathlib import Path

CURRENT_DIR = str(Path(__file__).resolve().parent.parent / 'utilities')

sys.path.append(CURRENT_DIR)
sys.path.insert(0, CURRENT_DIR)


def main():

    from functions import do_db_connection
    from config import DB_PATH
    import datetime
    import yfinance as yf


    connection = do_db_connection(DB_PATH)
    cursor = connection.cursor()


    first_date = cursor.execute('select DISTINCT date from historical_data ORDER by date limit 1').fetchone()['Date']

    CURRENT_DATE = datetime.date.today().isoformat()


    symbols = cursor.execute(
        "select distinct symbol from historical_data").fetchall()
    symbols = [symbol['Symbol'] for symbol in symbols]


    # Delete first day and update last (append new date)
    cursor.execute(
        "delete from historical_data where date = ?", (first_date,))



    # Update Begins Here

    data = yf.download(
        tickers=symbols,
        period='1d',
        interval='1d',
        group_by='ticker',
        auto_adjust=False,
        prepost=False,
        threads=True,
        proxy=None
    )

    data = data.T

    with open("results.txt", "w") as f:

        for j, symbol in enumerate(symbols):
            print(f"{round(j / len(symbols) * 100, 2)}%")
            df = data.loc[symbol].T
            f.write(str(df))
        for i, date in enumerate(df.index):
            cursor.execute(
                """
                INSERT INTO historical_data (Date, Symbol, Open, High, Low, Close, Volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (CURRENT_DATE,
                    symbol,
                    df.loc[date]['Open'],
                    df.loc[date]['High'],
                    df.loc[date]['Low'],
                    df.loc[date]['Close'],
                    df.loc[date]['Volume']))

    connection.commit()
    print("The Database has officially been updated\n")
    print(f"Latest Date: {CURRENT_DATE}")


if __name__ == "__main__":
    main()
