class Users:
    def __init__(self, db):
        self.collection = db.get_collection("users")

    def insert_user(self, user):
        self.collection.insert_one(user)

    # Другие методы для работы с пользователями
    def update_user_city(self, id: str, new_city: str):
        self.collection.update_one({"_id": id}, {"$set": {"city": new_city}})
        print(f"Город пользователя c id = {id} успешно обновлен на {new_city}")

    def find_users_by_city(self, city):
        # Поиск пользователей по городу доставки
        return list(self.collection.find({"city": city}))

    def find_users_by_name(self, name):
        # Поиск пользователей по имени
        return list(self.collection.find({"name": name}))
