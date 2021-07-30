### The instrument is used for futures candles data collection
#### Usage
To use the instrument you should run the main file
The current parameters are set in the config file.
#### Parameters description
  *"start_date": "2021-06-19"* - first date

  *"end_date": "2021-06-20"* - last date

  *"period": "1m"*, single candle period; at the moment can be sat as ***{'1m', '1h'}***

  *"saving_to": "database"* - ***"database"/"local"***

  *"user_name": "oleg"* - postgres username on the local machine

  *"database_name": "oleg"* - postgres db name on the local machine

  *"saving_path": ""* - path for local saving

  *"table_creation_sql": "CREATE TABLE IF NOT EXISTS candles (\nopen_time TIMESTAMP NOT NULL,\nclose_time TIMESTAMP NOT NULL,\nvolume DOUBLE PRECISION NOT NULL,\nlow_price DOUBLE PRECISION NOT NULL,\nhigh_price DOUBLE PRECISION NOT NULL,\nopen_price DOUBLE PRECISION NOT NULL,\nclose_price DOUBLE PRECISION NOT NULL,\nticker VARCHAR ( 50 ) NOT NULL,\nexchange VARCHAR ( 50 ) NOT NULL,\nid serial PRIMARY KEY\n);"* - SQL to create the table

  "*table_name": "candles"* - SHOULD BE THE SAME AS THE TABLE NAME IN ***table_creation_sql*** SQL 

  *"exchanges": [

    {
      "exchange_name": "binance",
      "pairs": ["YFIUSDT", "BTCUSDT", "ETHUSDT", "AAVEUSDT", "UNIUSDT", "BNBUSDT", "SUSHIUSDT", "MATICUSDT"]
    },
    {
      "exchange_name": "huobi",
      "pairs": ["YFI-USDT", "BTC-USDT", "ETH-USDT", "AAVE-USDT", "UNI-USDT", "BNB-USDT", "SUSHI-USDT", "FIL-USDT"]
    },
    {
      "exchange_name": "okex",
      "pairs": ["BTC-USDT-SWAP", "BTC-USDT-SWAP"]
    }
  ] - current implemented exchanges ***'binance'***, ***'huobi'***, ***'okex'***