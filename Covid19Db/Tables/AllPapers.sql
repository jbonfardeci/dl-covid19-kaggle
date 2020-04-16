CREATE TABLE [dbo].[AllPapers] (
    [paper_id]             VARCHAR (40)    NOT NULL,
    [source_x]             NVARCHAR (255)  NULL,
    [title]                NVARCHAR (MAX)  NULL,
    [doi]                  NVARCHAR (255)  NULL,
    [pmcid]                NVARCHAR (25)   NULL,
    [pubmed_id]            NVARCHAR (25)   NULL,
    [license]              NVARCHAR (255)  NULL,
    [abstract]             NVARCHAR (MAX)  NULL,
    [publish_time]         NVARCHAR (50)   NULL,
    [authors]              NVARCHAR (MAX)  NULL,
    [journal]              NVARCHAR (1000) NULL,
    [ms_academic_paper_id] NVARCHAR (15)   NULL,
    [who_covidence]        NVARCHAR (10)   NULL,
    [body_text]            NVARCHAR (MAX)  NULL,
    [publish_date]         DATE            NULL,
    [JournalId]            INT             NULL,
    [AuthorRank]           DECIMAL (12, 5) NULL,
    [JournalRank]          DECIMAL (12, 5) NULL,
    [Recency]              DECIMAL (12, 5) NULL,
    [CitedInstitutionRank] DECIMAL (12, 5) NULL,
    [CitedAuthorsRank]     DECIMAL (12, 5) NULL,
    [KmeansCluster]        INT             NULL,
    CONSTRAINT [PK__AllPaper__8A5B26BE03219E4E] PRIMARY KEY CLUSTERED ([paper_id] ASC),
    CONSTRAINT [fk_Paper_JournalId] FOREIGN KEY ([JournalId]) REFERENCES [dbo].[JournalMapping] ([Id])
);


GO
CREATE NONCLUSTERED INDEX [ix_publishedby_paper_id]
    ON [dbo].[AllPapers]([paper_id] ASC);

