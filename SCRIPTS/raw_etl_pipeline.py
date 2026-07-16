import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
import json as json

def load_base_dimensions(engine):
    print("Старт завантаження базових довідників...")
    
    data_dir = Path(__file__).resolve().parent.parent / 'DATA'

    # 1. Завантажуємо Dim_Farms
    print("Читання farms.csv...")
    farms_path = data_dir / 'farms.csv'
    df_farms = pd.read_csv(farms_path)
    # назва таблиці на сервері, з'єднання створене(місток),дописування до існуючих даниї,ігнорування індексів пандас
    df_farms.to_sql('Dim_Farms', con=engine,schema='raw', if_exists='replace', index=False)
    print("Таблиця Dim_Farms успішно заповнена!")
    print("----------------------------------------------------------------------------------")
    
    # 2. Завантажуємо Dim_Location
    print("Читання locations.csv...")
    locations_path = data_dir / 'locations.csv'
    df_locations = pd.read_csv(locations_path)
    df_locations.to_sql('Dim_Location', con=engine,schema='raw', if_exists='replace', index=False)
    print("Таблиця Dim_Location успішно заповнена!")
    print("----------------------------------------------------------------------------------")
    
    # 3. Завантажуємо Dim_Storage_Type
    print("Читання storage_types.csv...")
    types_path = data_dir / 'storage_types.csv'
    df_types = pd.read_csv(types_path)
    df_types.to_sql('Dim_Storage_Type', con=engine, schema='raw', if_exists='replace', index=False)
    print("Таблиця Dim_Storage_Type успішно заповнена!")
    print("----------------------------------------------------------------------------------")
    
    # 4. Завантажуємо Dim_Storages
    print("Обробка складного довідника Dim_Storages...")
    storages_path = data_dir / 'storages.csv'
    df_storages = pd.read_csv(storages_path) 
    df_storages.to_sql('Dim_Storages', con=engine, schema='raw', if_exists='replace', index=False)
    print("Таблиця Dim_Storages успішно заповнена!")
    print("----------------------------------------------------------------------------------")

def load_game_entities(engine):
    print("Старт завантаження довідників...")

    data_dir = Path(__file__).resolve().parent.parent / 'DATA'

    print("Читання buildings.csv...")
    buildings_path = data_dir / 'buildings.csv'
    df_buildings = pd.read_csv(buildings_path) 
    df_buildings.to_sql('Dim_Buildings', con=engine,schema='raw', if_exists='replace', index=False)
    print("Таблиця Dim_Buildings успішно заповнена!")
    print("----------------------------------------------------------------------------------")

    print("Читання products.csv...")
    products_path = data_dir / 'products.csv'
    df_products = pd.read_csv(products_path) 
    df_products.to_sql('Dim_Products', con=engine, schema='raw', if_exists='replace', index=False)
    print("Таблиця Dim_Products успішно заповнена!")
    print("----------------------------------------------------------------------------------")

    print("Читання crops.csv...")
    crops_path = data_dir / 'crops.csv'
    df_crops = pd.read_csv(crops_path) 
    df_crops.to_sql('Dim_Crops', con=engine, schema='raw', if_exists='replace', index=False)
    print("Таблиця Dim_Crops успішно заповнена!")
    print("----------------------------------------------------------------------------------")

    print("Читання pets.csv...")
    pets_path = data_dir / 'pets.csv'
    df_pets = pd.read_csv(pets_path)
    df_pets.to_sql('Dim_Pets', con=engine, schema='raw', if_exists='replace', index=False)
    print("Таблиця Dim_Pets успішно заповнена з урахуванням FOREIGN KEY!")
    print("----------------------------------------------------------------------------------")

    print("Читання animals.csv...")
    animals_path = data_dir / 'animals.csv'
    df_animals = pd.read_csv(animals_path)
    df_animals.to_sql('Dim_Animals', con=engine, schema='raw', if_exists='replace', index=False)
    print("Таблиця Dim_Animals успішно заповнена з урахуванням FOREIGN KEY!")
    print("----------------------------------------------------------------------------------")

def load_farm_facts(engine):
    print("Старт завантаження...")

    data_dir = Path(__file__).resolve().parent.parent / 'DATA'

    print("Читання farm_livestock.csv...")
    farm_livestock_path = data_dir / 'farm_livestock.csv'
    df_farm_livestock = pd.read_csv(farm_livestock_path) 
    df_farm_livestock.to_sql('Fact_Farm_Livestock', con=engine, schema='raw', if_exists='replace', index=False)
    print("Таблиця Fact_Farm_Livestock успішно заповнена!")
    print("----------------------------------------------------------------------------------")

    print("Читання pets_livestock.csv...")
    pets_livestock_path = data_dir / 'pets_livestock.csv'
    df_pets_livestock = pd.read_csv(pets_livestock_path)
    df_pets_livestock.to_sql('Fact_Pets_Livestock', con=engine, schema='raw', if_exists='replace', index=False)
    print("Таблиця Fact_Pets_Livestock успішно заповнена!")
    print("----------------------------------------------------------------------------------")

    print("Читання barn.csv...")
    barn_path = data_dir / 'barn.csv'
    df_barn = pd.read_csv(barn_path)
    df_barn.to_sql('Fact_Barn', con=engine, schema='raw', if_exists='replace', index=False)
    print("Таблиця Fact_Barn успішно заповнена!")
    print("----------------------------------------------------------------------------------")

    print("Читання silo.csv...")
    silo_path = data_dir / 'silo.csv'
    df_silo = pd.read_csv(silo_path)
    df_silo.to_sql('Fact_Silo', con=engine, schema='raw', if_exists='replace', index=False)
    print("Таблиця Fact_Silo успішно заповнена!")
    print("----------------------------------------------------------------------------------")

    print("Читання fact_buildings.csv...")
    fact_buildings_path = data_dir / 'fact_buildings.csv'
    df_fact_buildings = pd.read_csv(fact_buildings_path)
    df_fact_buildings.to_sql('Fact_Buildings', con=engine, schema='raw', if_exists='replace', index=False)
    print("Таблиця Fact_Buildings успішно заповнена!")
    print("----------------------------------------------------------------------------------")

def load_raw_data(engine):
    config_dir = Path(__file__).resolve().parent / 'raw_pipeline_config.json'
    data_dir = Path(__file__).resolve().parent.parent / 'DATA'

    with open(config_dir, 'r') as f:
        config_data = json.load(f)

    for i in config_data:
        # print('---------------------------------------')
        # print('||| Читаємо файл '+ i['file_name'] + '! |||')
        df = pd.read_csv(data_dir / i['file_name'])
        if df.empty:
            print('ПОМИЛКА! Порожній файл. Конвеєр пропускає його.')
            continue
        else:
            # print(df)
            df.to_sql(i['table_name'], con=engine, schema='raw', if_exists='replace', index=False)
            # print('||| Завантажено '+ i['file_name'] + ' у '+ i['table_name'] + ' |||')