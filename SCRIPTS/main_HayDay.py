import os
import logging
from raw_etl_pipeline import load_raw_data
from main_pipeline import Hay_Day_ETL_pipeline
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s", 
    handlers=[
        logging.FileHandler("pipeline.log", encoding="utf-8"),
        logging.StreamHandler()  
    ]
)

if __name__ == "__main__":
    server = os.environ.get("DB_SERVER", ".")
    database = os.environ.get("DB_DATABASE", "HayDay_Farm")
    try:
        logging.info("--- СТАРТ ФАЗИ 1: Завантаження сирих даних ---")

        connection_string = f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
        engine = create_engine(connection_string)

        load_raw_data(engine)
        logging.info("Фаза 1 успішно завершена.")

        logging.info("--- СТАРТ ФАЗИ 2: Трансформація даних ---")

        pipeline = Hay_Day_ETL_pipeline(server=server, database=database)
        
        pipeline.transform_base_dimensions()
        pipeline.transform_game_entities()
        pipeline.transform_farm_facts()

        logging.info("Увесь ETL-конвеєр виконано без помилок! Перевіряй таблиці.")
        
    except Exception as e:
        logging.critical(f"Критична помилка виконання конвеєра: {e}")