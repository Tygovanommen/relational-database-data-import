CREATE PROCEDURE InsertNewProduct
    @CategoryId INT,
    @ProductName VARCHAR(255),
    @Enabled BIT,
    @Stock_Quantity INT,
    @Price DECIMAL(4, 2),
    @TaxRateId INT,
    @ProductDescription VARCHAR(255) = NULL,
    @Vegetarian BIT = NULL,
    @Spicy BIT = NULL
    AS

DECLARE @ProductId INT

BEGIN TRANSACTION
    BEGIN TRY
        INSERT INTO product(category_id, product_name, product_description, spicy, vegetarian, enabled, date_from)
            VALUES (
                    @CategoryId,
                    @ProductName,
                    @ProductDescription,
                    @Spicy,
                    @Vegetarian,
                    @Enabled,
                    getdate())

        -- Get product_id. SCOPE_IDENTITY gets the most recent created id.
        SET @ProductId = (SELECT SCOPE_IDENTITY())

        INSERT INTO stock(product_id, quantity, date_from)
            VALUES (
                    @ProductId,
                    @Stock_Quantity,
                    getdate()
                    )
        INSERT INTO price(product_id, price, date_from)
            VALUES (
                    @ProductId,
                    @Price,
                    getdate()
                   )
        INSERT INTO tax_rate_product(tax_rate_id, product_id)
            VALUES (@TaxRateId,
                    @ProductId)

        COMMIT TRANSACTION
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION
        PRINT ERROR_MESSAGE()
    END CATCH
go

