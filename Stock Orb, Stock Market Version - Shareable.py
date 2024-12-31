#Stock Orb: Improved Error Handling (19-Dec-2024)
#(i.e., without creating a new new Bulb instance (bulb = Bulb(BULB_IP)) every time, which could be causing issues if the instance isn't being closed properly or too many connections are being made.

# Turns on light, starting in brown as unused color from other color keys.
#from yeelight import Bulb
#bulb = Bulb("192.168.1.202")
#bulb.turn_on()
#bulb.set_rgb(205, 127, 50)

# Import needed packages
import datetime
import pytz
import time
import requests
import requests.adapters
from yeelight import Bulb, BulbException, Flow, RGBTransition
from finnhub import Client

# Request adapters setting to 100 should resolve a pooling issue, set higher if crashing.
requests.adapters.DEFAULT_POOL_SIZE = 100

# Replace with your API key
API_KEY = "Your Finnnubb API KEY"

# Replace with your Yeelight Smart Light's IP address
BULB_IP = "Your YeeLight's IP address"

# Replace with your target stock symbol
# VOO is working S&P 500 ETF
# Works for Crypto stocks as well such as "BTC-USD"
SYMBOL = "VOO"

# Replace with your target stock exchange
# Tracking ETFs through Finhubb costs money, but for some reason VOO works just fine
EXCHANGE = "US"

# Replace with your timezone
TIMEZONE = "US/Eastern"

# Function that defines what 'pulsating' is, that being a quick on-off to give the apperance of rapid blinking
#  def start pulsating creates a function named start_pulsating that takes four parameters: 
#    bulb (the Yeelight Smart Light object), and r, g, b (the red, green, and blue color components).
#  transitions = creates a Creates a list of two RGBTransition objects:
#     The first transition sets the light to the specified color (r, g, b) over a duration of 500 milliseconds.     
#     The second transition sets the light to black (off) over the same duration, creating a pulsating effect.
#  flow = Creates a Flow object with the specified transitions. The count=0 means the pulsating effect will repeat indefinitely.
#  bulb.start_flow = Starts the flow on the bulb, making the light pulsate between the specified color and black (off) continuously.
def start_pulsating(bulb, r, g, b):
    transitions = [RGBTransition(r, g, b, duration=500), RGBTransition(0, 0, 0, duration=500)]
    flow = Flow(count=0, transitions=transitions)
    bulb.start_flow(flow)

# Function to handle retry logic for the Yeelight bulb connection.
# This function is called when a Yeelight Bulb Exception is encountered,
# and it attempts to re-establish a connection to the bulb after an error.
def handle_yeelight_error(bulb):
    print("Yeelight Bulb Exception occurred. Retrying...")
    # Print a message indicating that the Yeelight bulb encountered an error and the system will retry.
    time.sleep(10)  # Adding a delay of 10 seconds before attempting to reconnect to avoid overwhelming the system.
                    # In previous versions of the code, you would create a new Bulb instance (bulb = Bulb(BULB_IP)) every time, which could be causing issues if the instance isn't being closed properly or too many connections are being made.
    try:
        bulb.turn_off()       # Turn off the bulb before attempting to reconnect.
        bulb = Bulb(BULB_IP)  # Create a new instance of the Bulb using the same IP address. This is essentially reconnecting to the bulb, without actually creating a new instance, which can 
        bulb.turn_on()  # Ensure the bulb is on after reconnecting
    except BulbException as be:
        print("Failed to reconnect to Yeelight Bulb:", be)
        time.sleep(5)
    return bulb

# Main loop
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
                   #Connecting to the FinnHub API for the specific stock you specify
                    stock_data = finnhub_client.quote(SYMBOL)
                except Exception as e:
                    print("Error accessing Finnhub API:", e)
                    bulb.set_rgb(0, 0, 255)
                    time.sleep(5)
                    break  # Restart the script if an error occurs
                
                # Get the current stock price and previous day closing price
                current_price = stock_data['c']
                current_closing_price = stock_data['pc']

                # If this is not the first iteration of the loop
                if previous_closing_price is not None:
                    # Calculate the percent change in stock price
                    percent_change = (current_price - previous_closing_price) / previous_closing_price * 100
                    # Change the color of the Yeelight Smart Light based on the percent change in stock price
                    if percent_change >= 2.1:               
                        start_pulsating(bulb, 255, 215, 0)  # Pulsate Gold color for percent changes greater than or equal to +2.1%
                    elif percent_change > 1.5:              
                        bulb.set_rgb(255, 215, 0)           # Still Gold color for percent changes greater than +1.5%, but less than +2.1%
                    elif percent_change > 0:                
                        bulb.set_rgb(0, 255, 0)             # Still Green color for percent changes greater than +0%, but less than +1.5%
                    elif percent_change <= -2.1:            
                        start_pulsating(bulb, 128, 0, 128)  # Pulsate Purple color for percent changes greater than or equal to -2.1%
                    elif percent_change < -1.5:              
                        bulb.set_rgb(128, 0, 128)           # Still Purple color for percent changes greater than -1.5%, but less than -2.1%
                    elif percent_change < 0:                
                        bulb.set_rgb(255, 0, 0)             # Still Red color for percent changes greater than -0%, but less than -1.5%
                    else:                                   
                        bulb.set_rgb(255, 255, 255)         # Still White color for everything else, usually occurs when a change of exactly 0% as a result of current market price being the exact same as the prior day's closing market price

                    # Print current and previous closing stock prices with the current time
                    print(current_time, "Current price:", current_price)
                    print(current_time, "Previous closing price:", previous_closing_price)
                
                # Set the previous closing stock price to the current closing stock price for the next iteration
                # This allows for the previous closing price to update evry 24 hours   
                previous_closing_price = current_closing_price
                
                # Wait for 3 seconds before checking the stock price again
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

#Except command connects to Try command to tell code to print that it encountered error, then restart the code from the Try-line after 5 seconds.                 
    except BulbException as be:
        print("Yeelight Bulb Exception:", be)
        bulb = handle_yeelight_error(bulb)

    except Exception as e:
        print("Encountered error:", e)
        time.sleep(5)
        bulb.set_rgb(0, 0, 255)