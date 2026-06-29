import pandas as pd
from sqlalchemy import create_engine

def transform_base_dimensions():
    df_farms = pd.read_sql("SELECT * FROM raw.Dim_Farms", engine)

    df_farms = df_farms.dropna()
    df_farms['FarmName'] = df_farms['FarmName'].str.strip()
    df_farms['FarmLevel'] = df_farms['FarmName'].astype(int)
    df_farms['FarmExperience'] = df_farms['FarmExperience'].astype(int)
    df_farms['FarmCreatedAt'] = pd.to_datetime(df_farms['FarmCreatedAt'])


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