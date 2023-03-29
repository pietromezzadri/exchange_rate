from django.shortcuts import render
from .models import ExchangeRate
from .serializers import ExchangeRateSerializer
from .utils.vat_service import VatService
from .utils.response_parser import ResponseParser

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import requests
import json


class DailyExchangeRateView(APIView):

    def get(self, request):
        vat_service = VatService()
        response_parser = ResponseParser()
        response_parser.parse_response(vat_service.get_usd())

        record = ExchangeRate.objects.filter(
            rate_date=response_parser.exchange_rate['rate_date'])
        if not record:
            serializer = ExchangeRateSerializer(
                data=response_parser.exchange_rate)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ExchangeRateSerializer(record, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class ExchangeRateByDate(APIView):

    def get(self):
        pass


class ExchangeRateByPeriod(APIView):

    def get(self):
        pass
