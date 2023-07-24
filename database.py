import pymongo

class Database:
    def __init__(self):
        # Подключение к серверу MongoDB
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        # Получение базы данных
        self.database = self.client["eCommerceDB"]

    def get_collection(self, collection_name):
        # Получение коллекции по имени
        return self.database[collection_name]

    def create_index(self, collection_name, field):
        # Создание индексов
        self.get_collection(collection_name).create_index(field)