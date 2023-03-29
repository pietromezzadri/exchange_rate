from django.shortcuts import render
from django.shortcuts import redirect

from .models import ExchangeRate
from .forms import QueryForm
from .serializers import ExchangeRateSerializer
from .utils.vat_service import VatService
from .utils.response_parser import ResponseParser
from .utils.converter import Converter

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from datetime import datetime, timedelta

import requests
import json


class DailyExchangeRateView(APIView):

    def get(self, request):
        vat_service = VatService()
        response_parser = ResponseParser()
        response_parser.parse_response(vat_service.get_daily())

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

    def get(self, request):
        if request.query_params:
            date_str = request.query_params['date']
            exchange_rate = ExchangeRate.objects.filter(rate_date=date_str)
            if not exchange_rate:
                vat_service = VatService()
                response_parser = ResponseParser()
                response_parser.parse_response(
                    vat_service.get_by_date(date_str))
                serializer = ExchangeRateSerializer(
                    data=response_parser.exchange_rate)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = ExchangeRateSerializer(exchange_rate, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'ERROR', 'No date provided'}, status=status.HTTP_400_BAD_REQUEST)


class ExchangeRateByPeriod(APIView):

    def get(self):
        pass


class ExchangeRateChart(APIView):

    def get(self, request):
        print(request.query_params)
        form = QueryForm(request.POST)
        currency = request.query_params['currency']
        # If dates are not provided, return rates for current date
        if 'initial_date' in request.query_params and 'final_date' in request.query_params:
            initial_date = request.query_params['initial_date']
            final_date = request.query_params['final_date']
            initial_date_obj = datetime.strptime(initial_date, '%Y-%m-%d')
            final_date_obj = datetime.strptime(final_date, '%Y-%m-%d')
            time_delta = (final_date_obj - initial_date_obj).days
            if time_delta > 5 or time_delta < 0:
                initial_date = datetime.now().strftime('%Y-%m-%d')
                final_date = datetime.now().strftime('%Y-%m-%d')
                form.add_error(
                    'final_date', 'The date range cannot exceed 5 work days or be negative')
            else:
                for day in range(time_delta):
                    day_check = initial_date_obj + timedelta(days=day)
                    if day_check.weekday() >= 5:
                        initial_date = datetime.now().strftime('%Y-%m-%d')
                        final_date = datetime.now().strftime('%Y-%m-%d')
                        form.add_error(
                            'final_date', 'Weekends cannot be selected')
                        break
                    date_str = day_check.strftime('%Y-%m-%d')
                    exchange_rate = ExchangeRate.objects.filter(
                        rate_date=date_str)
                    if not exchange_rate:
                        vat_service = VatService()
                        response_parser = ResponseParser()
                        response_parser.parse_response(
                            vat_service.get_by_date(date_str))
                        serializer = ExchangeRateSerializer(
                            data=response_parser.exchange_rate)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            form.add_error(
                                'initial_date', 'unable to fetch data')
        else:
            initial_date = datetime.now().strftime('%Y-%m-%d')
            final_date = datetime.now().strftime('%Y-%m-%d')
        converter = Converter()
        exchage_rates = ExchangeRate.objects.filter(
            rate_date__range=[initial_date, final_date]).order_by('rate_date')
        dates = list(exchage_rates.values_list('rate_date', flat=True))
        if currency == 'BRL':
            rates = list(exchage_rates.values_list('brl_rate', flat=True))
            rates_float = converter.convert_number_float(rates)
        if currency == 'EUR':
            rates = list(exchage_rates.values_list('eur_rate', flat=True))
            rates_float = converter.convert_number_float(rates)
        if currency == 'JPY':
            rates = list(exchage_rates.values_list('jpy_rate', flat=True))
            rates_float = converter.convert_number_float(rates)
        dates_str = converter.convert_dates_str(dates)

        context = {'data': json.dumps({
            'chat': {'type': 'line'},
            'title': {'text': 'USD Exchange Rate'},
            'yAxis': {'title': {'text': 'Exchange Rate for 1 USD'}},
            'xAxis': {'title': {'text': 'Date'},
                      'type': 'date',
                      'categories': dates_str},
            'series': [{
                'name': currency,
                'data': rates_float,
            }]
        }),
            'form': form}
        return render(request, 'exchange_chart.html', context=context)
