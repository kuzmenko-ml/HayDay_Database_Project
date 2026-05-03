USE HayDay_Farm;
GO

CREATE TABLE Fact_Farm_Wallet(
RecordWalletID INT PRIMARY KEY IDENTITY(1,1),
FarmID INT NOT NULL,
CurrencyID INT NOT NULL,
CurrencyQuantity INT NOT NULL);