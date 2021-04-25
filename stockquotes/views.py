from django.shortcuts import render
import json
import requests

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


def about(request):
    return render(request, 'about.html', {})
