from abc import ABC, abstractmethod


class SaverABC(ABC):

    @abstractmethod
    def save_data(self, data):
        pass
