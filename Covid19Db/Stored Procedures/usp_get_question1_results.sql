-- =============================================
-- Author:		Espinoza, Segundo
-- Create date: 4/13/2020
-- Description:	Returns dataset for answering question: What is known about transmission, incubation, and environmental stability?​
-- =============================================
CREATE PROCEDURE [dbo].[usp_get_question1_results]
AS
BEGIN
SELECT        TOP (50) dbo.AllPapers.paper_id, dbo.AllPapers.title AS Article, dbo.AllPapers.body_text, dbo.AllPapers.publish_date, dbo.KeywordCounts.count_transmission, dbo.KeywordCounts.count_incubation, 
                         dbo.KeywordCounts.count_environmental_stability, dbo.KeywordCounts.count_covid19, dbo.KeywordCounts.count_sarscov2, 
                         SUM(dbo.KeywordCounts.count_transmission + dbo.KeywordCounts.count_incubation + dbo.KeywordCounts.count_environmental_stability) AS 'All Keyword Totals', dbo.JRanked.Journal, dbo.JRanked.CiteScore18, 
                         dbo.JRanked.SJR, dbo.JRanked.ImpactFactor
FROM            dbo.AllPapers INNER JOIN
                         dbo.JRanked ON dbo.AllPapers.journal = dbo.JRanked.Journal OR dbo.AllPapers.journal = dbo.JRanked.JournalAbbrOfficial INNER JOIN
                         dbo.KeywordCounts ON dbo.AllPapers.paper_id = dbo.KeywordCounts.paper_id
WHERE        (dbo.KeywordCounts.count_transmission > 0) AND (dbo.KeywordCounts.count_incubation > 0) AND (dbo.KeywordCounts.count_covid19 > 0) OR
                         (dbo.KeywordCounts.count_transmission > 0) AND (dbo.KeywordCounts.count_incubation > 0) AND (dbo.KeywordCounts.count_sarscov2 > 0)
GROUP BY dbo.AllPapers.title, dbo.AllPapers.body_text, dbo.AllPapers.paper_id, dbo.KeywordCounts.count_transmission, dbo.KeywordCounts.count_incubation, dbo.KeywordCounts.count_environmental_stability, 
                         dbo.JRanked.CiteScore18, dbo.JRanked.SJR, dbo.JRanked.Journal, dbo.JRanked.ImpactFactor, dbo.KeywordCounts.count_covid19, dbo.KeywordCounts.count_sarscov2, dbo.AllPapers.publish_date
ORDER BY 'All Keyword Totals' DESC, dbo.JRanked.CiteScore18 DESC, dbo.JRanked.SJR DESC
END
