USE HayDay_Farm;
GO

INSERT INTO Dim_Farms (FarmName, FarmLevel, FarmExperience, FarmCreatedAt) 
VALUES ('Феська', 71, 9219, '2015-05-03'), ('Ґудзик', 30, 12046, '2025-09-15');

INSERT INTO Dim_Location (LocationName, LocationRequiredLevel)
VALUES ('Main Farm ',1), ('Town ',34),('Fishing Area ',27);

SELECT * FROM Dim_Farms;
SELECT * FROM Dim_Location;

DROP TABLE Dim_Building;

SELECT * FROM Dim_Buildings;

INSERT INTO Dim_Buildings (BuildingName, BuildingRequiredLevel, LocationID, BuildingPrice, ConstructionTimeMinutes)
VALUES ('Bakery',2,1,20,1),
	   ('Crusher',3,1,3200,1),
	   ('Dairy',6,1,50,120),
	   ('Chicken Coop',1,1,5,0),
	   ('Goat Yard',32,1,1000,0);

INSERT INTO Dim_Products (ProductsName, ProductRequiredLevel, ProductMaxPrice, ProductExperience,ProductTimeMinutes,BuildingID)
VALUES ('Bread',2,21,3,5,1),
	   ('Chicken Feed',3,7,1,5,2),
	   ('Cream',6,50,6,20,3),
	   ('Egg',1,18,2,20,4),
	   ('Goat milk',32,64,6,480,5);

INSERT INTO Dim_Animals (AnimalName,ProductID,ProductionTimeMinutes,AnimalRequiredLevel)
VALUES ('Chicken',7,20,1),
	   ('Goat',8,480,32);

INSERT INTO Dim_Crops (CropName,CropRequiredLevel,CropExperience,CropTimeMinutes,CropMaxPrice)
VALUES ('Wheat',1,1,2,3),
	   ('Corn',2,1,5,7),
	   ('Soybean',5,2,20,10);

INSERT INTO Dim_Pets (PetName,PetRequiredLevel,CropID)
VALUES ('Bird',26,1);

INSERT INTO Dim_Tree_Bush (TreeOrBushName,TreeOrBushRequiredLevel)
VALUES ('Apple',15),
	   ('Cherry',22);

INSERT INTO Dim_Town_Buildings (TownBuildingName,TownBuildingRequiredReputation,LocationID)
VALUES ('Cinema',4,2),
	   ('Gift Shop',6,2);

INSERT INTO Dim_Tackle (TackleName, TackleRequiredLevel)
VALUES ('Simple Tackle',27),
	   ('Green Tackle',28);

INSERT INTO Dim_Fishing_Spots (SpotName,SpotCooldownMinutes,LocationID)
VALUES ('Simple Spot',200,3),
	   ('Dark Spot', 400,3),
	   ('Small Spot', 120,3);

SELECT * FROM Dim_Farms;
SELECT * FROM Dim_Location;
SELECT * FROM Dim_Buildings;
SELECT * FROM Dim_Products;
SELECT * FROM Dim_Animals;
SELECT * FROM Dim_Crops;
SELECT * FROM Dim_Pets;
SELECT * FROM Dim_Tree_Bush;
SELECT * FROM Dim_Town_Buildings;
SELECT * FROM Dim_Tackle;
SELECT * FROM Dim_Fishing_Spots;
SELECT * FROM Dim_Currencies;
SELECT * FROM Dim_Storage_Type;
SELECT * FROM Dim_Storages;

INSERT INTO Dim_Currencies (CurrencyName, CurrencyIsTemporary)
VALUES ('Coins', 1);

INSERT INTO Dim_Storage_Type (StorageTypeName)
VALUES ('Ambar'),
	   ('Silo');

INSERT INTO Dim_Storages (FarmID, StorageTypeID, StorageCapacity)
VALUES (1,1,1400),
	   (1,1,1350),
	   (2,1,300),
	   (2,2,250);

UPDATE Dim_Storages
SET StorageTypeID = 2
WHERE StorageID = 2;

INSERT INTO Dim_Storage_Type (StorageTypeName)
VALUES ('Tackle box');

SELECT * FROM Dim_Storage_Type;

DELETE FROM Dim_Storage_Type
WHERE StorageTypeID = 1002;

DBCC CHECKIDENT ('Dim_Storage_Type', RESEED, 2);

DELETE FROM Dim_Storages
WHERE StorageID = 1002;

DELETE FROM Dim_Storages
WHERE StorageID = 1003;

DBCC CHECKIDENT ('Dim_Storages', RESEED, 2);