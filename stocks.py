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
