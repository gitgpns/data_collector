from exchange_candle_loader_abc import CandleLoaderABC
import requests


class HuobiCandleLoader(CandleLoaderABC):
    # possible_pairs = ['BTC-USDT', 'ETH-USDT', 'LTC-USDT', 'DOGE-USDT', 'SHIB-USDT', 'ICP-USDT', 'XRP-USDT', 'LINK-USDT', 'TRX-USDT', 'DOT-USDT', 'ADA-USDT', 'EOS-USDT', 'BCH-USDT', 'BSV-USDT', 'YFI-USDT', 'UNI-USDT', 'FIL-USDT', 'YFII-USDT', 'SNX-USDT', 'BNB-USDT', 'ZEC-USDT', 'DASH-USDT', 'ETC-USDT', 'THETA-USDT', 'KSM-USDT', 'ATOM-USDT', 'AAVE-USDT', 'XLM-USDT', 'SUSHI-USDT', 'GRT-USDT', '1INCH-USDT', 'CRV-USDT', 'XTZ-USDT', 'ALGO-USDT', 'NEO-USDT', 'WAVES-USDT', 'COMP-USDT', 'ZIL-USDT', 'QTUM-USDT', 'XMR-USDT', 'KAVA-USDT', 'RSR-USDT', 'VET-USDT', 'OMG-USDT', 'XEM-USDT', 'ONT-USDT', 'AVAX-USDT', 'ZKS-USDT', 'MDX-USDT', 'MATIC-USDT', 'BAND-USDT', 'LRC-USDT', 'SOL-USDT', 'IOTA-USDT', 'MKR-USDT', 'IOST-USDT', 'REN-USDT', 'CVC-USDT', 'BAT-USDT', 'KNC-USDT', 'NEAR-USDT', 'AKRO-USDT', 'BAL-USDT', 'MANA-USDT', 'SAND-USDT', 'ZEN-USDT', 'BAGS-USDT', 'MASS-USDT', 'BTS-USDT', 'BNT-USDT', 'LUNA-USDT', 'FRONT-USDT', 'WOO-USDT', 'PHA-USDT', 'RVN-USDT', 'CHZ-USDT', 'UMA-USDT', 'SKL-USDT', 'BLZ-USDT', 'ENJ-USDT', 'REEF-USDT', 'ONE-USDT', 'HBAR-USDT', 'STORJ-USDT', 'CRO-USDT', 'LINA-USDT', 'ANKR-USDT', 'RNDR-USDT', 'OGN-USDT', 'BTT-USDT', 'MASK-USDT', 'FORTH-USDT', 'CSPR-USDT', 'XCH-USDT', 'CHR-USDT', 'LAT-USDT', 'O3-USDT']
    host_name = 'https://api.hbdm.com/'
    endpoint = 'linear-swap-ex/market/history/kline'
    name = 'huobi'

    def __init__(self, start_date, end_date, saver, period, pairs):
        if period == '1h':
            step = 1992

        else:
            step = 2000

        parsed_period = self._get_parsed_period(period)

        super().__init__(start_date, end_date, step, saver, parsed_period, pairs)

    def _get_single_period_data(self, period):
        print(f"CURRENT PERIOD {period[0]} - {period[1]}")
        period_data = list()
        start_date = period[0]
        end_date = period[1]

        for pair in self.pairs:
            single_period_data = self._get_single_pair_data(start_date, end_date, pair)
            self._save_data(single_period_data)

        return period_data

    def _get_single_pair_data(self, start_date, end_date, pair):
        url = self.host_name + self.endpoint
        data = {
            "contract_code": pair,
            "period": self.period,
            "from": start_date,
            "to": end_date
        }
        try:
            response = requests.get(url, params=data).json()#TODO hour requests last batch candle twice, before and after the day

            if response['status'] == 'ok':
                print(response)
                parsed_data = self._get_parsed_response(response, pair)

                return parsed_data

            else:
                print('--------------------No data-------------------------')
                print(response)

        except ConnectionError:#TODO finish
            print(ConnectionError)

    def _get_parsed_response(self, response, pair):
        result = list()
        data = response['data']

        for elem in data:
            single_candle = dict()
            single_candle['open_time'] = self.to_utc(elem['id'])
            single_candle['close_time'] = self.to_utc(elem['id'] + self._period_in_seconds)
            single_candle['volume'] = elem['amount']
            single_candle['low_price'] = elem['low']
            single_candle['high_price'] = elem['high']
            single_candle['open_price'] = elem['open']
            single_candle['close_price'] = elem['close']
            single_candle['ticker'] = pair
            single_candle['exchange'] = self.name

            result.append(single_candle)

        return result

    def _get_parsed_period(self, period):
        if period in ['1m', '1min']:
            return '1min'

        elif period in ['60min', '1h']:
            return '60min'

        else:
            raise ValueError("Wrong period in huobi exchange")
