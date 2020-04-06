create table Paper(
	paper_id varchar(40) primary key not null,
	title nvarchar(1000) null,
	abstract nvarchar(max) null,
	body_text nvarchar(max) null
)