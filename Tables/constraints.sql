
alter table dbo.Authored with check add constraint fk_authored_author_hash foreign key(author_hash) references dbo.Author(hash_id)
go

create nonclustered index ix_authored_author_hash on dbo.Authored(author_hash)
go

alter table dbo.Authored with check add constraint fk_authored_paper_id foreign key(paper_id) references dbo.AllPapers(paper_id)
go

create nonclustered index ix_authored_paper_id on dbo.Authored(paper_id)
go


alter table dbo.Affiliation with check add constraint fk_affiliation_author_hash foreign key(author_hash) references dbo.Author(hash_id)
go

create nonclustered index ix_affiliation_author_hash on dbo.Affiliation(author_hash)
go

alter table dbo.Affiliation with check add constraint fk_affiliation_institution_hash foreign key(institution_hash) references dbo.Institution(hash_id)
go

create nonclustered index ix_affiliation_paper_id on dbo.Affiliation(institution_hash)
go


alter table dbo.Citation with check add constraint fk_citation_author_hash foreign key(author_hash) references dbo.Author(hash_id)
go

create nonclustered index ix_citation_author_hash on dbo.Citation(author_hash)
go

alter table dbo.Citation with check add constraint fk_citation_paper_id foreign key(paper_id) references dbo.AllPapers(paper_id)
go

create nonclustered index ix_citation_paper_id on dbo.Citation(paper_id)
go


alter table dbo.PublishedBy with check add constraint fk_publishedby_journal_hash foreign key(journal_hash) references dbo.Journal(hash_id)
go

create nonclustered index ix_publishedby_journal_hash on dbo.PublishedBy(journal_hash)
go

alter table dbo.PublishedBy with check add constraint fk_publishedby_paper_id foreign key(paper_id) references dbo.AllPapers(paper_id)
go

create nonclustered index ix_publishedby_paper_id on dbo.AllPapers(paper_id)
go
