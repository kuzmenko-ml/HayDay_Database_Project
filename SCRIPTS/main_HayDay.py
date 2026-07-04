from main_pipeline import Hay_Day_ETL_pipeline

if __name__ == "__main__":
    try:
        print("(... Підключення до сервера SQL Server...")

        pipeline = Hay_Day_ETL_pipeline()
        
        pipeline.transform_base_dimensions()
        pipeline.transform_game_entities()
        pipeline.transform_farm_facts()

        print("...Конвеєр виконано без помилок! Перевіряй таблиці.")
        
    except Exception as e:
        print(f"(...Помилка виконання конвеєра: {e}")