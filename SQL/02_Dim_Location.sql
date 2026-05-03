USE HayDay_Farm;
GO

IF OBJECT_ID('Dim_Location','U') IS NOT NULL
	DROP TABLE Dim_Location
GO

CREATE TABLE Dim_Location(
	LocationID INT PRIMARY KEY IDENTITY(1,1),
	LocationName NVARCHAR(20) NOT NULL,
	LocationRequiredLevel INT NOT NULL);