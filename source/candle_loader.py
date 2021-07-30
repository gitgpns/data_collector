class CandleLoader:
    def __init__(self):
        self.exchanges = None

    def collect_exchanges_data(self):#TODO create threads for each exchange
        for exchange in self.exchanges:
            exchange.collect_data()
