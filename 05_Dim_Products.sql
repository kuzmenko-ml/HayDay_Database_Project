USE HayDay_Farm;
GO

IF OBJECT_ID('Dim_Products','U') IS NOT NULL
	DROP TABLE Dim_Products
GO

CREATE TABLE Dim_Products(
ProductID INT PRIMARY KEY IDENTITY(1,1),
ProductsName NVARCHAR(25) NOT NULL,
ProductRequiredLevel INT NOT NULL,
ProductMaxPrice INT NOT NULL,
ProductExperience INT NOT NULL,
ProductTimeMinutes INT NOT NULL,
ProductMachineID INT NOT NULL);

EXEC sp_rename 'Dim_Products.ProductMachineID', 'BuildingID', 'COLUMN';