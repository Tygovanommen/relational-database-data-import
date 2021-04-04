CREATE PROCEDURE zipcode_import as
    INSERT INTO zipcode
    SELECT * FROM zipcode_ghost

    DROP TABLE zipcode_ghost
go