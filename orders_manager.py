import json
from models import Order
from repository import JSONRepository
from repository import PostgreSQLRepository, DB_CONFIG

orders =[
    Order(1, "ООО 'ТТК'", 100_000),
    Order(2, "ИП Аведыев С.", 250_000)
]

BACKUP_FILENAME = "orders_backup.json"

order_repo = PostgreSQLRepository(DB_CONFIG)
backup_repo = JSONRepository(BACKUP_FILENAME)

# Чтение файла
orders = order_repo.load_orders()


# Возварщает только начальный список orders
def get_all_orders():
    return orders

# Запись текущего списка
def save_orders_to_file():
    order_repo.save_orders(orders)

# Добавляет заказ
def add_order(client_name, order_price):
    global orders
    client_name = client_name.strip()
    if len(client_name) == 0 or order_price <= 0:
        return False
    orders.append(Order(0, client_name, order_price))
    save_orders_to_file()
    orders = order_repo.load_orders()
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
    backup_repo.save_orders(orders)
    return True

# Загрузка резервной копии
def load_backup():
    global orders
    try:
        orders = backup_repo.load_orders()
        save_orders_to_file()
        return True
    except (FileNotFoundError, json.JSONDecodeError):
        return False
