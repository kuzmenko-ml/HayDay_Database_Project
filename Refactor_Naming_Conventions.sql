USE HayDay_Farm;
GO

/*EXEC sp_rename 'Dim_Pets.PetsID', 'PetID', 'COLUMN';
EXEC sp_rename 'Dim_Pets.PetsName', 'PetName', 'COLUMN';
EXEC sp_rename 'Dim_Products.ProductsName', 'ProductName', 'COLUMN';*/

EXEC sp_rename 'Fact_Pets_Livestock.PetsLivestockID', 'PetLivestockID', 'COLUMN';
