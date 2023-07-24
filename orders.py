class Orders:
    def __init__(self, db):
        self.collection = db.get_collection("orders")

    def insert_order(self, order):
        self.collection.insert_one(order)

    # Изменение статуса заказа
    def update_order_status(self, id: str, new_status: str):
        self.collection.update_one({'_id': id}, {'$set': {'status': new_status}})
        print(f"Статус заказа {id} изменился на {new_status}")

    # Поиск новых заказов
    def find_new_orders(self):

        results = self.collection.find({"status": "Processing"})
        return list(results)

    # Подсчет средней суммы заказов
    def aggregate_order_avg_sum(self):
        return self.collection.aggregate([{"$group": {
            "_id": "order_sum",
            "average_price": {"$avg": "$total_price"}
        }}])

    #Подсчет кол-ва продаж каждого продукта
    def aggregate_order_product_count(self):
        return self.collection.aggregate([{"$group": {
            "_id": "$products",
            "total_sales": {"$sum": 1}
        }}])
