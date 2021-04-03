CREATE PROCEDURE ImportCrustData AS

DECLARE
    @CrustName VARCHAR(255),
    @CrustPrice DECIMAL(4, 2),
    @CrustDescription VARCHAR(255),
    @CrustiDiameter TINYINT,
    @CrustCategoryId INT,
    @CrustTaxRateId INT,
    @CrustProductId INT

DECLARE cursor_crust CURSOR
FOR SELECT
        naam, toeslag, omschrijving, diameter
    FROM
         pizza_bodems_ghost

IF NOT EXISTS(SELECT id FROM category WHERE category_name = 'Pizza Crusts')
    BEGIN
        EXEC InsertNewCategory 'Pizza Crusts', 'De Pizzabodems'
    END
    SET @CrustCategoryId = (SELECT id FROM category WHERE category_name = 'Pizza Crusts')

IF NOT EXISTS(SELECT id FROM tax_rate WHERE tax_rate_type = 'Merged Data Tax Rate')
    BEGIN
        INSERT INTO tax_rate(tax_rate, tax_rate_type, date_from)
        VALUES (0, 'Merged Data Tax Rate', getdate())
    END

    SET @CrustTaxRateId = (SELECT id FROM tax_rate WHERE tax_rate_type = 'Merged Data Tax Rate' AND date_to IS NULL)

OPEN cursor_crust

FETCH NEXT FROM cursor_crust INTO @CrustName, @CrustPrice, @CrustDescription, @CrustiDiameter

WHILE @@FETCH_STATUS = 0
    BEGIN
        IF NOT EXISTS(SELECT @CrustName FROM product WHERE product_name = @CrustName)
            BEGIN
                -- Get new product id from InsertNewProduct SP output variable.
                EXEC @CrustProductId = InsertNewProduct
                    @CrustCategoryId,
                    @CrustName,
                    1, -- IsEnabled
                    1, -- Stock quantity
                    @CrustPrice,
                    @CrustTaxRateId

                            -- Save new product in crust table.
                BEGIN TRANSACTION
                    BEGIN TRY
                        INSERT INTO crust(product_id, crust_size_dia_cm)
                        VALUES (
                                @CrustProductId,
                                @CrustiDiameter
                               )
                        COMMIT TRANSACTION
                    END TRY
                    BEGIN CATCH
                        ROLLBACK TRANSACTION
                        PRINT ERROR_MESSAGE()
                    END CATCH
            END

        FETCH NEXT FROM cursor_crust INTO @CrustName, @CrustPrice, @CrustDescription, @CrustiDiameter
    END

CLOSE cursor_crust
DEALLOCATE cursor_crust
go

