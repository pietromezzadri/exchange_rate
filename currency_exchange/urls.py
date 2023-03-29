from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect(
        'exchange_chart/?currency=BRL', permanent=False), name='default'),
    path('daily_exchange_rate/', views.DailyExchangeRateView.as_view()),
    path('exchange_chart/', views.ExchangeRateChart.as_view()),
]
