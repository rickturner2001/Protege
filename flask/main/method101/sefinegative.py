
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


sp500 = yf.download("^GSPC", start="2021-04-30", end="2022-04-01", interval="1d")
df = pd.read_csv("sefi.csv")
df.index = df[list(df.columns)[0]]
df.drop(list(df.columns)[0], axis=1, inplace=True)
df.index.name = "date"

negative_sefi_value = df[df['Entry'] < 0]

# print(dir(df.index))

def position_return(index_location, df):
    if index_location  + 10 <= (len(sp500) - 1):
        start = df.iloc[index_location]
        end =  df.iloc[index_location + 10]
    else:
        start= df.iloc[index_location]
        end = df.iloc[-1]
    total_return =  round(((end['Close'] - start["Close"]) / end['Close']) * 100, 2)
    return total_return

retruns = []
for date in negative_sefi_value.index:

    index_location = sp500.index.get_loc(date)
    total_return = position_return(index_location, sp500)



print(retruns)

plt.hist(retruns, bins=20)
plt.show()

