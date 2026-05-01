USE HayDay_Farm;
GO

IF OBJECT_ID('Fact_Pets_Livestock','U') IS NOT NULL
	DROP TABLE Fact_Pets_Livestock
GO

CREATE TABLE Fact_Pets_Livestock(
PetLivestockID INT PRIMARY KEY IDENTITY(1,1),
FarmID INT NOT NULL,
PetID INT NOT NULL,
PetQuantity INT NOT NULL);