from abc import ABC, abstractmethod
import pandas as pd


class CandleLoaderABC(ABC):

    def __init__(self, start_date, end_date, step, saving_place):
        self._start_timestamp = pd.to_datetime(start_date).timestamp()
        self._end_timestamp = pd.to_datetime(end_date).timestamp()
        self._step = step
        self._saving_place = saving_place

        self._request_periods = None

        self._create_request_periods()

    def _create_request_periods(self):
        request_periods = list()
        current_end_timestamp = self._start_timestamp

        while current_end_timestamp != self._end_timestamp:
            current_start_timestamp = current_end_timestamp
            current_end_timestamp = min(current_start_timestamp + self._step, self._end_timestamp)

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

    def _save_data_to_db(self, data):
        pass