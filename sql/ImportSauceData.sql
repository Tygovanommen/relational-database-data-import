CREATE PROCEDURE ImportSauceData AS

DECLARE
    @SauceName       VARCHAR(255),
    @SauceCategoryId INT,
    @SauceTaxRateId  INT

DECLARE
    cursor_sauce CURSOR
        FOR SELECT pizzasaus_standaard
            FROM pizza_ingredienten_ghost
    IF NOT EXISTS(SELECT id
                  FROM category
                  WHERE category_name = 'Pizza Sauces')
        BEGIN
            EXEC InsertNewCategory 'Pizza Sauces', 'De Pizza Sauzen'
        END
    SET @SauceCategoryId = (SELECT id
                            FROM category
                            WHERE category_name = 'Pizza Sauces')
    IF NOT EXISTS(SELECT id
                  FROM tax_rate
                  WHERE tax_rate_type = 'Merged Data Tax Rate')
        BEGIN
            INSERT INTO tax_rate(tax_rate, tax_rate_type, date_from)
            VALUES (0, 'Merged Data Tax Rate', getdate())
        END

    SET @SauceTaxRateId = (SELECT id
                           FROM tax_rate
                           WHERE tax_rate_type = 'Merged Data Tax Rate'
                             AND date_to IS NULL)

    OPEN cursor_sauce

    FETCH NEXT FROM cursor_sauce INTO @SauceName
    WHILE @@FETCH_STATUS = 0
        BEGIN
            BEGIN TRANSACTION
                BEGIN TRY
                    IF NOT EXISTS(SELECT @SauceName FROM product WHERE product_name = @SauceName)
                        BEGIN
                            EXEC InsertNewProduct
                                 @SauceCategoryId,
                                 @SauceName,
                                 1, -- IsEnabled
                                 1, -- Stock quantity
                                 0, -- Sauce price is always 0
                                 @SauceTaxRateId
                        END
                    COMMIT TRANSACTION
                END TRY
                BEGIN CATCH
                    ROLLBACK TRANSACTION
                    PRINT ERROR_MESSAGE()
                    PRINT ERROR_LINE()
                    PRINT ERROR_PROCEDURE()
                END CATCH
                FETCH NEXT FROM cursor_sauce INTO @SauceName
        END

    CLOSE cursor_sauce
    DEALLOCATE cursor_sauce
go

