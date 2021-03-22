CREATE PROCEDURE ImportPizzaData AS

DECLARE
    @PizzaName             VARCHAR(255),
    @PizzaPrice            DECIMAL(4, 2),
    @PizzaDescription      VARCHAR(255),
    @SubCategoryId         INT,
    @PizzaTaxRateId        INT,
    @Spicy                 BIT,
    @Vegetarian            BIT,
    @SauceName             VARCHAR(255),
    @PizzaProductId        INT,
    @CrustProductId        INT,
    @SauceProductId        INT,
    @PizzaIngredientId     INT,
    @PizzaIngredientAmount TINYINT

-- Cursor for grabbing result set from pizza ingredienten staging table needed to fill target pizza product table
DECLARE
    [@cursor_pizza] CURSOR
        FOR SELECT productnaam,
                   prijs,
                   productomschrijving,
                   id AS subcategory_id,
                   spicy,
                   vegetarisch,
                   pizzasaus_standaard
            FROM pizza_ingredienten_ghost
                     LEFT JOIN category cat on subcategorie = category_name

DECLARE @cursor_pizza_ingredienten CURSOR

    SET @CrustProductId = (SELECT id
                           from product
                           WHERE product_name = 'Medium Pizza'
                             AND category_id = (select id FROM category where category_name = 'Pizza Crusts'))
    IF NOT EXISTS(SELECT id
                  FROM tax_rate
                  WHERE tax_rate_type = 'Merged Data Tax Rate')
        BEGIN
            INSERT INTO tax_rate(tax_rate, tax_rate_type, date_from)
            VALUES (0, 'Merged Data Tax Rate', getdate())
        END

    SET @PizzaTaxRateId = (SELECT id
                           FROM tax_rate
                           WHERE tax_rate_type = 'Merged Data Tax Rate'
                             AND date_to IS NULL)

    OPEN [@cursor_pizza]
    FETCH NEXT FROM [@cursor_pizza] INTO @PizzaName, @PizzaPrice, @PizzaDescription, @SubCategoryId, @Spicy, @Vegetarian, @SauceName
    WHILE @@FETCH_STATUS = 0
        BEGIN
            IF NOT EXISTS(SELECT * FROM product WHERE product_name = @PizzaName AND category_id = @SubCategoryId)
                BEGIN
                    SET @SauceProductId = (SELECT id FROM product WHERE product_name = @SauceName)

                    BEGIN TRANSACTION
                        BEGIN TRY
                            -- insert new pizza product and get new pizza product id from InsertNewProduct SP output variable.
                            EXEC @PizzaProductId = InsertNewProduct
                                                   @SubCategoryId,
                                                   @PizzaName,
                                                   1, -- IsEnabled
                                                   1, -- Stock quantity
                                                   @PizzaPrice,
                                                   @PizzaTaxRateId,
                                                   @PizzaDescription,
                                                   @Vegetarian,
                                                   @Spicy

                            INSERT INTO pizza(product_id, sauce_product_id, crust_product_id)
                            VALUES (@PizzaProductId, @SauceProductId, @CrustProductId)

                            -- Get ingredients related to previously inserted pizza product. Use this result set to populate target
                            -- pizza_ingredients link table.

                            -- Cursor for grabbing ingredient data from staging table to fill pizza_ingredient link table.
                            SET
                                @cursor_pizza_ingredienten = CURSOR
                                    FOR SELECT id, aantalkeer_ingredient
                                        FROM product
                                                 RIGHT JOIN pizza_ingredienten_ghost pig
                                                            ON product.product_name = pig.ingredientnaam
                                        WHERE productnaam = @PizzaName AND NOT @SubCategoryId = category_id

                            OPEN @cursor_pizza_ingredienten
                            FETCH NEXT FROM @cursor_pizza_ingredienten INTO @PizzaIngredientId, @PizzaIngredientAmount
                            WHILE @@FETCH_STATUS = 0
                                BEGIN
                                    INSERT INTO pizza_ingredient (ingredient_product_id, pizza_product_id, amount)
                                    VALUES (@PizzaIngredientId, @PizzaProductId, @PizzaIngredientAmount)
                                    FETCH NEXT FROM @cursor_pizza_ingredienten INTO @PizzaIngredientId, @PizzaIngredientAmount
                                END
                            CLOSE @cursor_pizza_ingredienten
                            DEALLOCATE @cursor_pizza_ingredienten
                            COMMIT TRANSACTION
                        END TRY
                        BEGIN CATCH
                            ROLLBACK TRANSACTION
                            PRINT ERROR_MESSAGE()
                            PRINT ERROR_PROCEDURE()
                        END CATCH
                END

            FETCH NEXT FROM [@cursor_pizza] INTO @PizzaName, @PizzaPrice, @PizzaDescription, @SubCategoryId, @Spicy, @Vegetarian, @SauceName
        END

    CLOSE [@cursor_pizza]
    DEALLOCATE [@cursor_pizza]
go

