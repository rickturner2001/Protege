import pandas as pd
from pandas import DataFrame
from sympy import limit
import talib


def db_historical_to_df(symbol: str, cursor, limit=0) -> DataFrame:
    if limit:
        cursor.execute("select * from historical_data where symbol = ? order by Date desc limit ?", (symbol, limit))
    else:
        cursor.execute("select * from historical_data where symbol = ? order by Date", (symbol,))
    data = cursor.fetchall()
    data = [[val['Date'], val['Open'], val['High'], val['Low'], val['Close'], val['Volume']] for val in data]
    data = pd.DataFrame(data, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    data.index = pd.to_datetime(data['Date'])
    data = data.drop('Date', axis=1)
    data.index.name = 'Date'

    return data

def get_talib_patterns(data, bullish=True):
    if bullish:
        patterns = {
                    'CDLABANDONEDBABY': talib.CDLABANDONEDBABY(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                    'CDLGRAVESTONEDOJI': talib.CDLGRAVESTONEDOJI(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                    'CDLHARAMI': talib.CDLHARAMI(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                    'CDLHARAMICROSS': talib.CDLHARAMICROSS(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                    'CDLHIKKAKE': talib.CDLHIKKAKE(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                    'CDLINVERTEDHAMMER': talib.CDLINVERTEDHAMMER(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                    'CDLMATHOLD': talib.CDLMATHOLD(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                    'CDLSEPARATINGLINES': talib.CDLSEPARATINGLINES(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                    'CDLSTICKSANDWICH': talib.CDLSTICKSANDWICH(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                    'CDLUNIQUE3RIVER': talib.CDLUNIQUE3RIVER(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),

        }
        return patterns
    patterns = {
                'CDL2CROWS': talib.CDL2CROWS(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDL3BLACKCROWS': talib.CDL3BLACKCROWS(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDL3INSIDE': talib.CDL3INSIDE(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDL3OUTSIDE': talib.CDL3OUTSIDE(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDL3LINESTRIKE': talib.CDL3LINESTRIKE(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDL3STARSINSOUTH': talib.CDL3STARSINSOUTH(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDL3WHITESOLDIERS': talib.CDL3WHITESOLDIERS(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLABANDONEDBABY': talib.CDLABANDONEDBABY(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLADVANCEBLOCK': talib.CDLADVANCEBLOCK(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLBELTHOLD': talib.CDLBELTHOLD(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLBREAKAWAY': talib.CDLBREAKAWAY(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLCLOSINGMARUBOZU': talib.CDLCLOSINGMARUBOZU(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLCONCEALBABYSWALL': talib.CDLCONCEALBABYSWALL(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLCOUNTERATTACK': talib.CDLCOUNTERATTACK(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLDARKCLOUDCOVER': talib.CDLDARKCLOUDCOVER(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLDOJI': talib.CDLDOJI(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLDOJISTAR': talib.CDLDOJISTAR(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLDRAGONFLYDOJI': talib.CDLDRAGONFLYDOJI(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLENGULFING': talib.CDLENGULFING(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLEVENINGDOJISTAR': talib.CDLEVENINGDOJISTAR(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLEVENINGSTAR': talib.CDLEVENINGSTAR(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLGAPSIDESIDEWHITE': talib.CDLGAPSIDESIDEWHITE(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLGRAVESTONEDOJI': talib.CDLGRAVESTONEDOJI(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLHAMMER': talib.CDLHAMMER(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLHANGINGMAN': talib.CDLHANGINGMAN(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLHARAMI': talib.CDLHARAMI(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLHARAMICROSS': talib.CDLHARAMICROSS(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLHIGHWAVE': talib.CDLHIGHWAVE(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLHIKKAKE': talib.CDLHIKKAKE(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLHIKKAKEMOD': talib.CDLHIKKAKEMOD(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLHOMINGPIGEON': talib.CDLHOMINGPIGEON(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLIDENTICAL3CROWS': talib.CDLIDENTICAL3CROWS(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLINNECK': talib.CDLINNECK(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLINVERTEDHAMMER': talib.CDLINVERTEDHAMMER(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLKICKING': talib.CDLKICKING(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLKICKINGBYLENGTH': talib.CDLKICKINGBYLENGTH(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLLADDERBOTTOM': talib.CDLLADDERBOTTOM(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLLONGLEGGEDDOJI': talib.CDLLONGLEGGEDDOJI(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLLONGLINE': talib.CDLLONGLINE(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLMARUBOZU': talib.CDLMARUBOZU(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLMATCHINGLOW': talib.CDLMATCHINGLOW(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLMATHOLD': talib.CDLMATHOLD(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLMORNINGDOJISTAR': talib.CDLMORNINGDOJISTAR(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLMORNINGSTAR': talib.CDLMORNINGSTAR(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLONNECK': talib.CDLONNECK(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLPIERCING': talib.CDLPIERCING(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLRICKSHAWMAN': talib.CDLRICKSHAWMAN(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLRISEFALL3METHODS': talib.CDLRISEFALL3METHODS(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLSEPARATINGLINES': talib.CDLSEPARATINGLINES(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLSHOOTINGSTAR': talib.CDLSHOOTINGSTAR(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLSHORTLINE': talib.CDLSHORTLINE(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLSPINNINGTOP': talib.CDLSPINNINGTOP(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLSTALLEDPATTERN': talib.CDLSTALLEDPATTERN(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLSTICKSANDWICH': talib.CDLSTICKSANDWICH(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLTAKURI': talib.CDLTAKURI(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLTASUKIGAP': talib.CDLTASUKIGAP(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLTHRUSTING': talib.CDLTHRUSTING(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLTRISTAR': talib.CDLTRISTAR(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLUNIQUE3RIVER': talib.CDLUNIQUE3RIVER(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLUPSIDEGAP2CROWS': talib.CDLUPSIDEGAP2CROWS(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                'CDLXSIDEGAP3METHODS': talib.CDLXSIDEGAP3METHODS(
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
                    }
    return patterns
