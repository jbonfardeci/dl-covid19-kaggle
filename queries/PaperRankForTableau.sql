/*I added all of the normalized ranks except for keyword rank to the AllPapers table, since these are relative.

Import tables into Tableau: 
	dbo.AllPapers
	dbo.PaperKeywordRankByQuestion

To calculate the normalized page rank for Question 1:
JB
*/

-- variable weights for each rank. change to your preferred weights.
declare 
    @beta1 float = 1.0
    , @beta2 float = 1.0
    , @beta3 float = 1.0
    , @beta4 float = 1.0
    , @beta5 float = 1.0
    , @beta6 float = 1.0
;

select 
    *
    , (x - min(x) over()) / (max(x) over() - min(x) over()) as Relevance
    , dense_rank() over(order by x desc) as RankOrder
from (
    select 
        p.paper_id
        --, isnull(p.title, 'N/A') as Title
        --, isnull(p.Abstract, p.body_text) as BodyText
        , p.AuthorRank
        , p.JournalRank
        , p.Recency
        , p.CitedAuthorsRank
        , p.CitedInstitutionRank
        , p.KmeansCluster
        , kw.q01 as KeywordRank -- replace with q02, q03, ...q10 for each Tableau rank calc.

        , ( 
            -- Total Rank
            @beta1*isnull(AuthorRank,0)
            + @beta2*isnull(JournalRank,0)
            + @beta3*isnull(Recency,0)
            + @beta4*isnull(CitedAuthorsRank,0)
            + @beta5*isnull(CitedInstitutionRank,0)
            + @beta6*isnull(kw.q01,0) -- KeywordRank -- replace with q02, q03, ...q10 for each Tableau rank calc.
        ) as x
    from 
        dbo.AllPapers as p
        
        inner join dbo.PaperKeywordRankByQuestion as kw
            on p.paper_id = kw.paper_id
) as t