CREATE PROCEDURE ImportCategoryData AS

DECLARE
    @categorie VARCHAR(255),
    @Subcategorie VARCHAR(255)

DECLARE cursor_categorie CURSOR
FOR SELECT DISTINCT
        categorie, subcategorie
    FROM
         pizza_ingredienten_ghost

OPEN cursor_categorie

FETCH NEXT FROM cursor_categorie INTO @categorie, @Subcategorie

WHILE @@FETCH_STATUS = 0
    BEGIN

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

        FETCH NEXT FROM cursor_categorie INTO @categorie, @Subcategorie
    END

CLOSE cursor_categorie
DEALLOCATE cursor_categorie
go

