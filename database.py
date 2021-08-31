import psycopg2
 
 
import sys
# make normal sys open database config look into instagram python example)
 
def connect_database():
	conn = psycopg2.connect()
	cur = conn.cursor
	return cur
 
 
def add_user(username, chat_id):
	cur = connect_database()
	query = 'insert into users (username, chat_id) values (%s, %s)'
	cur.execute(query, username, chat_id)
 
 
def user_stock_add(username, ticker, price, amount):
 
	cur = connect_database()
 
	query = "insert into user_stock (username, ticker, price, amount, date) values (%s, %s, %s, %s, today())"
	cur.execute(query, username, ticker, price, amount)
 
def user_stock_delete(username, ticker):
	pass
    