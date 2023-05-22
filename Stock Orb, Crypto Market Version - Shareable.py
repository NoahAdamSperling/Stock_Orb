# Import needed Python packages
import requests
import json
import time
from yeelight import Bulb

# Enter your Yeelight's IP address here
BULB_IP = "Your YeeLight's IP address"

# Enter your API key for Finnhub here
FINNHUB_API_KEY = "Your Finnnubb API KEY"

# Connect to your Yeelight bulb
bulb = Bulb(BULB_IP)
bulb.turn_on()

# Define a function to change the bulb color based on the percent change in Bitcoin price
def change_color(percent_change):
    if percent_change >= 3:
        bulb.set_rgb(255, 255, 0)
        # Yellow color for percent changes greater than or equal to 3
    elif percent_change > 0:
        bulb.set_rgb(0, 255, 0)
        # Green color for percent changes between 0 and 3
    elif percent_change <= -3:
        bulb.set_rgb(128, 0, 128)
        # Purple color for percent changes less than or equal to -3
    elif percent_change < 0:
         bulb.set_rgb(255, 0, 0)
        # Red color for percent changes less than or equal to -3
    else:
         bulb.set_rgb(255, 255, 255)
        # White color for everything else, generally will apply when percent change is zero, which would occur when the 
        # numerator current price is the same as the denominator previous closing price.

# Define a function to get the current Bitcoin price from Binance using the Finnhub API
# 'resolution=1&count=1' tells:
#     resolution=1 specifies the resolution of the data to be retrieved to be 1 second intervals.
#     count=1 specifies that only one candle or data point is required, which in this case is the most 
#             recent candle or data point, corresponding to the current Bitcoin price.
def get_btc_price():
    url = "https://finnhub.io/api/v1/crypto/candle?symbol=BINANCE:BTCUSDT&resolution=1&count=1&token=" + FINNHUB_API_KEY
    response = requests.get(url)
    data = json.loads(response.text)
    return data["c"][-1]


# Define a function to get the previous Bitcoin price from Binance using the Finnhub API
    # Get the timestamp for yesterday at 5:00pm
    # 'resolution=60&count=1' tells:
    #     resolution=1 specifies the resolution of the data to be retrieved to be 1 second intervals.
    #     The 'from' and 'to' parameters in the URL specify the time range for which to retrieve the candle data, 
    #     in Unix timestamp format. yesterday_5pm is a variable that stores the Unix timestamp for yesterday's date at 5:00 PM 
    #     in the local timezone. yesterday_5pm+60*60 adds 60 minutes to the yesterday_5pm timestamp, which represents the end 
    #     of the 1-hour interval for which the candle data is being retrieved.
    # So the full URL with parameters is retrieving the candle data for Bitcoin's price from Binance for a 
    # 1-hour interval that starts at yesterday's date at 5:00 PM and ends 1 hour later.
    # Denominator for the daily percent change is reset every hour to be the value of the crypto asset 24 hours ago from that refresh.
def get_prev_btc_price():
    yesterday_5pm = int(time.time()) - ((60 * 60 * 24) + (60 * 60 * 7))
    url = f"https://finnhub.io/api/v1/crypto/candle?symbol=BINANCE:BTCUSDT&resolution=60&from={yesterday_5pm}&to={yesterday_5pm+60*60}&token={FINNHUB_API_KEY}"
    response = requests.get(url)
    data = json.loads(response.text)
    return data["c"][-1]

# Define a function to get the percent change in Bitcoin price
def get_percent_change(current_price, prev_price):
    return ((current_price - prev_price) / prev_price) * 100

# Define a function to get the current Bitcoin price every 5 seconds and change the bulb color based on the percent change
def run():
    prev_price = get_prev_btc_price()
    while True:
        try:
            current_price = get_btc_price()
            percent_change = get_percent_change(current_price, prev_price)
            change_color(percent_change)
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            #^Add a time variable so the current time of each pull can be displayed in the terminal
            print(f"{now} - Current Price: {current_price:.2f}, Previous Price: {prev_price:.2f}")
            prev_price = get_prev_btc_price()
            time.sleep(3)
        #If an error occurs, print that an error occured to the terminal, then turn blue for 5 seconds, then restart
        except Exception as e:
            print(f"Error: {e}")
            for i in range(30, 0, -1):
                bulb.set_rgb(0, 0, 255)
                time.sleep(5)
                print(f"Restarting in {i} seconds...")
            bulb.set_rgb(255, 255, 255)
            time.sleep(5)

# This Python code defines a conditional block that checks whether the current module is
# being run as the main program. If the current module is being run as the main program,
# then the function run() is called.
# This is useful for writing test code and for defining a command-line interface for a module or package
if __name__ == '__main__':
    run()
