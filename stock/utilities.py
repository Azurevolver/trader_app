def process_stock_raw_data(raw_data: dict):
    result = {}

    try:
        result["symbol"] = raw_data["symbol"]
        result["companyName"] = raw_data["companyName"]
        result["latestPrice"] = "$ {:,.2f}".format(raw_data["latestPrice"])

        result["volume"] = "N/A"
        if raw_data["previousVolume"] is not None:
            result["volume"] = "{:,.2f}".format(raw_data["previousVolume"])

        result["marketCap"] = "$ {:,.2f}".format(raw_data["marketCap"])

        result["peRatio"] = "N/A"
        if raw_data["peRatio"] is not None:
            result["peRatio"] = "$ {:,.2f}".format(raw_data["peRatio"])

        result["week52High"] = "$ {:,.2f}".format(raw_data["week52High"])
        result["week52Low"] = "$ {:,.2f}".format(raw_data["week52Low"])

        if raw_data["ytdChange"] is not None:
            percentage = round(raw_data["ytdChange"] * 100, 2)
            result["ytdChange"] = "$ {:,.2f}".format(percentage) + "%"

    except Exception as e:
        res = "StockQuoteRequestError"

    return result
