select 
    p.paper_id
    , AuthorRank
    , JournalRank
    , Recency
    , CitedAuthorsRank
    , CitedInstitutionRank
    , q01
    , q02
    , q03
    , q04
    , q05
    , q06
    , q07
    , q08
    , q09
    , q10
from 
    dbo.AllPapers as p
    
    inner join dbo.PaperKeywordRankByQuestion as kw
        on p.paper_id = kw.paper_id;
