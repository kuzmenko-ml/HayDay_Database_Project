USE HayDay_Farm;
GO

INSERT INTO Dim_Farms (FarmName, FarmLevel, FarmExperience, FarmCreatedAt) 
VALUES ('Феська', 71, 9219, '2015-05-03'), ('Ґудзик', 30, 12046, '2025-09-15');

INSERT INTO Dim_Location (LocationName, LocationRequiredLevel)
VALUES ('Main Farm ',1), ('Town ',34),('Fishing Area ',27);

SELECT * FROM Dim_Farms;
SELECT * FROM Dim_Location;

DROP TABLE Dim_Building;

SELECT * FROM Dim_Buildings;