



import os
from pandas import read_csv
import urllib.request, json 
import requests
import json
from app.api import API_KEY


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

if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv"
    country_codes_df = read_csv(url)
    country_codes = country_codes_df.to_dict("records")

    all_codes=[]
    app_list=[]

    for c in country_codes:
        all_codes.append(str(c["alpha-2"]))

    #print(all_codes)

    request_url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"  
    response = requests.get(request_url)
    data = json.loads(response.text)

    for d in data["applist"]["apps"]:
        app_list.append(str(d["appid"]))

    #print(app_list)

    app_id=input("Please enter the app id for the game you would like to purchase: ") 

    while app_id not in app_list: 
            print ("Oops! Invalid app id. Please reenter: ")
            app_id=input()


    lowest_price=1000000
    lowest_currency="none"
    location="none"

    for code in all_codes:
            request_url=f"http://store.steampowered.com/api/appdetails?appids={app_id}&cc={code}&filters=price_overview"
            response = requests.get(request_url)
            data2 = json.loads(response.text)
            if data2 is not None:
                if data2[app_id]["success"]==False:
                    lowest_price=lowest_price
                    lowest_currency=lowest_currency
                else:
                    if len(data2[app_id]["data"])==0:
                        print("This game is yet to be released. Please check later.")
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
        print("Your selected game is cheapest in",lowest_currency,".")
        print("The lowest price in US dollar value is $%.2f."%(lowest_price))