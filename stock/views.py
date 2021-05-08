from django.shortcuts import render, redirect, get_object_or_404
import json
import requests
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from stock.models import Stock, ToDoItem
from django.contrib import messages
from .forms import ToDoItemForm
from .utilities import process_stock_raw_data
from datetime import datetime
from decimal import Decimal

KEY = "pk_9274979738c74528ad6d76dc1c59296a"
BASE_URL = "https://cloud.iexapis.com"
CRYPTO_BASE_URL = "https://min-api.cryptocompare.com"
CRYPTO_KEY = "5aa48fdb6bdae90671e8c0775404bc4e5e253f02b8d7b348aed9168a12f8e239"
CRYPTO_SYMBOL_URL = CRYPTO_BASE_URL + "/data/blockchain/list?&api_key=" + CRYPTO_KEY

"""
-----------------------------------------------------------------------------------------
Stock-related views
"""


def home(request):
    stock_symbol = "aapl"
    search_result = {}
    if request.method == "POST":
        stock_symbol = request.POST["stock_quote_input"]

    news_url = BASE_URL + "/stable/stock/" + stock_symbol + "/news/last?token=" + KEY
    raw_res = requests.get(news_url)
    try:
        search_result = json.loads(raw_res.content)

        for news in search_result:
            mil_sec = news["datetime"]
            date_string = datetime.fromtimestamp(mil_sec // 1000)
            news["datetime"] = date_string
    except Exception as e:
        res = "StockNewsRequestError"

    url = BASE_URL + "/stable/stock/" + stock_symbol + "/quote?token=" + KEY
    raw_res = requests.get(url)
    stock_detail = {}

    try:
        res = json.loads(raw_res.content)
        stock_detail = process_stock_raw_data(res)
    except Exception as e:
        stock_detail = "StockQuoteRequestError"

    return render(request, 'stock/home.html', {"search_result": search_result, "stock_detail": stock_detail})


def stock_list(request):
    stock_symbol_list = Stock.objects.all()

    for stock in stock_symbol_list:
        stock_symbol = stock.ticker
        price_url = BASE_URL + "/stable/stock/" + stock_symbol + "/quote/latestPrice?token=" + KEY
        raw_res = requests.get(price_url)

        try:
            latest_quote_price = json.loads(raw_res.content)
            # print("[DEBUG] res price: ")
            # print(res)
            stock.latest_price = latest_quote_price
        except Exception as e:
            print("[DEBUG] error occurs on fetch price")

    return render(request, 'stock/stock_list.html', {'stock_symbol_list': stock_symbol_list})


class StockDetail(View):
    def get(self, request, pk):
        stock_info = get_object_or_404(
            Stock,
            pk=pk
        )

        request_logo_url = BASE_URL + "/stable/stock/" + stock_info.ticker + "/logo?token=" + KEY
        raw_res = requests.get(request_logo_url)
        logo = json.loads(raw_res.content)
        stock_info.logo_url = logo["url"]

        return render(
            request,
            'stock/stock_detail.html',
            {'stock': stock_info}
        )


def add_stock(request):
    if request.method == "POST":
        stock_symbol = request.POST["ticker"]
        url = BASE_URL + "/stable/stock/" + stock_symbol + "/quote?token=" + KEY
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
            displayed_warning_msg = "Please enter a valid stock symbol."
            error_msg = e.__str__()
            if error_msg == "UNIQUE constraint failed: stock_stock.company_name":
                displayed_warning_msg = "The ticker symbol is already existed, please enter a new one!"

            all_tracking_stocks = "StockQuoteRequestError"
            messages.warning(request, displayed_warning_msg)

        all_tracking_stocks = Stock.objects.all().order_by('stock_id')

    return render(request, 'stock/stock_list.html', {"stock_symbol_list": all_tracking_stocks})


def delete_stock(request, stock_id):
    target_stock = Stock.objects.get(pk=stock_id)
    target_stock.delete()
    messages.success(request, "Stock has been deleted successfully.")
    return redirect('stock_list')


"""
-----------------------------------------------------------------------------------------
Crypto-related views
"""


def crypto_news(request):
    crypto_symbol = "BTC"
    crypto_news_results = {}
    crypto_exist = False
    if request.method == "POST":
        crypto_symbol = str(request.POST["crypto_input"]).upper()

    # detect whether crypto symbol exist
    crypto_id = 1182
    raw_res = requests.get(CRYPTO_SYMBOL_URL)
    try:
        crypto_symbol_info_results = json.loads(raw_res.content)
        if "Data" in crypto_symbol_info_results:
            if crypto_symbol in crypto_symbol_info_results["Data"]:
                print(crypto_symbol_info_results["Data"][crypto_symbol])
                crypto_id = crypto_symbol_info_results["Data"][crypto_symbol]["id"]
                crypto_exist = True
            else:
                crypto_news_results = "CryptoSymBolNotExistError"

    except Exception as e:
        crypto_news_results = "CryptoSymBolNotExistError"

    # fetch crypto stats within social media
    crypto_social_stats = {}
    social_stats_url = CRYPTO_BASE_URL + "/data/social/coin/latest?coinId=" + str(crypto_id) + "&api_key=" + CRYPTO_KEY
    raw_res = requests.get(social_stats_url)
    try:
        crypto_social_stats = json.loads(raw_res.content)
    except Exception as e:
        crypto_social_stats = "CryptoStatusNotExistError"

    # fetch price
    price_url = CRYPTO_BASE_URL + "/data/pricemultifull?fsyms=" + crypto_symbol + "&tsyms=USD&api_key=" + CRYPTO_KEY
    raw_res = requests.get(price_url)
    crypto_price = {}
    try:
        raw_price_dict = json.loads(raw_res.content)
        if "RAW" in raw_price_dict :
            if crypto_symbol in raw_price_dict["RAW"]:
                crypto_price = raw_price_dict["RAW"][crypto_symbol]["USD"]
    except Exception as e:
        crypto_price = "CryptoPriceNotExistError"

    # fetch crypto news
    news_url = CRYPTO_BASE_URL + "/data/v2/news/?categories=" + crypto_symbol + "&api_key=" + CRYPTO_KEY
    raw_res = requests.get(news_url)
    try:
        crypto_news_results = json.loads(raw_res.content)
    except Exception as e:
        crypto_news_results = "CryptoNewsRequestError"

    return render(request, 'crypto/crypto_news.html', {
                        "crypto_exist": crypto_exist,
                        "crypto_news_results": crypto_news_results,
                        "crypto_social_stats": crypto_social_stats,
                        "crypto_price": crypto_price
                  })

"""
-----------------------------------------------------------------------------------------
To-do item related views
"""


class ToDoItemList(ListView):
    model = ToDoItem


class ToDoItemCreate(CreateView):
    form_class = ToDoItemForm
    model = ToDoItem
    success_url = '/todoitem_list/'


class ToDoItemDetail(DetailView):
    model = ToDoItem

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        return context


class ToDoItemUpdate(UpdateView):
    form_class = ToDoItemForm
    model = ToDoItem
    template_name = 'stock/todoitem_update.html'


class ToDoItemDelete(DeleteView):
    model = ToDoItem
    success_url = reverse_lazy('to_do_item_list_url')


def about(request):
    return render(request, 'stock/about.html', {})
