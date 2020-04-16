CREATE TABLE [dbo].[Journal] (
    [hash_id]      VARCHAR (40)    NOT NULL,
    [journal_name] NVARCHAR (1000) NOT NULL,
    [issn]         NVARCHAR (255)  NULL,
    PRIMARY KEY CLUSTERED ([hash_id] ASC)
);

