from bs4 import BeautifulSoup
from arbitrage.models import Coin
from urllib.request import urlopen
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Populate Coin table with info from CMC'

    def handle(self, *args, **options):
        html = self.downloadpage('https://coinmarketcap.com/all/views/all/')
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.findAll('tr')
        for row in rows:
            if row is rows[0]:
                continue
            container = row.find('a', {'class': 'currency-name-container'})
            name = container.text.strip()
            if name.endswith('...'):
                name = self.fullname(container['href'])
            symbol = row.find('td', {'class': 'col-symbol'}).text.strip()
            obj, created = Coin.objects.get_or_create(name=name, symbol=symbol)
            if created:
                obj.save()

    def fullname(self, coinlink):
        html = self.downloadpage('https://coinmarketcap.com' + coinlink)
        soup = BeautifulSoup(html, 'html.parser')
        container = soup.find('h1')
        strings = container.text.split('  ')
        for string in strings:
            string = string.strip()
            if len(string) > 10:
                return string

    def downloadpage(self, url):
        while True:
            try:
                return urlopen(url)
            except (urllib.error.HTTPError, urllib.error.URLError, http.client.RemoteDisconnected):
                pass