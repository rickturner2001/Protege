import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


class FinvizScreener:
    def __init__(self, ticker):
        self.ticker = ticker
        self.base_url = 'https://finviz.com/'
        headers = {'User-Agent': 'Mozilla/5.0'}
        serviceurl = self.base_url + 'quote.ashx?t=' + self.ticker
        html = requests.get(serviceurl, headers=headers)
        self.soup = BeautifulSoup(html.content, 'html.parser')

    def get_general_data(self):
        print(f"Fetching data from {self.ticker}")
        tables = []
        filtered_tables = []
        tables = self.soup.findAll('table')
        tables = pd.read_html(str(tables))
        for table in tables:
            if len(table.index) > 3:
                filtered_tables.append(table)
        technical = filtered_tables[0]
        index = []
        values = []
        for i in range(len(technical.columns)):
            if i % 2 == 0:
                cols = technical[i].values
                for col in cols:
                    index.append(col)
            else:
                vals = technical[i].values
                for val in vals:
                    # First we check if the value has a percent sign, if it does we remove it so that we can
                    # change its type to float
                    if '%' in val:
                        val = val.replace('%', '')
                    try:
                        # Then we check if the type of value can be changed from str to float
                        values.append(float(val))
                    except:
                        # If we can't, it either means that the value is missing ("-")
                        # or the value is in fact a string ("NASDAQ")
                        if len(val) <= 1:
                            values.append(None)
                        else:
                            values.append(val)

        technical = pd.DataFrame(index=index, data=values)
        technical.columns = ['Values']

        return technical

    def analysis_related_data(self):
        table = self.soup.find('table', {'class': "snapshot-table2"})

        table_span = table.findAll('b')
        table_indices = table.findAll('td', {'class': "snapshot-td2-cp"})
        table_data = table.findAll('td', {'class': 'snapshot-td2'})

        index = []
        for val in table_indices:
            index.append(val.get_text())
        t_data = []
        for val in table_data:
            t_data.append(val.get_text())

        data = {'red': [], 'green': [], 'neutral': []}

        for i, span in enumerate(table_span):

            if span.span:

                class_ = span.span['class'][0]

                if class_ == 'is-green':
                    data["green"].append(i)
                else:
                    data["red"].append(i)
            else:
                data["neutral"].append(i)

        df = pd.DataFrame(index=index, columns=['values'], data=t_data)

        df['eval'] = [None for i in range(len(df))]

        for i, index in enumerate(df.index):
            if i in data['red']:
                df['eval'].iloc[i] = 'red'
            elif i in data['green']:
                df['eval'].iloc[i] = 'green'
            else:
                df['eval'].iloc[i] = 'neutral'

        index = [
            'P/E',
            'Forward P/E',
            'EPS (ttm)',
            'PEG', 'P/B',
            'Debt/Eq',
            'P/FCF',
            'Quick Ratio',
            'ROE', 'P/S',
            'Dividend %',
            'EPS next Y',
        ]

        my_df = pd.DataFrame(index=index, columns=['values', 'eval'])

        for i, val in enumerate(index):

            if not val == 'EPS next Y':
                my_df.iloc[i]['values'] = df.loc[val]['values']
                my_df.iloc[i]['eval'] = df.loc[val]['eval']

            else:
                my_df.iloc[i]['values'] = df.loc[val].iloc[0]['values']
                my_df.iloc[i]['eval'] = df.loc[val].iloc[0]['eval']

        return my_df


