
create table dbo.Institution(
	hash_id varchar(40) primary key not null,
	institution_name nvarchar(255) null,
	laboratory nvarchar(255) null,
	addrLine nvarchar(255),
	postCode nvarchar(50),
	settlement nvarchar(255),
	country nvarchar(255),
	region nvarchar(255)
)