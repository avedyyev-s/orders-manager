import json
class Order:
    def __init__(self, order_id, client_name, order_price):
        self.id = order_id
        self.name = client_name
        self.price = order_price
orders =[
    Order(1, "ООО 'ТТК'", 100_000),
    Order(2, "ИП Аведыев С.", 250_000)
]

BACKUP_FILENAME = "orders_backup.json"
ORDERS_FILENAME = "orders.json"

# Чтение файла
try:
    with open(ORDERS_FILENAME, "r", encoding="utf-8") as file:
        orders = json.load(file)
        if isinstance(orders, list):
            orders = [Order(item["id"], item["client"], item["price"]) for item in orders]
        else:
            orders = []
except (FileNotFoundError, json.JSONDecodeError):
    orders = []

# Возварщает только начальный список orders
def get_all_orders():
    return orders

# Запись текущего списка
def save_orders_to_file():
    raw_orders = [{"id": order.id, "client": order.name, "price": order.price} for order in orders]
    with open(ORDERS_FILENAME, "w", encoding="utf-8") as file:
        json.dump(raw_orders, file)

# Добавляет заказ
def add_order(client_name, order_price):
    client_name = client_name.strip()
    if len(client_name) == 0 or order_price <= 0:
        return False
    if len(orders) == 0:
        order_id = 1
    else:
        order_id = orders[-1].id + 1
    orders.append(Order(order_id, client_name, order_price))
    save_orders_to_file()
    return True

# Возварщает общую выручку
def get_total_revenue():
    total = 0
    for order in orders:
        total += order.price
    return total

# Удаляет заказ по ID
def delete_order_by_id(order_id):
    for order in orders:
        if order.id == order_id:
            orders.remove(order)
            save_orders_to_file()
            return True
    return False

# Поиск заказа по ID или по имени клиента
def search_orders(search_query):
    query = search_query.lower()
    orders_list = []
    for order in orders:
        if query == str(order.id) or query in order.name.lower():
            orders_list.append(order)
    return orders_list

# Сохранение резервной копии
def save_backup():
    with open(BACKUP_FILENAME, "w", encoding="utf-8") as backup_file:
        raw_orders = [{"id": order.id, "client": order.name, "price": order.price} for order in orders]
        json.dump(raw_orders, backup_file)
    return True

# Загрузка резервной копии
def load_backup():
    global orders
    try:
        with open(BACKUP_FILENAME, "r", encoding="utf-8") as file:
            orders = json.load(file)
            orders = [Order(item["id"], item["client"], item["price"]) for item in orders]
        save_orders_to_file()
        return True
    except (FileNotFoundError, json.JSONDecodeError):
        return False
