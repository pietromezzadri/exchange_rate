from .models import ExchangeRate
from rest_framework import serializers


class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRate
        fields = ['_id', 'base_currency', 'brl_rate',
                  'eur_rate', 'jpy_rate', 'rate_date', 'created_at']
