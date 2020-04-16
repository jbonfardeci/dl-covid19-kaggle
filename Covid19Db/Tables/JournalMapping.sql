CREATE TABLE [dbo].[JournalMapping] (
    [JournalNameInData]   NVARCHAR (1000) NULL,
    [StandardJournalName] NVARCHAR (255)  NULL,
    [Publisher]           NVARCHAR (255)  NULL,
    [ChiefEditor]         NVARCHAR (255)  NULL,
    [PrintISSN]           NVARCHAR (255)  NULL,
    [ElectronicISSN]      NVARCHAR (255)  NULL,
    [Id]                  INT             IDENTITY (1, 1) NOT NULL,
    [ImpactFactor]        REAL            NULL,
    PRIMARY KEY CLUSTERED ([Id] ASC)
);

