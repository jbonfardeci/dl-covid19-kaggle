CREATE VIEW dbo.vw_journals_ranked_sjr
AS
SELECT DISTINCT 
                         dbo.JRankBySJR.Title AS Journal, dbo.JRankBySJR.Rank, CAST(dbo.JRankBySJR.SJR / 1000 AS NUMERIC(10, 3)) AS SJR, dbo.JRankBySJR.Total_Docs_2018, dbo.JRankBySJR.Total_Refs, 
                         dbo.JRankBySJR.Total_Cites_3years, dbo.JRankBySJR.Citable_Docs_3years, dbo.JRankBySJR.Total_Docs_3years, dbo.JRankBySJR.Publisher, dbo.JRankBySJR.Country, dbo.vw_journals_issn.JournalAbbrOfficial, 
                         dbo.vw_journals_issn.JournalNameArticle, dbo.vw_journals_issn.JournalID
FROM            dbo.JRankBySJR INNER JOIN
                         dbo.vw_journals_issn ON TRIM(LOWER(dbo.JRankBySJR.Title)) = TRIM(LOWER(dbo.vw_journals_issn.JournalNameArticle)) OR
                         TRIM(LOWER(dbo.JRankBySJR.Title)) = TRIM(LOWER(dbo.vw_journals_issn.JournalNameOfficial))

GO
EXECUTE sp_addextendedproperty @name = N'MS_DiagramPane1', @value = N'[0E232FF0-B466-11cf-A24F-00AA00A3EFFF, 1.00]
Begin DesignProperties = 
   Begin PaneConfigurations = 
      Begin PaneConfiguration = 0
         NumPanes = 4
         Configuration = "(H (1[41] 4[35] 2[16] 3) )"
      End
      Begin PaneConfiguration = 1
         NumPanes = 3
         Configuration = "(H (1 [50] 4 [25] 3))"
      End
      Begin PaneConfiguration = 2
         NumPanes = 3
         Configuration = "(H (1 [50] 2 [25] 3))"
      End
      Begin PaneConfiguration = 3
         NumPanes = 3
         Configuration = "(H (4 [30] 2 [40] 3))"
      End
      Begin PaneConfiguration = 4
         NumPanes = 2
         Configuration = "(H (1 [56] 3))"
      End
      Begin PaneConfiguration = 5
         NumPanes = 2
         Configuration = "(H (2 [66] 3))"
      End
      Begin PaneConfiguration = 6
         NumPanes = 2
         Configuration = "(H (4 [50] 3))"
      End
      Begin PaneConfiguration = 7
         NumPanes = 1
         Configuration = "(V (3))"
      End
      Begin PaneConfiguration = 8
         NumPanes = 3
         Configuration = "(H (1[56] 4[18] 2) )"
      End
      Begin PaneConfiguration = 9
         NumPanes = 2
         Configuration = "(H (1 [75] 4))"
      End
      Begin PaneConfiguration = 10
         NumPanes = 2
         Configuration = "(H (1[66] 2) )"
      End
      Begin PaneConfiguration = 11
         NumPanes = 2
         Configuration = "(H (4 [60] 2))"
      End
      Begin PaneConfiguration = 12
         NumPanes = 1
         Configuration = "(H (1) )"
      End
      Begin PaneConfiguration = 13
         NumPanes = 1
         Configuration = "(V (4))"
      End
      Begin PaneConfiguration = 14
         NumPanes = 1
         Configuration = "(V (2))"
      End
      ActivePaneConfig = 0
   End
   Begin DiagramPane = 
      Begin Origin = 
         Top = 0
         Left = 0
      End
      Begin Tables = 
         Begin Table = "JRankBySJR"
            Begin Extent = 
               Top = 15
               Left = 321
               Bottom = 313
               Right = 516
            End
            DisplayFlags = 280
            TopColumn = 0
         End
         Begin Table = "vw_journals_issn"
            Begin Extent = 
               Top = 31
               Left = 62
               Bottom = 267
               Right = 259
            End
            DisplayFlags = 280
            TopColumn = 0
         End
      End
   End
   Begin SQLPane = 
   End
   Begin DataPane = 
      Begin ParameterDefaults = ""
      End
   End
   Begin CriteriaPane = 
      Begin ColumnWidths = 11
         Column = 1440
         Alias = 1605
         Table = 1170
         Output = 720
         Append = 1400
         NewValue = 1170
         SortType = 1350
         SortOrder = 1410
         GroupBy = 1350
         Filter = 1350
         Or = 1350
         Or = 1350
         Or = 1350
      End
   End
End
', @level0type = N'SCHEMA', @level0name = N'dbo', @level1type = N'VIEW', @level1name = N'vw_journals_ranked_sjr';


GO
EXECUTE sp_addextendedproperty @name = N'MS_DiagramPaneCount', @value = 1, @level0type = N'SCHEMA', @level0name = N'dbo', @level1type = N'VIEW', @level1name = N'vw_journals_ranked_sjr';

