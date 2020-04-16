CREATE TABLE [dbo].[KeywordCountsUnpivot] (
    [paper_id]     VARCHAR (40)  NULL,
    [KeywordCount] INT           NULL,
    [Keyword]      VARCHAR (100) NULL,
    CONSTRAINT [fk_KeywordCountsUnpivot_paper_id] FOREIGN KEY ([paper_id]) REFERENCES [dbo].[AllPapers] ([paper_id])
);


GO
CREATE NONCLUSTERED INDEX [ix_KeywordCountsUnpivot_paper_id]
    ON [dbo].[KeywordCountsUnpivot]([paper_id] ASC);

