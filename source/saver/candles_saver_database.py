import psycopg2
from ..saver_ABC import SaverABC


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

        conn.commit()
        conn.close()

    def _insert_single_row(self, row, cur):
        query = f"INSERT INTO {self.table_name} ({self.fields}) VALUES ({row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]},{row[5]}, {row[6]}, {row[7]}, {row[8]})"
        cur.execute(query)