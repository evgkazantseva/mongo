from database import Database
from data_generator import FakerDataGenerator
from orders import Orders
from products import Products
from users import Users
from bson import ObjectId

db = Database()


# Генерация фейковых данных и вставка их в базу данных
def generate_data(db, count):
    data_generator = FakerDataGenerator(db)
    for _ in range(count):
        data_generator.generate_product()
        data_generator.generate_user()
        data_generator.generate_order()

#Создание индексов на БД
def create_indexes(db):
    db.create_index('orders', 'status')
    db.create_index('products', 'quantity')
    db.create_index('products', 'price')
    db.create_index('products', 'name')
    db.create_index('users', 'city')
    db.create_index('users', 'name')

#Функция, для демонстрации поиска в БД
def find_entities(db):
    choice = int(input("Выберите вариант поиска:\n"
                       "1. Поиск новых заказов\n"
                       "2. Поиск продуктов, кол-во которых меньше, чем\n"
                       "3. Поиск продуктов по цене\n"
                       "4. Поиск продукта по названию\n"
                       "5. Поиск пользователей по городу доставки\n"
                       "6. Поиск пользователей по имени\n"
                       "0. Выход\n"))
    if choice == 1:
        order = Orders(db)
        print(order.find_new_orders())
    elif choice == 2:
        product = Products(db)
        print(product.find_products_below_quantity(10))
    elif choice == 3:
        product = Products(db)
        print(product.find_products_by_price_range(10, 50))
    elif choice == 4:
        product = Products(db)
        print(product.find_product_by_name('choice'))
    elif choice == 5:
        user = Users(db)
        print(user.find_users_by_city("New York"))
    elif choice == 6:
        user = Users(db)
        print(user.find_users_by_name("John Doe"))
    elif choice == 0:
        return False
    else:
        print("Некорректный выбор. Пожалуйста, повторите.")

#Функция для демонстрации агрегации данных
def agregate_data(db):
    choice = int(input("Выберите агрегацию:\n"
                       "1. Общее количество продаж каждого продукта\n"
                       "2. Средняя стоимость заказов\n"))
    if choice == 1:
        order = Orders(db)
        print(list(order.aggregate_order_product_count()))
    elif choice == 2:
        order = Orders(db)
        print(list(order.aggregate_order_avg_sum()))
    elif choice == 0:
        return False
    else:
        print("Некорректный выбор. Пожалуйста, повторите.")

#Функция для демонстрации изменения данных
def update_data(db):
    choice = int(input("Выберите объект для обновления:\n"
                       "1. Обновить остаток продуктов на складе\n"
                       "2. Обновить статус заказа\n"
                       "3. Обновить город пользователя\n"))
    if choice == 1:
        products = Products(db)
        product_id = input("Введите ID продукта: ")
        product_count = input("Введите остаток продукта на складе: ")
        products.update_product_count(ObjectId(product_id), product_count)
    elif choice == 2:
        orders = Orders(db)
        order_id = input("Введите ID заказа: ")
        new_status = input("Введите новый статус заказа: ")
        orders.update_order_status(ObjectId(order_id), new_status)
    elif choice == 3:
        users = Users(db)
        user_id = input("Введите ID пользователя: ")
        new_city = input("Введите новый город доставки: ")
        users.update_user_city(ObjectId(user_id), new_city)
    elif choice == 0:
        return False
    else:
        print("Некорректный выбор. Пожалуйста, повторите.")

#Функция-демонстранция реализации "транзакций": добавление продукта в уже существующий заказ
def transaction_view(db):
    products = Products(db)
    product_name = input("Введите название продукта: ")
    product_count = int(input("Введите кол-во заказываемого продукта: "))
    product = products.find_product_by_name(product_name)


    if not product:
        return "Product doesn't exist"

    if product['quantity'] == 0:
        return "Товара нет на складе"
    elif product['quantity'] < product_count:
        return "Такого кол-ва товара нет на складе"
    else:
        products.update_product_count(product['_id'], product['quantity']-product_count)
        data_generator = FakerDataGenerator(db)
        data_generator.generate_order_with_params(product['_id'], product_count)
        return "Заказ создан"


if __name__ == "__main__":
    while True:
        choice = input("Для вывода меню введите help. Для выхода - 0\n")

        if choice == "1":
            count = int(input('Введите кол-во генерируемых данных: '))
            generate_data(db, count)
            print("Данные успешно сгенерированы")
        elif choice == "2":
            create_indexes(db)
            print("Индексы успешно созданы")
        elif choice == "3":
            find_entities(db)
        elif choice == "4":
            agregate_data(db)
        elif choice == "5":
            update_data(db)
        elif choice == "6":
            transaction_view(db)
        elif choice == "0":
            break
        elif choice == "help":
            print("Меню:\n"
                  "1. Генерация данных\n"
                  "2. Формирование индексов\n"
                  "3. Поиск данных\n"
                  "4. Агрегация данных\n"
                  "5. Внесение изменений в данные\n"
                  "6. Работа с транзакциями\n"
                  "0. Выход\n")
        else:
            print("Некорректный выбор. Пожалуйста, повторите.")
