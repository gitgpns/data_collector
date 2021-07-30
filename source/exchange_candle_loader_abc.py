from abc import ABC, abstractmethod
import pandas as pd
import datetime


class CandleLoaderABC(ABC):

    def __init__(self, start_date, end_date, step, saver, period, pairs):
        self.period = period
        self._start_timestamp = pd.to_datetime(start_date).timestamp()
        self._end_timestamp = pd.to_datetime(end_date).timestamp()
        self._step = step
        self._data_saver = saver
        self.pairs = pairs
        self._period_in_seconds = self._get_period_to_seconds(period)

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

        self._data_saver.end_session()

    def _save_data(self, data):
        self._data_saver.save_data(data)

    @abstractmethod
    def _get_single_period_data(self, period):
        pass

    @staticmethod
    def _get_period_to_seconds(period):#TODO finish mapping
        if period in ['1min', '1m']:
            return 60

        elif period in ['60min', '60m', '1h', '1hour']:
            return 3600

    @staticmethod
    def to_utc(timestamp):
        return datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    @abstractmethod
    def _get_parsed_period(self, period):
        pass
