CREATE PROCEDURE ImportIngredientData AS

DECLARE
    @IngredientName       VARCHAR(255),
    @IngredientPrice      DECIMAL(4, 2),
    @IngredientCategoryId INT,
    @IngredientTaxRateId  INT

DECLARE
    cursor_ingredient CURSOR
        FOR SELECT Ingredient,
                   [Extra Price]
            FROM extra_ingredienten_ghost
    IF NOT EXISTS(SELECT id
                  FROM category
                  WHERE category_name = 'Pizza Ingredients')
        BEGIN
            EXEC InsertNewCategory 'Pizza Ingredients', 'De Pizza Ingredienten'
        END
    SET @IngredientCategoryId = (SELECT id
                                 FROM category
                                 WHERE category_name = 'Pizza Ingredients')
    IF NOT EXISTS(SELECT id
                  FROM tax_rate
                  WHERE tax_rate_type = 'Merged Data Tax Rate')
        BEGIN
            INSERT INTO tax_rate(tax_rate, tax_rate_type, date_from)
            VALUES (0, 'Merged Data Tax Rate', getdate())
        END

    SET @IngredientTaxRateId = (SELECT id
                                FROM tax_rate
                                WHERE tax_rate_type = 'Merged Data Tax Rate'
                                  AND date_to IS NULL)

    OPEN cursor_ingredient

    FETCH NEXT FROM cursor_ingredient INTO @IngredientName, @IngredientPrice
    WHILE @@FETCH_STATUS = 0
        BEGIN
            BEGIN TRANSACTION
                BEGIN TRY
                    IF NOT EXISTS(SELECT * FROM product WHERE product_name = @IngredientName AND category_id = @IngredientCategoryId)
                        BEGIN
                            EXEC InsertNewProduct
                                 @IngredientCategoryId,
                                 @IngredientName,
                                 1, -- IsEnabled
                                 1, -- Stock quantity
                                 @IngredientPrice,
                                 @IngredientTaxRateId
                        END
                    COMMIT TRANSACTION
                END TRY
                BEGIN CATCH
                    ROLLBACK TRANSACTION
                    PRINT ERROR_MESSAGE()
                    PRINT ERROR_LINE()
                    PRINT ERROR_PROCEDURE()
                END CATCH
                FETCH NEXT FROM cursor_ingredient INTO @IngredientName, @IngredientPrice
        END

    CLOSE cursor_ingredient
    DEALLOCATE cursor_ingredient
go

