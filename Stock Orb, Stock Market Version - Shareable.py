# Import needed Python packages
import datetime
import pytz
import time
import requests
import requests.adapters
from yeelight import Bulb
from finnhub import Client

# Request adapters setting to 100 should resolve a pooling issue, set higher if crashing.
requests.adapters.DEFAULT_POOL_SIZE = 100

# Replace with your Finnhub API key
API_KEY = "Your Finnnubb API KEY"

# Replace with your Yeelight Smart Light's IP address
# This IP address is found in the Yee Light app once the bulb is connected.
BULB_IP = "Your YeeLight's IP address"

# Replace with your target stock symbol
# VOO is an applicable S&P 500 ETF
SYMBOL = "VOO"

# Replace with your target stock exchange
EXCHANGE = "US"

# Replace with your timezone
TIMEZONE = "US/Eastern"

while True:
    #Try statement tells the code to re-run the code starting from this point downward if an error is encountered
    try:
        # Create a new instance of the Yeelight Smart Light
        bulb = Bulb(BULB_IP)
        
        # Create a new instance of the Finnhub API client
        finnhub_client = Client(api_key=API_KEY)
        
        # Initialize the previous closing stock price
        previous_closing_price = None

        while True:
            # Defining current_time using the date.time function from online
            current_time = datetime.datetime.now(pytz.timezone(TIMEZONE))
            # If current weekday is under 5 (i.e., 0 Monday through 4 Friday) and more than 8:30am and less than 6:30pm
            if current_time.weekday() < 5 and datetime.time(8, 30) <= current_time.time() <= datetime.time(18, 30):
                
                # Turn on the Yeelight Smart Light and set brightness to 50%
                bulb.turn_on()
                bulb.set_brightness(50)
                
                #Try-Except to Catch FinnHub API error
                #Turn bulb blue for 30 seconds if this error occurs
                try:
                    # Connecting to the FinnHub API for the specific stock you specify
                    stock_data = finnhub_client.quote(SYMBOL)
                except Exception as e:
                    print("Error accessing Finnhub API:", e)
                    bulb.set_rgb(0, 0, 255)
                    time.sleep(30)
                    continue
                
                # Get the current stock price and previous day closing price
                current_price = stock_data['c']
                current_closing_price = stock_data['pc']

                # If this is not the first iteration of the loop
                if previous_closing_price is not None:
                    # Calculate the percent change in stock price
                    percent_change = (current_price - previous_closing_price) / previous_closing_price * 100
                    # Change the color of the Yeelight Smart Light based on the percent change in stock price
                    if percent_change >= 3:
                        bulb.set_rgb(255, 215, 0)
                    # Gold color for percent changes greater than or equal to 3
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
                    
                    # Print current and previous closing stock prices with the current time
                    print(current_time, "Current price:", current_price)
                    print(current_time, "Previous closing price:", previous_closing_price)
                
                # Set the previous closing stock price to the current closing stock price for the next iteration
                # This allows for the previous closing price to update evry 24 hours   
                previous_closing_price = current_closing_price
                
                # Wait for 4 seconds before checking the stock price again    
                time.sleep(3)
            
            # What to do if not within trading hours        
            else:
                # If not within trading hours specified, turn the light off
                bulb.turn_off()
                
                # When light turns off, print the time in which turned off to denote trading hours closed and waiting for the trading floor to open back up
                print(current_time, "Trading hours closed, waiting for opening...")

                # Printing current time to checking if trading hours have resumed
                # The printing lets us see in terminal the code is still running
                while True:
                    current_time = datetime.datetime.now(pytz.timezone(TIMEZONE))
                    print(current_time, "Checking if trading hours have resumed...")
    
                    # If the current time is within trading hours, it will print that trading hours have resumed
                    # and apply the break command to tell this second loop to end and resume looping through
                    # checking stock prices from the current loop 
                    if current_time.weekday() < 5 and datetime.time(8, 30) <= current_time.time() <= datetime.time(18, 30):
                        print(current_time, "Trading hours resumed.")
                        break
                    
                    #time.sleep uses seconds, so 2 checks every 2 seconds, 60 every 1 minute, 1800 every 30 minutes, 3600 every 1 hour                    
                    time.sleep(1800)
 
 #Except command connects to Try command to tell code to print that it encountered error, then restart the code from the Try-line after 30 seconds.                 
    except Exception as e:
        print("Encountered error:", e)
        time.sleep(30)
        bulb.set_rgb(0, 0, 255)
        time.sleep(30)
