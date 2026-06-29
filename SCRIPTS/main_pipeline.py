import pandas as pd
from sqlalchemy import create_engine

def transform_base_dimensions():
    df_farms = pd.read_sql("SELECT * FROM raw.Dim_Farms", engine)

    df_farms = df_farms.dropna()
    df_farms['FarmName'] = df_farms['FarmName'].str.strip()
    df_farms['FarmLevel'] = df_farms['FarmName'].astype(int)
    df_farms['FarmExperience'] = df_farms['FarmExperience'].astype(int)
    df_farms['FarmCreatedAt'] = pd.to_datetime(df_farms['FarmCreatedAt'])

    df_location = pd.read_sql("SELECT * FROM raw.Dim_Location", engine)

    df_location = df_location.dropna()
    df_location['LocationName'] = df_location['LocationName'].str.strip()
    df_location['LocationRequiredLevel'] = df_location['LocationRequiredLevel'].astype(int)

    df_storage_type = pd.read_sql("SELECT * FROM raw.Dim_Storage_Type", engine)

    df_storage_type = df_storage_type.dropna()
    df_storage_type['StorageTypeName'] = df_storage_type['StorageTypeName'].str.strip()

    df_storages = pd.read_sql("SELECT * FROM raw.Storages", engine)

    df_storages = df_storages.merge(df_farms, on='FarmName', how='inner', index=False)
    df_storages = df_storages.merge(df_storage_type, on='StorageTypeName', how='inner', index=False)

    df_storages['FarmID'] = df_storages['FarmID'].astype(int)
    df_storages['StorageTypeID'] = df_storages['StorageTypeID'].astype(int)
    df_storages['StorageCapacity'] = df_storages['StorageCapacity'].astype(int)

    df_final_storages = df_storages[[
        'FarmID',
        'StorageTypeID',
        'StorageCapacity'
    ]]



if __name__ == "__main__":
    SERVER = '.' 
    DATABASE = 'HayDay_Farm'  
    
    connection_string = f"mssql+pyodbc://@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    
    try:
        print("(с2)... Підключення до сервера SQL Server...")
        engine = create_engine(connection_string)
        
        print("(с2)...Конвеєр виконано без помилок! Перевіряй таблиці.")
        
    except Exception as e:
        print(f"(с2)...Помилка виконання конвеєра: {e}")