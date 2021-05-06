from django.db import models
from django.urls import reverse


class Stock(models.Model):
    stock_id = models.AutoField(primary_key=True)
    ticker = models.CharField(max_length=10, unique=True)
    company_name = models.CharField(max_length=50, unique=True, default='')
    latest_price = models.CharField(max_length=10)
    volume = models.CharField(max_length=20)
    market_cap = models.CharField(max_length=30)
    pe_ratio = models.CharField(max_length=10, default='')
    w52_high = models.CharField(max_length=10)
    w52_low = models.CharField(max_length=10)
    ytd_change = models.CharField(max_length=10)

    def __str__(self):
        return self.ticker

    def get_absolute_url(self):
        return reverse("stock_detail_url", kwargs={'pk': self.pk})

