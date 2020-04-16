CREATE OR ALTER FUNCTION dbo.fn_CountOccurrences(@p_FullString VARCHAR(MAX), @p_SearchString VARCHAR(200))
RETURNS INT
BEGIN
    -- Source: http://www.sql-server-helper.com/functions/count-string.aspx
    RETURN (LEN(@p_FullString) - LEN(REPLACE(UPPER(@p_FullString), UPPER(@p_SearchString), ''))) / LEN(@p_SearchString);
END;
