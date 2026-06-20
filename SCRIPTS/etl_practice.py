import pandas as pd

def elt_practice():
    raw_factories = [
    {"factory_id": 1, "name": "Пекарня", "level": 2},
    {"factory_id": 2, "name": "Цукровий завод", "level": 7},
    {"factory_id": 3, "name": "Попкорн-машина", "level": 8}
    ]
    
    df_factories = pd.DataFrame(raw_factories)

    print("--- НАША ПЕРША ТАБЛИЦЯ В PANDAS ---")
    print(df_factories)
    print("----------------------------------------")

    print("\n--- АНАЛОГ SQL: SELECT name FROM table ---")
    print(df_factories["name"])
    print("----------------------------------------")

    print("\n--- АНАЛОГ SQL: SELECT name, level FROM table ---")
    print(df_factories[["name", "level"]])
    print("----------------------------------------")

    # --- ФІЛЬТРАЦІЯ РЯДКІВ ---

    high_level_factories = df_factories[df_factories["level"] > 5]
    print(high_level_factories)

    a = df_factories[df_factories["name"] == "Пекарня"]
    print(a)

    filtered_df = df_factories[(df_factories["level"] > 2) & (df_factories["level"] < 8)]
    print(filtered_df)

    # --- ЧИТАННЯ ФАЙЛІВ З ДИСКУ ---
    path = r'D:\HayDay_Database_Project\DATA\експеремент.csv'
    df = pd.read_csv(path)

    print("--- МИ ЗЧИТАЛИ ДАНІ З РЕАЛЬНОГО ФАЙЛУ ---")
    print(df)
    print("----------------------------------------\n")
    print("--- ВІДФІЛЬТРУВАЛИ ---")
    filtered_df = df[df["quantity"] > 120]
    print(filtered_df)

    output_path = r'D:\HayDay_Database_Project\DATA\результат.csv'
    filtered_df.to_csv(output_path, index=False)
    print("Супер! Новий файл 'результат.csv' успішно створено на диску D.")

    print(df.isna().sum())
    df["product"] = df["product"].fillna("Невідомий продукт")
    df["quantity"] = df["quantity"].fillna(0)
    print("--- ТАБЛИЦЯ ПІСЛЯ ОЧИЩЕННЯ ---")
    print(df)

def practice_stage_IO():
    print("=== ЕТАП INPUT/OUTPUT (ВВЕДЕННЯ/ВИВЕДЕННЯ) ===")
    # 1. ГОЛОВНИЙ EXTRACT: Зчитуємо файл
    path = r'D:\HayDay_Database_Project\DATA\експеремент.csv'
    df = pd.read_csv(path)
    print("\n1. Дані успішно зчитано з файлу. Ось перші рядочки:")
    print(df.head(2))

    # 2. МАГІЯ БУФЕРА ОБМІНУ (clipboard):       
    print("\n2. Пробуємо зчитати те, що скопійовано в буфері обміну (Ctrl+C):")
    try:
        df_clipboard = pd.read_clipboard(sep=',') 
        print(df_clipboard)
    except Exception as e:
        print("Буфер обміну порожній або там не табличні дані. Скопіюй щось через Ctrl+C!")

    # 3. ФІНАЛЬНИЙ LOAD: Зберігаємо копію в інший файл
    output_path = r'D:\HayDay_Database_Project\DATA\тест_виведення.csv'
    df.to_csv(output_path, index=False)
    print(f"\n3. Дані успішно переписано у новий файл: {output_path}")

def practice_stage_summarize_data():
    path = r'D:\HayDay_Database_Project\DATA\експеремент.csv'
    df = pd.read_csv(path)
    print(df)
    print('---------------------')
    print(df['product'].value_counts())
    print('---------------------')
    print(len(df))
    print('---------------------')
    print(df.shape)
    print('---------------------')
    print(df['factory_id'].nunique())
    print('---------------------')
    print(df.describe()) # можна писати без прінта
    print('---------------------')
    print(df.info()) # можна писати без прінта
    print('---------------------')
    print(df.memory_usage())
    print('---------------------')
    print(df.dtypes)
    print('---------------------')

    print(df['quantity'].sum())
    print(df['quantity'].count())
    print(df['quantity'].median())
    print(df['quantity'].min())

def practice_stage_handling_missing_data():
    print("=== ЕТАП HANDLING MISSING DATA (ОЧИЩЕННЯ) ===")
    path = r'D:\HayDay_Database_Project\DATA\експеремент.csv'
    df = pd.read_csv(path)
    print("1. ОРИГІНАЛЬНА ТАБЛИЦЯ (із дірками NaN):")
    print(df)
    print("----------------------------------------\n")

    # --- ВАРІАНТ А: Спробуємо видалити рядки з NaN ---
    df_dropped = df.dropna()
    print("2. ВАРІАНТ А: Таблиця після df.dropna() (рядки з NaN зникли):")
    print(df_dropped)
    print(f"Було рядків: {len(df)}, стало: {len(df_dropped)}")
    print("----------------------------------------\n")

    # --- ВАРІАНТ Б: Замінимо пустоти на конкретні значення ---
    # Можна замінити все разом: df_filled = df.fillna(0)
    # Але крутіше очистити кожен стовпець своїм логічним значенням:
    df_clean = df.copy() # робимо копію для очищення
    df_clean["product"] = df_clean["product"].fillna("Невідомий продукт")
    df_clean["quantity"] = df_clean["quantity"].fillna(0)

    print("3. ВАРІАНТ Б: Таблиця після точкового df.fillna():")
    print(df_clean)
    print("----------------------------------------\n")



