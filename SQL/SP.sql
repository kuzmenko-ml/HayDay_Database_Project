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

CREATE PROCEDURE SP_AllFarms
AS
BEGIN 
	SELECT f.FarmName, f.FarmLevel, f.FarmCreatedAt,
        MAX(CASE WHEN fw.CurrencyID = 1 THEN fw.CurrencyQuantity ELSE 0 END) AS Coins,
        MAX(CASE WHEN fw.CurrencyID = 2 THEN fw.CurrencyQuantity ELSE 0 END) AS Diamonds,
        MAX(CASE WHEN s.StorageTypeID = 1 THEN s.StorageCapacity ELSE 0 END) AS Ambar,
        MAX(CASE WHEN s.StorageTypeID = 2 THEN s.StorageCapacity ELSE 0 END) AS Silo,
        MAX(CASE WHEN s.StorageTypeID = 3 THEN s.StorageCapacity ELSE 0 END) AS [Tackle box]
    FROM Dim_Farms f
    INNER JOIN Fact_Farm_Wallet fw ON f.FarmID = fw.FarmID
    INNER JOIN Dim_Storages s ON f.FarmId = s.FarmID
    GROUP BY f.FarmName, f.FarmLevel, f.FarmCreatedAt
    ORDER BY f.FarmName DESC;
END;