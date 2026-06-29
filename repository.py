import os
import json
import psycopg2
from models import Order
from dotenv import load_dotenv

load_dotenv()

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

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

class PostgreSQLRepository:
    def __init__(self, db_config):
        self.__db_config = db_config

    def save_orders(self, orders):
        try:
            db_connection = psycopg2.connect(**self.__db_config) #Тут мы устанавливаем мост
            cursor = db_connection.cursor() #Тут получается курсор
            query_db = "INSERT INTO orders (client_name, price) VALUES (%s, %s)" #Запрос бд
            # delete_table = "TRUNCATE TABLE orders"
            # cursor.execute(delete_table)
            for order in orders:
                cursor.execute(query_db, (order.name, order.price))
            db_connection.commit()
            cursor.close()
            db_connection.close()
        except(psycopg2.OperationalError, Exception):
            print("Ошибка!")

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
    
    def delete_order(self, order_id):
        db_connection = psycopg2.connect(**self.__db_config) #Установка моста
        cursor = db_connection.cursor() #Установка курсора
        query_db = "DELETE FROM orders WHERE id = %s" #Запрос БД, пока не знаю ни каких запросов сам, как мог
        cursor.execute(query_db, (order_id,))
        db_connection.commit()
        cursor.close()
        db_connection.close()
     
    def add_order(self, order):
        db_connection = psycopg2.connect(**self.__db_config)
        cursor = db_connection.cursor()
        quary = "INSERT INTO orders (client_name, price) VALUES (%s, %s)"
        cursor.execute(quary, (order.name, order.price))
        db_connection.commit()
        cursor.close()
        db_connection.close()