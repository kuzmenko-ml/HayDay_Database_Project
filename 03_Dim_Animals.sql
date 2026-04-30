USE HayDay_Farm;
GO

IF OBJECT_ID('Dim_Animals','U') IS NOT NULL
	DROP TABLE Dim_Animals
GO

CREATE TABLE Dim_Animals(
	AnimalID INT PRIMARY KEY IDENTITY(1,1),
	AnimalName NVARCHAR(20) NOT NULL,
	ProductionTimeMinutes INT NOT NULL,
	AnimalRequiredLevel INT NOT NULL,
	AnimalExperience INT NOT NULL);