import logging
from main_pipeline import Hay_Day_ETL_pipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s", 
    handlers=[
        logging.FileHandler("pipeline.log", encoding="utf-8"),
        logging.StreamHandler()  
    ]
)

if __name__ == "__main__":
    try:
        logging.info("(Підключення до сервера SQL Server.")

        pipeline = Hay_Day_ETL_pipeline()
        
        pipeline.transform_base_dimensions()
        pipeline.transform_game_entities()
        pipeline.transform_farm_facts()

        logging.info("Конвеєр main_pipeline виконано без помилок! Перевіряй таблиці.")
        
    except Exception as e:
        logging.critical(f"(Помилка запуску конвеєра main_pipeline: {e}")