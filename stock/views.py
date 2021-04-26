from django.shortcuts import render, redirect
import json
import requests
from stock.models import Stock
from django.contrib import messages
from .forms import StockForm

KEY = "pk_9274979738c74528ad6d76dc1c59296a"
base_url = "https://cloud.iexapis.com"


def home(request):
    stock_symbol = "aapl"

    if request.method == "POST":
        stock_symbol = request.POST["stock_quote_input"]

    url = base_url + "/stable/stock/" + stock_symbol + "/quote?token=" + KEY
    raw_res = requests.get(url)

    try:
        res = json.loads(raw_res.content)
    except Exception as e:
        res = "StockQuoteRequestError"

    return render(request, 'home.html', {"res": res})


def stock_list(request):
    stock_symbol_list = Stock.objects.all()
    return render(request, 'stock_list.html', {'stock_symbol_list': stock_symbol_list})


def add_stock(request):
    if request.method == "POST":
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Stock has been added.")
            return redirect('stock_list')


def delete_stock(request, stock_id):
    target_stock = Stock.objects.get(pk=stock_id)
    target_stock.delete()
    messages.success(request, "Stock has been deleted successfully.")
    return redirect('stock_list')


def about(request):
    return render(request, 'about.html', {})
