drop table if exists AllSourcesMetadata;

create table AllSourcesMetadata (
	sha nvarchar(50),
	source_x nvarchar(255),
	title nvarchar(1000),
	doi nvarchar(255),
	pmcid nvarchar(25),
	pubmed_id nvarchar(25),
	license nvarchar(255),
	abstract nvarchar(max),
	publish_time nvarchar(50),
	authors nvarchar(max),
	journal nvarchar(1000),
	[Microsoft Academic Paper ID] nvarchar(15),
	[WHO #Covidence] nvarchar(10),
	has_full_text bit
);