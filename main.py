from flask import Flask, Response, request
import prometheus_client
import flask
from prometheus_client import Counter, generate_latest, Gauge
from os import environ
from threading import Thread
from time import sleep
import requests

app = Flask(__name__)

graphs = {}

# graphs["login"] = Gauge("lumenswap_login", "click count on login button")

COINCAPURL = environ['COINCAPURL']
INTERVAL= environ['INTERVAL']
CRYPTOS= environ['CRYPTOS']
APP_PORT=environ['APP_PORT']

CRYPTO_LIST = CRYPTOS.split(",")

graphs["cc_exporter_priceUsd"] = Gauge("cc_exporter_priceUsd",'priceUsd',["name"])
graphs["cc_exporter_rank"] = Gauge("cc_exporter_rank", 'rank',["name"])
graphs["cc_exporter_supply"] = Gauge("cc_exporter_supply", 'supply',["name"])
graphs["cc_exporter_maxSupply"] = Gauge("cc_exporter_maxSupply", 'maxSupply',["name"])
graphs["cc_exporter_marketCapUsd"] = Gauge("cc_exporter_marketCapUsd", 'marketCapUsd',["name"])
graphs["cc_exporter_volumeUsd24Hr"] = Gauge("cc_exporter_volumeUsd24Hr", 'volumeUsd24Hr',["name"])
graphs["cc_exporter_changePercent24Hr"] = Gauge("cc_exporter_changePercent24Hr", 'changePercent24Hr',["name"])
graphs["cc_exporter_vwap24Hr"] = Gauge("cc_exporter_vwap24Hr", 'vwap24Hr',["name"])




@app.route("/",methods = ['GET'])
def main():
    return "OK"


@app.route("/metrics")
def requests_count():
    res = []
    for k,v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(res, mimetype="text/plain")


def flaskThread():
    app.run(port=int(APP_PORT), host='0.0.0.0')
Thread(target = flaskThread).start()


def getLatestData():
    return requests.get(COINCAPURL).json()

def roundDec(floatNum):
    return round(floatNum,7)


def makeMetrics(singleCryptoRes):
    c_name = singleCryptoRes["id"]
    # print(singleCryptoRes)
    graphs["cc_exporter_priceUsd"].labels(c_name).set(singleCryptoRes["priceUsd"])
    graphs["cc_exporter_rank"].labels(c_name).set(singleCryptoRes["rank"])
    graphs["cc_exporter_supply"].labels(c_name).set(singleCryptoRes["supply"])
    try:
        graphs["cc_exporter_maxSupply"].labels(c_name).set(singleCryptoRes["maxSupply"])
    except:
        pass
        # graphs[c_name+"_maxSupply"].labels(c_name).set(0)
    graphs["cc_exporter_marketCapUsd"].labels(c_name).set(singleCryptoRes["marketCapUsd"])
    graphs["cc_exporter_volumeUsd24Hr"].labels(c_name).set(singleCryptoRes["volumeUsd24Hr"])
    graphs["cc_exporter_changePercent24Hr"].labels(c_name).set(singleCryptoRes["changePercent24Hr"])
    try:
        graphs["cc_exporter_vwap24Hr"].labels(c_name).set(singleCryptoRes["vwap24Hr"])
    except:
        pass
        # graphs[c_name+"_vwap24Hr"].labels(c_name).set(0)



def StartFetchingData():
    while True:
        result = getLatestData()
        # print(result["data"][1])
        for userCrypto in CRYPTO_LIST:
            for resutlCrypto in result["data"]:
                if userCrypto==resutlCrypto["id"]:
                    makeMetrics(resutlCrypto)


        print("Interval time")
        sleep(int(INTERVAL))

StartFetchingData()