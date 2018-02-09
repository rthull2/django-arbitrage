from django.contrib import admin

from .models import Coin, Exchange, Market

class CoinAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name')
    search_fields = ('symbol', 'name')


class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('name', 'wallet_support')


class MarketAdmin(admin.ModelAdmin):
    list_display = ('exchange', 'trading_pair', 'volume', 'price')

admin.site.register(Coin, CoinAdmin)
admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(Market, MarketAdmin)
