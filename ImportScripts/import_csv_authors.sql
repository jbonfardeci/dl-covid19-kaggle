
with authors as (
	select 
		hash_id
		, [first]
		, [last]
		, middle
	from (
		select 
			i.hash_id
			, i.[first]
			, i.[last]
			, i.middle
			, row_number() over(partition by i.hash_id order by i.hash_id) as rownum
		from 
			import.authors as i
			
			left join dbo.Author as a 
				on i.hash_id = a.hash_id
		where 
			a.hash_id is null
		group by 
			i.hash_id, i.[first], i.[last], i.middle
	) as t
	where 
		rownum = 1
)

insert into dbo.Author(hash_id, first_name, last_name, middle)
select 
	hash_id
	, [first] as first_name
	, [last] as last_name
	, middle 
from 
	authors;

insert into dbo.Authored(paper_id, author_hash)
	select lu.paper_id, lu.author_hash 
	from (
		select hash_id as author_hash, paper_id 
		from import.authors 
		group by hash_id, paper_id
	) as lu 

	inner join dbo.AllPapers as p 
		on lu.paper_id = p.paper_id
;
