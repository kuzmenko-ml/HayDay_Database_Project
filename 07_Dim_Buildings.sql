USE HayDay_Farm;
GO

CREATE TABLE Dim_Buildings(
BuildingID INT PRIMARY KEY IDENTITY(1,1),
BuildingName NVARCHAR(35) NOT NULL,
BuildingRequiredLevel INT NOT NULL);