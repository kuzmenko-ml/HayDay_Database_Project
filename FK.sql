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
