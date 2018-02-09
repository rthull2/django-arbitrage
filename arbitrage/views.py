import json
from urllib.parse import unquote
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import TemplateView
from django.db.models import Count, Q
from django.core import serializers
from django.core.management import call_command

from .models import Market, Coin, Exchange


class IndexView(TemplateView):
    template_name = 'arbitrage/index.html'

    def get(self, request, *args, **kwargs):
        call_command('scrape')
        try:
            exchanges = json.loads(unquote(request.COOKIES['exchanges']))
        except KeyError:
            exchanges = Exchange.objects.values_list('name', flat=True)

        context = self.get_context_data(exchanges=exchanges)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['coin_list'] = Coin.objects.annotate(exchange_count=Count('market__exchange', distinct=True, filter=Q(
            market__exchange__name__in=kwargs['exchanges']))).filter(exchange_count__gte=2)
        context['exchange_list'] = Exchange.objects.all()
        context['approved_exch'] = kwargs['exchanges']
        return context


def wallet_status(request):
    exchange = Exchange.objects.get(name=request.GET.get('exchange', None))
    coin = Coin.objects.get(name=request.GET.get('coin', None))
    status = exchange.wallet_status(coin.symbol)
    data = {
        'status': status
    }
    return JsonResponse(data)


def marketInfo(request):
    try:
        exchanges = json.loads(unquote(request.COOKIES['exchanges']))
    except KeyError:
        exchanges = Exchange.objects.values_list('name', flat=True)
    coin = Coin.objects.get(name=request.GET.get('coin', None))
    markets = coin.marketInfo(exchanges)
    data = []
    for market in markets:
        entry = {
            'source': market.exchange.name,
            'base': market.base.symbol,
            'wallet': market.exchange.wallet_support,
            'link': market.link,
            'volume': market.volume,
            'price': market.price
        }
        data.append(entry)

    return JsonResponse(data, safe=False)
