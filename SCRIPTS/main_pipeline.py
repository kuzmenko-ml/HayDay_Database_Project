import logging
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import json

class Hay_Day_ETL_pipeline:
    def __init__(self, server=None, database=None):
        self.SERVER = server if server else '.' 
        self.DATABASE = database if database else 'HayDay_Farm' 
    
        self.connection_string = f"mssql+pyodbc://@{self.SERVER}/{self.DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
        self.engine = create_engine(self.connection_string)
    
    def delete_null_data(self, df, columns=None, how='any'):
        return df.dropna(subset=columns, how=how)
    
    def clean_text(self, df, columns):
        for col in columns:
            if col in df.columns:
                df[col] = df[col].str.strip()
        return df
        
    def transform_base_dimensions(self):
        try:
            df_location = pd.read_sql("SELECT * FROM raw.Dim_Location", self.engine)

            df_location = self.delete_null_data(df_location)
            df_location = self.clean_text(df_location, ['LocationName'])
            df_location['LocationRequiredLevel'] = df_location['LocationRequiredLevel'].astype(int)

            existing_names = []
            try:
                df_location_existing = pd.read_sql("SELECT LocationName FROM Dim_Location", self.engine)
                existing_names = df_location_existing['LocationName'].tolist()
            except Exception as err:
                logging.warning(f"Не вдалося зчитати існуючі локації (можливо, таблиця ще порожня): {err}")

            df_location = df_location[~df_location['LocationName'].isin(existing_names)]
            df_location.to_sql('Dim_Location', con=self.engine, if_exists='append', index=False)
            logging.info("Dim_Location завантажено успішно!")
        except Exception as e:
            logging.error(f"Помилка! Завантаження файлу Dim_Location не відбулося. Помилка: {e}")

        farms_ok = True
        storage_type_ok = True

        try:
            df_farms = pd.read_sql("SELECT * FROM raw.Dim_Farms", self.engine)

            df_farms = self.delete_null_data(df_farms)
            df_farms = self.clean_text(df_farms, ['FarmName'])
            df_farms['FarmLevel'] = df_farms['FarmLevel'].astype(int)
            df_farms['FarmExperience'] = df_farms['FarmExperience'].astype(int)
            df_farms['FarmCreatedAt'] = pd.to_datetime(df_farms['FarmCreatedAt'])

            existing_names = []
            try:
                df_farms_existing = pd.read_sql("SELECT FarmName FROM Dim_Farms", self.engine)
                existing_names = df_farms_existing['FarmName'].tolist()
            except Exception as err:
                logging.warning(f"Не вдалося зчитати існуючі ферми (можливо, таблиця ще порожня): {err}")

            df_farms = df_farms[~df_farms['FarmName'].isin(existing_names)]

            df_farms.to_sql('Dim_Farms', con=self.engine, if_exists='append', index=False)
            logging.info("Dim_Farms завантажено успішно!")
        except Exception as e:
            logging.error(f"Помилка! Завантаження файлу Dim_Farms не відбулося. Помилка: {e}")
            farms_ok = False

        try:
            df_storage_type = pd.read_sql("SELECT * FROM raw.Dim_Storage_Type", self.engine)

            df_storage_type = self.delete_null_data(df_storage_type)
            df_storage_type = self.clean_text(df_storage_type, ['StorageTypeName'])

            existing_names = []
            try:
                df_storage_type_existing = pd.read_sql("SELECT StorageTypeName FROM Dim_Storage_Type", self.engine)
                existing_names = df_storage_type_existing['StorageTypeName'].tolist()
            except Exception as err:
                logging.warning(f"Не вдалося зчитати існуючі типи (можливо, таблиця ще порожня): {err}")

            df_storage_type = df_storage_type[~df_storage_type['StorageTypeName'].isin(existing_names)]

            df_storage_type.to_sql('Dim_Storage_Type', con=self.engine, if_exists='append', index=False)
            logging.info("Dim_Storage_Type завантажено успішно!")
        except Exception as e:
            logging.error(f"Помилка! Завантаження файлу Dim_Storage_Type не відбулося. Помилка: {e}")
            storage_type_ok = False

        if farms_ok and storage_type_ok:
            try:
                df_storages = pd.read_sql("SELECT * FROM raw.Dim_Storages", self.engine)

                db_farms = pd.read_sql("SELECT FarmID, FarmName FROM Dim_Farms", self.engine)
                db_storage_types = pd.read_sql("SELECT StorageTypeID, StorageTypeName FROM Dim_Storage_Type", self.engine) 
                
                df_storages = self.delete_null_data(df_storages)
                df_storages = self.clean_text(df_storages, ['FarmName', 'StorageTypeName'])

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

                existing_names = []
                try:
                    df_storages_existing = pd.read_sql("SELECT FarmID, StorageTypeID FROM Dim_Storages", self.engine)
                    existing_names = list(zip(df_storages_existing['FarmID'], df_storages_existing['StorageTypeID']))
                except Exception as err:
                    logging.warning(f"Не вдалося зчитати існуючі сховища (можливо, таблиця ще порожня): {err}")

                df_final_storages = df_final_storages[~df_final_storages.set_index(['FarmID', 'StorageTypeID']).index.isin(existing_names)]

                df_final_storages.to_sql('Dim_Storages', con=self.engine, if_exists='append', index=False)
                logging.info("Dim_Storages завантажено успішно!")
            except Exception as e:
                  logging.error(f"Помилка! Завантаження таблиці Dim_Storages не відбулося. Деталі: {e}")
        else:
            logging.warning("Попередження! Довідник Dim_Storages не оновлено, бо критичні довідники (Farms/Storage Types) не оновилися до нього.")

    def transform_game_entities(self): 
        buildings_ok = True
        try:
            df_buildings = pd.read_sql("SELECT * FROM raw.Dim_Buildings", self.engine)
            df_buildings = self.delete_null_data(df_buildings)

            db_location = pd.read_sql("SELECT LocationName, LocationID FROM Dim_Location", self.engine)

            df_buildings = self.clean_text(df_buildings, ['LocationName', 'BuildingName'])

            rows_before = len(df_buildings)

            df_buildings = df_buildings.merge(db_location, on='LocationName', how='inner')

            rows_after = len(df_buildings)
            if rows_after == 0:
                raise ValueError("Після з'єднання з локаціями залишилось 0 будівель.")
            if rows_after < rows_before:
                logging.warning(f"Увага! Загублено {rows_before - rows_after} будівель через те, що їхні локації не знайдені в Dim_Location.")

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

            existing_names = []
            try:
                df_buildings_existing = pd.read_sql("SELECT BuildingName FROM Dim_Buildings", self.engine)
                existing_names = df_buildings_existing['BuildingName'].tolist()
            except Exception as err:
                logging.warning(f"Не вдалося зчитати існуючі будівлі (можливо, таблиця ще порожня): {err}")

            df_final_buildings = df_final_buildings[~df_final_buildings['BuildingName'].isin(existing_names)]

            df_final_buildings.to_sql('Dim_Buildings', con=self.engine, if_exists='append', index=False)
            logging.info("Dim_Buildings завантажено успішно!")
        except Exception as e:
            logging.error(f"Помилка! Завантаження файлу Dim_Buildings не відбулося: {e}")
            buildings_ok = False

        products_ok = True
        if buildings_ok:
            try:
                df_products = pd.read_sql("SELECT * FROM raw.Dim_Products", self.engine)
                db_buildings = pd.read_sql("SELECT BuildingName, BuildingID FROM Dim_Buildings", self.engine)

                df_products = self.delete_null_data(df_products)
                df_products = self.clean_text(df_products, ['ProductName','BuildingName'])
                df_products['ProductRequiredLevel'] = df_products['ProductRequiredLevel'].astype(int)
                df_products['ProductMaxPrice'] = df_products['ProductMaxPrice'].astype(int)
                df_products['ProductExperience'] = df_products['ProductExperience'].astype(int)
                df_products['ProductTimeMinutes'] = df_products['ProductTimeMinutes'].astype(int)

                rows_before = len(df_products)

                df_products = df_products.merge(db_buildings, on='BuildingName', how='inner')

                rows_after = len(df_products)
                if rows_after == 0:
                    raise ValueError("Після з'єднання з будівлями залишилось 0 продуктів.")
                    
                if rows_after < rows_before:
                    logging.warning(f"Увага! Загублено {rows_before - rows_after} продуктів через те, що їхні будівлі не знайдені в Dim_Buildings.")

                df_final_products = df_products[[
                    'ProductName',
                    'ProductRequiredLevel',
                    'ProductMaxPrice',
                    'ProductExperience',
                    'ProductTimeMinutes',
                    'BuildingID'
                ]]

                existing_names = []
                try:
                    df_product_existing = pd.read_sql("SELECT ProductName FROM Dim_Products", self.engine)
                    existing_names = df_product_existing['ProductName'].tolist()
                except Exception as err:
                    logging.warning(f"Не вдалося зчитати існуючі продукти (можливо, таблиця ще порожня): {err}")

                df_final_products = df_final_products[~df_final_products['ProductName'].isin(existing_names)]

                df_final_products.to_sql('Dim_Products', con=self.engine, if_exists='append',index=False)
                logging.info("Dim_Products завантажено успішно!")
            except Exception as e:
                logging.error(f"Помилка! Завантаження файлу Dim_Products не відбулося: {e}")
                products_ok = False
        else:
            logging.warning("Необхідна таблиця порожня, тому Dim_Products не оброблено.")
            products_ok = False

        if products_ok:
            try:
                df_animals = pd.read_sql("SELECT * FROM raw.Dim_Animals", self.engine)
                db_products = pd.read_sql("SELECT ProductName, ProductID FROM Dim_Products", self.engine)

                df_animals = self.delete_null_data(df_animals)
                df_animals = self.clean_text(df_animals, ['AnimalName'])
                df_animals['ProductionTimeMinutes'] = df_animals['ProductionTimeMinutes'].astype(int)
                df_animals['AnimalRequiredLevel'] = df_animals['AnimalRequiredLevel'].astype(int)

                rows_before = len(df_animals)

                df_animals = df_animals.merge(db_products, on='ProductName', how='inner')

                rows_after = len(df_animals)
                if rows_after == 0:
                    raise ValueError("Після з'єднання з продуктами залишилось 0 тварин.")
                    
                if rows_after < rows_before:
                    logging.warning(f"Увага! Загублено {rows_before - rows_after} тварин через те, що їхні продукти не знайдені в Dim_Products.")

                df_final_animals = df_animals[[
                    'AnimalName',
                    'ProductID',
                    'ProductionTimeMinutes',
                    'AnimalRequiredLevel'
                ]]

                existing_names = []
                try:
                    df_animal_existing = pd.read_sql("SELECT AnimalName FROM Dim_Animals", self.engine)
                    existing_names = df_animal_existing['AnimalName'].tolist()
                except Exception as err:
                    logging.warning(f"Не вдалося зчитати існуючі тварини (можливо, таблиця ще порожня): {err}")

                df_final_animals = df_final_animals[~df_final_animals['AnimalName'].isin(existing_names)]

                df_final_animals.to_sql('Dim_Animals', con=self.engine, if_exists='append', index=False)
                logging.info("Dim_Animals завантажено успішно!")
            except Exception as e:
                logging.error(f"Помилка!Dim_Animals не оброблено: {e}")
        else:
            logging.warning("Помилка!Необхідна таблиця порожня, тому Dim_Animals не оброблено.")

        crops_ok = True
        try:
            df_crops = pd.read_sql("SELECT * FROM raw.Dim_Crops", self.engine)
            df_crops = self.delete_null_data(df_crops)
            df_crops = self.clean_text(df_crops, ['CropName'])
            df_crops['CropRequiredLevel'] = df_crops['CropRequiredLevel'].astype(int)
            df_crops['CropExperience'] = df_crops['CropExperience'].astype(int)
            df_crops['CropTimeMinutes'] = df_crops['CropTimeMinutes'].astype(int)
            df_crops['CropMaxPrice'] = df_crops['CropMaxPrice'].astype(int)

            existing_names = []
            try:
                df_crop_existing = pd.read_sql("SELECT CropName FROM Dim_Crops", self.engine)
                existing_names = df_crop_existing['CropName'].tolist()
            except Exception as err:
                logging.warning(f"Не вдалося зчитати існуючі культури (можливо, таблиця ще порожня): {err}")

            df_crops = df_crops[~df_crops['CropName'].isin(existing_names)]

            df_crops.to_sql('Dim_Crops', con=self.engine, if_exists='append', index=False)
            logging.info("Dim_Crops завантажено успішно!")
        except Exception as e:
            logging.error(f"Помилка! Завантаження файлу Dim_Crops не відбулося: {e}")
            crops_ok = False

        if products_ok and crops_ok:
            try:
                df_pets = pd.read_sql("SELECT * FROM raw.Dim_Pets", self.engine)
                db_products = pd.read_sql("SELECT ProductName, ProductID FROM Dim_Products", self.engine)
                db_crops = pd.read_sql("SELECT CropName, CropID FROM Dim_Crops", self.engine)

                df_pets = self.delete_null_data(df_pets, columns=['PetName', 'PetRequiredLevel'])
                df_pets = self.clean_text(df_pets, ['PetName'])
                df_pets['PetRequiredLevel'] = df_pets['PetRequiredLevel'].astype(int)

                rows_before = len(df_pets)

                df_pets = df_pets.merge(db_products, on='ProductName', how='left')
                df_pets = df_pets.merge(db_crops, on='CropName', how='left')

                df_pets = df_pets.dropna(subset=['ProductID', 'CropID'], how='all')
                rows_after = len(df_pets)

                if rows_after == 0:
                    raise ValueError("Помилка! Після з'єднання з довідниками улюбленців не залишилось.")

                if rows_after < rows_before:
                    logging.warning(f"Увага! Загублено {rows_before - rows_after} улюбленців, бо їхній корм не знайдено в Dim_Products або Dim_Crops.")

                df_final_pets = df_pets[[
                    'PetName',
                    'PetRequiredLevel',
                    'ProductID',
                    'CropID'
                ]]

                existing_names = []
                try:
                    df_pet_existing = pd.read_sql("SELECT PetName FROM Dim_Pets", self.engine)
                    existing_names = df_pet_existing['PetName'].tolist()
                except Exception as err:
                    logging.warning(f"Не вдалося зчитати існуючі улюбленці (можливо, таблиця ще порожня): {err}")

                df_final_pets = df_final_pets[~df_final_pets['PetName'].isin(existing_names)]

                df_final_pets.to_sql('Dim_Pets', con=self.engine, if_exists='append',index=False)
                logging.info("Dim_Pets завантажено успішно!")
            except Exception as e:
                logging.error(f"Помилка! Щось не так із даними Dim_Pets! Помилка: {e}")
        else:
            logging.warning("Помилка! Пропущено завантаження Dim_Pets, бо впали Dim_Crops або Dim_Products зламані.")

    def transform_farm_facts(self):
        try:
            df_farm_livestock = pd.read_sql("SELECT * FROM raw.Fact_Farm_Livestock", self.engine)
            db_farms = pd.read_sql("SELECT FarmName, FarmID FROM Dim_Farms", self.engine)
            db_animals = pd.read_sql("SELECT AnimalName, AnimalID FROM Dim_Animals", self.engine)

            initial_count = len(df_farm_livestock)

            df_farm_livestock = self.delete_null_data(df_farm_livestock)
            df_farm_livestock = self.clean_text(df_farm_livestock, ['FarmName','AnimalName'])
            df_farm_livestock['AnimalQuantity'] = df_farm_livestock['AnimalQuantity'].astype(int)

            df_farm_livestock = df_farm_livestock.merge(db_farms, on='FarmName', how='inner')
            df_farm_livestock = df_farm_livestock.merge(db_animals, on='AnimalName', how='inner')

            if len(df_farm_livestock) == 0 and initial_count > 0:
                logging.warning("Попередження! Нова поставка Fact_Farm_Livestock повністю анулювалася після мерджу! Дані в БД не додано.")
            else:
                if len(df_farm_livestock) < initial_count:
                    logging.warning(f"Зверни увагу: {initial_count - len(df_farm_livestock)} нових рядків фактів пропущено через невідповідність імен у довідниках.")
                    logging.warning("Успішно! АЛЕ ДАНІ ЗАВАНТАЖЕНО ЧАСТКОВО!")
                df_final_farm_livestock = df_farm_livestock[[
                    'FarmID',
                    'AnimalID',
                    'AnimalQuantity'
                ]]

                df_final_farm_livestock.to_sql('temp_clean_livestock', con=self.engine, schema='raw', if_exists='replace', index=False)
                logging.info("Успішно! temp_clean_livestock")

                with self.engine.begin() as connection:
                    connection.execute(text("EXEC SP_SyncLivestockFacts"))
                logging.info("Успішно! Fact_Farm_Livestock синхронізовано через збережену процедуру.")
        except Exception as e:
            logging.error(f"Помилка! Скрипт упав під час обробки Fact_Farm_Livestock. Деталі: {e}")

        try:
            df_pets_livestock = pd.read_sql("SELECT * FROM raw.Fact_Pets_Livestock", self.engine)
            db_pets = pd.read_sql("SELECT PetID, PetName FROM Dim_Pets", self.engine)
            db_farms = pd.read_sql("SELECT FarmID, FarmName FROM Dim_Farms", self.engine)

            initial_count = len(df_pets_livestock)

            df_pets_livestock = self.delete_null_data(df_pets_livestock)
            df_pets_livestock = self.clean_text(df_pets_livestock, ['FarmName','PetName'])
            df_pets_livestock['PetQuantity'] = df_pets_livestock['PetQuantity'].astype(int)

            df_pets_livestock =  df_pets_livestock.merge(db_farms, on='FarmName', how='inner')
            df_pets_livestock =  df_pets_livestock.merge(db_pets, on='PetName', how='inner')

            if len(df_pets_livestock) == 0 and initial_count > 0:
                logging.warning("Попередження! Нова поставка Fact_Pets_Livestock повністю анулювалася після мерджу! Дані в БД не додано.")
            else:
                if len(df_pets_livestock) < initial_count:
                    logging.warning(f"Зверни увагу: {initial_count - len(df_pets_livestock)} нових рядків фактів пропущено через невідповідність імен у довідниках.")

                df_final_pets_livestock = df_pets_livestock[[
                    'FarmID',
                    'PetID',
                    'PetQuantity'
                ]]

                df_final_pets_livestock.to_sql('temp_clean_pet_livestock', con=self.engine, schema='raw', if_exists='replace',index=False)
                logging.info("Успішно! temp_clean_pet_livestock")

                with self.engine.begin() as connection:
                    connection.execute(text("EXEC SP_SyncPetsLivestockFacts"))
                logging.info("Успішно! Fact_Pets_Livestock синхронізовано через збережену процедуру.")
        except Exception as e:
            logging.error(f"Помилка! Скрипт упав під час обробки Fact_Pets_Livestock. Деталі: {e}")

        try:
            df_barn = pd.read_sql("SELECT * FROM raw.Fact_Barn", self.engine)
            db_storages = pd.read_sql("SELECT StorageID, FarmID FROM Dim_Storages WHERE StorageTypeID = 1", self.engine)
            db_products = pd.read_sql("SELECT ProductID, ProductName FROM Dim_Products", self.engine)
            db_farms = pd.read_sql("SELECT FarmName, FarmID FROM Dim_Farms", self.engine)

            initial_count = len(df_barn)

            df_barn = self.delete_null_data(df_barn)
            df_barn = self.clean_text(df_barn, ['FarmName', 'ProductName'])
            df_barn['ProductCount'] = df_barn['ProductCount'].astype(int)

            df_barn = df_barn.merge(db_farms, on='FarmName', how='inner')
            df_barn = df_barn.merge(db_storages, on='FarmID', how='inner')
            df_barn = df_barn.merge(db_products, on='ProductName', how='inner')

            if len(df_barn) == 0 and initial_count > 0:
                logging.warning("Попередження! Нова поставка Fact_Barn повністю анулювалася після мерджу! Дані в БД не додано.")
            else:
                if len(df_barn) < initial_count:
                    logging.warning(f"Зверни увагу: {initial_count - len(df_barn)} нових рядків фактів комори пропущено через невідповідність ключів.")

                df_final_barn = df_barn[[
                    'StorageID',
                    'FarmID',
                    'ProductID',
                    'ProductCount'
                ]]

                df_final_barn.to_sql('temp_clean_barn', con=self.engine, schema='raw', if_exists='replace',index=False)
                logging.info("Успішно! temp_clean_barn")

                with self.engine.begin() as connection:
                    connection.execute(text("EXEC SP_SyncBarnFacts"))
                logging.info("Успішно! Fact_Barn синхронізовано через збережену процедуру.")
        except Exception as e:
            logging.error(f"Помилка! Скрипт упав під час обробки Fact_Barn. Деталі: {e}")

        try:
            df_silo = pd.read_sql("SELECT * FROM raw.Fact_Silo", self.engine)
            db_storages = pd.read_sql("SELECT StorageID, FarmID FROM Dim_Storages WHERE StorageTypeID = 2", self.engine)
            db_crops = pd.read_sql("SELECT CropID, CropName FROM Dim_Crops", self.engine)
            db_farms = pd.read_sql("SELECT FarmName, FarmID FROM Dim_Farms", self.engine)

            initial_count = len(df_silo)

            df_silo = self.delete_null_data(df_silo)
            df_silo = self.clean_text(df_silo, ['FarmName','CropName'])
            df_silo['CropCount'] = df_silo['CropCount'].astype(int)

            df_silo = df_silo.merge(db_farms, on='FarmName', how='inner')
            df_silo = df_silo.merge(db_storages, on='FarmID', how='inner')
            df_silo = df_silo.merge(db_crops, on='CropName', how='inner')

            if len(df_silo) == 0 and initial_count > 0:
                logging.warning("Попередження! Нова поставка Fact_Silo повністю анулювалася після мерджу! Дані в БД не додано.")
            else:
                if len(df_silo) < initial_count:
                    logging.warning(f"Зверни увагу: {initial_count - len(df_silo)} нових рядків фактів комори пропущено через невідповідність ключів.")

                df_final_silo = df_silo[[
                    'StorageID',
                    'FarmID',
                    'CropID',
                    'CropCount'
                ]]

                df_final_silo.to_sql('temp_clean_silo', con=self.engine, schema='raw', if_exists='replace',index=False)
                logging.info("Успішно! temp_clean_silo")

                with self.engine.begin() as connection:
                    connection.execute(text("EXEC SP_SyncSiloFacts"))
                logging.info("Успішно! Fact_Silo синхронізовано через збережену процедуру.")
        except Exception as e:
            logging.error(f"Помилка! Скрипт упав під час обробки Fact_Silo. Деталі: {e}")

        try:
            df_buildings = pd.read_sql("SELECT * FROM raw.Fact_Buildings", self.engine)
            db_buildings = pd.read_sql("SELECT BuildingName, BuildingID FROM Dim_Buildings", self.engine)
            db_location = pd.read_sql("SELECT LocationName, LocationID FROM Dim_Location", self.engine)
            db_farms = pd.read_sql("SELECT FarmName, FarmID FROM Dim_Farms", self.engine)

            initial_count = len(df_buildings)

            df_buildings = self.delete_null_data(df_buildings)
            df_buildings = self.clean_text(df_buildings, ['FarmName','BuildingName','LocationName'])
            df_buildings['ProductionSlots'] = df_buildings['ProductionSlots'].astype(int)
            df_buildings['MasteryStars'] = df_buildings['MasteryStars'].astype(int)

            df_buildings = df_buildings.merge(db_farms, on='FarmName', how='inner')
            df_buildings = df_buildings.merge(db_location, on='LocationName', how='inner')
            df_buildings = df_buildings.merge(db_buildings, on='BuildingName', how='inner')

            if len(df_buildings) == 0 and initial_count > 0:
                logging.warning("Попередження! Нова поставка Fact_Buildings повністю анулювалася після мерджу! Дані в БД не додано.")
            else:
                if len(df_buildings) < initial_count:
                    logging.warning(f"Зверни увагу: {initial_count - len(df_buildings)} нових рядків фактів комори пропущено через невідповідність ключів.")

                df_final_buildings = df_buildings[[
                    'BuildingID',
                    'FarmID',
                    'LocationID',
                    'ProductionSlots',
                    'MasteryStars'
                ]]
                df_final_buildings.to_sql('temp_clean_buildings', con=self.engine, schema='raw', if_exists='replace',index=False)
                logging.info("Успішно! temp_clean_buildings")

                with self.engine.begin() as connection:
                    connection.execute(text("EXEC SP_SyncBuildingFacts"))
                logging.info("Успішно! Fact_Buildings синхронізовано через збережену процедуру.")
        except Exception as e:
            logging.error(f"Помилка! Скрипт упав під час обробки Fact_Buildings. Деталі: {e}")

    def load_new_demensions_config(self):
        with open("D:/HayDay_Database_Project/SCRIPTS/pipeline_config.json", 'r') as c:
            config = json.load(c)

        dim = config["new_dimensions"]

        for i in dim:
            table_name = i["table_name"]
            file_path = i["source_file_path"]
            colums_to_clean = i["clean_text_columns"]
            int_columns = i["int_columns"]
            business_keys = i["business_keys"]
            lookups = i.get("lookups", None)

            try:
                temp_df = pd.read_csv(file_path)
                logging.info(f"Файл успішно прочитано. Знайдено рядків: {len(temp_df)}")
            except Exception as e:
                logging.error(f"Критична помилка при читанні файлу {file_path}: {e}")
                continue

            temp_df = self.delete_null_data(temp_df)

            if colums_to_clean:
                temp_df = self.clean_text(temp_df, colums_to_clean)

            if lookups:
                for lookup in lookups:
                    src_col = lookup["source_col"]
                    lk_table = lookup["lookup_table"]
                    lk_key = lookup["lookup_key"]
                    id_col = lookup["id_col"]

                    if src_col in temp_df.columns:
                        try:
                            db_lookup_df = pd.read_sql(f"SELECT {lk_key}, {id_col} FROM {lk_table}", self.engine)
                            
                            db_lookup_df = self.clean_text(db_lookup_df, [lk_key])

                            temp_df = temp_df.merge(db_lookup_df, left_on=src_col, right_on=lk_key, how='inner')
                            
                            cols_to_drop = [src_col]
                            if lk_key != src_col:
                                cols_to_drop.append(lk_key)
                                
                            temp_df = temp_df.drop(columns=cols_to_drop)
                            logging.info(f"Успішно змаплено {src_col} -> {id_col} через таблицю {lk_table}")
                        except Exception as lookup_err:
                            logging.error(f"Помилка динамічного маппінгу для {src_col} у таблиці {table_name}: {lookup_err}")

            if int_columns:
                for col in int_columns:
                    try:
                        temp_df[col] = temp_df[col].astype(int)
                    except Exception as int_err:
                        logging.error(f"Помилка конвертації колонки {col} в INT: {int_err}")

            existing_names = []
            business_keys_str = ", ".join(business_keys)
            try:
                db_df = pd.read_sql(f"SELECT {business_keys_str} FROM {table_name}", self.engine)
                existing_names = db_df[business_keys[0]].tolist()
            except Exception as err:
                logging.warning(f"Не вдалося зчитати існуючі дані (можливо, таблиця ще порожня): {err}")

            temp_df = temp_df[~temp_df[business_keys[0]].isin(existing_names)]
            after_filter = len(temp_df)

            if after_filter > 0:
                try:
                    logging.info(f"Запис {after_filter} нових рядків у таблицю {table_name}...")
                    temp_df.to_sql(table_name, con=self.engine, if_exists='append', index=False)
                    logging.info(f"Успіх! Довідник {table_name} оновлено.")
                except Exception as sql_err:
                    logging.error(f"Помилка запису в БД для {table_name}: {sql_err}")
        else:
            logging.info("Завершено завантаження довідників.")

    def load_new_facts_config(self):
        with open("D:/HayDay_Database_Project/SCRIPTS/pipeline_config.json", 'r') as c:
            config = json.load(c)

        facts = config["new_facts"]

        for i in facts:
            table_name = i["table_name"]
            path = i["source_file_path"]
            temp_table_name = i["temp_table_name"] 
            sp = i["procedure_name"]
            lookups = i.get("lookups", [])

            df = pd.read_csv(path)

            df = self.delete_null_data(df)

            if lookups:
                logging.info(f"Старт збагачення даних ключами для таблиці {table_name}")
                for lookup in lookups:
                    src_col = lookup["source_col"]       
                    id_col = lookup["target_id_col"]     
                    dim_table = lookup["dim_table"]      

                    try:

                        dim_df = pd.read_sql(f"SELECT {id_col}, {src_col} FROM {dim_table}", self.engine)
                        
                        df = df.merge(dim_df, on=src_col, how='left')

                        df = df.drop(columns=[src_col])
                        
                        logging.info(f"Успішно підтягнуто {id_col} замість {src_col}")
                    except Exception as lookup_err:
                        logging.error(f"Помилка пошуку ID у таблиці {dim_table}: {lookup_err}")

            df.to_sql(temp_table_name, con=self.engine, schema='raw', if_exists='replace', index=False)

            try:
                with self.engine.connect() as con:
                    con.execute(text(f"EXEC {sp}"))
                    con.commit()
                    logging.info(f"Таблицю фактів {table_name} успішно оновлено!")
            except Exception as er:
                logging.error(f"Помилка при виконанні процедури {sp}: {er}")
