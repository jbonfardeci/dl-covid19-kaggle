-- select top 100 * from dbo.vw_TableauTable
create view dbo.vw_TableauTable as 

with inst as (
    select 
        paper_id 
        , string_agg(cast(i.institution_name as nvarchar(max)), '; ') as AuthorInstitutions
    from 
        dbo.Authored as auth 

        inner join dbo.Affiliation as af 
            on auth.author_hash = af.author_hash

        inner join dbo.Institution as i 
            on af.institution_hash = i.hash_id
    group by 
        paper_id
)

, kw as (
    select 
        paper_id 
        , isnull([1],0) as Q01KeywordCount
        , isnull([2],0) as Q02KeywordCount
        , isnull([3],0) as Q03KeywordCount
        , isnull([4],0) as Q04KeywordCount
        , isnull([5],0) as Q05KeywordCount
        , isnull([6],0) as Q06KeywordCount
        , isnull([7],0) as Q07KeywordCount
        , isnull([8],0) as Q08KeywordCount
        , isnull([9],0) as Q09KeywordCount
    from (
        select 
            paper_id
            , q.question_id
            , convert(real, sum(KeywordCount)) as x
        from 
            dbo.KeywordCountsUnpivot as k

            inner join dbo.Question as q
                on k.Keyword in (q.keyword1, q.keyword2, q.keyword3, q.keyword4)
        group by
            paper_id
            , q.question_id
    ) as t
    pivot(sum(x) for question_id in (
        [1], [2], [3], [4], [5], [6], [7], [8], [9]
    )) as p
)

select 
    p.paper_id
    , isnull(p.title, 'N/A') as Title
    , isnull(p.Abstract, 'N/A') as Abstract 
    , isnull(body_text, 'N/A') as BodyText
    , coalesce(jm.StandardJournalName, jm.JournalNameInData, 'N/A') as Journal
    , ag.Authors
    , p.AuthorRank
    , p.AuthorRankNormal
    , p.JournalRank
    , p.JournalRankNormal
    , p.Recency
    , p.RecencyNormal
    , p.CitedAuthorsRank
    , p.CitedAuthorsRankNormal
    , inst.AuthorInstitutions
    , p.CitedInstitutionRank as AuthorInstitutionsRank
    , p.CitedInstitutionRankNormal as AuthorInstitutionsRankNormal
    , p.KmeansCluster
    , Q01KeywordCount
    , Q02KeywordCount
    , Q03KeywordCount
    , Q04KeywordCount
    , Q05KeywordCount
    , Q06KeywordCount
    , Q07KeywordCount
    , Q08KeywordCount
    , Q09KeywordCount
from 
    dbo.AllPapers as p
    
    inner join kw
        on p.paper_id = kw.paper_id

    inner join dbo.AuthorsAgg as ag 
        on p.paper_id = ag.paper_id

    left join dbo.JournalMapping as jm 
        on p.JournalId = jm.Id

    left join inst 
        on p.paper_id = inst.paper_id
;
