USE HayDay_Farm;
GO

IF OBJECT_ID('Fact_Fishing_Spots', 'U') IS NOT NULL
	DROP TABLE Fact_Fishing_Spots;
GO

CREATE TABLE Fact_Fishing_Spots(
RecordFishingSpotID INT PRIMARY KEY IDENTITY(1,1),
FarmID INT NOT NULL,
LocationID INT NOT NULL,
SpotID INT NOT NULL);