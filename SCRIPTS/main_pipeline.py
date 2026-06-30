import pandas as pd
from sqlalchemy import create_engine

def transform_base_dimensions():
    df_farms = pd.read_sql("SELECT * FROM raw.Dim_Farms", engine)

    df_farms = df_farms.dropna()
    df_farms['FarmName'] = df_farms['FarmName'].str.strip()
    df_farms['FarmLevel'] = df_farms['FarmLevel'].astype(int)
    df_farms['FarmExperience'] = df_farms['FarmExperience'].astype(int)
    df_farms['FarmCreatedAt'] = pd.to_datetime(df_farms['FarmCreatedAt'])

    df_farms.to_sql('Dim_Farms', con=engine, if_exists='append', index=False)

    df_location = pd.read_sql("SELECT * FROM raw.Dim_Location", engine)

    df_location = df_location.dropna()
    df_location['LocationName'] = df_location['LocationName'].str.strip()
    df_location['LocationRequiredLevel'] = df_location['LocationRequiredLevel'].astype(int)

    df_location.to_sql('Dim_Location', con=engine, if_exists='append', index=False)

    df_storage_type = pd.read_sql("SELECT * FROM raw.Dim_Storage_Type", engine)

    df_storage_type = df_storage_type.dropna()
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

def transform_game_entities(): 
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




if __name__ == "__main__":
    SERVER = '.' 
    DATABASE = 'HayDay_Farm'  
    
    connection_string = f"mssql+pyodbc://@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    
    try:
        print("(с2)... Підключення до сервера SQL Server...")
        engine = create_engine(connection_string)
        # transform_base_dimensions()

        print("(с2)...Конвеєр виконано без помилок! Перевіряй таблиці.")
        
    except Exception as e:
        print(f"(с2)...Помилка виконання конвеєра: {e}")