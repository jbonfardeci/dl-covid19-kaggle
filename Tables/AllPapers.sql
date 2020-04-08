
CREATE TABLE dbo.AllPapers(
	paper_id nvarchar(40) primary key,
	source_x nvarchar(255) NULL,
	title nvarchar(1000) NULL,
	doi nvarchar(255) NULL,
	pmcid nvarchar(25) NULL,
	pubmed_id nvarchar(25) NULL,
	license nvarchar(255) NULL,
	abstract nvarchar(max) NULL,
	publish_time nvarchar(50) NULL,
	authors nvarchar(max) NULL,
	journal nvarchar(1000) NULL,
	ms_academic_paper_id nvarchar(15) NULL,
	who_covidence nvarchar(10) NULL,
	body_text nvarchar(max)
) 
GO


