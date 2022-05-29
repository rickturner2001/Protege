import numpy as np
import yfinance as yf
import datetime
import warnings
warnings.filterwarnings('ignore')

def slope(x1, y1, x2, y2):
    x = (y2 - y1) / (x2 - x1)
    return x


class Pattern:
    def __init__(self, symbols:str):
        
        self.mean_result = None
        self.results = None
        self.paired_interceptions = None
        self.reverse = None
        self.reverse_dates = None
        self.regular_dates = None
        self.dates = None
        self.symbols = symbols
        self.CURRENT_DATE = datetime.date.today()
        self.date_list = [self.CURRENT_DATE - datetime.timedelta(days=x) for x in range(10)]
        self.data = yf.download(
                                tickers = symbols,
                                period = '1y',
                                interval = '1d',
                                group_by = 'ticker',
                                auto_adjust = False,
                                prepost = False,
                                threads = True,
                                proxy = None
                                )

        self.data = self.data.T
        self.dfs = []
    def download_data(self):

        for i, symbol in enumerate(self.symbols):
            print(f"{round(i / len(self.symbols) * 100, 2)}%")
            df  =  self.data.loc[symbol].T
            
            df['MA20'] = df['Adj Close'].rolling(window=20).mean()
            df['MA50'] = df['Adj Close'].rolling(window=50).mean()
            df.dropna(inplace=True)
            df['Pct Change'] = df['Close'].pct_change(1)
            df.dropna(inplace=True)
            self.dfs.append(df)
        
        return self.dfs

    @staticmethod
    def ma_interception(df):
        dates = []
        regular_dates = []
        reverse_dates = []

        for i, date in enumerate(df.index):
            if i > 0:
                if df.iloc[i - 1]['MA50'] < df.iloc[i - 1]['MA20']: 
                    if df.iloc[i]['MA50'] > df.iloc[i]['MA20']:
                        dates.append((date, False))
                        regular_dates.append(date)
                if df.iloc[i - 1]['MA20'] < df.iloc[i - 1]['MA50']: 
                    if df.iloc[i]['MA20'] > df.iloc[i]['MA50']:
                        dates.append((date, True))
                        reverse_dates.append(date)
        
        return dates, reverse_dates, regular_dates

    def pair_interceptions(self, df):
        
        dates, reverse_dates, regular_dates = self.ma_interception(df)
        reverse = dates[0][1]
        
        if reverse:
            del reverse_dates[0]
        
        paired_interceptions = list(zip(regular_dates, reverse_dates))
        return paired_interceptions
   
    def intercepitons(self):
        interceptions = []
        for i, df in enumerate(self.dfs):
            interception = self.pair_interceptions(df)
            if interception:
                last_interception = interception[-1]
                start, end = last_interception
            else:
                interception = None
                end = None
            if end in self.date_list:
                interception = end
                print(f"== Found recent interception ==\n\n== {self.symbols[i]} -> {end} ==")
            else:
                print(f"== No relevant interceptions found for {self.symbols[i]} ==")
                interception = None
            interceptions.append(interception)
        return interceptions

    def evaluate(self):
        self.results = []
        for start, end in self.paired_interceptions:
            df = self.df[start:end]
            result = round(df['Pct Change'].cumsum()[-1] * 100, 2)
            self.results.append(result)

            self.mean_result = round(np.array(self.results).mean(), 2)
        
        return self.mean_result

