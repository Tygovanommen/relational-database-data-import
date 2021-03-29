CREATE PROCEDURE zipcode_import as
    INSERT INTO zipcode
    SELECT * FROM zipcode_ghost
go