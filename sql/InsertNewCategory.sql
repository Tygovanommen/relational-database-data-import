CREATE PROCEDURE InsertNewCategory
    @CategoryName VARCHAR(255),
    @CategoryDescription VARCHAR(255) = NULL,
    @ParentCategoryId INT = NULL

AS

BEGIN TRANSACTION
    BEGIN TRY

        INSERT INTO category(parent_category_id, category_name, category_description)
        VALUES (@ParentCategoryId, @CategoryName, @CategoryDescription)
        COMMIT TRANSACTION

    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION
        PRINT ERROR_MESSAGE()
    END CATCH
go

