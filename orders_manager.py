import json
orders =[
    {"id": 1, "client": "ООО 'ТТК'", "price": 100_000},
    {"id": 2, "client": "ИП Аведыев С.", "price": 250_000}

]
BACKUP_FILENAME = "orders_backup.json"
ORDERS_FILENAME = "orders.json"

# Чтение файла
try:
    with open(ORDERS_FILENAME, "r", encoding="utf-8") as file:
        orders = json.load(file)
        if isinstance(orders, list):
            pass
        else:
            orders = []
except (FileNotFoundError, json.JSONDecodeError):
    orders = []

# Возварщает только начальный список orders
def get_all_orders():
    return orders

# Запись текущего списка
def save_orders_to_file():
    with open(ORDERS_FILENAME, "w", encoding="utf-8") as file:
        json.dump(orders, file)

# Добавляет заказ
def add_order(client_name, order_price):
    if len(orders) == 0:
        order_id = 1
    else:
        order_id = orders[-1]['id'] + 1
    orders.append({"id": order_id, "client": client_name, "price": order_price})
    save_orders_to_file()

# Возварщает общую выручку
def get_total_revenue():
    total = 0
    for order in orders:
        total += order["price"]
    return total

# Удаляет заказ по ID
def delete_order_by_id(order_id):
    for order in orders:
        if order["id"] == order_id:
            orders.remove(order)
            save_orders_to_file()
            return True
    return False

# Поиск заказа по ID или по имени клиента
def search_orders(search_query):
    query = search_query.lower()
    orders_list = []
    for order in orders:
        if query == str(order["id"]) or query in order["client"].lower():
            orders_list.append(order)
    return orders_list

# Сохранение резервной копии
def save_backup():
    with open(BACKUP_FILENAME, "w", encoding="utf-8") as backup_file:
        json.dump(orders, backup_file)
    return True

# Загрузка резервной копии
def load_backup():
    global orders
    try:
        with open(BACKUP_FILENAME, "r", encoding="utf-8") as file:
            orders = json.load(file)
        save_orders_to_file()
        return True
    except (FileNotFoundError, json.JSONDecodeError):
        return False
