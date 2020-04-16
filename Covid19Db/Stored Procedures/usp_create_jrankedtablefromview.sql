-- =============================================
-- Author:		Espinoza, Segundo
-- Create date: 4/14/2020
-- Description:	Recreates JRanked table from vw_journals_ranked_combined view
-- =============================================
CREATE PROCEDURE [usp_create_jrankedtablefromview]
AS
BEGIN
	DROP TABLE [dbo].[JRanked]
	

	SELECT *
	INTO [dbo].[JRanked]
	FROM vw_journals_ranked_combined

	
END
