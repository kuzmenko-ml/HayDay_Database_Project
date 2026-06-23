import pandas as pd
from sqlalchemy import create_engine

SERVER = '.'         
DATABASE = 'master'  

connection_string = f"mssql+pyodbc://@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

try:
    engine = create_engine(connection_string)
    
    with engine.connect() as connection:
        print("Ура! Python успішно підключився до MS SQL Server через '.'!")
        
except Exception as e:
    print("Помилка підключення:")
    print(e)