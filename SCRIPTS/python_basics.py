import datetime
import random

print("працює")
print("---------------------------")
farm_name = "Super Cow Farm"

farm_level = 27

milk_price = 4.50

is_active = True

print("name of my farm:")
print(farm_name)
print("---------------------------")
print("level of my farm:")
print(farm_level)
print("---------------------------")

milk_bottles = 10     
price_per_bottle = 4.5 

total_earned = milk_bottles * price_per_bottle

print("Всього зароблено монет:")
print(total_earned)
print("---------------------------")

first_name = "Корова"
last_name = "Мурка"

full_name = first_name + " " + last_name

print("Ім'я нашої тваринки:")
print(full_name)
print("---------------------------")

farm_level = 28

if farm_level >= 30:
    print("Доступно нове обладнання: Цукровий завод!")
    print("---------------------------")
elif farm_level >= 20:
    print("Доступно нове обладнання: Ткацький станок!")
    print("---------------------------")
else:
    print("Нове обладнання недоступне. Качайте рівень.")
    print("---------------------------")

player_coins = 500
has_free_space = True

if player_coins >= 450 and has_free_space:
    print("Ви можете купити нову корову!")
    print("---------------------------")

order_product = "Попкорн"
product_quantity = 5

player_popcorn_stock = 5

print("Перевірка замовлення...")

if player_popcorn_stock >= product_quantity:
    print("Замовлення виконано! Ви отримали монети та досвід.")
    print("---------------------------")
else:
    missing = product_quantity - player_popcorn_stock
    print("Недостатньо товару на складі.")
    print("Вам не вистачає одиниць попкорну в кількості:")
    print(missing)
    print("---------------------------")

for i in range(5):
    print("Ітерація №:")
    print(i)
    print("---------------------------")

products = ["Пшениця", "Кукурудза", "Цукор"]

for prod in products:
    print("Гравець збирає врожай:")
    print(prod)
    print("---------------------------")

silo_space = 0 
max_capacity = 3 

while silo_space < max_capacity:
    print("Додаємо мішок зерна в амбар...")
    silo_space = silo_space + 1 
    print("Поточна завантаженість амбару:")
    print(silo_space)
    print("---------------------------")

print("Амбар заповнено!")
print("---------------------------")

new_players_ids = [101, 102, 103, 104]
daily_bonus_coins = 50

print("--- Старт обробки черги гравців ---")

for player_id in new_players_ids:
    print("Підключаємось до бази даних...")
    print("Нараховуємо бонус для Player_ID:")
    print(player_id)
    
    print("Успішно додано " + str(daily_bonus_coins) + " монет.")
    print("---------------------------------")

print("--- Обробку всієї пачки завершено! ---")
print("---------------------------")

def calculate_total_price(quantity, price_per_unit):
    total = quantity * price_per_unit
    return total 

final_cost = calculate_total_price(10, 4.5)

print("Результат роботи функції:")
print(final_cost)
print("---------------------------")

def get_farm_stats():
    level = 42
    rating = 4.9
    return level, rating

current_level, current_rating = get_farm_stats()
print(current_level,current_rating)
print("---------------------------")

def check_order_status(stock, required):
    if stock >= required:
        return "READY"
    else:
        return "NOT_ENOUGH"

orders = [3, 12, 5, 8] 
my_current_stock = 7  

print("--- ЗАПУСК СКРИПТА ПЕРЕВІРКИ ЗАМОВЛЕНЬ ---")

for order in orders:
    status = check_order_status(my_current_stock, order)
    
    print("Замовлення на кількість " + str(order) + " шт. Статус: " + status)

print("--- ПЕРЕВІРКУ ЗАВЕРШЕНО ---")
print("---------------------------")
orders_queue = [12, 5, 8]
orders_queue.append(20)

print("Поточна черга замовлень:")
print(orders_queue)

total_orders = len(orders_queue)
print("Всього замовлень в черзі: " + str(total_orders))

first_order = orders_queue[0]
print("Перше замовлення на перевірку: " + str(first_order))
print("---------------------------")

mill_status = {
    "building_name": "Млин №1",
    "slots_total": 3,
    "is_working": False
}

print("--- Початковий стан млина ---")
print(mill_status)

mill_status["is_working"] = True

mill_status["current_product"] = "Борошно"

print("\n--- Оновлений стан млина ---")
print("Назва будівлі: " + mill_status["building_name"])
print("Що виробляє: " + mill_status["current_product"])
print("Чи працює зараз? " + str(mill_status["is_working"]))
print("---------------------------")

factories_table = [
    {"name": "Цукровий завод", "level_required": 7, "is_built": True},
    {"name": "Ткацький станок", "level_required": 16, "is_built": True},
    {"name": "Пекарня", "level_required": 2, "is_built": False},
    {"name": "Шахта", "level_required": 24, "is_built": False}
]

print("--- АНАЛІЗ СТАНУ БУДІВЕЛЬ НА ФЕРМІ ---")

for factory in factories_table:
    if not factory["is_built"]:
        print("Будівлю '" + factory["name"] + "' потрібно побудувати!")
        print("Вона стане доступна на рівні: " + str(factory["level_required"]))
        print("---------------------------------")

print("--- АНАЛІЗ ЗАВЕРШЕНО ---")
print("---------------------------------")

total_gold = 5000
active_players = 0 

print("--- Спроба розрахувати бонус ---")

try:
    gold_per_player = total_gold / active_players
    print("Кожен гравець отримує: " + str(gold_per_player))
    
except ZeroDivisionError:
    print("Помилка! Кількість активних гравців дорівнює нулю.")
    print("Нарахування бонусу перенесено на завтра.")

print("--- Скрипт продовжив роботу без аварійного завершення! ---")
print("---------------------------------")
current_time = datetime.datetime.now()

print("Поточна дата та час на комп'ютері:")
print(current_time)
print("---------------------------------")
print("--- ЗАПУСК СИСТЕМИ МОНІТОРИНГУ ХЕЙДЕЙ ---")

online_players = random.randint(500, 1000)

timestamp = datetime.datetime.now().strftime("%H:%M:%S")

print("[" + timestamp + "] Поточний онлайн: " + str(online_players) + " гравців.")

print("--- МОНІТОРИНГ ЗАВЕРШЕНО УСПІШНО ---")
