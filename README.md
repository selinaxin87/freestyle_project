# freestyle_project

Steam Game Finder
This web application allows users to find the cheapest available price for a game on Steam. The user simply enters the game's app ID, and the app will search through all available Steam regions to find the lowest price and currency. The result is displayed on the page in US dollars.

Running the app
To run the app, follow these steps:

Clone the repository: git clone https://github.com/<your-username>/steam-game-finder.git
Install the required dependencies: pip install -r requirements.txt
Set the FLASK_APP environment variable: export FLASK_APP=main.py
Start the app: flask run
The app will now be running at http://127.0.0.1:5000/.

Using the app
To use the app, simply go to the homepage and enter the app ID of the game you want to find. The app will search through all available Steam regions and display the lowest price in US dollars.

Notes
The app uses the Steam API to get information about available games and their prices in different regions.
The app uses the AlphaVantage API to convert prices to US dollars. You will need to provide your own API key in order for this feature to work.
License
This project is licensed under the MIT License. See LICENSE for details.