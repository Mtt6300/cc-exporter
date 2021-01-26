# cc-exporter
CC-Exporter is a Prometheus metrics exporter developed with Python which allows you to monitor Cryptocurrencies Market Cap from Grafana dashboards and define multiple alerts by generating metrics from CoinCap public api.


# Run
```bash
$ git clone https://github.com/Mtt6300/cc-exporter
$ cd cc-exporter
$ docker-compose up -d
```
Now you should be able to visit grafana dashboard on `http://localhost:3000`

*Note*: By default user and password is `admin`.



# Customization
For Customization you need to change these envs in `cc-exporter` service from `docker-compose.yaml` file:
- `INTERVAL`: Timeout for fetch in data from api. (default: 50)
- `CRYPTOS`: String that shows which Coins you want to monitor. If is more than 1, you must separate `coin id`'s with Commas.(default: ethereum,bitcoin,xrp,binance-coin,stellar,tether) 
- `APP_PORT`: Cc-exporter port. (default: 5000)
- `COINCAPURL`: Coin Cap Api url. (default: https://api.coincap.io/v2/assets)

*Note*: You should find the correct `coin id` from CoinCap public api. (link: https://api.coincap.io/v2/assets)


# Contributing , idea ,issue
Feel free to fill an issue or create a pull request, I'll check it ASAP
