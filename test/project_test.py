def test_steam_prices():
    # Test the conversion function
    assert conversion("USD", 100) == 100
    assert conversion("EUR", 100) == 112.61
    assert conversion("JPY", 100) == 0.89

    # Test the API endpoint for app IDs
    response = requests.get(request_url)
    assert response.status_code == 200
    data = json.loads(response.text)
    assert "applist" in data and "apps" in data["applist"]
    assert len(data["applist"]["apps"]) > 0

    # Test the API endpoint for app details
    app_id = data["applist"]["apps"][0]["appid"]
    request_url = f"http://store.steampowered.com/api/appdetails?appids={app_id}&cc=US&filters=price_overview"
    response = requests.get(request_url)
    assert response.status_code == 200
    data = json.loads(response.text)
    assert app_id in data and data[app_id]["success"] == True
    assert "data" in data[app_id] and "price_overview" in data[app_id]["data"]

    # Test the main function
    assert main(app_id) == ("Your selected game is cheapest in USD.", "The lowest price in US dollar value is $x.xx.")
