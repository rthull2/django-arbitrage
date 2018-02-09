import ssl
import json
import hmac
import time
import base64
import urllib
import socket
import hashlib
import requests
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote_plus

gateio_key = ''
gateio_secret = b''

bittrex_key = ''
bittrex_secret = b''

binance_key = ''
binance_secret = b''

cryptopia_key = ''
_cryptopia_secret = ''
cryptopia_secret = base64.b64decode(
    _cryptopia_secret + '=' * (-len(_cryptopia_secret) % 4))

hitbtc_key = ''
hitbtc_secret = ''

kucoin_key = ''
kucoin_secret = ''


def binance(symbol):
    url = 'https://api.binance.com/wapi/v3/depositAddress.html'
    values = {'asset': symbol, 'recvWindow': 10000,
              'timestamp': int(time.time() * 1000)}
    body = urlencode(values)
    signature = hmac.new(binance_secret, body.encode(
        'utf-8'), hashlib.sha256).hexdigest()
    params = []
    for k, v in values.items():
        params.append((k, v))
    params.append(('signature', signature))
    headers = {
        'X-MBX-APIKEY': binance_key,
    }
    req = requests.get(url, params=params, headers=headers)
    return json.loads(req.text)['success']


def coinexchange(symbol):
    url = 'https://www.coinexchange.io/api/v1/getcurrency?ticker_code=' + symbol
    req = requests.get(url)
    try:
        return json.loads(req.text)['result']['WalletStatus'] == 'online'
    except (KeyError, json.decoder.JSONDecodeError):
        return None


def coinsmarkets(symbol):
    return None


def cryptopia(symbol):
    url = 'https://www.cryptopia.co.nz/Api/GetDepositAddress'
    nonce = str(int(time.time() * 1000))
    data = json.dumps({'Currency': symbol})
    md5 = hashlib.md5()
    md5.update(data.encode('utf-8'))
    data64 = base64.b64encode(md5.digest())
    signature = bytes(cryptopia_key + "POST" +
                      quote_plus(url).lower() + nonce, 'utf-8') + data64
    sign = base64.b64encode(
        hmac.new(cryptopia_secret, signature, hashlib.sha256).digest())
    authorization = bytes("amx " + cryptopia_key + ":",
                          'utf-8') + sign + bytes(":" + nonce, 'utf-8')
    headers = {
        'Authorization': authorization,
        'Content-Type': 'application/json; charset=utf-8'
    }
    req = requests.post(url, data=data, headers=headers)
    return json.loads(req.text)['Success']


def gateio(symbol):
    url = "https://data.gate.io/api2/1/private/depositAddress"
    values = {'currency': symbol}
    body = urlencode(values)
    signature = hmac.new(gateio_secret, body.encode(
        'utf-8'), hashlib.sha512).hexdigest()
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "KEY": gateio_key,
        "SIGN": signature
    }
    req = requests.post(url, data=values, headers=headers)
    status = json.loads(req.text)['addr']
    if 'New address' not in status:
        return True
    return False


def mercatox(symbol):
    return None


def gdax(symbol):
    return None


def bittrex(symbol):
    exdict = {}
    url = 'https://bittrex.com/api/v2.0/pub/Currencies/GetWalletHealth'
    signature = hmac.new(bittrex_secret, url.encode(
        'utf-8'), hashlib.sha512).hexdigest()
    headers = {'apisign': signature}
    req = requests.get(url, headers=headers)
    status = json.loads(req.text)['result']
    for row in status:
        sym = row['Health']['Currency']
        if sym == symbol:
            return row['Health']['IsActive']
    return None


def hitbtc(symbol):
    url = 'https://api.hitbtc.com/api/2/account/crypto/address/' + symbol
    session = requests.session()
    session.auth = (hitbtc_key, hitbtc_secret)
    res = session.get(url).json()
    return 'error' not in res


def kucoin(symbol):
    url = 'https://api/kucoin.com/v1/account/' + symbol + '/wallet/address/'
    session = requests.session()
    headers = {
        'Accept': 'application/json',
        'KC-API-KEY': kucoin_key,
    }
    session.headers.update(headers)


exchanges = {
    "Binance": binance,
    "CoinExchange": coinexchange,
    "CoinsMarkets": coinsmarkets,
    "Gate.io": gateio,
    "Mercatox": mercatox,
    "GDAX": gdax,
    "Bittrex": bittrex,
    "Cryptopia": cryptopia,
    "HitBTC": hitbtc,
    "Kucoin": kucoin,
}


def check(exchange, symbol):
    while True:
        try:
            return exchanges[exchange](symbol)
        except (socket.gaierror, urllib.error.URLError, ssl.SSLEOFError, json.decoder.JSONDecodeError):
            time.sleep(.5)


if __name__ == "__main__":
    print(hitbtc('XRP'))
