
CREATE procedure dbo.usp_UpdateJournalTableFromImport as

truncate table dbo.Journal;
truncate table dbo.PublishedBy;

insert into dbo.PublishedBy(journal_hash, paper_id)
	select convert(nvarchar(40), HASHBYTES('md5', isnull(StandardJournalName, JournalNameInData)), 1) as journal_hash, p.paper_id
	from dbo.JournalMapping as m
	inner join dbo.AllPapers as p 
		on p.journal = isnull(StandardJournalName, JournalNameInData);

insert into dbo.Journal(hash_id, journal_name, issn)
	select 
		hash_id, journal_name, issn 
	from (
		select *, ROW_NUMBER() over(partition by hash_id order by hash_id) as rn 
		from (
			select 
				convert(nvarchar(40), HASHBYTES('md5', isnull(StandardJournalName, JournalNameInData)), 1) as hash_id
				, isnull(StandardJournalName, JournalNameInData) as journal_name
				, m.PrintISSN as issn
			from dbo.JournalMapping as m
		) as t1
	) as t2 where rn = 1;
	
update dbo.AllPapers set JournalId = t.Id
from (
	select Id
	from dbo.JournalMapping as m
	inner join dbo.AllPapers as p on p.journal = m.JournalNameInData
	and len(p.journal) > 0
) as t;


