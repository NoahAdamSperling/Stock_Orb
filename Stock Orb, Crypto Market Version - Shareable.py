#Stock Orb: CRYPTO Pulsating Update - As of 19-Aug-2024#

# PLEASE READ:
        # The percent changes displayed are compared to a base price that is equal to the price when the code is first ran,
        # which then updates roughly 24 hours later to be the new price at that start time, just from the next day.
        #   This process was selected as access to historical trends of crypto data (captured in the Candles function 
        #   on Finnub) are a Premium function. Thus, this is a free work around to get the script ro run 24/7.
        #   If you are okay with the code running just during typical market hours, simply use the STOCK version
        #   of the code, and set it to a stock that tracks crpyto currencies such as "BTC-USD".
        
        # For example, this means that the closing price which is being used to compare against the current price will always be the price at
        # the time in which you began running the code (for example 5:09PM EST); thus, as the code keeps running, the comparison price
        # will get closer to that of 24 hours ago as time continues, before updating again at 5:09PM EST the next day;
        # Thus, when checking the crypto percent change, the closer you are to the start time without going over 
        # (ex: 5:08PM EST check relative to 5:09PM EST start time), regardless of day, the more accurate an approximation
        # it is to a 24 hour percent change; while conversly, when checking the crypto percent change, the closer you are 
        # to the start time when going over (ex: 5:10PM EST check relative to 5:09PM EST start time), regardless of day, 
        # the less accurate an approximation it is to a 24 hour percent change.

# Import needed packages
import datetime
import pytz
import time
from yeelight import Bulb, BulbException, Flow, RGBTransition
from finnhub import Client

# Replace with your API key
API_KEY = "Your Finnnubb API KEY"

# Replace with your Yeelight Smart Light's IP address
BULB_IP = "Your YeeLight's IP address"

# Replace with your target cryptocurrency symbol
# Another example one would be "BINANCE:ETHUSDT"
SYMBOL = "BINANCE:BTCUSDT"

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

# Main loop
try:
    # Create a new instance of the Yeelight Smart Light
    bulb = Bulb(BULB_IP)
    
    # Create a new instance of the Finnhub API client
    finnhub_client = Client(api_key=API_KEY)
    
    # Initialize previous_closing_price to None
    previous_closing_price = None
    
    # Track the last time the closing price was updated
    last_update_time = None
    
    while True:
        # Defining current_time using the date.time function from online
        current_time = datetime.datetime.now(pytz.timezone(TIMEZONE))
        
        # Fetch the current price using the correct method
        # Connecting to the FinnHub API for the specific stock you specify
        try:
            crypto_data = finnhub_client.quote(SYMBOL)
            current_price = crypto_data['c']
         # Try-Except to Catch FinnHub API error
         # Turn bulb blue for 30 seconds if this error occurs
        except Exception as e:
            print("Error accessing Finnhub API:", e)
            bulb.set_rgb(0, 0, 255)
            time.sleep(5)
            continue  # Skip to the next iteration if there's an error

        # If previous_closing_price is None, set it to current_price (this will happen on the first run)
        if previous_closing_price is None:
            previous_closing_price = current_price
            last_update_time = current_time  # Set the last update time to now
        
        # Calculate the percent change in price
        percent_change = (current_price - previous_closing_price) / previous_closing_price * 100
        
        # Apply color changes based on the percentage change
        if percent_change >= 2.1:
            start_pulsating(bulb, 255, 215, 0)  # Pulsate Gold color for percent changes greater than or equal to +2.1%
        elif percent_change > 1.5:
            bulb.set_rgb(255, 215, 0)  # Still Gold color for percent changes greater than +1.5%, but less than +2.1%
        elif percent_change > 0:
            bulb.set_rgb(0, 255, 0)  # Still Green color for percent changes greater than +0%, but less than +1.5%
        elif percent_change <= -2.1:
            start_pulsating(bulb, 128, 0, 128)  # Pulsate Purple color for percent changes greater than or equal to -2.1%
        elif percent_change < -1.5:
            bulb.set_rgb(128, 0, 128)  # Still Purple color for percent changes greater than -1.5%, but less than -2.1%
        elif percent_change < 0:
            bulb.set_rgb(255, 0, 0)  # Still Red color for percent changes greater than -0%, but less than -1.5%
        else:
            bulb.set_rgb(255, 255, 255)  # Still White color for everything else, usually occurs when a change of exactly 0% as a result of current market price being the exact same as the closing market price
                                         # Thus, code will always start white as for CRYPTO variant, the closing price value always starts at the starting price value

        # Print current and previous closing stock prices with the current time
        print(current_time, "Current price:", current_price)
        print(current_time, "Previous closing price:", previous_closing_price)

        # Update previous_closing_price every 24 hours, i.e., 86,400 seconds
        # 2 means checks every 2 seconds, 60 every 1 minute, 1800 every 30 minutes, 3600 every 1 hour , 86,400 every 24 hours 
        # This means that the closing price which is being used to compare against the current price will always be the price at
        # the time in which you began running the code (for example 5:09PM EST); thus, as the code keeps running, the comparison price
        # will get closer to that of 24 hours ago as time continues, before updating again at 5:09PM EST the next day;
        # Thus, when checking the crypto percent change, the closer you are to the start time without going over 
        # (ex: 5:08PM EST check relative to 5:09PM EST start time), regardless of day, the more accurate an approximation
        # it is to a 24 hour percent change; while conversly, when checking the crypto percent change, the closer you are 
        # to the start time when going over (ex: 5:10PM EST check relative to 5:09PM EST start time), regardless of day, 
        # the less accurate an approximation it is to a 24 hour percent change 
        
        #   This process was selected as access to historical trends of crypto data (captured in the Candles function 
        #   on Finnub) are a Premium function. Thus, this is a free work around to get the script ro run 24/7.
        #   If you are okay with the code running just during typical market hours, simply use the STOCK version
        #   of the code, and set it to a stock that tracks crpyto currencies such as "BTC-USD"       
        if last_update_time and (current_time - last_update_time).total_seconds() >= 86400:
            previous_closing_price = current_price
            last_update_time = current_time  # Update the last update time
        
        # Wait for 3 seconds before checking the price again
        time.sleep(3)

#Except command connects to Try command to tell code to print that it encountered error, then restart the code from the Try-line after 30 seconds.                 
except BulbException as be:
    print("Yeelight Bulb Exception:", be)
    time.sleep(5)
    bulb.set_rgb(0, 0, 255)
    # Reconnect to the bulb by creating a new Bulb instance
    bulb = Bulb(BULB_IP)
    bulb.turn_off() # Turn off the bulb to reset its state

except Exception as e:
    print("Encountered error:", e)
    time.sleep(5)
    bulb.set_rgb(0, 0, 255)