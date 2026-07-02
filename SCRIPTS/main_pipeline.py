import pandas as pd
from sqlalchemy import create_engine

def delete_null_data(df, columns=None):
    return df.dropna()

def clean_text(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = df[col].str.strip()
    return df

def transform_base_dimensions(engine):
    try:
        df_location = pd.read_sql("SELECT * FROM raw.Dim_Location", engine)

        df_location = delete_null_data(df_location)
        df_location = clean_text(df_location, ['LocationName'])
        df_location['LocationRequiredLevel'] = df_location['LocationRequiredLevel'].astype(int)

        existing_names = []
        try:
            df_location_existing = pd.read_sql("SELECT LocationName FROM Dim_Location", engine)
            existing_names = df_location_existing['LocationName'].tolist()
        except:
            pass

        df_location = df_location[~df_location['LocationName'].isin(existing_names)]
        df_location.to_sql('Dim_Location', con=engine, if_exists='append', index=False)
    except Exception as e:
        print('Помилка! Завантаження файлу Dim_Location не відбулося.')

    farms_ok = True
    storage_type_ok = True

    try:
        df_farms = pd.read_sql("SELECT * FROM raw.Dim_Farms", engine)

        df_farms = delete_null_data(df_farms)
        df_farms = clean_text(df_farms, ['FarmName'])
        df_farms['FarmLevel'] = df_farms['FarmLevel'].astype(int)
        df_farms['FarmExperience'] = df_farms['FarmExperience'].astype(int)
        df_farms['FarmCreatedAt'] = pd.to_datetime(df_farms['FarmCreatedAt'])

        df_farms.to_sql('Dim_Farms', con=engine, if_exists='append', index=False)
    except Exception as e:
        print('Помилка! Завантаження файлу Dim_Farms не відбулося.')
        farms_ok = False

    try:
        df_storage_type = pd.read_sql("SELECT * FROM raw.Dim_Storage_Type", engine)

        df_storage_type = delete_null_data(df_storage_type)
        df_storage_type = clean_text(df_storage_type, ['StorageTypeName'])

        df_storage_type.to_sql('Dim_Storage_Type', con=engine, if_exists='append', index=False)
    except Exception as e:
        print('Помилка! Завантаження файлу Dim_Storage_Type не відбулося.')
        storage_type_ok = False

    if farms_ok and storage_type_ok:
        try:
            df_storages = pd.read_sql("SELECT * FROM raw.Dim_Storages", engine)

            db_farms = pd.read_sql("SELECT FarmID, FarmName FROM Dim_Farms", engine)
            db_storage_types = pd.read_sql("SELECT StorageTypeID, StorageTypeName FROM Dim_Storage_Type", engine) 

            df_storages = clean_text(df_storages, ['FarmName', 'StorageTypeName'])

            df_storages = df_storages.merge(db_farms, on='FarmName', how='inner')
            df_storages = df_storages.merge(db_storage_types, on='StorageTypeName', how='inner')

            df_storages['FarmID'] = df_storages['FarmID'].astype(int)
            df_storages['StorageTypeID'] = df_storages['StorageTypeID'].astype(int)
            df_storages['StorageCapacity'] = df_storages['StorageCapacity'].astype(int)

            df_final_storages = df_storages[[
                'FarmID',
                'StorageTypeID',
                'StorageCapacity'
            ]]

            df_final_storages.to_sql('Dim_Storages', con=engine, if_exists='append', index=False)
        except Exception as e:
            print('Помилка! Завантаження файлу Dim_Storages не відбулося.')  
    else:
        print('Помилка! Цей довідник не оновлено. Бо критичні довідники не оновились до нього.')

def transform_game_entities(engine): 
    buildings_ok = True
    try:
        df_buildings = pd.read_sql("SELECT * FROM raw.Dim_Buildings", engine)
        df_buildings = delete_null_data(df_buildings)

        db_location = pd.read_sql("SELECT LocationName, LocationID FROM Dim_Location", engine)
        if db_location.empty:
            print('Помилка! Таблиця LocationName порожня. Зупиняю роботу')
            buildings_ok = False
        else:
            df_buildings = clean_text(df_buildings, ['LocationName', 'BuildingName'])

            df_buildings = df_buildings.merge(db_location, on='LocationName', how='inner')

            df_buildings['BuildingRequiredLevel'] = df_buildings['BuildingRequiredLevel'].astype(int)
            df_buildings['LocationID'] = df_buildings['LocationID'].astype(int)
            df_buildings['BuildingPrice'] = df_buildings['BuildingPrice'].astype(int)
            df_buildings['ConstructionTimeMinutes'] = df_buildings['ConstructionTimeMinutes'].astype(int)

            df_final_buildings = df_buildings[[
                'BuildingName',
                'BuildingRequiredLevel',
                'LocationID',
                'BuildingPrice',
                'ConstructionTimeMinutes'
            ]]

            df_final_buildings.to_sql('Dim_Buildings', con=engine, if_exists='append', index=False)
            print('Dim_Buildings завантажено успішно!')
            print('------------------------------------')
    except Exception as e:
        print('Помилка! Завантаження файлу Dim_Buildings не відбулося.')
        buildings_ok = False

    df_crops = pd.read_sql("SELECT * FROM raw.Dim_Crops", engine)
    df_crops = delete_null_data(df_crops)
    df_crops = clean_text(df_crops, ['CropName'])
    df_crops['CropRequiredLevel'] = df_crops['CropRequiredLevel'].astype(int)
    df_crops['CropExperience'] = df_crops['CropExperience'].astype(int)
    df_crops['CropTimeMinutes'] = df_crops['CropTimeMinutes'].astype(int)
    df_crops['CropMaxPrice'] = df_crops['CropMaxPrice'].astype(int)

    df_crops.to_sql('Dim_Crops', con=engine, if_exists='append', index=False)
    print('Dim_Crops завантажено успішно!')
    print('------------------------------------')

    df_products = pd.read_sql("SELECT * FROM raw.Dim_Products", engine)
    db_buildings = pd.read_sql("SELECT BuildingName, BuildingID FROM Dim_Buildings", engine)

    df_products = delete_null_data(df_products)
    df_products = clean_text(df_products, ['ProductName','BuildingName'])
    df_products['ProductRequiredLevel'] = df_products['ProductRequiredLevel'].astype(int)
    df_products['ProductMaxPrice'] = df_products['ProductMaxPrice'].astype(int)
    df_products['ProductExperience'] = df_products['ProductExperience'].astype(int)
    df_products['ProductTimeMinutes'] = df_products['ProductTimeMinutes'].astype(int)

    df_products = df_products.merge(db_buildings, on='BuildingName', how='inner')

    df_final_products = df_products[[
        'ProductName',
        'ProductRequiredLevel',
        'ProductMaxPrice',
        'ProductExperience',
        'ProductTimeMinutes',
        'BuildingID'
    ]]

    df_final_products.to_sql('Dim_Products', con=engine, if_exists='append',index=False)
    print('Dim_Products завантажено успішно!')
    print('------------------------------------')

    df_pets = pd.read_sql("SELECT * FROM raw.Dim_Pets", engine)
    db_products = pd.read_sql("SELECT ProductName, ProductID FROM Dim_Products", engine)
    db_crops = pd.read_sql("SELECT CropName, CropID FROM Dim_Crops", engine)

    df_pets = df_pets.dropna(subset=['PetName', 'PetRequiredLevel'], how='any')
    df_pets = df_pets.dropna(subset=['ProductName', 'CropName'], how='all')
    df_pets = clean_text(df_pets, ['PetName'])
    df_pets['PetRequiredLevel'] = df_pets['PetRequiredLevel'].astype(int)

    df_pets = df_pets.merge(db_products, on='ProductName', how='left')
    df_pets = df_pets.merge(db_crops, on='CropName', how='left')

    df_final_pets = df_pets[[
        'PetName',
        'PetRequiredLevel',
        'ProductID',
        'CropID'
    ]]

    df_final_pets.to_sql('Dim_Pets', con=engine, if_exists='append',index=False)
    print('Dim_Pets завантажено успішно!')
    print('------------------------------------')

    df_animals = pd.read_sql("SELECT * FROM raw.Dim_Animals", engine)

    df_animals = delete_null_data(df_animals)
    df_animals = clean_text(df_animals, ['AnimalName'])
    df_animals['ProductionTimeMinutes'] = df_animals['ProductionTimeMinutes'].astype(int)
    df_animals['AnimalRequiredLevel'] = df_animals['AnimalRequiredLevel'].astype(int)

    df_animals = df_animals.merge(db_products, on='ProductName', how='inner')

    df_final_animals = df_animals[[
        'AnimalName',
        'ProductID',
        'ProductionTimeMinutes',
        'AnimalRequiredLevel'
    ]]

    df_final_animals.to_sql('Dim_Animals', con=engine, if_exists='append', index=False)
    print('Dim_Animals завантажено успішно!')
    print('------------------------------------')

def transform_farm_facts(engine):
    df_farm_livestock = pd.read_sql("SELECT * FROM raw.Fact_Farm_Livestock", engine)
    db_farms = pd.read_sql("SELECT FarmName, FarmID FROM Dim_Farms", engine)
    db_animals = pd.read_sql("SELECT AnimalName, AnimalID FROM Dim_Animals", engine)

    df_farm_livestock = delete_null_data(df_farm_livestock)
    df_farm_livestock = clean_text(df_farm_livestock, ['FarmName','AnimalName'])
    df_farm_livestock['AnimalQuantity'] = df_farm_livestock['AnimalQuantity'].astype(int)

    df_farm_livestock = df_farm_livestock.merge(db_farms, on='FarmName', how='inner')
    df_farm_livestock = df_farm_livestock.merge(db_animals, on='AnimalName', how='inner')

    df_final_farm_livestock = df_farm_livestock[[
        'FarmID',
        'AnimalID',
        'AnimalQuantity'
    ]]

    df_final_farm_livestock.to_sql('Fact_Farm_Livestock', con=engine, if_exists='append', index=False)
    print('Успішно! Fact_Farm_Livestock')
    print('------------------------------')

    df_pets_livestock = pd.read_sql("SELECT * FROM raw.Fact_Pets_Livestock", engine)
    db_pets = pd.read_sql("SELECT PetID, PetName FROM Dim_Pets", engine)

    df_pets_livestock = delete_null_data(df_pets_livestock)
    df_pets_livestock = clean_text(df_pets_livestock, ['FarmName','PetName'])
    df_pets_livestock['PetQuantity'] = df_pets_livestock['PetQuantity'].astype(int)

    df_pets_livestock =  df_pets_livestock.merge(db_farms, on='FarmName', how='inner')
    df_pets_livestock =  df_pets_livestock.merge(db_pets, on='PetName', how='inner')

    df_final_pets_livestock = df_pets_livestock[[
        'FarmID',
        'PetID',
        'PetQuantity'
    ]]

    df_final_pets_livestock.to_sql('Fact_Pets_Livestock', con=engine, if_exists='append',index=False)
    print('Успішно! Fact_Pets_Livestock')
    print('------------------------------')

    df_barn = pd.read_sql("SELECT * FROM raw.Fact_Barn", engine)
    db_storages = pd.read_sql("SELECT StorageID, FarmID FROM Dim_Storages WHERE StorageTypeID = 1", engine)
    db_products = pd.read_sql("SELECT ProductID, ProductName FROM Dim_Products", engine)

    df_barn = delete_null_data(df_barn)
    df_barn = clean_text(df_barn, ['FarmName', 'ProductName'])
    df_barn['ProductCount'] = df_barn['ProductCount'].astype(int)

    df_barn = df_barn.merge(db_farms, on='FarmName', how='inner')
    df_barn = df_barn.merge(db_storages, on='FarmID', how='inner')
    df_barn = df_barn.merge(db_products, on='ProductName', how='inner')

    df_final_barn = df_barn[[
        'StorageID',
        'FarmID',
        'ProductID',
        'ProductCount'
    ]]

    df_final_barn.to_sql('Fact_Barn', con=engine, if_exists='append',index=False)
    print('Успішно! Fact_Barn')
    print('------------------------------')

    df_silo = pd.read_sql("SELECT * FROM raw.Fact_Silo", engine)
    db_storages = pd.read_sql("SELECT StorageID, FarmID FROM Dim_Storages WHERE StorageTypeID = 2", engine)
    db_crops = pd.read_sql("SELECT CropID, CropName FROM Dim_Crops", engine)

    df_silo = delete_null_data(df_silo)
    df_silo = clean_text(df_silo, ['FarmName','CropName'])
    df_silo['CropCount'] = df_silo['CropCount'].astype(int)

    df_silo = df_silo.merge(db_farms, on='FarmName', how='inner')
    df_silo = df_silo.merge(db_storages, on='FarmID', how='inner')
    df_silo = df_silo.merge(db_crops, on='CropName', how='inner')

    df_final_silo = df_silo[[
        'StorageID',
        'FarmID',
        'CropID',
        'CropCount'
    ]]

    df_final_silo.to_sql('Fact_Silo', con=engine, if_exists='append',index=False)
    print('Успішно! Fact_Silo')
    print('------------------------------')

    df_buildings = pd.read_sql("SELECT * FROM raw.Fact_Buildings", engine)
    db_buildings = pd.read_sql("SELECT BuildingName, BuildingID FROM Dim_Buildings", engine)
    db_location = pd.read_sql("SELECT LocationName, LocationID FROM Dim_Location", engine)

    df_buildings = delete_null_data(df_buildings)
    df_buildings = clean_text(df_buildings, ['FarmName','BuildingName','LocationName'])
    df_buildings['ProductionSlots'] = df_buildings['ProductionSlots'].astype(int)
    df_buildings['MasteryStars'] = df_buildings['MasteryStars'].astype(int)

    df_buildings = df_buildings.merge(db_farms, on='FarmName', how='inner')
    df_buildings = df_buildings.merge(db_location, on='LocationName', how='inner')
    df_buildings = df_buildings.merge(db_buildings, on='BuildingName', how='inner')

    df_final_buildings = df_buildings[[
        'BuildingID',
        'FarmID',
        'LocationID',
        'ProductionSlots',
        'MasteryStars'
    ]]

    df_final_buildings.to_sql('Fact_Buildings', con=engine, if_exists='append',index=False)
    print('Успішно! Fact_Buildings')
    print('------------------------------')

if __name__ == "__main__":
    SERVER = '.' 
    DATABASE = 'HayDay_Farm'  
    
    connection_string = f"mssql+pyodbc://@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    
    try:
        print("(с2)... Підключення до сервера SQL Server...")
        engine = create_engine(connection_string)
        # transform_base_dimensions(engine)
        # transform_game_entities(engine)
        transform_farm_facts(engine)

        print("(с2)...Конвеєр виконано без помилок! Перевіряй таблиці.")
        
    except Exception as e:
        print(f"(с2)...Помилка виконання конвеєра: {e}")