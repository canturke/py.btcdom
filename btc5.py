import time
from binance.client import Client
from binance.enums import *

API_KEY = 'AsiQfZyWoQ27UV5bCo2i69enZYPth5iGdlyqldkf9AiLROPW47k0td9nRPtNVnpm'
API_SECRET = '9XV9FAOAbYOrH09sbgzS2kSW5bQgJ8XtgrgBJEzlTWvq93QdEQ2cSkanZZGVHOyV'


client = Client(API_KEY, API_SECRET)

def get_precision(symbol):
    info = client.futures_exchange_info()
    for symbol_info in info['symbols']:
        if symbol_info['symbol'] == symbol:
            return symbol_info['quantityPrecision']
    return None

def place_order(symbol, quantity, side, leverage=10):
    precision = get_precision(symbol)
    quantity = round(quantity, precision)
    # Change leverage
    client.futures_change_leverage(symbol=symbol, leverage=leverage)
    # Place order
    order = client.futures_create_order(symbol=symbol, side=side, type=ORDER_TYPE_MARKET, quantity=quantity)
    return order

def check_profit(symbol):
    profit = 0
    # Fetch all open positions
    positions = client.futures_position_information()
    for position in positions:
        if position['symbol'] == symbol and float(position['positionAmt']) != 0:
            profit += float(position['unRealizedProfit'])
    return profit

def close_positions(symbol):
    # Fetch all open positions
    positions = client.futures_position_information()
    for position in positions:
        if position['symbol'] == symbol and float(position['positionAmt']) != 0:
            # Calculate the quantity to close
            quantity = abs(float(position['positionAmt']))
            precision = get_precision(symbol)
            quantity = round(quantity, precision)
            # Define the order side (opposite to the position's side)
            side = SIDE_SELL if float(position['positionAmt']) > 0 else SIDE_BUY
            # Place a reduce only order
            try:
                client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=ORDER_TYPE_MARKET,
                    quantity=quantity,
                    reduceOnly='true')
                print(f"{symbol} position closed")
            except Exception as e:
                print(f"Error in closing {symbol}: {e}")

count = 0
while count < 10:
    # Calculate quantity in USDT
    btc_price = float(client.futures_ticker(symbol="BTCUSDT")['lastPrice'])
    btc_quantity = 100 / btc_price
    btc_dom_price = float(client.futures_ticker(symbol="BTCDOMUSDT")['lastPrice'])
    btc_dom_quantity = 110 / btc_dom_price

    # Place orders
    place_order('BTCUSDT', btc_quantity, SIDE_BUY)
    print('BTCUSDT buy order placed')
    place_order('BTCDOMUSDT', btc_dom_quantity, SIDE_BUY)
    print('BTCDOMUSDT buy order placed')

    for i in range(10):
        time.sleep(2)  # wait for 2 seconds
        btc_profit = check_profit('BTCUSDT')
        btc_dom_profit = check_profit('BTCDOMUSDT')
        total_profit = btc_profit + btc_dom_profit
        print(f'Check {i+1}: Profit: {total_profit} USDT')

        if total_profit < -0.01 or total_profit > 0.01:
            close_positions('BTCUSDT')
            close_positions('BTCDOMUSDT')
            print('Positions closed due to profit limit reached')
            break

    if i == 9:
        close_positions('BTCUSDT')
        close_positions('BTCDOMUSDT')
        print('Positions closed after 10th check')

    print('Waiting for 30 seconds to place orders again...')
    count += 1
    time.sleep(30)  # wait for 30 seconds
