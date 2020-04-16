CREATE TABLE [dbo].[PublishedBy] (
    [Id]           INT          IDENTITY (1, 1) NOT NULL,
    [journal_hash] VARCHAR (40) NOT NULL,
    [paper_id]     VARCHAR (40) NOT NULL,
    PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [fk_publishedby_paper_id] FOREIGN KEY ([paper_id]) REFERENCES [dbo].[AllPapers] ([paper_id])
);


GO
CREATE NONCLUSTERED INDEX [ix_publishedby_journal_hash]
    ON [dbo].[PublishedBy]([journal_hash] ASC);

