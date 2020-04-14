
drop table if exists vert.Papers;
create table vert.Papers(
	paper_id varchar(40) primary key,
	title nvarchar(max)
) as node;

drop table if exists vert.Authors;
create table vert.Authors(
	hash_id varchar(40) primary key,
	first_name nvarchar(255) null,
	last_name nvarchar(255) null,
	middle nvarchar(25) null,
	suffix nvarchar(10) null,
	email nvarchar(255) null
) as node;

drop table if exists edg.Wrote;
create table edg.Wrote(
	constraint ec_wrote connection (vert.Authors to vert.Papers)
) as edge;

truncate table vert.Papers
insert into vert.Papers(paper_id, title)
	select paper_id, title from dbo.AllPapers;

truncate table vert.Authors
insert into vert.Authors(hash_id, first_name, last_name, middle, suffix, email)
	select hash_id, first_name, last_name, middle, suffix, email
	from dbo.Author;

truncate table edg.Wrote;
insert into edg.Wrote($from_id, $to_id)
	select 
		a.$node_id, p.$node_id 
	from 
		vert.Papers as p
			
		inner join dbo.Authored as auth 
			on p.paper_id = auth.paper_id

		inner join vert.Authors as a 
			on auth.author_hash = a.hash_id
;

