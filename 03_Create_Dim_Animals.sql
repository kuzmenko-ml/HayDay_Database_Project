USE HayDay_Farm;
GO

CREATE TABLE Dim_Animals(
	AnimalID INT PRIMARY KEY IDENTITY(1,1),
	AnimalName NVARCHAR(20) NOT NULL,
	ProductionTimeMinutes INT NOT NULL);