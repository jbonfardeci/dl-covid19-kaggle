
create view dbo.vw_journals_issn as
select
   jm.JournalNameInData as JournalNameArticle
   , pub.Journal_title as JournalNameOfficial
   , pub.NLM_TA as JournalAbbrOfficial
   , jm.ChiefEditor
   , jm.PrintISSN as pISSN
   , jm.ElectronicISSN as eISSN
   , jm.Publisher
   , jm.ImpactFactor
   , jm.Id as JournalId
from 
    dbo.JournalMapping as jm 

    left join dbo.JByPubMed as pub
        on TRIM(LOWER(jm.JournalNameInData)) = TRIM(LOWER(pub.Journal_title)) or
            TRIM(LOWER(jm.JournalNameInData)) = TRIM(LOWER(pub.NLM_TA))
;
