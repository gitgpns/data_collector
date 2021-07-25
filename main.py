from tqdm import tqdm
import datetime

from binance_candle_loader import BinanceCandleLoader
from okex_candle_loader import OkexCandleLoader
from huobi_candle_loader import HuobiCandleLoader


def main(params):
    start_date = params['start_date']
    end_date = params['end_date']
    exchanges = params['exchanges']

    if 'binance' in exchanges:
        binance_loader = BinanceCandleLoader(start_date, end_date)
        binance_loader.collect_data()

    elif 'huobi' in exchanges:
        huobi_loader = HuobiCandleLoader(start_date, end_date)

        huobi_loader.collect_data()

    elif 'okex' in exchanges:
        okex_loader = OkexCandleLoader(start_date, end_date)

        okex_loader.collect_data()


if __name__ == "__main__":
    params = {
        'exchanges': ['okex'],
        'start_date': '2021-06-20',
        'end_date': '2021-06-21'
    }
    main(params)
