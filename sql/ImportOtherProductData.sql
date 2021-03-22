CREATE PROCEDURE ImportOtherProductData AS

DECLARE
    @OtherProductName        VARCHAR(255),
    @OtherProductPrice       DECIMAL(4, 2),
    @OtherProductDescription VARCHAR(255),
    @SubCategoryId           INT,
    @OtherProductTaxRateId   INT,
    @Spicy                   BIT,
    @Vegetarian              BIT

DECLARE
    [@cursor_Other_Product] CURSOR
        FOR SELECT productnaam,
                   prijs,
                   productomschrijving,
                   id AS subcategory_id,
                   spicy,
                   vegetarisch
            FROM overige_producten_ghost
                     LEFT JOIN category cat on subcategorie = category_name

    IF NOT EXISTS(SELECT id
                  FROM tax_rate
                  WHERE tax_rate_type = 'Merged Data Tax Rate')
        BEGIN
            INSERT INTO tax_rate(tax_rate, tax_rate_type, date_from)
            VALUES (0, 'Merged Data Tax Rate', getdate())
        END

    SET @OtherProductTaxRateId = (SELECT id
                                  FROM tax_rate
                                  WHERE tax_rate_type = 'Merged Data Tax Rate'
                                    AND date_to IS NULL)

    OPEN [@cursor_Other_Product]
    FETCH NEXT FROM [@cursor_Other_Product] INTO @OtherProductName, @OtherProductPrice, @OtherProductDescription, @SubCategoryId, @Spicy, @Vegetarian
    WHILE @@FETCH_STATUS = 0
        BEGIN
            IF NOT EXISTS(SELECT * FROM product WHERE product_name = @OtherProductName AND category_id = @SubCategoryId)
                BEGIN

                    BEGIN TRANSACTION
                        BEGIN TRY
                            -- insert new pizza product and get new pizza product id from InsertNewProduct SP output variable.
                            EXEC InsertNewProduct
                                 @SubCategoryId,
                                 @OtherProductName,
                                 1, -- IsEnabled
                                 1, -- Stock quantity
                                 @OtherProductPrice,
                                 @OtherProductTaxRateId,
                                 @OtherProductDescription,
                                 @Vegetarian,
                                 @Spicy
                            COMMIT TRANSACTION
                        END TRY
                        BEGIN CATCH
                            ROLLBACK TRANSACTION
                            PRINT ERROR_MESSAGE()
                            PRINT ERROR_PROCEDURE()
                        END CATCH
                END

            FETCH NEXT FROM [@cursor_Other_Product] INTO @OtherProductName, @OtherProductPrice, @OtherProductDescription, @SubCategoryId, @Spicy, @Vegetarian
        END
go

