USE HayDay_Farm;
GO

IF OBJECT_ID('Dim_Town_Buildings', 'U') IS NOT NULL
    DROP TABLE Dim_Town_Buildings;
GO

CREATE TABLE Dim_Town_Buildings(
    TownBuildingID INT PRIMARY KEY IDENTITY(1,1),
    TownBuildingName NVARCHAR(35) NOT NULL,
    FarmID INT NOT NULL,
    TownBuildingRequiredReputation INT NOT NULL, 
    LocationID INT NOT NULL);