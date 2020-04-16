CREATE view dbo.vw_Question05 as 
/*
	Normalize numbers from 0-1
	z = (x - min(x)) / (max(x) - min(x)) 
*/
with kw as (
	select 
		paper_id 
		, (x - min(x) over()) / (max(x) over() - min(x) over()) as KeywordRank
	from (
		select 
			paper_id 
			, KeywordCount as x
		from 
			dbo.vw_KeywordRankByQuestion
		where 
			QuestionNum = 5
	) as t
)

select 
	*
	, dense_rank() over(order by Relevance desc) as rnk
from (
	select 
		PaperId
		, PaperTitle
		, Published
		, AuthorRank
		, JournalRank
		, Recency
		, CitedAuthorsRank
		, CitedInstitutionRank
		, KeywordRank
		, (x - min(x) over()) / (max(x) over() - min(x) over()) as Relevance
	from (
		select 
			p.paper_id as PaperId
			, isnull(p.title, 'N/A') as PaperTitle
			, p.Abstract
			, p.publish_date as Published

			, AuthorRank
			, JournalRank
			, Recency
			, CitedAuthorsRank
			, CitedInstitutionRank
			, convert(decimal(8,5), KeywordRank) as KeywordRank

			, ( 
				-- Total Rank
				AuthorRank
				+ JournalRank
				+ Recency
				+ CitedAuthorsRank
				+ CitedInstitutionRank
				+ KeywordRank
			) as x -- Total impact factor
		from 
			dbo.AllPapers as p 

			left join kw 
				on p.paper_id = kw.paper_id
	) as t1
) as t2