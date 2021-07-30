import psycopg2
from saver_abc import SaverABC


class CandlesSaverDB(SaverABC):
    fields = 'open_time, close_time, volume, low_price, high_price, open_price, close_price, ticker, exchange'

    def __init__(self, table_name, dbname, user):
        self._table_name = table_name

        self._conn = psycopg2.connect(f"dbname={dbname} user={user}")
        self._cur = self._conn.cursor()

    def save_data(self, data):
        for row in data:
            self._insert_single_row(row)

            print(f"Data from {row['open_time']} to {row['close_time']} on exchange {row['exchange']} for ticker {row['ticker']} saved to db")

        self._conn.commit()

    def _insert_single_row(self, row):
        values = f"'{row['open_time']}', '{row['close_time']}', {row['volume']}, {row['low_price']}, {row['high_price']},{row['open_price']}, {row['close_price']}, '{row['ticker']}', '{row['exchange']}'"
        query = f"INSERT INTO {self._table_name} ({self.fields}) VALUES ({values})"
        self._cur.execute(query)

    def end_session(self):
        self._conn.close()
