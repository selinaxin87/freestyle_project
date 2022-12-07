from flask import Flask, render_template

app = Flask(__name__)

@app.route("/game/<int:app_id>")
def show_game(app_id):
    # Download the CSV file if it doesn't already exist
    url = "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv"

    # Read the CSV file into a DataFrame
    country_codes_df = read_csv(url)
    country_codes = country_codes_df.to_dict("records")

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
    response = requests.get(request_url)
    data = json.loads(response.text)
    for d in data["applist"]["apps"]:
        app_list.append(str(d["appid"]))

    # Check if the app ID is valid
    if app_id not in app_list:
        return "Invalid app ID"

    # Find the cheapest price for the game
    lowest_price = 1000000
    lowest_currency = "none"
    for code in all_codes:
        request_url = f"http://store.steampowered.com/api/appdetails?appids={app_id}&cc={code}&filters=price_overview"
        response = requests.get(request_url)
        data2 = json.loads(response.text)
        if data2 is not None:
            if data2[app_id]["success"] == False:
                continue
            else:
                if len(data2[app_id]["data"]) == 0:
                    return "This game is yet to be released. Please check later."
               
