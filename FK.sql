USE HayDay_Farm;
GO

-- зв'язки (зелена лінія)

ALTER TABLE Dim_Buildings
ADD CONSTRAINT FK_Buildings_Location
FOREIGN KEY (LocationID) REFERENCES Dim_Location(LocationID);

ALTER TABLE Dim_Town_Buildings
ADD CONSTRAINT FK_Town_Buildings_Location
FOREIGN KEY (LocationID) REFERENCES Dim_Location(LocationID);

ALTER TABLE Dim_Fishing_Spots
ADD CONSTRAINT FK_DimFishingSpots_Location
FOREIGN KEY (LocationID) REFERENCES Dim_Location(LocationID);

ALTER TABLE Fact_Fishing_Spots
ADD CONSTRAINT FK_FactFishingSpots_Location
FOREIGN KEY (LocationID) REFERENCES Dim_Location(LocationID);

ALTER TABLE Fact_Tackle_Box
ADD CONSTRAINT FK_Tackle_Box_Location
FOREIGN KEY (LocationID) REFERENCES Dim_Location(LocationID);

ALTER TABLE Fact_Town_Buildings
ADD CONSTRAINT FK_Fact_Town_Buildings_Location
FOREIGN KEY (LocationID) REFERENCES Dim_Location(LocationID);

-- зв'язки (червона лінія)

ALTER TABLE Dim_Pets
ADD CONSTRAINT FK_Pets_Products
FOREIGN KEY (ProductID) REFERENCES Dim_Products(ProductID);

ALTER TABLE Dim_Pets
ADD CONSTRAINT FK_Pets_Crops
FOREIGN KEY (CropID) REFERENCES Dim_Crops(CropID);

-- зв'язки (помаранчева лінія)

ALTER TABLE Dim_Storages
ADD CONSTRAINT FK_Storages_Types
FOREIGN KEY (StorageTypeID) REFERENCES Dim_Storage_Type(StorageTypeID);

-- зв'зки (жовта лінія)

ALTER TABLE Fact_Barn
ADD CONSTRAINT FK_FactBarn_DimStorages
FOREIGN KEY (StorageID) REFERENCES Dim_Storages (StorageID);

ALTER TABLE Fact_Silo
ADD CONSTRAINT FK_FactSilo_DimStorages
FOREIGN KEY (StorageID) REFERENCES Dim_Storages (StorageID);

ALTER TABLE Fact_Tackle_Box
ADD CONSTRAINT FK_FactTackleBox_DimStorages
FOREIGN KEY (StorageID) REFERENCES Dim_Storages (StorageID);

-- зв'язки (рожева лінія)

ALTER TABLE Fact_Farm_Livestock
ADD CONSTRAINT FK_FactFarmLivestock_DimFarms
FOREIGN KEY (FarmID) REFERENCES Dim_Farms (FarmID);

ALTER TABLE Fact_Pets_Livestock
ADD CONSTRAINT FK_FactPetsLivestock_DimFarms
FOREIGN KEY (FarmID) REFERENCES Dim_Farms (FarmID);

ALTER TABLE Fact_Barn
ADD CONSTRAINT FK_FactBarn_DimFarms
FOREIGN KEY (FarmID) REFERENCES Dim_Farms (FarmID);

ALTER TABLE Fact_Silo
ADD CONSTRAINT FK_FactSilo_DimFarms
FOREIGN KEY (FarmID) REFERENCES Dim_Farms (FarmID);

ALTER TABLE Fact_Buildings
ADD CONSTRAINT FK_FactBuildings_DimFarms
FOREIGN KEY (FarmID) REFERENCES Dim_Farms (FarmID);

ALTER TABLE Fact_Tree_Bush
ADD CONSTRAINT FK_FactTreeBush_DimFarms
FOREIGN KEY (FarmID) REFERENCES Dim_Farms (FarmID);

ALTER TABLE Dim_Town_Buildings
ADD CONSTRAINT FK_DimTownBuildings_DimFarms
FOREIGN KEY (FarmID) REFERENCES Dim_Farms (FarmID);

ALTER TABLE Fact_Tackle_Box
ADD CONSTRAINT FK_FactTackleBox_DimFarms
FOREIGN KEY (FarmID) REFERENCES Dim_Farms (FarmID);

ALTER TABLE Fact_Fishing_Spots
ADD CONSTRAINT FK_FactFishingSpots_DimFarms
FOREIGN KEY (FarmID) REFERENCES Dim_Farms (FarmID);

ALTER TABLE Fact_Farm_Wallet
ADD CONSTRAINT FK_FactFarmWallet_DimFarms
FOREIGN KEY (FarmID) REFERENCES Dim_Farms (FarmID);

-- зв'язки (синя лінія)

ALTER TABLE Fact_Farm_Livestock
ADD CONSTRAINT FK_FactFarmLivestock_DimAnimals
FOREIGN KEY (AnimalID) REFERENCES Dim_Animals (AnimalID);

ALTER TABLE Fact_Pets_Livestock
ADD CONSTRAINT FK_FactPetsLivestock_DimPets
FOREIGN KEY (PetID) REFERENCES Dim_Pets (PetID);

ALTER TABLE Fact_Barn
ADD CONSTRAINT FK_FactBarn_DimProducts
FOREIGN KEY (ProductID) REFERENCES Dim_Products (ProductID);

ALTER TABLE Fact_Silo
ADD CONSTRAINT FK_FactSilo_DimCrops
FOREIGN KEY (CropID) REFERENCES Dim_Crops (CropID);

ALTER TABLE Fact_Buildings
ADD CONSTRAINT FK_FactBuildings_DimBuildings
FOREIGN KEY (BuildingID) REFERENCES Dim_Buildings (BuildingID);

ALTER TABLE Fact_Tree_Bush
ADD CONSTRAINT FK_FactTreeBush_DimTreeBush
FOREIGN KEY (TreeOrBushID) REFERENCES Dim_Tree_Bush (TreeOrBushID);

ALTER TABLE Fact_Town_Buildings
ADD CONSTRAINT FK_FactTownBuildings_DimTownBuildings
FOREIGN KEY (TownBuildingID) REFERENCES Dim_Town_Buildings (TownBuildingID);

ALTER TABLE Fact_Tackle_Box
ADD CONSTRAINT FK_FactTackleBox_DimTackle
FOREIGN KEY (TackleID) REFERENCES Dim_Tackle (TackleID);

ALTER TABLE Fact_Fishing_Spots
ADD CONSTRAINT FK_FactFishingSpots_DimFishingSpots
FOREIGN KEY (SpotID) REFERENCES Dim_Fishing_Spots (SpotID);

ALTER TABLE Fact_Farm_Wallet
ADD CONSTRAINT FK_FactFarmWallet_DimCurrencies
FOREIGN KEY (CurrencyID) REFERENCES Dim_Currencies (CurrencyID);
