import os
import urllib
import pandas as pd
from sqlalchemy import create_engine

# Налаштування відображення в консолі
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# --- НАЛАШТУВАННЯ ПІДКЛЮЧЕННЯ ---
SERVER_NAME = '.'
DATABASE_NAME = 'HayDay_Farm'

# Створюємо магічний місток (engine) до SQL Server
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER_NAME};"
    f"DATABASE={DATABASE_NAME};"
    f"Trusted_Connection=yes;"
)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# Шлях до файлу Excel
file_path = os.path.join('DATA', 'ПершийФайл.xlsx')

# Наш ітеративний план: спочатку працюємо лише з двома таблицями
# Ключ — вкладка в Excel, значення — таблиця в базі
mapping = {
    'Buildings': 'Dim_Building',
    'Animals': 'Dim_Animals'
}

print("=== СТАРТ ЗАВАНТАЖЕННЯ ДАНИХ ===")

try:
    # Перевіряємо наявність файлу
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Не знайдено файл за шляхом: {file_path}")

    # Цикл по наших двох таблицях
    for sheet, table in mapping.items():
        print(f"\nОбробка вкладки '{sheet}' для таблиці '{table}'...")

        # 1. Зчитуємо дані з Excel
        df = pd.read_excel(file_path, sheet_name=sheet)
        df.columns = df.columns.str.strip()

        # Виведемо перші рядки в консоль, щоб ти бачила, що процес іде
        print(f"Знайдено дані для {sheet}. Перші рядки:")
        print(df.head(2))

        # 2. Заливаємо дані в базу даних SQL Server
        # if_exists='append' — просто додає рядки в існуючу таблицю
        # index=False — не створює зайвих стовпчиків для індексів Excel
        df.to_sql(name=table, con=engine, if_exists='append', index=False)

        print(f"Успішно! Завантажено {len(df)} рядків у таблицю {table}.")

    print("\n=== ПРОЦЕС ЗАВАНТАЖЕННЯ ЗАВЕРШЕНО УСПІШНО ===")

except Exception as e:
    print(f"\nЩось пішло не так: {e}")