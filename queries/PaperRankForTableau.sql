select 
    *
    , (x - min(x) over()) / (max(x) over() - min(x) over()) as Relevance
    , dense_rank() over(order by x desc) as RankOrder
from (
    select 
        p.paper_id
        , isnull(p.title, 'N/A') as Title
        , isnull(p.Abstract, p.body_text) as BodyText
        , p.AuthorRank
        , p.JournalRank
        , p.Recency
        , p.CitedAuthorsRank
        , p.CitedInstitutionRank
        , kw.q01 as KeywordRank

        , ( 
            -- Total Rank
            isnull(AuthorRank,0)
            + isnull(JournalRank,0)
            + isnull(Recency,0)
            + isnull(CitedAuthorsRank,0)
            + isnull(CitedInstitutionRank,0)
            + isnull(kw.q01,0) -- KeywordRank
        ) as x
    from 
        dbo.AllPapers as p
        
        inner join dbo.PaperKeywordRankByQuestion as kw
            on p.paper_id = kw.paper_id
) as t