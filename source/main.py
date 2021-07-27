from source.binance_candle_loader import BinanceCandleLoader
from source.okex_candle_loader import OkexCandleLoader
from source.huobi_candle_loader import HuobiCandleLoader


def main(params):
    start_date = params['start_date']
    end_date = params['end_date']
    exchanges = params['exchanges']
    period = params['period']

    if 'binance' in exchanges:
        binance_loader = BinanceCandleLoader(start_date, end_date, period=period)
        binance_loader.collect_data()

    elif 'huobi' in exchanges:
        huobi_loader = HuobiCandleLoader(start_date, end_date, period=period)

        huobi_loader.collect_data()

    elif 'okex' in exchanges:
        okex_loader = OkexCandleLoader(start_date, end_date, period=period)

        okex_loader.collect_data()


if __name__ == "__main__":
    params = {
        'exchanges': ['binance'],
        'start_date': '2020-6-21',
        'end_date': '2021-06-21',
        'period': '1m'
    }
    main(params)
