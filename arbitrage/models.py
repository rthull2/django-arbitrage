from django.db import models
from . import walletstatus


class Coin(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=15)

    def __str__(self):
        return self.name

    def getRatio(self, exchanges):
        markets = list(self.market_set.filter(exchange__name__in=exchanges))
        sortmarkets = sorted(
            markets, key=lambda Market: Market.price, reverse=True)
        return '{0:.3f}'.format(sortmarkets[0].price / sortmarkets[len(sortmarkets) - 1].price)

    def marketInfo(self, exchanges):
        markets = list(self.market_set.filter(exchange__name__in=exchanges))
        return sorted(markets, key=lambda Market: Market.price, reverse=True)


class Exchange(models.Model):
    name = models.CharField(max_length=50)
    wallet_support = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def wallet_status(self, symbol):
        return walletstatus.check(self.name, symbol) if self.wallet_support else None


class Market(models.Model):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    base = models.ForeignKey(
        Coin, on_delete=models.CASCADE, related_name='pair')
    link = models.CharField(max_length=150)
    volume = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=11)

    def __str__(self):
        return '%s %s/%s' % (self.exchange, self.coin.symbol, self.base.symbol)

    def trading_pair(self):
        return '%s/%s' % (self.coin.symbol, self.base.symbol)
