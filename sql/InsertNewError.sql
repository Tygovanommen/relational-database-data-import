CREATE PROCEDURE InsertNewError @ErrorMessage VARCHAR(MAX),
                                @ErrorProcedure VARCHAR(255) = NULL,
                                @SourceTable VARCHAR(255) = NULL,
                                @SourceRow INT = NULL,
                                @TargetTable VARCHAR(255) = NULL
AS
    IF NOT EXISTS(SELECT *
                  FROM INFORMATION_SCHEMA.TABLES
                  WHERE TABLE_SCHEMA = 'dbo'
                    AND TABLE_NAME = 'product_import_error_log')
        BEGIN
            CREATE TABLE [product_import_error_log]
            (
                id              INT IDENTITY NOT NULL,
                error_message   VARCHAR(MAX) NOT NULL,
                error_procedure VARCHAR(255),
                source_table    VARCHAR(255),
                source_row      INT,
                target_table    VARCHAR(255)
            )
            INSERT INTO product_import_error_log
            VALUES (@ErrorMessage, @ErrorProcedure, @SourceTable, @SourceRow, @TargetTable)
        END
    ELSE
        BEGIN
            INSERT INTO product_import_error_log
            VALUES (@ErrorMessage, @ErrorProcedure, @SourceTable, @SourceRow, @TargetTable)
        END
go

