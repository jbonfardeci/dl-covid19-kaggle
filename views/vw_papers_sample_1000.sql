
create view dbo.vw_papers_sample_1000 as 

with sampl as (
	select top 1000 paper_id 
	from (
		select paper_id, newid() as rowId 
		from dbo.AllPapers
	) as t
	order by rowId
)

select 
	p.* 
from 
	dbo.vw_papers as p 
	inner join sampl 
		on p.paper_id = sampl.paper_id;