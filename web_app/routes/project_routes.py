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

from app.api import API_KEY

load_dotenv()


urllib3.disable_warnings()

logger = logging.getLogger()

home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
@home_routes.route("/home")
def index():
    print("HOME...")
    #return "Welcome Home"
    return render_template("home.html")



def conversion(lowest_currency,lowest_price):
    with urllib.request.urlopen(f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={lowest_currency}&to_currency=USD&apikey={API_KEY}') as url:
        data3 = json.load(url)
        if "Realtime Currency Exchange Rate" in data3:
            rt = float(data3["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
            converted_price = rt * lowest_price
            return converted_price
        else:
            # print("Exchange Rate does not exist")
            return None

def show_game_func(app_id_int):
    app_id = "%d" % app_id_int
    logger.error(app_id)

    isInvalid = True
    lowest_price=1000000
    lowest_currency="none"
    

    url = "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv"
    country_codes_df = read_csv(url)
    country_codes = country_codes_df.to_dict("records")

    all_codes=[]
    app_list=[]

    for c in country_codes:
        all_codes.append(str(c["alpha-2"])) 

    #print(all_codes)

    request_url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"  
    response = requests.get(request_url, verify=False)
    data = json.loads(response.text)

    for d in data["applist"]["apps"]:
        app_list.append(str(d["appid"]))

    _app_id_flag = False
    for _app_id in app_list:
        if _app_id == app_id:
            _app_id_flag = True
            break
    if _app_id_flag != True:
        return isInvalid, lowest_currency, lowest_price
    #print(app_list)


    location="none"

    for code in all_codes:
        request_url=f"http://store.steampowered.com/api/appdetails?appids={app_id}&cc={code}&filters=price_overview"
        response = requests.get(request_url, verify=False)
        data2 = json.loads(response.text)
        if data2 is not None:
            if data2[app_id]["success"]==False:
                lowest_price=lowest_price
                lowest_currency=lowest_currency
            else:
                if len(data2[app_id]["data"])==0:
                    # print("This game is yet to be released. Please check later.")
                    isInvalid = False
                    return isInvalid, lowest_currency, lowest_price
                    break
                else:
                    price = data2[app_id]["data"]["price_overview"]["final"]/100
                    currency = data2[app_id]["data"]["price_overview"]["currency"]
                    price_in_usd=conversion(currency,price)
                    if price_in_usd is None:
                        continue
                    elif price_in_usd < lowest_price:
                        lowest_price = price_in_usd
                        lowest_currency = currency

    if lowest_price != 1000000:
        # print("Your selected game is cheapest in",lowest_currency,".")
        # print("The lowest price in US dollar value is $%.2f."%(lowest_price))
        # OK
        isInvalid = False
        return isInvalid, lowest_currency, lowest_price
    # not find
    isInvalid = False
    return isInvalid, lowest_currency, lowest_price


@home_routes.route("/game/<int:app_id>",  methods=["POST","GET"])
def show_game(app_id):
    try:
        isInvalid, lowest_currency, lowest_price = show_game_func(app_id)
        return render_template("result.html", isInvalid=isInvalid, lowest_currency=lowest_currency, lowest_price="%d"%lowest_price)
        pass
    except Exception as err:
        logger.error(err)
        return render_template("error.html")
        pass

    pass
