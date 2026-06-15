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