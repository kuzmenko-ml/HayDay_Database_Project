USE HayDay_Farm;
GO

IF OBJECT_ID('Dim_Buildings', 'U') IS NOT NULL
    DROP TABLE Dim_Buildings;
GO

CREATE TABLE Dim_Buildings(
    BuildingID INT PRIMARY KEY IDENTITY(1,1),
    BuildingName NVARCHAR(35) NOT NULL,
    BuildingRequiredLevel INT NOT NULL,
    LocationID INT NOT NULL); 