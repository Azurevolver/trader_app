from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
import json
import requests
from django.views import View
from django.views.generic import DetailView

from stock.models import Stock
from django.contrib import messages
from .utilities import process_stock_raw_data
from datetime import datetime

KEY = "pk_9274979738c74528ad6d76dc1c59296a"
base_url = "https://cloud.iexapis.com"


def home(request):
    stock_symbol = "aapl"
    search_result = {}
    if request.method == "POST":
        stock_symbol = request.POST["stock_quote_input"]

    news_url = base_url + "/stable/stock/" + stock_symbol + "/news/last?token=" + KEY
    raw_res = requests.get(news_url)
    try:
        search_result = json.loads(raw_res.content)

        for news in search_result:
            mil_sec = news["datetime"]
            date_string = datetime.fromtimestamp(mil_sec // 1000)
            news["datetime"] = date_string
    except Exception as e:
        res = "StockNewsRequestError"

    url = base_url + "/stable/stock/" + stock_symbol + "/quote?token=" + KEY
    raw_res = requests.get(url)
    stock_detail = {}

    try:
        res = json.loads(raw_res.content)
        stock_detail = process_stock_raw_data(res)
    except Exception as e:
        stock_detail = "StockQuoteRequestError"

    return render(request, 'home.html', {"search_result": search_result, "stock_detail": stock_detail})


def stock_list(request):
    stock_symbol_list = Stock.objects.all()

    for stock in stock_symbol_list:
        stock_symbol = stock.ticker
        price_url = base_url + "/stable/stock/" + stock_symbol + "/quote/latestPrice?token=" + KEY
        raw_res = requests.get(price_url)

        try:
            latest_quote_price = json.loads(raw_res.content)
            # print("[DEBUG] res price: ")
            # print(res)
            stock.latest_price = latest_quote_price
        except Exception as e:
            print("[DEBUG] error occurs on fetch price")

    return render(request, 'stock_list.html', {'stock_symbol_list': stock_symbol_list})


class StockDetail(View):
    def get(self, request, pk):
        stock_info = get_object_or_404(
            Stock,
            pk=pk
        )

        request_logo_url = base_url + "/stable/stock/" + stock_info.ticker + "/logo?token=" + KEY
        raw_res = requests.get(request_logo_url)
        logo = json.loads(raw_res.content)
        stock_info.logo_url = logo["url"]
        return render(
            request,
            'stock_detail.html',
            {'stock': stock_info}
        )

# class StockDetail(DetailView):
#     model = Stock
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # stock_info = self.get_object()
#         return context


def add_stock(request):
    if request.method == "POST":
        stock_symbol = request.POST["ticker"]
        url = base_url + "/stable/stock/" + stock_symbol + "/quote?token=" + KEY
        raw_res = requests.get(url)
        response_content = {}
        all_tracking_stocks = {}

        try:
            res = json.loads(raw_res.content)
            response_content = process_stock_raw_data(res)
            stock_data = Stock(
                ticker=response_content['symbol'],
                company_name=response_content['companyName'],
                latest_price=response_content["latestPrice"],
                volume=response_content["volume"],
                market_cap=response_content["marketCap"],
                pe_ratio=response_content["peRatio"],
                w52_high=response_content["week52High"],
                w52_low=response_content["week52Low"],
                ytd_change=response_content["ytdChange"],
            )
            stock_data.save()
            messages.success(request, stock_symbol.upper() + "is added to your watch list successfully.")
        except Exception as e:
            all_tracking_stocks = "StockQuoteRequestError"
            messages.warning(request, "Please enter a valid stock symbol.")

        all_tracking_stocks = Stock.objects.all().order_by('stock_id')

    return render(request, 'stock_list.html', {"stock_symbol_list": all_tracking_stocks})


def delete_stock(request, stock_id):
    target_stock = Stock.objects.get(pk=stock_id)
    target_stock.delete()
    messages.success(request, "Stock has been deleted successfully.")
    return redirect('stock_list')


def about(request):
    return render(request, 'about.html', {})

