from source.candleLoaderABC import CandleLoaderABC

import requests


class OkexCandleLoader(CandleLoaderABC):
    period = '1m'
    pairs = ['BTC-USDT-SWAP']
    # pairs = ['BTC-USDT-SWAP', 'ETH-USDT-SWAP', 'LTC-USDT-SWAP', 'ETC-USDT-SWAP', 'XRP-USDT-SWAP', 'EOS-USDT-SWAP', 'BCH-USDT-SWAP', 'BSV-USDT-SWAP', 'TRX-USDT-SWAP']
    db_name = ''
    user_name = ''
    name = 'okex'

    host_name = 'https://www.okex.com'
    endpoint = '/api/v5/market/history-candles'

    def __init__(self, start_date, end_date, step=100, saving_place='database', period=period):
        super(OkexCandleLoader, self).__init__(start_date, end_date, step, saving_place, period)

    def collect_data(self):
        for period in self._request_periods:
            print(self.to_utc(period[0]))
            self._get_single_period_data(period)

    def _get_single_period_data(self, period):
        period_data = list()
        start_date = period[0] * 1000
        end_date = period[1] * 1000

        for pair in self.pairs:
            single_period_data = self._get_single_pair_data(start_date, end_date, pair)
            self._save_data(single_period_data)

        return period_data

    def _get_single_pair_data(self, start_date, end_date, pair):
        url = self.host_name + self.endpoint
        print(self.to_utc(start_date / 1000))
        data = {
            "instId": pair,
            "bar": self.period,
            "after": end_date,
            # "before": end_date,
            "limit": 100
        }

        response = requests.get(url, params=data).json()
        if len(response['data']):
            parsed_data = self._get_parsed_response(response, pair)

            return parsed_data

        else:
            print('--------------------No data-------------------------')
            print(response)

    def _get_parsed_response(self, response, pair):
        result = list()
        data = response['data']

        for elem in data:
            single_candle = dict()
            single_candle['open_time'] = self.to_utc(int(elem[0]) / 1000)
            single_candle['close_time'] = self.to_utc(int(elem[0]) / 1000 + self._period_in_seconds)
            single_candle['volume'] = float(elem[6])
            single_candle['low_price'] = float(elem[3])
            single_candle['high_price'] = float(elem[2])
            single_candle['open_price'] = float(elem[1])
            single_candle['close_price'] = float(elem[4])
            single_candle['ticker'] = pair
            single_candle['exchange'] = self.name

            result.append(single_candle)

        return result
