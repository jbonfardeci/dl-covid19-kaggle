create table Author(
	hash_id varchar(40) primary key,
	first_name nvarchar(255) null,
	last_name nvarchar(255) null,
	middle nvarchar(25) null,
	suffix nvarchar(10) null,
	email nvarchar(255) null
)