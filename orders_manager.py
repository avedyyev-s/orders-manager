import json
orders =[
    {"id": 1, "client": "ООО 'ТТК'", "price": 100_000},
    {"id": 2, "client": "ИП Аведыев С.", "price": 250_000}

]
try:
    with open("orders.json", "r", encoding="utf-8") as file:
        orders = json.load(file)
        if isinstance(orders, list):
            pass
        else:
            orders = []
except (FileNotFoundError, json.JSONDecodeError):
    orders = []

def get_all_orders():
    return orders

def add_order(client_name, order_price):
    if len(orders) == 0:
        order_id = 1
    else:
        order_id = orders[-1]['id'] + 1
    orders.append({"id": order_id, "client": client_name, "price": order_price})
    with open("orders.json", "w", encoding="utf-8") as file:
            json.dump(orders, file)

def get_total_revenue():
    total = 0
    for order in orders:
        total += order["price"]
    return total

def delete_order_by_id(order_id):
    for order in orders:
        if order["id"] == order_id:
            orders.remove(order)
            with open("orders.json", "w", encoding="utf-8") as file:
                json.dump(orders, file)
            return True
    return False

def search_orders(search_query):
    query = search_query.lower()
    orders_list = []
    for order in orders:
        if query == str(order["id"]) or query in order["client"].lower():
            orders_list.append(order)
    return orders_list

def save_backup():
    with open("orders_backup.json", "w", encoding="utf-8") as backup_file:
        json.dump(orders, backup_file)
    return True

def load_backup():
    global orders
    try:
        with open("orders_backup.json", "r", encoding="utf-8") as file:
            orders = json.load(file)
        with open("orders.json", "w", encoding="utf-8") as new_file:
            json.dump(orders, new_file)
        return True
    except (FileNotFoundError, json.JSONDecodeError):
        return False
