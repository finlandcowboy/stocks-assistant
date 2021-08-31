import os
def create_user(chat_id):
    os.system(f'touch {chat_id}')
    path = os.path.join(os.getcwd, f'{chat_id}')
    return path


def add_stock(chat_id, stock, price):
    f = open(f'{chat_id}', 'a')
    import datetime
    date = datetime.datetime.now()
    f.write(f'{stock} {price} {date}')


def parse_file(chat_id):
    f = open(f'{chat_id}', 'r')
    lines = f.readlines()
    data = []
    for line in lines:
        tmp = {}
        tmp['stock'] = line.split()[0]
        tmp['price'] = line.split()[1]
        tmp['date'] = line.split[2]
        data.append(tmp)

    return data

def delete_stock(chat_id, stock):
    data = parse_file(chat_id)
    f = open(f'{chat_id}', 'w')
    for d in data:
        if d['stock'] == stock:
            continue
        
        f.write(f'{d['price']} {d['price']} {d['date']}')


