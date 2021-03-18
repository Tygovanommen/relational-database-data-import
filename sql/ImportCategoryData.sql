CREATE PROCEDURE ImportCategoryData AS

DECLARE
    @categorie    VARCHAR(255),
    @Subcategorie VARCHAR(255)

DECLARE
    cursor_categorie CURSOR
        FOR SELECT DISTINCT categorie,
                            subcategorie
            FROM pizza_ingredienten_ghost

    OPEN cursor_categorie

    FETCH NEXT FROM cursor_categorie INTO @categorie, @Subcategorie
    WHILE @@FETCH_STATUS = 0
        BEGIN
            BEGIN TRANSACTION
                BEGIN TRY


                    IF NOT EXISTS(SELECT category_name FROM category WHERE category_name = @categorie)
                        BEGIN
                            EXEC InsertNewCategory @categorie
                        END

                    IF NOT EXISTS(SELECT category_name FROM category WHERE category_name = @Subcategorie)
                        BEGIN
                            DECLARE @parentId INT
                            SET @parentId = (SELECT id FROM category WHERE category_name = @categorie)
                            EXEC InsertNewCategory @Subcategorie, NULL,
                                 @parentId
                        END
                    COMMIT TRANSACTION
                END TRY
                BEGIN CATCH
                    ROLLBACK TRANSACTION
                    PRINT ERROR_MESSAGE()
                    PRINT ERROR_LINE()
                    PRINT ERROR_PROCEDURE()
                END CATCH
                FETCH NEXT FROM cursor_categorie INTO @categorie, @Subcategorie
        END

    CLOSE cursor_categorie
    DEALLOCATE cursor_categorie
go

