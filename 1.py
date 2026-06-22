orders = [
    {"id": 1, "name": "Sohbet", "price": 100_000_000},
    {"id": 2, "name": "Hydyr", "price": 100_000},
    {"id": 3, "name": "Maksat", "price": 100_500},
    {"id": 4, "name": "Muhammet", "price": 500_000_000},
    {"id": 5, "name": "Begench", "price": 300_500}
]

class Order:
    def __init__(self, order_id, client_name, order_price):
        self.id = order_id
        self.name = client_name
        self.price = order_price

ordersC =[
    Order(1, "ООО 'ТТК'", 100_000),
    Order(2, "ИП Аведыев С.", 250_000)
]

for i in orders:
    print(i)
for i in ordersC:
    print(i)