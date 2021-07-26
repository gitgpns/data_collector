import psycopg2
from source.saver_ABC import SaverABC


class CandlesSaverDB(SaverABC):
    table_name = 'candles'
    dbname = 'oleg'
    user = 'oleg'
    fields = 'open_time, close_time, volume, low_price, high_price, open_price, close_price, ticker, exchange'
    fields_keys = ['open_time', 'close_time', 'volume', 'low_price', 'high_price', 'open_price', 'close_price', 'ticker', 'exchange']

    def __init__(self):
        pass

    def save_data(self, data):
        conn = psycopg2.connect(f"dbname={self.dbname} user={self.user}")
        cur = conn.cursor()

        for row in data:
            self._insert_single_row(row, cur)

            print(f"Data from {row['open_time']} to {row['close_time']} on exchange {row['exchange']} for ticker {row['ticker']} saved to db")

        conn.commit()
        conn.close()

    def _insert_single_row(self, row, cur):
        values = f"'{row['open_time']}', '{row['close_time']}', {row['volume']}, {row['low_price']}, {row['high_price']},{row['open_price']}, {row['close_price']}, '{row['ticker']}', '{row['exchange']}'"
        query = f"INSERT INTO {self.table_name} ({self.fields}) VALUES ({values})"
        cur.execute(query)
