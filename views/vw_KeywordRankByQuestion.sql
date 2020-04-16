create view dbo.vw_KeywordRankByQuestion as
select 
    paper_id
    , question_id as QuestionNum
    , x KeywordCount
    , dense_rank() over(partition by question_id order by x desc) as KeywordRankOrder
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
) as t;
