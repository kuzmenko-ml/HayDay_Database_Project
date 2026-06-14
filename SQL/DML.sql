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

INSERT INTO Fact_Farm_Livestock (FarmID,AnimalID,AnimalQuantity)
VALUES (1,1,18),
	   (1,2,12),
	   (2,1,15);

INSERT INTO Fact_Pets_Livestock (FarmID,PetID,PetQuantity)
VALUES (1,2,3),
	   (2,2,1);


INSERT INTO Fact_Barn (StorageID,FarmID,ProductID,ProductCount)
VALUES (1,1,4,31),
	   (1,1,7,10),
	   (3,2,4,5),
	   (3,2,6,8);

INSERT INTO Fact_Silo (StorageID,FarmID,CropID,CropCount)
VALUES (2,1,3,107),
	   (2,1,1,480),
	   (4,2,1,68),
	   (4,2,2,4);

INSERT INTO Fact_Buildings (BuildingID,FarmID,LocationID,ProductionSlots,MasteryStars)
VALUES (1,1,1,8,3),
       (2,1,1,5,3),
	   (3,1,1,7,3),
	   (4,1,1,0,0),
	   (5,1,1,0,0),
	   (1,2,1,4,1),
	   (2,2,1,4,0),
	   (3,2,1,5,1),
	   (4,2,1,0,0);

INSERT INTO Fact_Tree_Bush (FarmID,TreeOrBushID,TreeOrBushCount)
VALUES (1,1,13),
	   (1,2,20),
	   (2,2,40);

INSERT INTO Fact_Town_Buildings (FarmID,LocationID,TownBuildingID,TownBuildingSlotQuantity,
							     TownBuildingMoneyLevel,TownBuildingXPLevel,TownBuildingTimeLevel)
VALUES (1,2,1,4,2,1,2),
       (1,2,2,4,1,1,1),
	   (2,2,1,2,1,1,1);

INSERT INTO Dim_Storages (FarmID,StorageTypeID,StorageCapacity)
VALUES (1,3,60),
	   (2,3,20);

INSERT INTO Fact_Tackle_Box (LocationID,StorageID,FarmID,TackleID,TackleQuantity)
VALUES (3,5,1,1,7),
       (3,5,1,2,10),
	   (3,6,2,2,15);

INSERT INTO Fact_Fishing_Spots (FarmID,LocationID,SpotID)
VALUES (1,3,1),
       (1,3,2),
	   (1,3,3),
	   (2,3,1),
	   (2,3,2);

INSERT INTO Fact_Farm_Wallet(FarmID,CurrencyID,CurrencyQuantity)
VALUES (1,1,450789),
	   (2,1,84030);

SELECT * FROM Fact_Farm_Livestock;
SELECT * FROM Fact_Pets_Livestock;
SELECT * FROM Fact_Barn;
SELECT * FROM Fact_Silo;
SELECT * FROM Fact_Buildings;
SELECT * FROM Fact_Tree_Bush;
SELECT * FROM Fact_Town_Buildings;
SELECT * FROM Fact_Tackle_Box;
SELECT * FROM Fact_Fishing_Spots;
SELECT * FROM Fact_Farm_Wallet;

EXEC SP_NewFarm @FarmName = 'Перевірка', @FarmLevel = 28, @FarmExperience = 3876, @FarmCreatedAt = '2001-08-15';
SELECT * FROM Dim_Farms;
SELECT * FROM Dim_Storages;
SELECT * FROM Fact_Farm_Wallet;

SELECT f.FarmName, f.FarmLevel,f.FarmCreatedAt,c.CurrencyName,fw.CurrencyQuantity
FROM Dim_Farms f
INNER JOIN Fact_Farm_Wallet fw ON f.FarmId = fw.FarmID
INNER JOIN Dim_Currencies c ON c.CurrencyID = fw.CurrencyID
ORDER BY FarmName DESC;

SELECT f.FarmName, f.FarmLevel, f.FarmCreatedAt,
        SUM(CASE WHEN fw.CurrencyID = 1 THEN fw.CurrencyQuantity ELSE 0 END) AS Coins,
        SUM(CASE WHEN fw.CurrencyID = 2 THEN fw.CurrencyQuantity ELSE 0 END) AS Diamonds
FROM Dim_Farms f
INNER JOIN Fact_Farm_Wallet fw ON f.FarmID = fw.FarmID
GROUP BY f.FarmName, f.FarmLevel, f.FarmCreatedAt
ORDER BY f.FarmName DESC;

