from exchange_candle_loader_abc import CandleLoaderABC

import requests


class BinanceCandleLoader(CandleLoaderABC):

    # possible_pairs = ['BTCUSDT', 'ETHUSDT', 'BCHUSDT', 'XRPUSDT', 'EOSUSDT', 'LTCUSDT', 'TRXUSDT', 'ETCUSDT', 'LINKUSDT', 'XLMUSDT', 'ADAUSDT', 'XMRUSDT', 'DASHUSDT', 'ZECUSDT', 'XTZUSDT', 'BNBUSDT', 'ATOMUSDT', 'ONTUSDT', 'IOTAUSDT', 'BATUSDT', 'VETUSDT', 'NEOUSDT', 'QTUMUSDT', 'IOSTUSDT', 'THETAUSDT', 'ALGOUSDT', 'ZILUSDT', 'KNCUSDT', 'ZRXUSDT', 'COMPUSDT', 'OMGUSDT', 'DOGEUSDT', 'SXPUSDT', 'KAVAUSDT', 'BANDUSDT', 'RLCUSDT', 'WAVESUSDT', 'MKRUSDT', 'SNXUSDT', 'DOTUSDT', 'DEFIUSDT', 'YFIUSDT', 'BALUSDT', 'CRVUSDT', 'TRBUSDT', 'YFIIUSDT', 'RUNEUSDT', 'SUSHIUSDT', 'SRMUSDT', 'BZRXUSDT', 'EGLDUSDT', 'SOLUSDT', 'ICXUSDT', 'STORJUSDT', 'BLZUSDT', 'UNIUSDT', 'AVAXUSDT', 'FTMUSDT', 'HNTUSDT', 'ENJUSDT', 'FLMUSDT', 'TOMOUSDT', 'RENUSDT', 'KSMUSDT', 'NEARUSDT', 'AAVEUSDT', 'FILUSDT', 'RSRUSDT', 'LRCUSDT', 'MATICUSDT', 'OCEANUSDT', 'CVCUSDT', 'BELUSDT', 'CTKUSDT', 'AXSUSDT', 'ALPHAUSDT', 'ZENUSDT', 'SKLUSDT', 'GRTUSDT', '1INCHUSDT', 'BTCBUSD', 'AKROUSDT', 'CHZUSDT', 'SANDUSDT', 'ANKRUSDT', 'LUNAUSDT', 'BTSUSDT', 'LITUSDT', 'UNFIUSDT', 'DODOUSDT', 'REEFUSDT', 'RVNUSDT', 'SFPUSDT', 'XEMUSDT', 'COTIUSDT', 'CHRUSDT', 'MANAUSDT', 'ALICEUSDT', 'HBARUSDT', 'ONEUSDT', 'LINAUSDT', 'STMXUSDT', 'DENTUSDT', 'CELRUSDT', 'HOTUSDT', 'MTLUSDT', 'OGNUSDT', 'BTTUSDT', 'NKNUSDT', 'SCUSDT', 'DGBUSDT', '1000SHIBUSDT', 'ICPUSDT', 'BAKEUSDT', 'GTCUSDT', 'ETHBUSD', 'BTCDOMUSDT', 'KEEPUSDT', 'TLMUSDT']
    pairs = ['YFIUSDT', 'BTCUSDT', 'ETHUSDT', 'BCHUSDT', 'ICPUSDT', 'BNBUSDT', 'LTCUSDT', 'FILUSDT']
    db_name = ''
    user_name = 'oleg'
    name = 'binance'
    period = '1m'

    host_name = 'https://fapi.binance.com'
    endpoint = '/fapi/v1/klines'

    def __init__(self, start_date, end_date, saver, period, pairs):
        if period == '1h':
            step = 1488
        else:
            step = 1500

        parsed_period = self._get_parsed_period(period)

        super().__init__(start_date, end_date, step, saver, parsed_period, pairs)

    def _get_single_period_data(self, period):#TODO refactor different timestamps formats
        period_data = list()
        start_date = period[0] * 1000
        end_date = period[1] * 1000

        for pair in self.pairs:
            single_period_data = self._get_single_pair_data(start_date, end_date, pair)

            if single_period_data:
                self._save_data(single_period_data)

            else:
                print(f"Failure Start: {start_date}, End: {end_date}, pair: {pair}")

        return period_data

    def _get_single_pair_data(self, start_date, end_date, pair):
        url = self.host_name + self.endpoint
        data = {
            "symbol": pair,
            "interval": self.period,
            "startTime": start_date,
            "endTime": end_date,
            "limit": self._step
        }

        try:
            response = requests.get(url, params=data).json()
            print(response)

            if len(response):
                parsed_data = self._get_parsed_response(response, pair)

                return parsed_data

            else:
                print('--------------------No data-------------------------')
                print(response)

        except ConnectionError:  # TODO finish
            print(ConnectionError)

    def _get_parsed_response(self, data, pair):
        result = list()

        for elem in data:
            single_candle = dict()
            single_candle['open_time'] = self.to_utc(elem[0] / 1000)
            single_candle['close_time'] = self.to_utc(elem[0] / 1000 + self._period_in_seconds)
            single_candle['volume'] = elem[5]
            single_candle['low_price'] = elem[3]
            single_candle['high_price'] = elem[2]
            single_candle['open_price'] = elem[1]
            single_candle['close_price'] = elem[4]
            single_candle['ticker'] = pair
            single_candle['exchange'] = self.name

            result.append(single_candle)

        return result

    def _get_parsed_period(self, period):
        if period in ['1m', '1min']:
            return '1m'

        elif period in ['60min', '60m', '1hour', '1h']:
            return '1h'

        else:
            raise ValueError("Wrong period in Binance exchange")