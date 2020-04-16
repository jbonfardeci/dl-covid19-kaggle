CREATE OR ALTER FUNCTION dbo.fn_GetKeywordCounts(@p_FullString   VARCHAR(MAX)
                                                ,@p_SearchString VARCHAR(100))
RETURNS INT
BEGIN
/*
    -- Variables for development and debugging
    DECLARE @p_FullString    VARCHAR(1000) = 'Is THIS is a test sentence to test my-test stuff for testing-my sentence test. How is this for my test?';
    DECLARE @p_SearchString  VARCHAR(100) = 'my';
    DECLARE @DebugMode       BIT = 1;
*/
    DECLARE @str_Prefix                VARCHAR(10);
    DECLARE @str_Suffix                VARCHAR(10);
    DECLARE @str_SearchString          VARCHAR(100);
    DECLARE @int_TempOccurrenceCounter INT = 0;
    DECLARE @int_OccurrenceCounter     INT = 0;

    DECLARE cursor_Delimiter CURSOR FOR SELECT prefix, suffix FROM dbo.ref_word_delimiters;

    OPEN cursor_Delimiter;
    FETCH NEXT FROM cursor_Delimiter INTO @str_Prefix, @str_Suffix;

    WHILE @@FETCH_STATUS = 0
        BEGIN
            SET @str_SearchString = @str_Prefix + @p_SearchString + @str_Suffix;
            SET @int_TempOccurrenceCounter = dbo.fn_CountOccurrences(@p_FullString, @str_SearchString);
            SET @int_OccurrenceCounter = @int_OccurrenceCounter + @int_TempOccurrenceCounter;

            -- Display debugging output
            --PRINT(@str_SearchString + ' = ' + CAST(@int_TempOccurrenceCounter AS VARCHAR));

            FETCH NEXT FROM cursor_Delimiter INTO @str_Prefix, @str_Suffix;
        END;

    CLOSE cursor_Delimiter;
    DEALLOCATE cursor_Delimiter;

    -- Display debugging output
    --PRINT('Total occurrences of "' + @p_SearchString + '" in the corpus = ' + CAST(@int_OccurrenceCounter AS VARCHAR));

    RETURN @int_OccurrenceCounter;
END;
