create table Authored(
	Id int primary key identity(1,1),
	author_hash varchar(40) not null,
	paper_id varchar(40) not null
)