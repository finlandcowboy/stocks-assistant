import telebot
import stocks
import database
token = '1686246223:AAFpGIs77TFZ89QErNnq65yTqzN7ULORvNQ'

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def greeting_command(message):
    text = f'''Hello {message.from_user.username}!
I\'m your stocks assistant bot.
I can help you to manage your stocks portfolio.

Here\'s something of what I can do.
Show you realtime prices of your stocksW
Predict the price of your stocks for a week
Notify you when you might want to sell stocks

For more help and commands /help

Created by @yungstepik'''
    database.add_user(message.from_user.username, message.chat.id)
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help'])
def help_command(message):
    text = '''<b>Commands</b>
/add - Add stock
/delete - Delete Stock (if you sell it or smth)
/list - List your stocks 
/predict - Predict your stock value for desirable amount of time 
/set_percent - Set percent for notifying you about growth'''
    bot.send_message(message.chat.id, text, parse_mode='html')


adding_stock_args = []
@bot.message_handler(commands=['add'])
def command_add(message):
    text = 'Enter a *ticker* (not a company name)'
    msg = bot.send_message(message.chat.id, text, parse_mode='Markdown')
    bot.register_next_step_handler(msg, adding_ticker)
    
def adding_ticker(message):
    if stocks.found_ticker(message.text):
        adding_stock_args.append(message.text)
        text = 'Enter a price in *USD $$*'
        msg = bot.send_message(message.chat.id, text, parse_mode='Markdown')
        bot.register_next_step_handler(msg, adding_price)
    else:
        text = "Ticker not found.\nYou can find a correct ticker <a href='finance.yahoo.com'>here</a>"
        msg = bot.send_message(message.chat.id, text, parse_mode='html')
        bot.register_next_step_handler(msg, command_add)


def adding_price(message):
    try:
        price_input = float(message.text.replace(',', '.'))
        adding_stock_args.append(price_input)
        text = 'Enter **amount** of stock you bought'
        msg = bot.send_message(message.chat.id, text, parse_mode='Markdown')
        bot.register_next_step_handler(msg, adding_amount)
    except:
        text = "Wrong input price.\nPlease try again"
        msg = bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(msg, adding_ticker)

    
def adding_amount(message):
    try:
        adding_stock_args.append(int(message.text))
        print(adding_stock_args)
        text = f'Alright, added a {adding_stock_args[0]} in amount of {adding_stock_args[2]} and sum price: {round(float(adding_stock_args[2]) * float(adding_stock_args[1]),2)}'
        
        database.add_stock(message.from_user.username, adding_stock_args[0], adding_stock_args[1], adding_stock_args[2])
        bot.send_message(message.chat.id, text)
        adding_stock_args.clear()
    except:
        text = "Amount must be an integer. E.g. 10, 5, 1, 100.\nPlease, try again."
        msg = bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(msg, adding_price)

delete_stock_args = []    
@bot.message_handler(commands=['delete'])
def command_delete(message):
    text = "What's ticker you want to sell?"
    msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(msg, delete_ticker)

    
def delete_ticker(message):
    delete_stock_args.append(message.text)
    amount = 0
    '''
    Query to get amount of stocks by ticker form database
    '''
    text = 'How many stocks you want to sell?\nRight now you have ' + str(amount)
    msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(msg, delete_amount)

def delete_amount(message):
    '''
    Add try catch if input isnt int 
    '''
    
    delete_stock_args.append(int(message.text))
    database.delete_stock(message.from_user.username, 
                            delete_stocks_args[0],
                            delete_stock_args[1]    
                        )
    bot.send_message(message.chat.id, f'Okay, I sold {delete_stock_args[0]}\nIn amount of {delete_stock_args[1]}')
    


@bot.message_handler(commands=['list'])
def command_list(message):
    '''
    Get list of tickers with current prices by API and database
    '''
    
    stocks_list = database.get_stocks(message.from_user.username)
    print(stocks_list)
    if not stocks_list:
        bot.send_message(message.chat.id, 'You need to add stocks before you can list them')

    else:
        text = '<b>Your stocks list</b>'
        for stock in stocks_list:
            price = stocks.get_current_price(stock)
            text += f'\n{stock} {price}' 
        
        bot.send_message(message.chat.id, text, parse_mode='html')
    
@bot.message_handler(commands=['set_percent'])
def command_set_percent(message):
    '''
    Get users percent to notify him
    '''
    text = "From what's percent of stock growth you want to be notified? Enter a number."
    msg = bot.send_message(message.chat.id, text)
    
    bot.register_next_step_handler(msg, set_percent_percent)

def set_percent_percent(message):
    '''
    Query to nisert percent to user_id (table user_percent)
    '''
    text = f'Your {message.text}% percent notifications is set'
    bot.send_message(message.chat.id, text)
    
@bot.message_handler(commands=['chatid'])
def command_chatid(message):
    bot.send_message(message.chat.id, message.chat.id)
    
plot_args = []
@bot.message_handler(commands=['plot'])
def command_plot(message):
    text = 'Enter a ticker for a plot'
    msg = bot.send_message(message.chat.id, message.chat.id)
    bot.register_next_step_handler(msg, plot_adding_ticker)
    
def plot_adding_ticker(message):
    text = 'Enter an interval for a plot.\nE.g. 1 week, 7 day, 1 year, 1 month'
    plot_args.append(message.text)
    msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(msg, plot_adding_interval)
    
def plot_adding_interval(message):
    plot_args.append(message.text)
    bot.send_chat_action(message.chat.id, 'upload_photo')
    
    bot.send_message(message.chat.id,f'Plot ticker: {plot_args[0]} with interval {plot_args[1]}')
    plot = plot_stock(plot_args[0], plot_args[1])
    bot.send_photo(message.chat.id, plot)
    
from threading import Thread
import schedule, time
from datetime import datetime

def stocks_info():
    users_info = database.get_users()
    date = str(datetime.now().day) + '.' + str(datetime.now().month)
    for user, chat_id in users_info:
        stocks_list = database.get_stocks(user)
        text = f'<b>{date} UPDATED</b>\nYour stocks list right now'
        for stock in stocks_list:
            price = stocks.get_current_price(stock)
            text += f'\n{stock} {price}' 
        text += '\n\n<b>Have a good day</b>'
        bot.send_message(chat_id, text, parse_mode='html')

def main_loop():
    thread = Thread(target=do_schedule)
    thread.start()
    bot.polling(True)

def do_schedule():
    schedule.every().day.at("11:00").do(stocks_info)

    while True:
        schedule.run_pending()
        time.sleep(1)

main_loop()