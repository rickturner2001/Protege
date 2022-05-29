import sys
sys.path.append('.')
from screener import FinvizScreener
import json
from functions import valuate

class FundamentalAnalysis:
    def __init__(self) -> None:
        self.filtered_data = None
        self.dataStatus = None
        self.symbol = None
        self.dataStatus = {}

        self.labels = [
                        ('PEG', 0, 2),
                        ('ROE', 45, 0),
                        ('P/B', 0, 5),
                        ('Gross Margin', 100, 0),
                        ('Quick Ratio', 3, 0.5),
                        ('Current Ratio', 4.5, 1),
                        ('P/S', 0, 10),
                        ('Forward P/E', 4, 50),
                        ('Recom', 1, 5),
                    ]


    def get_data(self, labels: list, data: dict, symbol: str) -> float:
        score = 0
        for label in labels:
            key, best_val, worst_val = label
            value, valuation = valuate(data=data, key=key, best_val=best_val, worst_val=worst_val)
            self.dataStatus[symbol][key] = (value, valuation)
            score += valuation
        return round(score, 2)
        

    def finalize_result(self,symbol):
        total_score = 0
        # print(f"Working with: {symbol}")
        self.dataStatus[symbol] = {}
        # Finviz Ticker Data
        screener = FinvizScreener(symbol)
        ticker_data = screener.get_general_data()
        valuation = self.get_data(labels=self.labels, data=ticker_data, symbol=symbol)
        self.dataStatus[symbol]['Score'] = valuation
        


    def get_results(self):
        return self.dataStatus


    def filter_results(self, threshold: int) -> dict:
        """
        Filters `self.dataStatus` by `self.THRESHOLD`
        """

        self.filtered_data = {}
        filtered_symbols = []
        while not filtered_symbols:
            filtered_symbols = list(filter(lambda x: self.dataStatus[x]['Score'] >= threshold, self.dataStatus))
            if not filtered_symbols:
                if not threshold == 0:
                    print(f"No tickers found with a score of {threshold} or higher... Trying with {threshold - 1}")
                    threshold -= 1
                else:
                    print("No tickers where found")
                    return None


        for symbol in filtered_symbols:
            self.filtered_data[symbol] = {}
            for key in self.dataStatus[symbol]:
                self.filtered_data[symbol][key] = self.dataStatus[symbol][key]

        return self.filtered_data

    def result_to_json(self, filtered=True) -> None:
        """
        Get a JSON file of the results from the `do_analysis` method
        """

        with open('results.json', 'w') as f:
            if filtered:
                f.write(json.dumps(self.filtered_data, indent=4))
            else:
                f.write(json.dumps(self.dataStatus, indent=4))

# analyze = FundamentalAnalysis(['AAPL', 'TSLA', 'MSFT', 'TSLA', 'FB', 'IP', 'CRM', 'KO'])