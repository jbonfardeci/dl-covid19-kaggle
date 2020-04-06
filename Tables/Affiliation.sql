create table Affiliation(
	Id int primary key identity(1,1),
	institution_hash varchar(40) not null,
	author_hash varchar(40) not null
)