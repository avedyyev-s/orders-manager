class Order:
    def __init__(self, order_id, client_name, order_price):
        self.__name = ""
        self.__price = 0
        self.__id = order_id
        self.name = client_name
        self.price = order_price
    @property
    def id(self):
        return self.__id
    @property
    def name(self):
        return self.__name
    @property
    def price(self):
        return self.__price
    @name.setter
    def name(self, new_name):
        if len(new_name.strip()) > 0:
            self.__name = new_name
    @price.setter
    def price(self, new_price):
        if new_price > 0:
            self.__price = new_price