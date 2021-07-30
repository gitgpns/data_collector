from saver_abc import SaverABC

import pandas as pd
import os


class LocalSaver(SaverABC):

    def __init__(self, saving_path):
        self._saving_path = saving_path

        self._result_data = list()

    def save_data(self, data):
        for row in data:
            self._insert_single_row(row)

            print(f"Data from {row['open_time']} to {row['close_time']} on exchange {row['exchange']} for ticker {row['ticker']} added to csv")

    def _insert_single_row(self, row):
        self._result_data.append(row)

    def end_session(self):
        final_df = pd.DataFrame(self._result_data)
        final_df.to_csv(os.path.join(self._saving_path, self.exchange_name + '.csv'))
