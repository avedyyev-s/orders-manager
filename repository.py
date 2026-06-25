import json
import psycopg2
from models import Order

class JSONRepository:
    
    def __init__(self, filepath):
        self.__filepath = filepath
    
    def save_orders(self, orders):
        raw_orders = [{"id": order.id, "client": order.name, "price": order.price} for order in orders]
        with open(self.__filepath, "w", encoding="utf-8") as file:
            json.dump(raw_orders, file)

    def load_orders(self):
        try:
            with open(self.__filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return [Order(item["id"], item["client"], item["price"]) for item in data]
        except(FileNotFoundError, json.JSONDecodeError):
            return []


class PostgreSQLRepository:
    def __init__(self, db_config):
        self.__db_config = db_config

    def save_orders(self, orders):
        pass

    def load_orders(self):
        try:
            db_connection = psycopg2.connect(**self.__db_config)
            cursor = db_connection.cursor()
            cursor.execute("SELECT * FROM orders")
            rows = cursor.fetchall()
            cursor.close()
            db_connection.close()
            return [Order(row[0], row[1], row[2]) for row in rows]
        except(psycopg2.OperationalError, Exception):
            print("Ошибка при работе с базой данных!")
            return []