from asyncio import log
import logging
from exceptiongroup import catch
from flask import Blueprint, jsonify, request, render_template
import flask
from pandas import read_csv

import requests
import json
import urllib

import os
from dotenv import load_dotenv
import urllib3


load_dotenv()
API_KEY = os.getenv("API_KEY")


urllib3.disable_warnings()

logger = logging.getLogger()

home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
@home_routes.route("/home")
def index():
    print("HOME...")
    #return "Welcome Home"
    return render_template("home.html")



def show_game_func(app_id):
    # Download the CSV file if it doesn't already exist
    url = "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv"

    # Read the CSV file into a DataFrame
    country_codes_df = read_csv(url)
    country_codes = country_codes_df.to_dict("records")


    # 
    isInvalid = False
    lowest_price = 1000000
    lowest_currency = "none"

    # Define a function to convert prices to USD
    def conversion(lowest_currency,lowest_price):
        with urllib.request.urlopen(f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={lowest_currency}&to_currency=USD&apikey={API_KEY}') as url:
            data3 = json.load(url)
            if "Realtime Currency Exchange Rate" in data3:
                rt = float(data3["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
                converted_price = rt * lowest_price
                return converted_price
            else:
                return None

    # Get the list of all country codes
    all_codes = [str(c["alpha-2"]) for c in country_codes]

    # Get the list of all app IDs
    app_list = []
    request_url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    response = requests.get(request_url, verify=False)
    data = json.loads(response.text)
    for d in data["applist"]["apps"]:
        app_list.append(str(d["appid"]))

    # Check if the app ID is valid
    if app_id not in app_list:
        isInvalid = True
        return isInvalid, lowest_currency, lowest_price
        # return "Invalid app ID"

    # Find the cheapest price for the game

    for code in all_codes:
        request_url = f"http://store.steampowered.com/api/appdetails?appids={app_id}&cc={code}&filters=price_overview"
        response = requests.get(request_url, verify=False)
        data2 = json.loads(response.text)
        if data2 is not None:
            if data2[app_id]["success"] == False:
                continue
            else:
                if len(data2[app_id]["data"]) == 0:
                    isInvalid = True
                    return isInvalid, lowest_currency, lowest_price
                    # return "This game is yet to be released. Please check later."
            
        pass
    raise SyntaxError("api error")
    pass

@home_routes.route("/game/<int:app_id>",  methods=["POST","GET"])
def show_game(app_id):
    try:
        isInvalid, lowest_currency, lowest_price = show_game_func(app_id)
        return render_template("result.html", isInvalid=isInvalid, lowest_currency=lowest_currency, lowest_price=lowest_price)
        pass
    except Exception as err:
        logger.error(err)
        return render_template("error.html")
        pass

    pass
