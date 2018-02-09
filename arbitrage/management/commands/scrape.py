import threading
from socket import timeout
from bs4 import BeautifulSoup
from arbitrage.models import Market, Exchange, Coin
from urllib.request import urlopen
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Populate Market table with info from CMC'

    def handle(self, *args, **options):
        Market.objects.all().delete()
        threads = []
        for ex in Exchange.objects.all():
            t = threading.Thread(target=self.scrapeExchange, args=(ex,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

    def downloadpage(self, url):
        while True:
            try:
                return urlopen(url, timeout=1)
            except timeout:
                pass

    def scrapeExchange(self, exchange):
        exname = exchange.name.replace('.', '-')
        html = self.downloadpage('https://coinmarketcap.com/exchanges/' + exname)
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.findAll('tr')
        markets = []
        for row in rows:
            if row is rows[0]:
                continue
            try:
                volume = float(row.find('span', {'class': 'volume'})['data-btc'])
            except ValueError:
                volume = 0
            if volume < 5:
                break

            container = row.findAll('a', limit=2)
            name = container[0].text.strip()
            pair = container[1].text.strip().split('/')
        
            try: 
                coin = Coin.objects.get(name=name, symbol=pair[0])
                base = Coin.objects.get(symbol=pair[1])
            except Coin.DoesNotExist:
                continue
            tradelink = container[1]['href']
            price = float(row.find('span', {'class': 'price'})['data-btc'])
            stalebox = row.find('td', {'class': 'stale-box'})
            
            if not stalebox:
                markets.append(Market(exchange=exchange, coin=coin, base=base, link=tradelink, volume=volume, price=price))

        Market.objects.bulk_create(markets)