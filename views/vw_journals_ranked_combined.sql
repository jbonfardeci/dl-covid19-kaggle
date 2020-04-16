
create view dbo.vw_journals_ranked_combined AS
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
