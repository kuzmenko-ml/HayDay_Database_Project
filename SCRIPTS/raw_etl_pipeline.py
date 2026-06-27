import pandas as pd
from sqlalchemy import create_engine
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
    print("----------------------------------------------------------------------------------")
    
    # 2. Завантажуємо Dim_Location
    print("Читання locations.csv...")
    locations_path = data_dir / 'locations.csv'
    df_locations = pd.read_csv(locations_path)
    df_locations.to_sql('Dim_Location', con=engine, if_exists='append', index=False)
    print("Таблиця Dim_Location успішно заповнена!")
    print("----------------------------------------------------------------------------------")
    
    # 3. Завантажуємо Dim_Storage_Type
    print("Читання storage_types.csv...")
    types_path = data_dir / 'storage_types.csv'
    df_types = pd.read_csv(types_path)
    df_types.to_sql('Dim_Storage_Type', con=engine, if_exists='append', index=False)
    print("Таблиця Dim_Storage_Type успішно заповнена!")
    print("----------------------------------------------------------------------------------")
    
    # 4. ОБРОБКА ТА ЗАВАНТАЖЕННЯ ЗАЛЕЖНОЇ ТАБЛИЦІ Dim_Storages
    print("Обробка складного довідника Dim_Storages...")
    storages_path = data_dir / 'storages.csv'
    df_storages = pd.read_csv(storages_path) # Текстовий файл (FarmName, StorageTypeName, StorageCapacity)
    
    # Витягуємо з бази актуальні ID, які SQL Server щойно згенерував для ферм та типів
    db_farms = pd.read_sql("SELECT FarmID, FarmName FROM Dim_Farms", engine)
    db_types = pd.read_sql("SELECT StorageTypeID, StorageTypeName FROM Dim_Storage_Type", engine)
    
    # Робимо MERGE, щоб замінити тексти на реальні ID з бази даних
    df_storages = df_storages.merge(db_farms, on='FarmName', how='inner')
    df_storages = df_storages.merge(db_types, on='StorageTypeName', how='inner')
    
    # Залишаємо тільки ті стовпчики, які чекає таблиця Dim_Storages в SQL Server
    df_final_storages = df_storages[['FarmID', 'StorageTypeID', 'StorageCapacity']]
    
    # Заливаємо фінальний результат у базу
    df_final_storages.to_sql('Dim_Storages', con=engine, if_exists='append', index=False)
    print("Таблиця Dim_Storages успішно заповнена з урахуванням FOREIGN KEY!")
    print("----------------------------------------------------------------------------------")

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
    print("----------------------------------------------------------------------------------")

    print("Читання products.csv...")
    products_path = data_dir / 'products.csv'
    df_products = pd.read_csv(products_path) 

    db_buildings = pd.read_sql("SELECT BuildingID, BuildingName FROM Dim_Buildings", engine)
    df_products = df_products.merge(db_buildings, on='BuildingName', how='inner')

    df_final_products = df_products[[
        'ProductName', 
        'ProductRequiredLevel', 
        'ProductMaxPrice', 
        'ProductExperience', 
        'ProductTimeMinutes',
        'BuildingID'
    ]]

    df_final_products.to_sql('Dim_Products', con=engine, if_exists='append', index=False)
    print("Таблиця Dim_Products успішно заповнена з урахуванням FOREIGN KEY!")
    print("----------------------------------------------------------------------------------")

    print("Читання crops.csv...")
    crops_path = data_dir / 'crops.csv'
    df_crops = pd.read_csv(crops_path) 
    df_crops.to_sql('Dim_Crops', con=engine, if_exists='append', index=False)
    print("Таблиця Dim_Crops успішно заповнена!")
    print("----------------------------------------------------------------------------------")

    print("Читання pets.csv...")
    pets_path = data_dir / 'pets.csv'
    df_pets = pd.read_csv(pets_path)

    db_products = pd.read_sql("SELECT ProductID, ProductName FROM Dim_Products", engine)
    db_crops = pd.read_sql("SELECT CropID, CropName FROM Dim_Crops", engine)

    df_pets = df_pets.merge(db_products, on='ProductName', how='left')
    df_pets = df_pets.merge(db_crops, on='CropName', how='left')

    df_final_pets = df_pets[[
        'PetName',
        'PetRequiredLevel',
        'ProductID',
        'CropID'
    ]]

    df_final_pets.to_sql('Dim_Pets', con=engine, if_exists='append', index=False)
    print("Таблиця Dim_Pets успішно заповнена з урахуванням FOREIGN KEY!")
    print("----------------------------------------------------------------------------------")

    print("Читання animals.csv...")
    animals_path = data_dir / 'animals.csv'
    df_animals = pd.read_csv(animals_path)

    df_animals = df_animals.merge(db_products, on='ProductName', how='inner')

    df_final_animals = df_animals [[
        'AnimalName',
        'ProductID',
        'ProductionTimeMinutes',
        'AnimalRequiredLevel'
    ]]

    df_final_animals.to_sql('Dim_Animals', con=engine, if_exists='append', index=False)
    print("Таблиця Dim_Animals успішно заповнена з урахуванням FOREIGN KEY!")
    print("----------------------------------------------------------------------------------")

