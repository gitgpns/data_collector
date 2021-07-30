from abc import ABC, abstractmethod
import uuid


class SaverABC(ABC):
    fields_keys = ['open_time', 'close_time', 'volume', 'low_price', 'high_price', 'open_price', 'close_price',
                   'ticker', 'exchange']

    exchange_name = uuid.uuid4()

    @abstractmethod
    def save_data(self, data):
        pass

    @abstractmethod
    def end_session(self):
        pass