class Signals:
    def __init__(self):
        self.soup = None
        self.headers = {'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en'}

    def parse_table(self, response, base_url):
        self.soup = BeautifulSoup(response.content, 'html.parser')

        tables = pd.read_html(self.soup.prettify())
        main_table = tables[14]

        main_table.index = main_table[main_table.columns[0]]
        main_table = main_table.drop(main_table.columns[0], axis=1)
        columns = main_table.iloc[0].values
        main_table.columns = columns
        main_table = main_table.iloc[1:]
        main_table.index.name = 'No.'

        try:
            second_table = requests.get(base_url, params={'r': len(main_table) + 1}, headers=self.headers)
            if second_table.ok:
                soup = BeautifulSoup(second_table.content, 'html.parser')
                tables = pd.read_html(soup.prettify())
                second_main_table = tables[14]

                second_main_table.index = second_main_table[second_main_table.columns[0]]
                second_main_table = second_main_table.drop(second_main_table.columns[0], axis=1)
                columns = second_main_table.iloc[0].values
                second_main_table.columns = columns
                second_main_table = second_main_table.iloc[1:]
                second_main_table.index.name = 'No.'
                main_table.append(second_main_table)
                return main_table
            else:
                print(second_table.status_code)
        except Exception as e:
            print(e)

    def major_news(self):
        """..."""
        data = {}
        base_url = f'https://finviz.com/screener.ashx?v=111&s=n_majornews&f=idx_sp500'
        response = requests.get(base_url, headers=self.headers)
        data['results'] = self.parse_table(response, base_url)
        news = self.get_news('https://finviz.com/screener.ashx?v=321&s=n_majornews&f=idx_sp500')
        data['news'] = news

        return data

    def double_bottom(self):
        """78.55%"""
        data = {}
        base_url = f'https://finviz.com/screener.ashx?v=111&s=ta_p_doublebottom&f=idx_sp500'
        response = requests.get(base_url, headers=self.headers)
        data['results'] = self.parse_table(response, base_url)
        news = self.get_news('https://finviz.com/screener.ashx?v=321&s=ta_p_doublebottom&f=idx_sp500')
        data['news'] = news

        return data

    def multiple_bottoms(self):
        """...%"""
        data = {}
        base_url = f'https://finviz.com/screener.ashx?v=111&s=ta_p_multiplebottom&f=idx_sp500'
        response = requests.get(base_url, headers=self.headers)
        data['results'] = self.parse_table(response, base_url)
        news = self.get_news('https://finviz.com/screener.ashx?v=321&s=ta_p_multiplebottom&f=idx_sp500')
        data['news'] = news

        return data

    def wedge_down(self):
        """..."""
        data = {}
        base_url = f'https://finviz.com/screener.ashx?v=111&s=ta_p_wedgedown&f=idx_sp500'
        response = requests.get(base_url, headers=self.headers)
        data['results'] = self.parse_table(response, base_url)
        news = self.get_news('https://finviz.com/screener.ashx?v=321&s=ta_p_wedgedown&f=idx_sp500')
        data['news'] = news

        return data

    def channel_up(self):
        """..."""
        data = {}

        base_url = f'https://finviz.com/screener.ashx?v=111&s=ta_p_channelup&f=idx_sp500'
        response = requests.get(base_url, headers=self.headers)
        data['results'] = self.parse_table(response, base_url)
        news = self.get_news('https://finviz.com/screener.ashx?v=321&s=ta_p_channelup&f=idx_sp500')
        data['news'] = news

        return data

    def channel_down(self):
        """..."""
        data = {}
        base_url = f'https://finviz.com/screener.ashx?v=111&s=ta_p_channeldown&f=idx_sp500'
        response = requests.get(base_url, headers=self.headers)

        data['results'] = self.parse_table(response, base_url)
        news = self.get_news('https://finviz.com/screener.ashx?v=321&s=ta_p_channeldown&f=idx_sp500')
        data['news'] = news

        return data

    def head_and_shoulders(self):
        """83.04% Sell"""
        data = {}
        base_url = f'https://finviz.com/screener.ashx?v=111&s=ta_p_headandshoulders&f=idx_sp500'
        response = requests.get(base_url, headers=self.headers)

        data['results'] = self.parse_table(response, base_url)
        news = self.get_news('https://finviz.com/screener.ashx?v=321&s=ta_p_headandshoulders&f=idx_sp500')
        data['news'] = news

        return data

    def head_and_shoulders_inverse(self):
        """83.44% Buy"""
        data = {}
        base_url = f'https://finviz.com/screener.ashx?v=111&s=ta_p_headandshouldersinv&f=idx_sp500'
        response = requests.get(base_url, headers=self.headers)

        data['results'] = self.parse_table(response, base_url)
        news = self.get_news('https://finviz.com/screener.ashx?v=321&s=ta_p_headandshouldersinv&f=idx_sp500')
        data['news'] = news

        return data

    def ascending_triangle(self):
        """Bullish Pattern"""
        data = {}
        base_url = f'https://finviz.com/screener.ashx?v=111&s=ta_p_wedgeresistance&f=idx_sp500'
        response = requests.get(base_url, headers=self.headers)

        data['results'] = self.parse_table(response, base_url)
        news = self.get_news('https://finviz.com/screener.ashx?v=321&s=ta_p_wedgeresistance&f=idx_sp500')
        data['news'] = news

        return data

    @staticmethod
    def industry_distribution(results):
        data = {}

        count = results['Industry'].value_counts()

        vals = []
        columns = []

        for i, val in enumerate(count):
            vals.append(val)
            columns.append(count.index[i])

        tot_vals = sum(vals)
        vals = [round(val * 100 / tot_vals, 2) for val in vals]

        for i, column in enumerate(columns):
            data[column] = vals[i]

        return data

    def get_    (self, news_url):
        news_response = requests.get(news_url, headers=self.headers)
        soup = BeautifulSoup(news_response.content, 'html.parser')
        news = soup.findAll('table', {'class': 'body-table-news'})
        data = []

        for i, headline in enumerate(news):
            links = []
            titles = []
            for td in headline.findAll('td'):
                a = td.find('a')
                if a:
                    links.append(a['href'])
                    titles.append(a.get_text())

            data.append(list(zip(titles, links)))

        return data


