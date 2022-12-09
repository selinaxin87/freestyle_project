from app.project import conversion

def test_steam_prices():
    # Test the conversion function
    assert conversion("USD", 100) == 100
    assert conversion("EUR", 100) > 100
    assert conversion("JPY", 100) < 100

