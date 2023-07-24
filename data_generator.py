from faker import Faker


class FakerDataGenerator:
    def __init__(self, db):
        self.db = db
        self.fake = Faker()

    def generate_product(self):
        product = {
            "name": self.fake.word(),
            "price": self.fake.random_int(min=10, max=100),
            "description": self.fake.sentence(),
            "category_id": self.fake.random_int(min=1, max=5),
            "sizes": [self.fake.random_element(["S", "M", "L"])],
            "colors": [self.fake.color_name()],
            "image_url": self.fake.image_url(),
            "quantity": self.fake.random_int(min=0, max=50)
        }
        products_collection = self.db.get_collection("products")
        products_collection.insert_one(product)

    def generate_order(self):
        products_collection = self.db.get_collection("products")
        users_collection = self.db.get_collection("users")

        product_ids = products_collection.distinct("_id")
        user_ids = users_collection.distinct("_id")

        order = {
            "user_id": self.fake.random_element(user_ids),
            "products": [self.fake.random_element(product_ids)],
            "count": self.fake.random_int(min=0, max=50),
            "total_price": self.fake.random_int(min=100, max=1000),
            "status": self.fake.random_element(["Processing", "Shipped", "Delivered"])
        }
        orders_collection = self.db.get_collection("orders")
        orders_collection.insert_one(order)

    def generate_user(self):
        user = {
            "name": self.fake.name(),
            "email": self.fake.email(),
            "password": self.fake.password(),
            "phone": self.fake.phone_number(),
            "country": self.fake.country(),
            "city": self.fake.city(),
            "address": self.fake.address()
        }
        users_collection = self.db.get_collection("users")
        users_collection.insert_one(user)

    def generate_order_with_params(self, product_id, count):
        users_collection = self.db.get_collection("users")

        user_ids = users_collection.distinct("_id")

        order = {
            "user_id": self.fake.random_element(user_ids),
            "products": [product_id],
            "count": count,
            "total_price": self.fake.random_int(min=100, max=1000),
            "status": "New"
        }
        orders_collection = self.db.get_collection("orders")
        orders_collection.insert_one(order)
