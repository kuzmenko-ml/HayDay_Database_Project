USE HayDay_Farm;
GO

CREATE TABLE Dim_Town_Buildings(
TownBuildingID INT PRIMARY KEY IDENTITY(1,1),
TownBuildingName NVARCHAR(35) NOT NULL,
TownBuildingRequiredReputation INT NOT NULL,
TownBuildingSpotQuantity INT NOT NULL DEFAULT 1,
LocationID INT NOT NULL);