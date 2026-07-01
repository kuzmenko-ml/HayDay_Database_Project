import pandas as pd
from sqlalchemy import create_engine

def delete_null_data(df, columns=None):
    return df.dropna()

def transform_base_dimensions(engine):
    df_farms = pd.read_sql("SELECT * FROM raw.Dim_Farms", engine)

    df_farms = delete_null_data(df_farms)
    df_farms['FarmName'] = df_farms['FarmName'].str.strip()
    df_farms['FarmLevel'] = df_farms['FarmLevel'].astype(int)
    df_farms['FarmExperience'] = df_farms['FarmExperience'].astype(int)
    df_farms['FarmCreatedAt'] = pd.to_datetime(df_farms['FarmCreatedAt'])

    df_farms.to_sql('Dim_Farms', con=engine, if_exists='append', index=False)

    df_location = pd.read_sql("SELECT * FROM raw.Dim_Location", engine)

    df_location = delete_null_data(df_location)
    df_location['LocationName'] = df_location['LocationName'].str.strip()
    df_location['LocationRequiredLevel'] = df_location['LocationRequiredLevel'].astype(int)

    df_location.to_sql('Dim_Location', con=engine, if_exists='append', index=False)

    df_storage_type = pd.read_sql("SELECT * FROM raw.Dim_Storage_Type", engine)

    df_storage_type = delete_null_data(df_storage_type)
    df_storage_type['StorageTypeName'] = df_storage_type['StorageTypeName'].str.strip()

    df_storage_type.to_sql('Dim_Storage_Type', con=engine, if_exists='append', index=False)

    df_storages = pd.read_sql("SELECT * FROM raw.Dim_Storages", engine)

    db_farms = pd.read_sql("SELECT FarmID, FarmName FROM Dim_Farms", engine)
    db_storage_types = pd.read_sql("SELECT StorageTypeID, StorageTypeName FROM Dim_Storage_Type", engine) 

    df_storages['FarmName'] = df_storages['FarmName'].str.strip()
    df_storages['StorageTypeName'] = df_storages['StorageTypeName'].str.strip()

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

def transform_game_entities(engine): 
    df_buildings = pd.read_sql("SELECT * FROM raw.Dim_Buildings", engine)
    df_buildings = df_buildings.dropna()

    db_location = pd.read_sql("SELECT LocationName, LocationID FROM Dim_Location", engine)

    df_buildings['LocationName'] = df_buildings['LocationName'].str.strip()

    df_buildings = df_buildings.merge(db_location, on='LocationName', how='inner')

    df_buildings['BuildingName'] = df_buildings['BuildingName'].str.strip()
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

    df_crops = pd.read_sql("SELECT * FROM raw.Dim_Crops", engine)
    df_crops = df_crops.dropna()
    df_crops['CropName'] = df_crops['CropName'].str.strip()
    df_crops['CropRequiredLevel'] = df_crops['CropRequiredLevel'].astype(int)
    df_crops['CropExperience'] = df_crops['CropExperience'].astype(int)
    df_crops['CropTimeMinutes'] = df_crops['CropTimeMinutes'].astype(int)
    df_crops['CropMaxPrice'] = df_crops['CropMaxPrice'].astype(int)

    df_crops.to_sql('Dim_Crops', con=engine, if_exists='append', index=False)
    print('Dim_Crops завантажено успішно!')
    print('------------------------------------')

    df_products = pd.read_sql("SELECT * FROM raw.Dim_Products", engine)
    db_buildings = pd.read_sql("SELECT BuildingName, BuildingID FROM Dim_Buildings", engine)

    df_products = df_products.dropna()
    df_products['ProductName'] = df_products['ProductName'].str.strip()
    df_products['ProductRequiredLevel'] = df_products['ProductRequiredLevel'].astype(int)
    df_products['ProductMaxPrice'] = df_products['ProductMaxPrice'].astype(int)
    df_products['ProductExperience'] = df_products['ProductExperience'].astype(int)
    df_products['ProductTimeMinutes'] = df_products['ProductTimeMinutes'].astype(int)
    df_products['BuildingName'] = df_products['BuildingName'].str.strip()

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
    df_pets['PetName'] = df_pets['PetName'].str.strip()
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

    df_animals = df_animals.dropna()
    df_animals['AnimalName'] = df_animals['AnimalName'].str.strip()
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

    df_farm_livestock = df_farm_livestock.dropna()
    df_farm_livestock['FarmName'] = df_farm_livestock['FarmName'].str.strip()
    df_farm_livestock['AnimalName'] = df_farm_livestock['AnimalName'].str.strip()
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

    df_pets_livestock = df_pets_livestock.dropna()
    df_pets_livestock['FarmName'] = df_pets_livestock['FarmName'].str.strip()
    df_pets_livestock['PetName'] = df_pets_livestock['PetName'].str.strip()
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

    df_barn = df_barn.dropna()
    df_barn['FarmName'] = df_barn['FarmName'].str.strip()
    df_barn['ProductName'] = df_barn['ProductName'].str.strip()
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

    df_silo = df_silo.dropna()
    df_silo['FarmName'] = df_silo['FarmName'].str.strip()
    df_silo['CropName'] = df_silo['CropName'].str.strip()
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

    df_buildings = df_buildings.dropna()
    df_buildings['FarmName'] = df_buildings['FarmName'].str.strip()
    df_buildings['BuildingName'] = df_buildings['BuildingName'].str.strip()
    df_buildings['LocationName'] = df_buildings['LocationName'].str.strip()
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