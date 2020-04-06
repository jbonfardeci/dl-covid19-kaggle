create table PublishedBy(
	Id int primary key identity(1,1),
	journal_hash varchar(40) not null,
	paper_id varchar(40) not null
)