SELECT f.FarmName, f.FarmLevel, f.FarmCreatedAt,
        MAX(CASE WHEN fw.CurrencyID = 1 THEN fw.CurrencyQuantity ELSE 0 END) AS Coins,
        MAX(CASE WHEN fw.CurrencyID = 2 THEN fw.CurrencyQuantity ELSE 0 END) AS Diamonds,
        MAX(CASE WHEN s.StorageTypeID = 1 THEN s.StorageCapacity ELSE 0 END) AS Ambar,
        MAX(CASE WHEN s.StorageTypeID = 2 THEN s.StorageCapacity ELSE 0 END) AS Silo,
        MAX(CASE WHEN s.StorageTypeID = 3 THEN s.StorageCapacity ELSE 0 END) AS [Tackle box]
FROM Dim_Farms f
INNER JOIN Fact_Farm_Wallet fw ON f.FarmID = fw.FarmID
INNER JOIN Dim_Storages s ON f.FarmId = s.FarmID
GROUP BY f.FarmName, f.FarmLevel, f.FarmCreatedAt
ORDER BY f.FarmName DESC;

UPDATE Dim_Storages
SET StorageCapacity = 250
WHERE StorageID = 7;

UPDATE Dim_Storages
SET StorageCapacity = 100
WHERE StorageID = 8;

UPDATE Fact_Farm_Wallet
SET CurrencyQuantity = 9810
WHERE FarmID = 3 AND CurrencyID = 1;

INSERT INTO Dim_Currencies (CurrencyName, CurrencyIsTemporary)
VALUES ('Diamonds', 1);

INSERT INTO Fact_Farm_Wallet (FarmID,CurrencyID,CurrencyQuantity)
VALUES (1,2,98),
	   (2,2,20),
	   (3,2,40);

EXEC SP_FarmInfoUpdate @FarmID = 2, @NewFarmExperience = 13333;
EXEC SP_FarmInfoUpdate @FarmID = 2, @CurrencyName = 'coins ', @NewCurrencyQuantity = 10000;
EXEC SP_FarmInfoUpdate @FarmID = 2, @StorageType = ' Silo ', @StorageCapacity = 300;
EXEC SP_AllFarms;

EXEC SP_FarmInfoUpdate @FarmID = 2, @CurrencyName = 'diamonds ', @NewCurrencyQuantity = 11;

SELECT f.FarmName,b.ProductID, b.ProductCount
FROM Dim_Farms f
INNER JOIN Fact_Barn b ON f.FarmID = b.FarmID;

CREATE PROCEDURE SP_GetProductFromBarn
	@FarmID INT,
	@ProductName NVARCHAR(50)
AS
BEGIN 
	IF EXISTS (SELECT 1 FROM Dim_Products WHERE UPPER(ProductsName) = UPPER(@ProductName))
		BEGIN
			IF EXISTS (SELECT 1 FROM Fact_Barn WHERE UPPER(ProductName) = UPPER(@ProductName))
		END
	

	SELECT f.FarmName,b.ProductID, b.ProductCount
	FROM Dim_Farms f
	INNER JOIN Fact_Barn b ON f.FarmID = b.FarmID
	WHERE f.FarmID = @FarmID;
END;

SELECT * FROM Fact_Barn;
SELECT * FROM Dim_Products;

IF UPPER(@ProductName) = (SELECT UPPER(ProductsName) FROM Dim_Products)
	BEGIN
		SET @ProductIDTemp = 
	END;

CREATE TRIGGER TR_EggsCount
ON Fact_Barn
AFTER UPDATE
AS
BEGIN
	IF EXISTS (
		SELECT 1 FROM inserted i
		INNER JOIN deleted d ON i.FarmID = d.FarmID AND i.ProductID = d.ProductID
		WHERE i.FarmID = 1 
		AND i.ProductID = 4 
		AND d.ProductCount > 0
		AND i.ProductCount = 0
	)
	BEGIN
		PRINT 'NEED TO BUY EGGS! There is 0 eggs!'
	END
END;

DROP PROCEDURE SP_AllFarms;

CREATE VIEW dbo.vw_AllFarms AS
SELECT f.FarmName, f.FarmLevel, f.FarmCreatedAt,
       MAX(CASE WHEN fw.CurrencyID = 1 THEN fw.CurrencyQuantity ELSE 0 END) AS Coins,
       MAX(CASE WHEN fw.CurrencyID = 2 THEN fw.CurrencyQuantity ELSE 0 END) AS Diamonds,
       MAX(CASE WHEN s.StorageTypeID = 1 THEN s.StorageCapacity ELSE 0 END) AS Ambar,
       MAX(CASE WHEN s.StorageTypeID = 2 THEN s.StorageCapacity ELSE 0 END) AS Silo,
       MAX(CASE WHEN s.StorageTypeID = 3 THEN s.StorageCapacity ELSE 0 END) AS [Tackle box]
FROM Dim_Farms f
INNER JOIN Fact_Farm_Wallet fw ON f.FarmID = fw.FarmID
INNER JOIN Dim_Storages s ON f.FarmID = s.FarmID
GROUP BY f.FarmName, f.FarmLevel, f.FarmCreatedAt;