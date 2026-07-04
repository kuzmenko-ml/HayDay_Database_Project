import logging
import pandas as pd
from sqlalchemy import create_engine

class Hay_Day_ETL_pipeline:
    def __init__(self):
        self.SERVER = '.' 
        self.DATABASE = 'HayDay_Farm'  
    
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

            df_farms.to_sql('Dim_Farms', con=self.engine, if_exists='append', index=False)
        except Exception as e:
            logging.error(f"Помилка! Завантаження файлу Dim_Farms не відбулося. Помилка: {e}")
            farms_ok = False

        try:
            df_storage_type = pd.read_sql("SELECT * FROM raw.Dim_Storage_Type", self.engine)

            df_storage_type = self.delete_null_data(df_storage_type)
            df_storage_type = self.clean_text(df_storage_type, ['StorageTypeName'])

            df_storage_type.to_sql('Dim_Storage_Type', con=self.engine, if_exists='append', index=False)
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

                df_final_storages.to_sql('Dim_Storages', con=self.engine, if_exists='append', index=False)
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

            df_final_buildings.to_sql('Dim_Buildings', con=self.engine, if_exists='append', index=False)
            logging.info('Dim_Buildings завантажено успішно!')
        except Exception as e:
            logging.error(f'Помилка! Завантаження файлу Dim_Buildings не відбулося: {e}')
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

                df_products = df_products.merge(db_buildings, on='BuildingName', how='inner')

                df_final_products = df_products[[
                    'ProductName',
                    'ProductRequiredLevel',
                    'ProductMaxPrice',
                    'ProductExperience',
                    'ProductTimeMinutes',
                    'BuildingID'
                ]]

                df_final_products.to_sql('Dim_Products', con=self.engine, if_exists='append',index=False)
                logging.info('Dim_Products завантажено успішно!')
            except Exception as e:
                logging.error(f'Помилка! Завантаження файлу Dim_Products не відбулося: {e}')
                products_ok = False
        else:
            logging.warning('Необхідна таблиця порожня, тому Dim_Products не оброблено.')
            products_ok = False

        if products_ok:
            try:
                df_animals = pd.read_sql("SELECT * FROM raw.Dim_Animals", self.engine)
                db_products = pd.read_sql("SELECT ProductName, ProductID FROM Dim_Products", self.engine)

                df_animals = self.delete_null_data(df_animals)
                df_animals = self.clean_text(df_animals, ['AnimalName'])
                df_animals['ProductionTimeMinutes'] = df_animals['ProductionTimeMinutes'].astype(int)
                df_animals['AnimalRequiredLevel'] = df_animals['AnimalRequiredLevel'].astype(int)

                df_animals = df_animals.merge(db_products, on='ProductName', how='inner')

                df_final_animals = df_animals[[
                    'AnimalName',
                    'ProductID',
                    'ProductionTimeMinutes',
                    'AnimalRequiredLevel'
                ]]

                df_final_animals.to_sql('Dim_Animals', con=self.engine, if_exists='append', index=False)
                logging.info('Dim_Animals завантажено успішно!')
            except Exception as e:
                logging.error(f'Помилка!Dim_Animals не оброблено: {e}')
        else:
            logging.warning('Помилка!Необхідна таблиця порожня, тому Dim_Animals не оброблено.')

        crops_ok = True
        try:
            df_crops = pd.read_sql("SELECT * FROM raw.Dim_Crops", self.engine)
            df_crops = self.delete_null_data(df_crops)
            df_crops = self.clean_text(df_crops, ['CropName'])
            df_crops['CropRequiredLevel'] = df_crops['CropRequiredLevel'].astype(int)
            df_crops['CropExperience'] = df_crops['CropExperience'].astype(int)
            df_crops['CropTimeMinutes'] = df_crops['CropTimeMinutes'].astype(int)
            df_crops['CropMaxPrice'] = df_crops['CropMaxPrice'].astype(int)

            df_crops.to_sql('Dim_Crops', con=self.engine, if_exists='append', index=False)
            logging.info('Dim_Crops завантажено успішно!')
        except Exception as e:
            logging.error(f'Помилка! Завантаження файлу Dim_Crops не відбулося: {e}')
            crops_ok = False

        if products_ok and crops_ok:
            try:
                df_pets = pd.read_sql("SELECT * FROM raw.Dim_Pets", self.engine)
                db_products = pd.read_sql("SELECT ProductName, ProductID FROM Dim_Products", self.engine)
                db_crops = pd.read_sql("SELECT CropName, CropID FROM Dim_Crops", self.engine)

                df_pets = df_pets.delete_null_data(subset=['PetName', 'PetRequiredLevel'])
                df_pets = df_pets.delete_null_data(subset=['ProductName', 'CropName'], how='all')
                df_pets = self.clean_text(df_pets, ['PetName'])
                df_pets['PetRequiredLevel'] = df_pets['PetRequiredLevel'].astype(int)

                df_pets = df_pets.merge(db_products, on='ProductName', how='left')
                df_pets = df_pets.merge(db_crops, on='CropName', how='left')

                df_final_pets = df_pets[[
                    'PetName',
                    'PetRequiredLevel',
                    'ProductID',
                    'CropID'
                ]]

                df_final_pets.to_sql('Dim_Pets', con=self.engine, if_exists='append',index=False)
                logging.info('Dim_Pets завантажено успішно!')
            except Exception as e:
                logging.error(f'Помилка! Щось не так із даними Dim_Pets! Помилка: {e}')
        else:
            logging.warning('Помилка! Пропущено завантаження Dim_Pets, бо впали Dim_Crops або Dim_Products зламані.')

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
                print('Попередження! Нова поставка Fact_Farm_Livestock повністю анулювалася після мерджу! Дані в БД не додано.')
            else:
                if len(df_farm_livestock) < initial_count:
                    print(f'Зверни увагу: {initial_count - len(df_farm_livestock)} нових рядків фактів пропущено через невідповідність імен у довідниках.')

                df_final_farm_livestock = df_farm_livestock[[
                    'FarmID',
                    'AnimalID',
                    'AnimalQuantity'
                ]]

                df_final_farm_livestock.to_sql('Fact_Farm_Livestock', con=self.engine, if_exists='append', index=False)
                print('Успішно! Частина або всі нові дані Fact_Farm_Livestock додані в БД.')
            print('------------------------------')
        except Exception as e:
            print(f'Помилка! Скрипт упав під час обробки Fact_Farm_Livestock. Деталі: {e}')
            print('------------------------------')

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
                print('Попередження! Нова поставка Fact_Pets_Livestock повністю анулювалася після мерджу! Дані в БД не додано.')
            else:
                if len(df_pets_livestock) < initial_count:
                    print(f'Зверни увагу: {initial_count - len(df_pets_livestock)} нових рядків фактів пропущено через невідповідність імен у довідниках.')

                df_final_pets_livestock = df_pets_livestock[[
                    'FarmID',
                    'PetID',
                    'PetQuantity'
                ]]

                df_final_pets_livestock.to_sql('Fact_Pets_Livestock', con=self.engine, if_exists='append',index=False)
                print('Успішно! Fact_Pets_Livestock')
            print('------------------------------')
        except Exception as e:
            print(f'Помилка! Скрипт упав під час обробки Fact_Pets_Livestock. Деталі: {e}')

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
                print('Попередження! Нова поставка Fact_Barn повністю анулювалася після мерджу! Дані в БД не додано.')
            else:
                if len(df_barn) < initial_count:
                    print(f'Зверни увагу: {initial_count - len(df_barn)} нових рядків фактів комори пропущено через невідповідність ключів.')

                df_final_barn = df_barn[[
                    'StorageID',
                    'FarmID',
                    'ProductID',
                    'ProductCount'
                ]]

                df_final_barn.to_sql('Fact_Barn', con=self.engine, if_exists='append',index=False)
                print('Успішно! Fact_Barn')
            print('------------------------------')
        except Exception as e:
            print(f'Помилка! Скрипт упав під час обробки Fact_Barn. Деталі: {e}')

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
                print('Попередження! Нова поставка Fact_Silo повністю анулювалася після мерджу! Дані в БД не додано.')
            else:
                if len(df_silo) < initial_count:
                    print(f'Зверни увагу: {initial_count - len(df_silo)} нових рядків фактів комори пропущено через невідповідність ключів.')

                df_final_silo = df_silo[[
                    'StorageID',
                    'FarmID',
                    'CropID',
                    'CropCount'
                ]]

                df_final_silo.to_sql('Fact_Silo', con=self.engine, if_exists='append',index=False)
                print('Успішно! Fact_Silo')
            print('------------------------------')
        except Exception as e:
            print(f'Помилка! Скрипт упав під час обробки Fact_Silo. Деталі: {e}')

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
                print('Попередження! Нова поставка Fact_Barn повністю анулювалася після мерджу! Дані в БД не додано.')
            else:
                if len(df_buildings) < initial_count:
                    print(f'Зверни увагу: {initial_count - len(df_buildings)} нових рядків фактів комори пропущено через невідповідність ключів.')

                df_final_buildings = df_buildings[[
                    'BuildingID',
                    'FarmID',
                    'LocationID',
                    'ProductionSlots',
                    'MasteryStars'
                ]]

                df_final_buildings.to_sql('Fact_Buildings', con=self.engine, if_exists='append',index=False)
                print('Успішно! Fact_Buildings')
            print('------------------------------')
        except Exception as e:
            print(f'Помилка! Скрипт упав під час обробки Fact_Buildings. Деталі: {e}')

