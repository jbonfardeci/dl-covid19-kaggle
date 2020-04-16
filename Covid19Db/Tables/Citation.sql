CREATE TABLE [dbo].[Citation] (
    [Id]          INT          IDENTITY (1, 1) NOT NULL,
    [author_hash] VARCHAR (40) NOT NULL,
    [paper_id]    VARCHAR (40) NOT NULL,
    PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [fk_citation_author_hash] FOREIGN KEY ([author_hash]) REFERENCES [dbo].[Author] ([hash_id]),
    CONSTRAINT [fk_citation_paper_id] FOREIGN KEY ([paper_id]) REFERENCES [dbo].[AllPapers] ([paper_id])
);


GO
CREATE NONCLUSTERED INDEX [ix_citation_author_hash]
    ON [dbo].[Citation]([author_hash] ASC);


GO
CREATE NONCLUSTERED INDEX [ix_citation_paper_id]
    ON [dbo].[Citation]([paper_id] ASC);

