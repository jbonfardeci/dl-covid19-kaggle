

CREATE view [dbo].[vw_papers] as

select 
	p.paper_id
	, p.title
	, isnull(p.body_text, p.abstract) as body_text
	, isnull(m.StandardJournalName, p.journal) as journal
	, m.ElectronicISSN as e_issn
	, m.PrintISSN as issn
	, m.ImpactFactor as impact_factor
	, p.publish_time
	, p.who_covidence
	, p.ms_academic_paper_id
	, p.source_x
	, p.doi
	, p.license
	, p.pmcid
	, p.pubmed_id
	, rtrim(concat(a.last_name, ', ', a.first_name, ' ', isnull(a.middle, ''), ' ', isnull(a.suffix, ''))) as author
	, rtrim(concat(cited.last_name, ', ', cited.first_name, ' ', isnull(cited.middle, ' '), ' ', isnull(cited.suffix, ' '), inst.institution_name, ' ', inst.laboratory)) as cited	
from 
	dbo.AllPapers as p 

	left join dbo.Authored as wrote 
		on p.paper_id = wrote.paper_id
		
	left join dbo.Author as a
		on wrote.author_hash = a.hash_id

	left join dbo.Citation as cite
		on cite.paper_id = p.paper_id

	left join dbo.Author as cited 
		on cite.author_hash = cited.hash_id 

	left join dbo.PublishedBy as pub 
		on pub.paper_id = p.paper_id 

	left join dbo.JournalMapping as m
		on m.JournalNameInData = p.journal

	left join dbo.Affiliation as aff 
		on aff.author_hash = cited.hash_id

	left join dbo.Institution as inst
		on inst.hash_id = aff.institution_hash
