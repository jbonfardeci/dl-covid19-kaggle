-- View for overall paper ranking
-- WIP
-- John Bonfardeci / 2020-04-14

-- convert(decimal(12,5), (x - min(x) over()) / (max(x) over() - min(x) over())) as KeywordRank

/*
	Normalize numbers from 0-1
	z = (x - min(x)) / (max(x) - min(x)) 
*/
select top 1000
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
		, (x - min(x) over()) / (max(x) over() - min(x) over()) as Relevance
	from (
		select 
			p.paper_id as PaperId
			, isnull(p.title, 'N/A') as PaperTitle
			--, p.Abstract
			, p.publish_date as Published

			, AuthorRank
			, JournalRank
			, Recency
			, CitedAuthorsRank
			, CitedInstitutionRank

			, ( 
				-- Total Rank
				AuthorRank
				+ JournalRank
				+ Recency
				+ CitedAuthorsRank
				+ CitedInstitutionRank
			) as x -- Total impact factor
		from 
			dbo.AllPapers as p 
	) as t1
) as t2