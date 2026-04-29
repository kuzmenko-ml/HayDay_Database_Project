USE HayDay_Farm;
GO

CREATE TABLE Dim_Location(
	LocationID INT PRIMARY KEY IDENTITY(1,1),
	LocationName NVARCHAR(20) NOT NULL,
	RequiredLevel INT NOT NULL);