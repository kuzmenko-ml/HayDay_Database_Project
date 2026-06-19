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
