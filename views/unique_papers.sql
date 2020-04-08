create view dbo.vw_unique_papers as 

with csv_papers as (
	select * from (
		select 
			isnull(sha, lower(convert(NVARCHAR(40), HashBytes('sha1'
				, concat(a.title, doi, a.abstract, source_x, pmcid, pubmed_id, license, journal, authors, a.[Microsoft Academic Paper ID], a.[WHO #Covidence], publish_time)), 2))) as paper_id
			, source_x
			, title
			, doi
			, pmcid
			, pubmed_id
			, license
			, abstract
			, publish_time
			, authors
			, journal
			, a.[Microsoft Academic Paper ID] as ms_academic_paper_id 
			, a.[WHO #Covidence] as who_covidence
		from 
			AllSourcesMetadata as a
	) as t
	group by 
		paper_id
		, source_x
		, title
		, doi
		, pmcid
		, pubmed_id
		, license
		, abstract
		, publish_time
		, authors
		, journal
		, ms_academic_paper_id 
		, who_covidence
)

, json_papers as (
	select 
		a.paper_id
		, source_x
		, a.title
		, doi
		, pmcid
		, pubmed_id
		, license
		, a.abstract
		, publish_time
		, authors
		, journal
		, ms_academic_paper_id 
		, who_covidence
		, a.body_text
	from 
		dbo.Paper as a

		left join csv_papers as b
			on a.paper_id = b.paper_id		
)

select * from (
	select *, row_number() over(partition by paper_id order by paper_id) as rn 
	from (
		select *, null as body_text from csv_papers as a where a.paper_id not in (select paper_id from dbo.Paper)
		union all
		select * from json_papers
	) as t1
) as t2 where rn = 1 or (rn > 1 and body_text is not null);

