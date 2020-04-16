CREATE TABLE [dbo].[JRanked] (
    [JournalID]           INT             NOT NULL,
    [Journal]             NVARCHAR (1000) NULL,
    [CiteScore18]         NVARCHAR (50)   NULL,
    [SJR]                 NUMERIC (10, 3) NULL,
    [ImpactFactor]        NVARCHAR (255)  NULL,
    [JournalAbbrOfficial] NVARCHAR (MAX)  NULL,
    [JournalNameOfficial] NVARCHAR (MAX)  NULL,
    [pISSN]               NVARCHAR (255)  NULL,
    [eISSN]               NVARCHAR (255)  NULL,
    [Publisher]           NVARCHAR (255)  NULL,
    [ChiefEditor]         NVARCHAR (255)  NULL
);

