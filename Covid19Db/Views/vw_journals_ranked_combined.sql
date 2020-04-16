
CREATE view dbo.vw_journals_ranked_combined AS
select        
    jm.Id as JournalId 
    , trim(coalesce(jm.StandardJournalName, sjr.Title, scop.Journal, pub.Journal_title, jm.JournalNameInData)) AS Journal
    , scop.CiteScore18
    , CAST(sjr.SJR / 1000 AS NUMERIC(10, 3)) AS SJR
    , coalesce(jm.ImpactFactor, scop.CiteScore18, CAST(sjr.SJR / 1000 AS NUMERIC(10, 3))) as ImpactFactor
    , pub.NLM_TA as JournalAbbrOfficial
    , pub.Journal_title as JournalNameOfficial
    , coalesce(jm.PrintISSN, scop.Print_ISSN, pub.pISSN, sjr.Issn) as pISSN
    , coalesce(jm.ElectronicISSN, scop.E_ISSN, pub.eISSN, sjr.Issn) as eISSN
    , coalesce(jm.Publisher, sjr.Publisher, scop.Publisher_s_Name, pub.Publisher) as Publisher
    , jm.ChiefEditor
from            
    dbo.JournalMapping as jm
    
    left join dbo.JRankBySJR as sjr
        on TRIM(LOWER(isnull(jm.StandardJournalName, jm.JournalNameInData))) = TRIM(LOWER(sjr.Title))
    
    left join dbo.JRankByScopus as scop
        on TRIM(LOWER(isnull(jm.StandardJournalName, jm.JournalNameInData))) = TRIM(LOWER(scop.Journal)) 
            or TRIM(LOWER(sjr.Title)) = TRIM(LOWER(scop.Journal))

    left join dbo.JByPubMed as pub
        on TRIM(LOWER(isnull(jm.StandardJournalName, jm.JournalNameInData))) = TRIM(LOWER(pub.Journal_title))
            or TRIM(LOWER(sjr.Title)) = TRIM(LOWER(pub.NLM_TA))
            or TRIM(LOWER(scop.Journal)) = TRIM(LOWER(pub.NLM_TA))
where        
    not (
            scop.CiteScore18 is null
            and sjr.SJR is null
            and ImpactFactor is null
        )
;

GO
EXECUTE sp_addextendedproperty @name = N'MS_DiagramPane1', @value = N'[0E232FF0-B466-11cf-A24F-00AA00A3EFFF, 1.00]
Begin DesignProperties = 
   Begin PaneConfigurations = 
      Begin PaneConfiguration = 0
         NumPanes = 4
         Configuration = "(H (1[41] 4[37] 2[19] 3) )"
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
         Begin Table = "vw_journals_issn"
            Begin Extent = 
               Top = 6
               Left = 38
               Bottom = 237
               Right = 235
            End
            DisplayFlags = 280
            TopColumn = 0
         End
         Begin Table = "JRankBySJR"
            Begin Extent = 
               Top = 188
               Left = 289
               Bottom = 338
               Right = 526
            End
            DisplayFlags = 280
            TopColumn = 6
         End
         Begin Table = "JRankByScopus"
            Begin Extent = 
               Top = 4
               Left = 353
               Bottom = 170
               Right = 585
            End
            DisplayFlags = 280
            TopColumn = 3
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
         Column = 2955
         Alias = 2010
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
', @level0type = N'SCHEMA', @level0name = N'dbo', @level1type = N'VIEW', @level1name = N'vw_journals_ranked_combined';


GO
EXECUTE sp_addextendedproperty @name = N'MS_DiagramPaneCount', @value = 1, @level0type = N'SCHEMA', @level0name = N'dbo', @level1type = N'VIEW', @level1name = N'vw_journals_ranked_combined';

