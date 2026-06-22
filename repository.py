import json
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