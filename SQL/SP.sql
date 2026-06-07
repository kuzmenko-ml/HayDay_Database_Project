USE HayDay_Farm;
GO

CREATE PROCEDURE SP_NewFarm
	@FarmName NVARCHAR(50),
	@FarmLevel INT,
	@FarmExperience INT,
	@FarmCreatedAt DATE
AS
BEGIN
	BEGIN TRANSACTION; 
    BEGIN TRY

		INSERT INTO Dim_Farms 
		VALUES (@FarmName,@FarmLevel,@FarmExperience,@FarmCreatedAt)

		DECLARE @NewFarmID INT;
		SET @NewFarmID = SCOPE_IDENTITY();

		INSERT INTO Fact_Farm_Wallet (FarmID, CurrencyID, CurrencyQuantity)
        VALUES (@NewFarmID, 1, 500);

		INSERT INTO Dim_Storages (FarmID, StorageTypeID, StorageCapacity)
		VALUES (@NewFarmID, 1, 50);

		INSERT INTO Dim_Storages (FarmID, StorageTypeID, StorageCapacity)
		VALUES (@NewFarmID, 2, 50);

		IF @FarmLevel >= 27
		BEGIN
			INSERT INTO Dim_Storages (FarmID, StorageTypeID, StorageCapacity)
			VALUES (@NewFarmID, 3, 10);
		END

		COMMIT TRANSACTION;
		PRINT 'Farm created successfully!';
	END TRY
	BEGIN CATCH
        ROLLBACK TRANSACTION; 
        PRINT 'Error. Farm was not created.';
    END CATCH
END;