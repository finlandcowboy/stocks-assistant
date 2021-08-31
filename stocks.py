<<<<<<< HEAD
import yfinance as yf
 
def get_current_price(ticker):
	try:
		tickerData = yf.Ticker(ticker)
		ticker_close_price = round(tickerData.history(history="1m").iloc[0].Close,2)
		return ticker_close
	except:
		print("Your ticker isnt found on the stock market (NASQAD)")
		return None	
 
def get_stock_plot(ticker, period):
	import re
	history_digit=re.match([0-9], period)
	# find day, week, year, minute, hour,month
	history_period= ''
	history = '''
 
	ADD PARSING ANSWER FROM PERIOD INPUT TO HISTORY FORMAT
	'''
 
	tickerData = yf.Ticker(ticker)
	tickerDf = tickerData.history(history=history)		
	#add candle plot from matplot lib
=======
import uuid

import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
from mpl_finance import candlestick_ochl
import mpl_finance as mpf

def found_ticker(ticker):
    try: 
        yf.Ticker(ticker)
        return True
    except:
        return False

def get_current_price(ticker) -> float:
    price = 0
    if found_ticker():
        tickerData = yf.Ticker(ticker)
        if tickerData.info['currency'] == 'RUB':
            import numpy as np
            from currency_converter import CurrencyConverter
            c = CurrencyConverter()
            price = np.round(c.convert(tickerData.history('1d').iloc[0].Close, 'RUB', 'USD'), 2)
        else:
            price = np.round(tickerData.history(history='7d', history_input='2m').iloc[0].Close, 2)
        return price
    else:
        return 'Ticker not found'


    
'''
import finplot as fplt 
    
def save():
    fplt.screenshot(open(filename, 'wb'))
    
from io import BytesIO
def plot_stock(history_input, ticker):
    tickerData = yf.Ticker(ticker)
    history_inputs = ['week', 'day', 'month', 'year']
    for inter in history_inputs:
        if inter in history_input:
            history_input_args = history_input.split()
            history = ''
            for arg in history_input_args:
                try:
                    int(arg)
                    history += arg
                except:
                    history += arg[0]
            plt.style.use('ggplot')
            tickerDf = tickerData.history(period=history, interval='5m')
            tickerDf = tickerDf.rename(columns={'index':'Datetime', 'Date':'Datetime'})
            import uuid
            filename = uuid.uuid1().hex + '.png'
            print(f'Filename: {filename}')


            
            fplt.candlestick_ochl(tickerDf[['Open', 'Close', 'High', 'Low']])
            fplt.timer_callback(save, seconds=0.5, single_shot=True)
            fplt.show()
            fplt.close()
            import os
            if filename in os.listdir():
                print('File saved')
                return filename
            else:
                print('Error: File not saved')
             '''           
>>>>>>> 8e8ef2ef7bfc3098cec4858f954149463c7bc888
