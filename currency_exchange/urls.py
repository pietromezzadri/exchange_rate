from django.urls import path
from . import views

urlpatterns = [
    path('daily_exchange_rate/', views.DailyExchangeRateView.as_view()),
]
