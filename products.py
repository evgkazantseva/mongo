class Products:
    def __init__(self, db):
        self.collection = db.get_collection("products")

    def insert_product(self, product):
        self.collection.insert_one(product)

    # Другие методы для работы с продуктами
    def update_product_count(self, id: str, new_count: int):
        self.collection.update_one({"_id": id}, {"$set": {"quantity": new_count}})
        print(f"Количество товара c id = {id} успешно обновлено на {new_count}")

    def find_products_below_quantity(self, quantity):
        # Поиск продуктов, кол-во которых меньше указанного значения
        return list(self.collection.find({"quantity": {"$lt": quantity}}))

    def find_products_by_price_range(self, min_price, max_price):
        # Поиск продуктов по ценовому диапазону
        return list(self.collection.find({"price": {"$gte": min_price, "$lte": max_price}}))

    def find_product_by_name(self, product_name):
        # Поиск продукта по названию
        return self.collection.find_one({"name": product_name})