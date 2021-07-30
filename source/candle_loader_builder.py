from database_saver import CandlesSaverDB
from local_saver import LocalSaver
from candle_loader import CandleLoader
from binance_candle_loader import BinanceCandleLoader
from okex_candle_loader import OkexCandleLoader
from huobi_candle_loader import HuobiCandleLoader

import psycopg2


class CandleLoaderBuilder:
    def __init__(self, config):
        self._config = config

        self._candle_loader = None

    def build(self):
        self._init_candle_loader()

        self._add_exchanges()

        return self._candle_loader

    def _init_candle_loader(self):
        self._candle_loader = CandleLoader()

    def _check_database_parameters(self):
        try:
            table_name = self._config['table_name']
            table_creation_sql = self._config['table_creation_sql']
            user_name = self._config['user_name']
            database_name = self._config['database_name']

        except KeyError:
            raise KeyError("Ether table_name/table_creation_sql/user_name/database_name parameter is not found")

    def _add_exchanges(self):
        exchanges_parameters = self._config['exchanges']
        created_exchanges = list()

        for exchange_parameters in exchanges_parameters:
            new_exchange = self._get_exchange(exchange_parameters)
            created_exchanges.append(new_exchange)

        self._candle_loader.exchanges = created_exchanges

    def _get_exchange(self, exchange_parameters):
        start_date = self._config['start_date']
        end_date = self._config['end_date']
        period = self._config['period']

        pairs = exchange_parameters['pairs']
        exchange_name = exchange_parameters['exchange_name'].lower()

        saver = self._get_saver()
        saver.exchange_name = exchange_name

        if exchange_name == 'binance':
            new_exchange = BinanceCandleLoader(start_date, end_date, saver, period, pairs)

        elif exchange_name == 'okex':
            new_exchange = OkexCandleLoader(start_date, end_date, saver, period, pairs)

        elif exchange_name == 'huobi':
            new_exchange = HuobiCandleLoader(start_date, end_date, saver, period, pairs)

        else:
            raise ValueError(f"Not valid exchange name: {exchange_name}")

        return new_exchange

    def _get_saver(self):
        saving_parameter = self._config['saving_to']

        if saving_parameter == 'database':
            new_saver = self._get_database_saver()

        elif saving_parameter == 'local':
            new_saver = self._add_local_saver()

        else:
            raise ValueError(f"Not valid saving parameter {saving_parameter}")

        return new_saver

    def _get_database_saver(self):
        self._check_database_parameters()

        self._create_table_if_not_exist()

        table_name = self._config['table_name']
        user_name = self._config['user_name']
        database_name = self._config['database_name']

        new_saver = CandlesSaverDB(table_name=table_name, dbname=database_name, user=user_name)
        return new_saver

    def _create_table_if_not_exist(self):
        query = self._config['table_creation_sql']
        dbname = self._config['database_name']
        user = self._config['table_name']

        conn = psycopg2.connect(f"dbname={dbname} user={user}")
        cur = conn.cursor()

        cur.execute(query)
        conn.commit()

        conn.close()

    def _add_local_saver(self):
        saving_path = self._config['saving_path']
        new_saver = LocalSaver(saving_path=saving_path)

        return new_saver
