
# Steam Game Price Comparison
This web application allows users to find the cheapest available price for a game on Steam. The user simply enters the game's app ID, and the app will search through all available Steam regions to find the lowest price and currency. The result is displayed on the page in US dollars.

## Notes
The app uses the Steam API to get information about available games and their prices in different regions.
The app uses the AlphaVantage API to convert prices to US dollars. You will need to provide your own API key in order for this feature to work:

## Setup
Create and activate a virtual environment:

```sh
conda create -n SteamPC-env python=3.8

conda activate SteamPC-env
```
Install package dependencies:

```sh
pip install -r requirements.txt
```
## Configuration

[Obtain an API Key](https://www.alphavantage.co/support/#api-key) from AlphaVantage.

Then create a local ".env" file and provide the key like this:

```sh
# this is the ".env" file...

API_KEY="_________"
```
## Usage
Run the Price Comparison App:

```sh
python app/project.py
```

```sh
# or pass  env var from command to run
API_KEY="_____" python app/project.py
```
### Web App

Run the web app (then view in the browser at http://localhost:5000/):

To use the app, simply go to the homepage and enter the app ID of the game you want to find. The app will search through all available Steam regions and display the lowest price in US dollars.

```sh
# Mac OS:
FLASK_APP=web_app flask run

# Windows OS:
# ... if `export` doesn't work for you, try `set` instead
# ... or set FLASK_APP variable via ".env" file
export FLASK_APP=web_app
flask run
```

## Testing
Run tests:

```sh
pytest
```



## License
This project is licensed under the MIT License. See LICENSE for details:

