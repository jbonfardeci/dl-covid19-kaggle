

CREATE VIEW [dbo].[vw_author_ranked_aif]
AS
WITH a as (
	select a.hash_id
	   ,a.last_name
	   ,a.first_name
	   ,a.middle
	   ,a.suffix
	   ,a.email
	   ,SUM(CASE WHEN (LEFT(TRIM(ap2.publish_time),4))=(datepart(year,getdate()) - 3) THEN 1 ELSE 0 END) as paper_cnt_3yearsPrior
	   ,SUM(CASE WHEN (LEFT(TRIM(ap2.publish_time),4))=(datepart(year,getdate()) - 2) THEN 1 ELSE 0 END) as paper_cnt_2yearPrior
	   ,SUM(CASE WHEN (LEFT(TRIM(ap2.publish_time),4))IN(datepart(year,getdate()) - 3,datepart(year,getdate()) - 2) THEN 1 ELSE 0 END) as total2year_paper_cnt
	  ,count(distinct ap2.paper_id) as totalAllYears_paper_cnt
	from Author a
	INNER JOIN Authored ad
	ON a.hash_id = ad.author_hash
	INNER JOIN AllPapers ap2
	ON ad.paper_id = ap2.paper_id
	GROUP BY a.hash_id
	, first_name
	, last_name
	, middle
	, suffix
	, email
),
c AS (
	select a.hash_id
		   ,a.last_name
		   ,a.first_name
		   ,a.middle
		   ,a.suffix
		   ,a.email
		   ,SUM(CASE WHEN (LEFT(TRIM(ap.publish_time),4))=(datepart(year,getdate()) - 1) THEN 1 ELSE 0 END) as citation_cnt_priorYear
		   ,count(distinct ap.paper_id) as totalAllYears_citation_cnt
	from Author a
	INNER JOIN Citation c
	ON a.hash_id = c.author_hash
	INNER JOIN AllPapers ap
	ON c.paper_id = ap.paper_id
	GROUP BY a.hash_id
	, first_name
	, last_name
	, middle
	, suffix
	, email
)
select a.hash_id
	   ,a.last_name
	   ,a.first_name
	   ,a.middle 
	   ,a.suffix
	   ,a.email
	   ,a.paper_cnt_2yearPrior
	   ,a.paper_cnt_3yearsPrior
	   ,a.total2year_paper_cnt
	   ,c.citation_cnt_priorYear
	   ,a.totalAllYears_paper_cnt
	   ,c.totalAllYears_citation_cnt
	   ,ROUND(ISNULL(cast(c.citation_cnt_priorYear as float)/NULLIF(cast(a.total2year_paper_cnt as float),0.00),0.00),2) as author_impact_factor_2yr
	   ,rank() over(order by ROUND(ISNULL(cast(c.citation_cnt_priorYear as float)/NULLIF(cast(a.total2year_paper_cnt as float),0.00),0.00),2) desc) aif_rank
from a
JOIN c
ON a.hash_id = c.hash_id
