from config_reader import ConfigReader
from candle_loader_builder import CandleLoaderBuilder


def run():
    config_reader = ConfigReader()
    config_reader.read_config()

    config = config_reader.config

    candle_loader_builder = CandleLoaderBuilder(config)
    candle_loader = candle_loader_builder.build()

    candle_loader.collect_exchanges_data()


if __name__ == "__main__":
    run()
