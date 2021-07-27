from abc import ABC, abstractmethod
import pandas as pd
from source.saver.candles_saver_database import CandlesSaverDB
from saver_ABC import SaverABC
import datetime


class CandleLoaderABC(ABC):#TODO add candle period mapping; and step mapping

    def __init__(self, start_date, end_date, step, saving_place, period):
        self._start_timestamp = pd.to_datetime(start_date).timestamp()
        self._end_timestamp = pd.to_datetime(end_date).timestamp()
        self._step = step
        self._saving_place = saving_place
        self._period_in_seconds = self._get_parsed_period(period)

        self._data_saver: SaverABC = CandlesSaverDB()

        self._request_periods = None

        self._create_request_periods()

    def _create_request_periods(self):
        request_periods = list()
        current_end_timestamp = self._start_timestamp

        while current_end_timestamp != self._end_timestamp:
            current_start_timestamp = current_end_timestamp
            current_end_timestamp = min(current_start_timestamp + self._step * self._period_in_seconds, self._end_timestamp)

            request_periods.append([int(current_start_timestamp), int(current_end_timestamp)])

        self._request_periods = request_periods

    def collect_data(self):
        for period in self._request_periods:
            self._get_single_period_data(period)

    def _save_data(self, data):
        if self._saving_place == 'csv':
            self._save_data_to_csv(data)

        elif self._saving_place == 'database':
            self._save_data_to_db(data)

        else:
            raise ValueError(f'Wrong data saving command name {self._saving_place}')

    @abstractmethod
    def _get_single_period_data(self, period):
        pass

    def _save_data_to_csv(self, data):
        print(data)

    def save_failed_request(self):
        pass

    def _save_data_to_db(self, data):
        self._data_saver.save_data(data)

    @staticmethod
    def _get_parsed_period(period):#TODO finish mapping
        if period in ['1min', '1m']:
            return 60

        elif period in ['60min', '60m', '1h', '1hour']:
            return 3600

    @staticmethod
    def to_utc(timestamp):
        return datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