def load_farm_facts(engine):
    print("Старт завантаження...")

    data_dir = Path(__file__).resolve().parent.parent / 'DATA'

    print("Читання farm_livestock.csv...")
    farm_livestock_path = data_dir / 'farm_livestock.csv'
    df_farm_livestock = pd.read_csv(farm_livestock_path) 

    db_farms = pd.read_sql("SELECT FarmID, FarmName FROM Dim_Farms", engine)
    db_animals = pd.read_sql("SELECT AnimalID, AnimalName FROM Dim_Animals", engine)

    df_farm_livestock = df_farm_livestock.merge(db_farms, on='FarmName' ,how='inner',)
    df_farm_livestock = df_farm_livestock.merge(db_animals, on='AnimalName' ,how='inner',)

    df_final_farm_livestock = df_farm_livestock [[
        'FarmID',
        'AnimalID',
        'AnimalQuantity'
    ]]

    df_final_farm_livestock.to_sql('Fact_Farm_Livestock', con=engine, if_exists='append', index=False)
    print("Таблиця Fact_Farm_Livestock успішно заповнена з урахуванням FOREIGN KEY!")
    print("----------------------------------------------------------------------------------")

    print("Читання pets_livestock.csv...")
    pets_livestock_path = data_dir / 'pets_livestock.csv'
    df_pets_livestock = pd.read_csv(pets_livestock_path)

    db_pets = pd.read_sql("SELECT PetID, PetName FROM Dim_Pets", engine)

    df_pets_livestock = df_pets_livestock.merge(db_farms, on='FarmName', how='inner')
    df_pets_livestock = df_pets_livestock.merge(db_pets, on='PetName', how='inner')

    df_final_pets_livestock = df_pets_livestock [[
        'FarmID',
        'PetID',
        'PetQuantity'
    ]]

    df_final_pets_livestock.to_sql('Fact_Pets_Livestock', con=engine, if_exists='append', index=False)
    print("Таблиця Fact_Pets_Livestock успішно заповнена з урахуванням FOREIGN KEY!")
    print("----------------------------------------------------------------------------------")

    print("Читання barn.csv...")
    barn_path = data_dir / 'barn.csv'
    df_barn = pd.read_csv(barn_path)

    db_storages = pd.read_sql("SELECT StorageID, FarmID FROM Dim_Storages WHERE StorageTypeID = 1", engine)
    db_products = pd.read_sql("SELECT ProductID, ProductName FROM Dim_Products", engine)

    df_barn = df_barn.merge(db_farms, on='FarmName', how='inner')
    df_barn = df_barn.merge(db_products, on='ProductName', how='inner')
    df_barn = df_barn.merge(db_storages, on='FarmID', how='inner')

    df_final_barn = df_barn [[
        'StorageID',
        'FarmID',
        'ProductID',
        'ProductCount'
    ]]

    df_final_barn.to_sql('Fact_Barn', con=engine, if_exists='append', index=False)
    print("Таблиця Fact_Barn успішно заповнена з урахуванням FOREIGN KEY!")
    print("----------------------------------------------------------------------------------")

    print("Читання silo.csv...")
    silo_path = data_dir / 'silo.csv'
    df_silo = pd.read_csv(silo_path)

    db_storages = pd.read_sql("SELECT StorageID, FarmID FROM Dim_Storages WHERE StorageTypeID = 2", engine)
    db_crop = pd.read_sql("SELECT CropID, CropName FROM Dim_Crops", engine)

    df_silo = df_silo.merge(db_farms, on='FarmName', how='inner')
    df_silo = df_silo.merge(db_crop, on='CropName', how='inner')
    df_silo = df_silo.merge(db_storages, on='FarmID', how='inner')

    df_final_silo = df_silo [[
        'StorageID',
        'FarmID',
        'CropID',
        'CropCount'
    ]]

    df_final_silo.to_sql('Fact_Silo', con=engine, if_exists='append', index=False)
    print("Таблиця Fact_Silo успішно заповнена з урахуванням FOREIGN KEY!")
    print("----------------------------------------------------------------------------------")

    print("Читання fact_buildings.csv...")
    fact_buildings_path = data_dir / 'fact_buildings.csv'
    df_fact_buildings = pd.read_csv(fact_buildings_path)

    db_buildings = pd.read_sql("SELECT BuildingID, BuildingName FROM Dim_Buildings", engine)
    db_locations = pd.read_sql("SELECT LocationID, LocationName FROM Dim_Location", engine)

    df_fact_buildings = df_fact_buildings.merge(db_buildings, on='BuildingName', how='inner')
    df_fact_buildings = df_fact_buildings.merge(db_farms, on='FarmName', how='inner')
    df_fact_buildings = df_fact_buildings.merge(db_locations, on='LocationName', how='inner')

    df_final_fact_buildings = df_fact_buildings[[
        'BuildingID',
        'FarmID',
        'LocationID',
        'ProductionSlots',
        'MasteryStars'
    ]]

    df_final_fact_buildings.to_sql('Fact_Buildings', con=engine, if_exists='append', index=False)
    print("Таблиця Fact_Buildings успішно заповнена з урахуванням FOREIGN KEY!")
    print("----------------------------------------------------------------------------------")


if __name__ == "__main__":
    SERVER = '.' 
    DATABASE = 'HayDay_Farm'  
    
    connection_string = f"mssql+pyodbc://@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    
    try:
        print("Підключення до сервера SQL Server...")
        engine = create_engine(connection_string)
        
        # це вже виконано
        # load_base_dimensions(engine)
        # load_game_entities(engine)
        # load_farm_facts(engine)
        
        print("Конвеєр виконано без помилок! Перевіряй таблиці.")
        
    except Exception as e:
        print(f"Помилка виконання конвеєра: {e}")