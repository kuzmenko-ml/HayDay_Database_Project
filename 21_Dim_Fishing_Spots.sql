USE HayDay_Farm;
GO

IF OBJECT_ID('Dim_Fishing_Spots', 'U') IS NOT NULL
    DROP TABLE Dim_Fishing_Spots;
GO

CREATE TABLE Dim_Fishing_Spots(
SpotID INT PRIMARY KEY IDENTITY(1,1),
SpotName NVARCHAR(40) NOT NULL,
SpotCooldownMinutes INT NOT NULL,
LocationID INT NOT NULL);