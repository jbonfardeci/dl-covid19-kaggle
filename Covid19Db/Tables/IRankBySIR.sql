CREATE TABLE [dbo].[IRankBySIR] (
    [Global_Rank]      INT           NOT NULL,
    [Institution]      VARCHAR (137) NOT NULL,
    [Country]          VARCHAR (3)   NOT NULL,
    [Sector]           VARCHAR (12)  NOT NULL,
    [institution_hash] VARCHAR (40)  NULL,
    PRIMARY KEY CLUSTERED ([Global_Rank] ASC)
);

