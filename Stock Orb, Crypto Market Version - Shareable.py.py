#Stock Orb: CRYPTO VERSION, MutliColor Pulsating Update - As of 13-Mar-2025#

# PLEASE READ:
        # The percent changes displayed are compared to a base price that is equal to the price when the code is first ran,
        # which then updates roughly 24 hours later to be the new price at that start time, just from the next day.
        #   This process was selected as access to historical trends of crypto data (captured in the Candles function 
        #   on Finnub) are a Premium function. Thus, this is a free work around to get the script ro run 24/7.
        #   If you are okay with the code running just during typical market hours, simply use the STOCK version
        #   of the code, and set it to a stock that tracks crpyto currencies such as "GBTC".
        
        # For example, this means that the closing price which is being used to compare against the current price will always be the price at
        # the time in which you began running the code (for example 5:09PM EST); thus, as the code keeps running, the comparison price
        # will get closer to that of 24 hours ago as time continues, before updating again at 5:09PM EST the next day;
        # Thus, when checking the crypto percent change, the closer you are to the start time without going over 
        # (ex: 5:08PM EST check relative to 5:09PM EST start time), regardless of day, the more accurate an approximation
        # it is to a 24 hour percent change; while conversly, when checking the crypto percent change, the closer you are 
        # to the start time when going over (ex: 5:10PM EST check relative to 5:09PM EST start time), regardless of day, 
        # the less accurate an approximation it is to a 24 hour percent change.

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

# Replace with your target cryptocurrency symbol
# Another example one would be "BINANCE:ETHUSDT"
SYMBOL = "BINANCE:BTCUSDT"

# Replace with your timezone
TIMEZONE = "US/Eastern"

# Function that defines what 'pulsating' is, that being a quick on-off to give the apperance of rapid blinking.
#  def single pulsating creates a function named single_pulsating that switches between one color and off, taking four parameters: 
#    bulb (the Yeelight Smart Light object), and r, g, b (the red, green, and blue color components).
#  transitions = creates a Creates a list of two RGBTransition objects:
#     The first transition sets the light to the specified color (r, g, b) over a duration of 500 milliseconds.     
#     The second transition sets the light to black (off; i.e., 0,0,0 R-G-B values) over the same duration, creating a pulsating effect.
#  flow = Creates a Flow object with the specified transitions. The count=0 means the pulsating effect will repeat indefinitely.
#  bulb.start_flow = Starts the flow on the bulb, making the light pulsate between the specified color and black (off) continuously.
#  Durations of 800 and 330 are pleasant to look at speeds, for making the pulse look natural given the refresh every 3 seconds later on in code.
#  Duration 800 is slow pulse, while duration 330 is a faster pulse.
def single_pulsating(bulb, r, g, b):
    transitions = [RGBTransition(r, g, b, duration=800), RGBTransition(0, 0, 0, duration=800)]
    flow = Flow(count=0, transitions=transitions)
    bulb.start_flow(flow)

# double pulsating switches between two colors (r1, g1, b1 being the first color; r2, g2, b2 being the second color).
def double_pulsating(bulb, r1, g1, b1, r2, g2, b2):
    transitions = [RGBTransition(r1, g1, b1, duration=330), RGBTransition(r2, g2, b2, duration=330)] #r1/g1/b1 are the first color, #r2/g2/b2 are the second color. 
    flow = Flow(count=0, transitions=transitions)
    bulb.start_flow(flow)

# triple pulsating switches between three colors (r1, g1, b1 being the first color; r2, g2, b2 being the second color; r3, g3, b3 being the third color).
# Duration of 500, then 500, then 700 was choosen to make the transition between colors look more crisp and not have the rapid transition between colors make it look like other colors are there.
#   ^^For example, switching rapidly between blue and red made it look like purple was in there as well.
# tripple pulsating is not currently used in code, but added for future use if so desired.
# As such, the same, principles and formatting can be repeated to make pulsating for four, five, six, etc number of colors. 
def triple_pulsating(bulb, r1, g1, b1, r2, g2, b2, r3, g3, b3):
    transitions = [
        RGBTransition(r1, g1, b1, duration=500),  # First color
        RGBTransition(r2, g2, b2, duration=500),  # Second color
        RGBTransition(r3, g3, b3, duration=700)   # Third color
    ]
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
        bulb.turn_on()        # Ensure the bulb is on after reconnecting.
    except BulbException as be:
        print("Failed to reconnect to Yeelight Bulb:", be)
        time.sleep(5)
    return bulb

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
        if percent_change >= 2.5:               
            double_pulsating(bulb, 255, 215, 0, 0, 255, 0)    # Fast Pulsate Gold/Green for everything greater than or equal to +2.5%.
        elif percent_change > 2.5:
            single_pulsating(bulb, 255, 215, 0)               # Slow Pulsate Gold for greater than +2.0%, but less than +2.5%.
        elif percent_change > 1.5:              
            bulb.set_rgb(255, 215, 0)                         # Still Gold for percent changes greater than +1.5%, but less than +2.0%.
        elif percent_change > 1.0:
            single_pulsating(bulb, 0, 255, 0)                 # Slow Pulsate Green for percent changes greater than +1.0%, but less than 1.5%.
        elif percent_change > 0:                
            bulb.set_rgb(0, 255, 0)                           # Still Green for percent changes greater than +0%, but less than +1.0%.
        elif percent_change <= -2.5:
            double_pulsating(bulb, 255, 0, 0, 148, 0, 211)    # Fast Pulsate Purple/Red for everything greater than or equal to -2.5%.
        elif percent_change < -2.0:            
            single_pulsating(bulb, 128, 0, 128)               # Slow Pulsate Purple for greater than -2.0%, but less than -2.5%.
        elif percent_change < -1.5:              
            bulb.set_rgb(128, 0, 128)                         # Still Purple for percent changes greater than -1.5%, but less than -2.0%.
        elif percent_change < -1.0:                
            single_pulsating(bulb, 255, 0, 0)                 # Pulsate Red for percent changes greater than -1.0%, but less than -1.5%.
        elif percent_change < 0:
            bulb.set_rgb(255, 0, 0)                           # Still Red for percent changes less than -0%, but less than -1.0%.
        else:                                   
            bulb.set_rgb(255, 255, 255)                       # Still White color for everything else, usually occurs when a change of exactly 0% as a result of current market price being the exact same as the closing market price
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

# Except command connects to Try command to tell code to print that it encountered error, turn the color Blue to indiciate that an error has occured, then restart the code from the Try-line after 5 seconds.                 
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