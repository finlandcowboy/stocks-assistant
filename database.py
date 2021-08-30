import psycopg2
def connect_database():
    conn = psycopg2.connect(dbname='stepik', 
                            host='5.45.114.35', 
                            port=5432, 
                            user='stepik', 
                            password='F(ZNEjDJV;d<c@qTu(e8R#Rz6[_=({5S')
    cur = conn.cursor()
    return (cur, conn)

def add_user(username, chat_id):
	cur, conn = connect_database()
	query = '''insert into user_chat_id (username, chat_id) 
	select %s, %s
	where not exists (
		select username from user_chat_id where username = %s
		)'''
	cur.execute(query, (username, chat_id, username))
	conn.commit()
	cur.close()
	conn.close()

def add_stock(username, ticker, price, amount):
	cur, conn = connect_database()
	query = '''insert into user_stock (username, ticker, price, amount)
	values (%s, %s, %s, %s)
	'''
	cur.execute(query, (username, ticker, price, amount))
	conn.commit()
	cur.close()
	conn.close()

def delete_stock(username, ticker, amount):
	cur, conn = connect_database()

	query = f'''delete from user_stock where username = %s and ticker = %s and amount = %s
	'''
	cur.execute(query, (username, ticker, amount))
	conn.commit()
	cur.close()
	conn.close()

def get_stocks(username):
	cur, conn = connect_database()
	query = '''select ticker from user_stock where username = %s'''
	cur.execute(query, (username,))
	res = [x[0] for x in cur.fetchall()]
	print('Fetch:', res)
	cur.close()
	conn.close()
	return res 


def get_users():
	cur, conn = connect_database()

	query = 'select * from user_chat_id'

	cur.execute(query)
	fetch = cur.fetchall()
	cur.close()
	conn.close()
	return fetch