USE HayDay_Farm;
GO

CREATE TABLE Fact_Farm_Livestock(
LivestockID INT PRIMARY KEY IDENTITY(1,1),
FarmID INT NOT NULL,
AnimalID INT NOT NULL,
AnimalQuantity INT NOT NULL);

ALTER TABLE Fact_Farm_Livestock DROP CONSTRAINT FK_FactFarmLivestock_DimAnimals;