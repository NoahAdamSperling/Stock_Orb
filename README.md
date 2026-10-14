# 📈🔮 The Stock Orb 📈🔮

The Stock Orb is a Python project that turns a Yeelight smart bulb into a real-time market indicator. The script checks market quotes through the Finnhub API and changes the bulb's color and animation to reflect the selected asset's price movement.

The project includes separate scripts for stock-market-hours monitoring and cryptocurrency monitoring. It is designed as a personal, customizable hardware-and-software project, not as a trading system.

## Contents

- [What it does](#what-it-does)
- [Color guide](#color-guide)
- [How it works](#how-it-works)
- [Requirements](#requirements)
- [Setup](#setup)
- [Configure the script](#configure-the-script)
- [Run Stock Orb](#run-stock-orb)
- [Important behavior and limitations](#important-behavior-and-limitations)
- [Troubleshooting](#troubleshooting)
- [Security and disclaimer](#security-and-disclaimer)

## What it does

Stock Orb queries Finnhub for a quote, calculates a percentage change against a reference price, and translates that change into a color and, at larger moves, a pulsing pattern on a Yeelight smart bulb.

The repository's scripts are intended for two different use cases:

- **Stock script:** checks quotes during a configured weekday time window and turns the bulb off outside that window.
- **Crypto script:** checks quotes continuously, making it suitable for assets that trade around the clock. Its current reference-price logic should be reviewed before treating its colors as a true rolling 24-hour change; see [Important behavior and limitations](#important-behavior-and-limitations).

## Color guide

The current scripts use these thresholds. The comparison is based on the script's reference price, not necessarily the asset's official daily return.

| Price change | Bulb behavior |
| --- | --- |
| +2.5% or higher | 🟡/🟢 Rapidly Pulses Between Gold and Green 🟡/🟢 |
| Above +2.0% to below +2.5% | 🟡 Slowly Pulses Gold 🟡 |
| Above +1.5% to +2.0% | 🟡 Solid Gold 🟡 |
| Above +1.0% to +1.5% | 🟢 Slowly Pulses Green 🟢 |
| Above 0% to +1.0% | 🟢 Solid Green 🟢 |
| Exactly 0% | ⚪ Solid White ⚪ |
| Below 0% to -1.0% | 🔴 Solid Red 🔴 |
| Below -1.0% to -1.5% | 🔴 Slowly Pulses Red 🔴 |
| Below -1.5% to -2.0% | 🟣 Solid Purple 🟣 |
| Below -2.0% to -2.5% | 🟣 Slowly Pulses purple 🟣 |
| -2.5% or lower | 🟣/🔴Rapidly Pulses Between Purple and Red 🟣/🔴 |
| Quote/API error | 🔵 Blue is used as an error indication in the scripts' error-handling paths 🔵 |

Threshold boundaries follow the comparisons in the code. Because the conditions use a mixture of `>` and `>=`, exact boundary values can behave differently from ranges described informally in comments.

## How it works

1. **Connects to the bulb.** The script uses the `yeelight` Python package and the bulb's local IP address to send commands over the local network.
2. **Connects to Finnhub.** The `finnhub-python` client requests a quote for the ticker or symbol you enter.
3. **Calculates a change.** The script compares the current quote with the reference value used by that script.
4. **Maps the result to a light state.** RGB values represent the colors, while Yeelight `Flow` and `RGBTransition` objects create pulsing effects.
5. **Repeats.** The scripts poll approximately every three seconds during their active loops and print quote information or status messages to the terminal.
6. **Attempts recovery.** Error-handling code prints exceptions and attempts to recover from some bulb or quote errors. This is best-effort error handling, not a guarantee that the process will recover from every failure.

The thresholds on seconds for refresh, color, and stock are all fully customizable! Feel free to edit the fields to suit your needs. Theoretically, the logic should hold for different APIs, allowing you to use the script to track all sorts of things (the weather, gas prices, box office results, etc.). 

## Requirements

- Windows 10 or Windows 11 (the scripts may be adaptable to other platforms, but these instructions focus on Windows).
- Python installed and available from Command Prompt or PowerShell.
- A Yeelight bulb that supports LAN control, with the bulb and computer on the same local network.
- A Finnhub account and API key.
- Internet access for quote requests.
- A stable local IP address for the bulb is recommended. If the router changes the bulb's IP address, update the script.
- Although a spherical light fixture is not needed for the light to work, it is helpful for giving the final product a more crystal ball kinda feel 🔮.

### Python packages

The scripts import these third-party packages:

- `pytz`
- `requests`
- `yeelight`
- `finnhub-python`

The other imports (`datetime` and `time`) are part of Python's standard library and do not need to be installed separately.

## Setup

### 1. Check Python

Open PowerShell or Command Prompt and run:

```powershell
python --version
python -m pip --version
```

If `python` is not recognized, install Python from [python.org](https://www.python.org/downloads/) and enable the option to add Python to PATH during installation. On some systems, use `py` instead of `python`.

### 2. Open the project folder

Clone the repository, or download and extract it from GitHub. In PowerShell, change to the folder containing the script you want to run:

```powershell
cd path\to\Stock_Orb
```

If you cloned the repository, the folder may be named `Stock_Orb`.

### 3. (Recommended) Create a virtual environment

A virtual environment keeps this project's packages separate from other Python projects:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

If PowerShell blocks activation, you can avoid changing execution policy and invoke the environment's Python directly, for example:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

### 4. Install the dependencies

With the virtual environment activated, run:

```powershell
python -m pip install pytz requests yeelight finnhub-python
```

Or, without activating it:

```powershell
.\.venv\Scripts\python.exe -m pip install pytz requests yeelight finnhub-python
```

Install packages into the same Python environment that you use to run the script. If an import fails, a common cause is installing a package into a different Python installation.

### 5. Enable Yeelight LAN control

The bulb must allow local-network control. Use the supported Yeelight app/firmware controls for your bulb model to enable LAN control, if available. The exact menu can vary by model and firmware.

Find the bulb's current IP address in your router's connected-device list or through a network discovery tool. Confirm that the computer and bulb are on the same LAN and that the computer can reach the bulb.

In the event the Yeelight Classic app is no longer available, please use my other project  [Yeelight_Reecovery_Tool](https://github.com/NoahAdamSperling/Yeelight_Recovery_Tool) as an alternate way to connect the bulb to the internet, obtain the bulb IP, and enable and verify LAN control.

## Configure the script

Before running either script, open it in a text editor and review the configuration values near the top.

### Finnhub API key

Replace the placeholder API key with your own key:

```python
API_KEY = "YOUR_FINNHUB_API_KEY"
```

Do not commit a real API key to a public repository. If a key has already been committed publicly, revoke or rotate it through the provider.

### Bulb IP address

Replace the placeholder with the bulb's current local IP address:

```python
BULB_IP = "192.168.x.x"
```

Use the actual IP address assigned to your bulb. A DHCP reservation in your router can help prevent the address from changing.

### Select an asset

The scripts prompt you for a symbol when launched. Enter the symbol exactly as supported by Finnhub, then press Enter. Examples in the source include `VOO` for the stock script and symbols such as `BINANCE:BTCUSDT` for crypto. Provider coverage and API-plan restrictions vary; not every ticker or data endpoint is available on every Finnhub plan.

The stock script also defines `EXCHANGE = "USD"`, but the current source does not use that variable in its quote request.

### Time zone and stock monitoring window

The scripts use `US/Eastern` as their configured time zone. In the stock script, the active window is weekdays from 8:30 a.m. through 6:30 p.m. Eastern, rather than the exact official trading session. The script does not independently check exchange holidays.

## Run Stock Orb

Run the script you want from the project directory. Replace the example filenames below with the exact filenames in your local repository.

```powershell
python .\your_stock_script.py
```

For the crypto version:

```powershell
python .\your_crypto_script.py
```

If using the recommended virtual environment without activating it:

```powershell
.\.venv\Scripts\python.exe .\your_stock_script.py
```

The program runs continuously until stopped. Press **Ctrl+C** in the terminal to stop it.

### Should it be run as Administrator?

**Administrator privileges are not normally required** for Python to make internet requests or control a Yeelight over the local network. Start with a regular PowerShell or Command Prompt window.

If communication fails, running as Administrator is not a substitute for checking LAN control, IP address, network isolation, firewall rules, and Python environment. Only try an elevated terminal as a troubleshooting step if you have a specific Windows permission issue, and avoid making elevation the default.

## Important behavior and limitations

- **The light is a visual indicator, not a trading signal.** It does not place trades or account for fees, volatility, liquidity, or your investment objectives.
- **Quote availability depends on Finnhub.** Free and paid plans can differ in symbol coverage, update frequency, and endpoint access. An API key can be valid while a particular symbol or quote request is unavailable.
- **The stock script's comparison logic needs care.** It initializes `previous_closing_price` to `None`, so the first successful quote does not produce a percentage-change color decision. On subsequent loops it assigns the latest quote's `pc` value to the reference variable. Verify that this is the baseline you intend and that it matches the provider's meaning for the symbol.
- **The polling interval is approximately three seconds.** This may be faster than the update frequency of the underlying quote data and could cause unnecessary API requests. Check your provider's limits and adjust the interval as appropriate.
- **Market hours are simplified.** The stock script uses weekdays and a fixed Eastern-time window; it does not account for market holidays or special sessions.
- **Recovery is best-effort.** A persistent network problem, invalid API key, unsupported symbol, or unavailable API endpoint may require manual intervention.
- **The source includes a `requests.adapters.DEFAULT_POOL_SIZE = 100` setting.** It is a tuning attempt, not a guarantee that connection-pool issues are resolved; confirm that it is effective for your installed Requests version before relying on it.

## Troubleshooting

### `ModuleNotFoundError: No module named ...`

Install the missing package into the same Python environment used to launch the script:

```powershell
python -m pip install pytz requests yeelight finnhub-python
```

If multiple Python versions are installed, check `python --version` and `python -m pip --version`, or run both commands through `.venv\Scripts\python.exe`.

### The bulb cannot be reached

1. Confirm the bulb is powered on and LAN control is enabled.
2. Confirm the computer and bulb are connected to the same local network, not isolated guest networks.
3. Verify the bulb's current IP address in your router and update `BULB_IP`.
4. From Command Prompt, test basic reachability:

   ```powershell
   ping 192.168.x.x
   ```

   Replace the example address with the bulb's actual IP. A successful ping does not prove that Yeelight's control service is available, and a failed ping alone does not always prove the bulb is unreachable.
5. Check Windows Firewall and router/client-isolation settings. Do not broadly disable the firewall; create only a narrowly scoped rule if you have confirmed it is needed.

### Finnhub errors or a blue bulb

- Check that the API key is correct and has not been revoked.
- Confirm that the entered symbol is supported by Finnhub and by your plan.
- Check internet access, provider status, and any rate limits.
- Read the terminal exception. The blue light is only a rough error cue; use the printed message to diagnose the cause.

### The color does not match the price change

- Confirm the symbol and the reference-price behavior described above.
- Remember that the source uses threshold boundaries with strict and inclusive comparisons.
- Confirm the provider is returning current data for the selected symbol.
- For crypto, inspect and correct the mismatch between the code and the comments before interpreting the light as a rolling 24-hour return.

### The program exits or repeatedly reconnects

- Keep the terminal open so you can read the exception.
- Check the bulb's IP address and local network connection.
- Confirm all packages are installed in the correct environment.
- If the script enters a repeated error cycle, stop it with **Ctrl+C**, resolve the underlying issue, and restart it.

## Security and disclaimer

- Keep your Finnhub API key private. Do not commit it to GitHub or include it in screenshots, logs, or shared copies.
- Consider moving credentials into environment variables or a local configuration file excluded from version control.
- This is an educational/personal project and is provided as-is, without guarantees of uptime, accuracy, or fitness for a particular purpose.
- Market data can be delayed, incomplete, or unavailable. Nothing in this repository is financial advice.
