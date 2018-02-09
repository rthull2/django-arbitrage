from django.urls import path

from . import views

app_name = 'arbitrage'
urlpatterns = [
    path('', views.IndexView.as_view(), name='magic'),
    path('ajax/wallet_status', views.wallet_status, name='wallet_status'),
    path('ajax/marketInfo', views.marketInfo, name='marketInfo')
]