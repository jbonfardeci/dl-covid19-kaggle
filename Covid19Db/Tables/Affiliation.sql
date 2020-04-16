CREATE TABLE [dbo].[Affiliation] (
    [Id]               INT          IDENTITY (1, 1) NOT NULL,
    [institution_hash] VARCHAR (40) NOT NULL,
    [author_hash]      VARCHAR (40) NOT NULL,
    PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [fk_affiliation_author_hash] FOREIGN KEY ([author_hash]) REFERENCES [dbo].[Author] ([hash_id]),
    CONSTRAINT [fk_affiliation_institution_hash] FOREIGN KEY ([institution_hash]) REFERENCES [dbo].[Institution] ([hash_id])
);


GO
CREATE NONCLUSTERED INDEX [ix_affiliation_author_hash]
    ON [dbo].[Affiliation]([author_hash] ASC);


GO
CREATE NONCLUSTERED INDEX [ix_affiliation_paper_id]
    ON [dbo].[Affiliation]([institution_hash] ASC);

