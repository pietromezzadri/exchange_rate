![Github Workflow](https://github.com/pietromezzadri/exchange_rate/actions/workflows/django.yml/badge.svg) <img src="https://cdn-icons-png.flaticon.com/512/873/873120.png" alt= “” width="20" height="20">[Heroku App](https://salty-plateau-96183.herokuapp.com/)

# Currency Exchange Rate

## Table of Contents

- [About](#about)
- [API](#api)
  - [daily exchange rate](#daily_exchange_rate)
  - [exchange rate](#exchange_rate)

## About

A simple project to display the rate of BRL, EUR and JPY within a week, using USD as the base currency. It also has API calls for daily per date rates. Rates are queried from [VAT Comply](https://www.vatcomply.com/).

![Screenshot](/media/screenshot.png)

## API

Allows get requests using params for queries.

### `daily_exchange_rate`

`GET APP_URL/api/daily_exchange_rate/`

returns json with rates for the current date.

```json
[
  {
    "_id": 4,
    "base_currency": "USD",
    "brl_rate": "5.10113907771449500000",
    "eur_rate": "0.91861106007716330000",
    "jpy_rate": "132.66580929634392000000",
    "rate_date": "2023-03-30",
    "created_at": "2023-03-30T15:51:13.993534Z"
  }
]
```

### `exchange_rate`

`GET APP_URL/api/exchange_rate/?date='%Y-%m-%d'`

returns json with rates for the current date.

`GET APP_URL/api/exchange_rate/?date=2023-03-30`

output:

```json
[
  {
    "_id": 4,
    "base_currency": "USD",
    "brl_rate": "5.10113907771449500000",
    "eur_rate": "0.91861106007716330000",
    "jpy_rate": "132.66580929634392000000",
    "rate_date": "2023-03-30",
    "created_at": "2023-03-30T15:51:13.993534Z"
  }
]
```

Developed with:

<img src="https://static.djangoproject.com/img/logos/django-logo-negative.png" alt="" height="50"> [Django](https://www.djangoproject.com/)

<img src="https://picocss.com/img/opengraph.jpg" alt="" height="50"> [Pico.css](https://picocss.com/)

<img src="https://static-00.iconduck.com/assets.00/highcharts-icon-512x487-mq4vqgn3.png" alt="" height="50"> [Highcharts](https://www.highcharts.com/)

[Vat Comply](https://www.vatcomply.com/)
