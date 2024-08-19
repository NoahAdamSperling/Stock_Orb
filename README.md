# The Stock Orb :chart_with_upwards_trend::crystal_ball:
The Stock Orb is a Python script that utilizes a smart bulb to create a real-time visual indicator of percent changes in stock market data (i.e., a stock market lamp) relative to the prior day's closing price. This project uses a YeeLight brand smart bulb and the financial API Finnhub.

# Materials Needed
A YeeLight brand [smart light](https://www.amazon.com/dp/B09B91X2XQ).

A spherical [light fixture](https://www.amazon.com/gp/product/B00EMBZISM/).

*Although the spherical light fixture is not needed for the light to work, it is helpful for giving the final product a more crystal ball kinda feel :crystal_ball:.*

# Script Descriptions
Stock Orb, Stock Market Version: Changes Smartlight color and patterns to reflect daily percent change in stock market data.

Stock Orb, Crypto Market Version: Changes Smartlight color and patterns to reflect percent changes in crpyto market data.

<sub>*Please note that given the limitations of data provided under the free-version of the Finnhub API, the percent changes displayed are compared to a base price that is equal to the price when the code is first ran, which then updates roughly 24 hours later to be the new price at that start time, just from the next day. This process was selected as access to historical trends of crypto data (captured in the Candles function  on Finnub) are a Premium function. Thus, this is a free work around to get the script ro run 24/7. If you are okay with the code running just during typical market hours, simply use the STOCK version of the code, and set it to a stock that tracks crpyto currencies such as "BTC-USD".*

<p align="center"> 
  Visitor count<br>
  <img src="https://profile-counter.glitch.me/NoahAdamSperling/count.svg" />
</p>
