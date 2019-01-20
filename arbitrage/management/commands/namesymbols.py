import urllib3
from bs4 import BeautifulSoup
from arbitrage.models import Coin
from django.core.management.base import BaseCommand
urllib3.disable_warnings()


class Command(BaseCommand):
    help = 'Populate Coin table with info from CMC'

    def handle(self, *args, **options):
        self.http = urllib3.PoolManager()
        html = self.downloadpage('https://coinmarketcap.com/all/views/all/')
        soup = BeautifulSoup(html.data, 'html.parser')
        rows = soup.findAll('tr')
        for row in rows[:200]:
            if row is rows[0]:
                continue
            try:
                container = row.find('a', {'class': 'currency-name-container'})
                name = container.text.strip()
                if name.endswith('...'):
                    name = self.fullname(container['href'])
                symbol = row.find('td', {'class': 'col-symbol'}).text.strip()
                obj, created = Coin.objects.get_or_create(name=name, symbol=symbol)
                if created:
                    obj.save()
            except Exception:
                pass

    def fullname(self, coinlink):
        html = self.downloadpage('https://coinmarketcap.com' + coinlink)
        soup = BeautifulSoup(html.data, 'html.parser')
        container = soup.find('h1')
        strings = container.text.split('  ')
        for string in strings:
            string = string.strip()
            if len(string) > 10:
                return string


    def downloadpage(self, url):
        while True:
            try:
                return self.http.request('GET', url)
            except Exception:
                pass