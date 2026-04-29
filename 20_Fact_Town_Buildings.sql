USE HayDay_Farm;
GO

CREATE TABLE Fact_Town_Buildings(
RecordTownBuildingsID INT PRIMARY KEY IDENTITY (1,1),
FarmID INT NOT NULL,
LocationID INT NOT NULL,
TownBuildingID INT NOT NULL,
TownBuildingSlotQuantity INT NOT NULL DEFAULT 1,
TownBuildingMoneyLevel INT NOT NULL DEFAULT 0,
TownBuildingXPLevel INT NOT NULL DEFAULT 0,
TownBuildingTimeLevel INT NOT NULL DEFAULT 0);