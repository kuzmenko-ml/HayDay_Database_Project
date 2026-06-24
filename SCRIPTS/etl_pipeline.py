import pandas as pd
from sqlalchemy import create_engine
import os
from pathlib import Path

def load_base_dimensions(engine):
    print("Старт завантаження базових довідників...")
    
    data_dir = Path(__file__).resolve().parent.parent / 'DATA'

    # 1. Завантажуємо Dim_Farms
    print("Читання farms.csv...")
    farms_path = data_dir / 'farms.csv'
    df_farms = pd.read_csv(farms_path)
    # назва таблиці на сервері, з'єднання створене(місток),дописування до існуючих даниї,ігнорування індексів пандас
    df_farms.to_sql('Dim_Farms', con=engine, if_exists='append', index=False)
    print("Таблиця Dim_Farms успішно заповнена!")
    print("-----------------------------------------------")
    
    # 2. Завантажуємо Dim_Location
    print("Читання locations.csv...")
    locations_path = data_dir / 'locations.csv'
    df_locations = pd.read_csv(locations_path)
    df_locations.to_sql('Dim_Location', con=engine, if_exists='append', index=False)
    print("Таблиця Dim_Location успішно заповнена!")
    print("-----------------------------------------------")
    
    # 3. Завантажуємо Dim_Storage_Type
    print("Читання storage_types.csv...")
    types_path = data_dir / 'storage_types.csv'
    df_types = pd.read_csv(types_path)
    df_types.to_sql('Dim_Storage_Type', con=engine, if_exists='append', index=False)
    print("Таблиця Dim_Storage_Type успішно заповнена!")
    print("-----------------------------------------------")
    
    # 4. ОБРОБКА ТА ЗАВАНТАЖЕННЯ ЗАЛЕЖНОЇ ТАБЛИЦІ Dim_Storages
    print("Обробка складного довідника Dim_Storages...")
    storages_path = data_dir / 'storages.csv'
    df_storages = pd.read_csv(storages_path) # Текстовий файл (FarmName, StorageTypeName, StorageCapacity)
    
    # Витягуємо з бази актуальні ID, які SQL Server щойно згенерував для ферм та типів
    db_farms = pd.read_sql("SELECT FarmId, FarmName FROM Dim_Farms", engine)
    db_types = pd.read_sql("SELECT StorageTypeID, StorageTypeName FROM Dim_Storage_Type", engine)
    
    # Робимо MERGE, щоб замінити тексти на реальні ID з бази даних
    df_storages = df_storages.merge(db_farms, on='FarmName', how='inner')
    df_storages = df_storages.merge(db_types, on='StorageTypeName', how='inner')
    
    # Залишаємо тільки ті стовпчики, які чекає таблиця Dim_Storages в SQL Server
    df_final_storages = df_storages[['FarmId', 'StorageTypeID', 'StorageCapacity']]
    
    # Заливаємо фінальний результат у базу
    df_final_storages.to_sql('Dim_Storages', con=engine, if_exists='append', index=False)
    print("Таблиця Dim_Storages успішно заповнена з урахуванням FOREIGN KEY!")
    print("-----------------------------------------------")

def load_game_entities(engine):
    print("Старт завантаження довідників...")

    data_dir = Path(__file__).resolve().parent.parent / 'DATA'

    print("Читання buildings.csv...")
    buildings_path = data_dir / 'buildings.csv'
    df_buildings = pd.read_csv(buildings_path) 

    db_locations = pd.read_sql("SELECT LocationID, LocationName FROM Dim_Location", engine)
    df_buildings = df_buildings.merge(db_locations, on='LocationName', how='inner')

    df_final_buildings = df_buildings[[
        'BuildingName', 
        'BuildingRequiredLevel', 
        'LocationID', 
        'BuildingPrice', 
        'ConstructionTimeMinutes'
    ]]

    df_final_buildings.to_sql('Dim_Buildings', con=engine, if_exists='append', index=False)
    print("Таблиця Dim_Buildings успішно заповнена з урахуванням FOREIGN KEY!")
    print("-----------------------------------------------")


if __name__ == "__main__":
    SERVER = '.' 
    DATABASE = 'HayDay_Farm'  
    
    connection_string = f"mssql+pyodbc://@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    
    try:
        print("Підключення до сервера SQL Server...")
        engine = create_engine(connection_string)
        
        # це вже виконано
        # load_base_dimensions(engine)
        load_game_entities(engine)
        
        print("Конвеєр виконано без помилок! Перевіряй таблиці.")
        
    except Exception as e:
        print(f"Помилка виконання конвеєра: {e}")