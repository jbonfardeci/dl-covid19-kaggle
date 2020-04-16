CREATE TABLE [dbo].[Authored] (
    [Id]          INT          IDENTITY (1, 1) NOT NULL,
    [author_hash] VARCHAR (40) NOT NULL,
    [paper_id]    VARCHAR (40) NOT NULL,
    PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [fk_authored_author_hash] FOREIGN KEY ([author_hash]) REFERENCES [dbo].[Author] ([hash_id]),
    CONSTRAINT [fk_authored_paper_id] FOREIGN KEY ([paper_id]) REFERENCES [dbo].[AllPapers] ([paper_id])
);


GO
CREATE NONCLUSTERED INDEX [ix_authored_author_hash]
    ON [dbo].[Authored]([author_hash] ASC);


GO
CREATE NONCLUSTERED INDEX [ix_authored_paper_id]
    ON [dbo].[Authored]([paper_id] ASC);

