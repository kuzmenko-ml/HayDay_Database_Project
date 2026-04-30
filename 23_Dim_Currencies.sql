USE HayDay_Farm;
GO

CREATE TABLE Dim_Currencies(
CurrencyID INT PRIMARY KEY IDENTITY(1,1),
CurrencyName NVARCHAR(25) NOT NULL,
CurrencyIsTemporary BIT NOT NULL);