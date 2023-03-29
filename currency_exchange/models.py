from django.db import models


""" class ExchangeRate(models.Model):
    currency_choices = [('BRL', 'Brazilian Real'),
                        ('EUR', 'Euro'), ('JPY', 'Japanese Yen')]

    _id = models.AutoField(primary_key=True)
    base_currency = models.CharField(
        max_length=3, choices=currency_choices, null=False, blank=False, default='USD')
    target_currency = models.CharField(
        max_length=3, choices=currency_choices, null=False, blank=False)
    rate = models.DecimalField(decimal_places=4, max_digits=20)
    rate_date = models.DateField()
    created_at = models.DateField(auto_now_add=True) """


class ExchangeRate(models.Model):
    _id = models.AutoField(primary_key=True)
    base_currency = models.CharField(
        max_length=3, null=False, blank=False, default='USD')
    brl_rate = models.DecimalField(decimal_places=20, max_digits=50)
    eur_rate = models.DecimalField(decimal_places=20, max_digits=50)
    jpy_rate = models.DecimalField(decimal_places=20, max_digits=50)
    rate_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
