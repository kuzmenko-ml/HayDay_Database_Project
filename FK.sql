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