from arbitrage.models import Exchange
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Populate Exchange table with exchanges'

    def handle(self, *args, **options):
        for exchange in {('Bittrex', True), ('Binance', True), ('GDAX', False),
                         ('Cryptopia', True), ('Gate.io', True), ('CoinsMarkets', True),
                         ('Mercatox', False), ('CoinExchange', True)}:
            obj, updated = Exchange.objects.update_or_create(name=exchange[0], defaults={'wallet_support': exchange[1]})
            obj.save()