class YahooScreener:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.base_url = 'https://finance.yahoo.com/'
        self.headers = {'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en'}

    def get_page_results(self, param):
        service_url = self.base_url + param + self.ticker
        response = requests.get(service_url, headers=self.headers)
        if response.ok:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        else:
            print(f"Bad response from url: {response.url}. status-code: {response.status_code}")

    def broad_research(self):
        data = {}
        data['summary'] = self.summary()
        data['statistic'] = self.statistic()
        data['financials'] = self.financials()
        data['analysis'] = self.analysis()
        data['sustainability'] = self.sustainability()
        return data

    def summary(self):
        soup = self.get_page_results(f'quote/{self.ticker}%3B/')
        tables = soup.findAll('table')
        tables = pd.read_html(str(tables))
        index = []
        values = []
        for table in tables:
            ind = table[table.columns[0]].values
            for i in ind:
                index.append(i)
            vals = table[table.columns[1]].values
            for val in vals:
                values.append(val)
        summary = pd.DataFrame(index=index, data=values)
        summary.index.name = 'tag'
        summary.columns = ['value']
        return summary

    def statistic(self):
        data = {}
        soup = self.get_page_results(f'quote/{self.ticker}/key-statistics?p={self.ticker}')
        tables = soup.findAll('table')
        statistic = pd.read_html(str(tables))
        data['valuation_measures'] = statistic[0]
        data['stock_price_history'] = statistic[1]
        data['share_statistic'] = statistic[2]
        data['dividends_and_splits'] = statistic[3]
        data['fiscal_year'] = statistic[4]
        data['profitability'] = statistic[5]
        data['management_effectiveness'] = statistic[6]
        data['income_statement'] = statistic[7]
        data['balance_sheet'] = statistic[8]
        data['cashflow_statement'] = statistic[9]

        for key in data:
            data[key].index = data[key][data[key].columns[0]]
            data[key] = data[key].drop(data[key].columns[0], axis=1)
            data[key].index.name = 'tag'
            data[key].columns = ['value']
        return data

    def financials(self):
        financials = self.get_page_results(f'quote/{self.ticker}%3B/financials?p={self.ticker}%3B')
        content = financials.find('div', {'class': 'W(100%) Whs(nw) Ovx(a) BdT Bdtc($seperatorColor)'})
        columns = []
        for i in range(42, 51, 2):
            column = content.find('span', {'data-reactid': f'{i}'})
            columns.append(column.get_text())

        index_content = content.findAll('div', {'class': 'D(tbr) fi-row Bgc($hoverBgColor):h'})
        index = []
        current = []
        previous = []
        previous_two = []
        previous_three = []
        previous_four = []
        for content in index_content:
            children = content.children
            for i, child in enumerate(children):
                if i == 0:
                    index.append(child.get_text())
                elif i == 1:
                    current.append(child.get_text())
                elif i == 2:
                    previous.append(child.get_text())
                elif i == 3:
                    previous_two.append(child.get_text())
                elif i == 4:
                    previous_three.append(child.get_text())
                elif i == 5:
                    previous_four.append(child.get_text())
        df = pd.DataFrame(index=index, columns=columns)
        for i, c in enumerate(df.columns):
            if i == 0:
                df[c] = current
            elif i == 1:
                df[c] = previous
            elif i == 2:
                df[c] = previous_two
            elif i == 3:
                df[c] = previous_three
            elif i == 4:
                df[c] = previous_four
        return df

    def analysis(self):
        """
        Funamental analysis scrap from Yahoo finance based on ticker passed on Class instanciation 

        Returns:
            dict: returns a dictionary with earnings estimates, esp trends and revenue estimates
        """
        analysis = {}
        soup = self.get_page_results(f'quote/{self.ticker}%3B/analysis?p={self.ticker}%3B')
        tables = soup.findAll('table')
        tables = pd.read_html(str(tables))

        analysis['earnings_estimates'] = tables[0]
        analysis['revenue_estimates'] = tables[1]
        analysis['earnings_history'] = tables[2]
        analysis['eps_trend'] = tables[3]
        analysis['eps_revisions'] = tables[4]
        analysis['growth_estimates'] = tables[5]
        for key in analysis:
            analysis[key].index = analysis[key][analysis[key].columns[0]]
            analysis[key] = analysis[key].drop(analysis[key].columns[0], axis=1)
            analysis[key].index.name = 'tag'
        return analysis

    def sustainability(self):
        soup = self.get_page_results(f'quote/{self.ticker}%3B/sustainability?p={self.ticker}%3B')
        data = soup.findAll('div', {'class': 'Pos(r) H(55px) smartphone_Mb(15px)'})
        content = []
        for tag in data:
            for child in tag.children:
                try:
                    for c in child.children:
                        content.append(c.get_text())
                except:
                    content.append(child.get_text())

        data = {'esg_score': int(content[1]), 'percentile': content[2], 'esg_evaluation': content[-1]}
        return data
