from cnadleLoaderABC import CandleLoaderABC

import requests


class BinanceCandleLoader(CandleLoaderABC):
    period = '1m'
    pairs = ['BTCUSDT', 'ETHUSDT', 'BCHUSDT', 'XRPUSDT', 'EOSUSDT', 'LTCUSDT', 'TRXUSDT', 'ETCUSDT', 'LINKUSDT', 'XLMUSDT', 'ADAUSDT', 'XMRUSDT', 'DASHUSDT', 'ZECUSDT', 'XTZUSDT', 'BNBUSDT', 'ATOMUSDT', 'ONTUSDT', 'IOTAUSDT', 'BATUSDT', 'VETUSDT', 'NEOUSDT', 'QTUMUSDT', 'IOSTUSDT', 'THETAUSDT', 'ALGOUSDT', 'ZILUSDT', 'KNCUSDT', 'ZRXUSDT', 'COMPUSDT', 'OMGUSDT', 'DOGEUSDT', 'SXPUSDT', 'KAVAUSDT', 'BANDUSDT', 'RLCUSDT', 'WAVESUSDT', 'MKRUSDT', 'SNXUSDT', 'DOTUSDT', 'DEFIUSDT', 'YFIUSDT', 'BALUSDT', 'CRVUSDT', 'TRBUSDT', 'YFIIUSDT', 'RUNEUSDT', 'SUSHIUSDT', 'SRMUSDT', 'BZRXUSDT', 'EGLDUSDT', 'SOLUSDT', 'ICXUSDT', 'STORJUSDT', 'BLZUSDT', 'UNIUSDT', 'AVAXUSDT', 'FTMUSDT', 'HNTUSDT', 'ENJUSDT', 'FLMUSDT', 'TOMOUSDT', 'RENUSDT', 'KSMUSDT', 'NEARUSDT', 'AAVEUSDT', 'FILUSDT', 'RSRUSDT', 'LRCUSDT', 'MATICUSDT', 'OCEANUSDT', 'CVCUSDT', 'BELUSDT', 'CTKUSDT', 'AXSUSDT', 'ALPHAUSDT', 'ZENUSDT', 'SKLUSDT', 'GRTUSDT', '1INCHUSDT', 'BTCBUSD', 'AKROUSDT', 'CHZUSDT', 'SANDUSDT', 'ANKRUSDT', 'LUNAUSDT', 'BTSUSDT', 'LITUSDT', 'UNFIUSDT', 'DODOUSDT', 'REEFUSDT', 'RVNUSDT', 'SFPUSDT', 'XEMUSDT', 'COTIUSDT', 'CHRUSDT', 'MANAUSDT', 'ALICEUSDT', 'HBARUSDT', 'ONEUSDT', 'LINAUSDT', 'STMXUSDT', 'DENTUSDT', 'CELRUSDT', 'HOTUSDT', 'MTLUSDT', 'OGNUSDT', 'BTTUSDT', 'NKNUSDT', 'SCUSDT', 'DGBUSDT', '1000SHIBUSDT', 'ICPUSDT', 'BAKEUSDT', 'GTCUSDT', 'ETHBUSD', 'BTCDOMUSDT', 'KEEPUSDT', 'TLMUSDT']
    db_name = ''
    user_name = 'oleg'
    name = 'binance'

    host_name = 'https://fapi.binance.com'
    endpoint = '/fapi/v1/klines'

    def __init__(self, start_date, end_date, step=1500, saving_place='csv'):
        super().__init__(start_date, end_date, step, saving_place)

    def _get_single_period_data(self, period):#TODO refactor different timestamps formats
        period_data = list()
        start_date = period[0] * 1000
        end_date = period[1] * 1000

        for pair in self.pairs:
            single_period_data = self._get_single_pair_data(start_date, end_date, pair)
            self._save_data(single_period_data)

        return period_data

    def _get_single_pair_data(self, start_date, end_date, pair):
        url = self.host_name + self.endpoint
        data = {
            "symbol": pair,
            "interval": self.period,
            "startTime": start_date,
            "endTime": end_date
        }

        response = requests.get(url, params=data).json()
        if len(response):
            parsed_data = self._get_parsed_response(response, pair)

            return parsed_data

        else:
            print('--------------------No data-------------------------')
            print(response)

    def _get_parsed_response(self, data, pair):
        result = list()

        for elem in data:
            single_candle = dict()
            single_candle['open_time'] = elem[0] % 10_000_000_000
            single_candle['close_time'] = elem[0] % 10_000_000_000 + 60
            single_candle['volume'] = elem[5]
            single_candle['low_price'] = elem[3]
            single_candle['high_price'] = elem[2]
            single_candle['open_price'] = elem[1]
            single_candle['close_price'] = elem[4]
            single_candle['ticker'] = pair
            single_candle['exchange'] = self.name

            result.append(single_candle)

        return result
