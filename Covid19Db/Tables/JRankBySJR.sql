CREATE TABLE [dbo].[JRankBySJR] (
    [Rank]                NVARCHAR (50)  NOT NULL,
    [Sourceid]            FLOAT (53)     NOT NULL,
    [Title]               NVARCHAR (200) NOT NULL,
    [Type]                NVARCHAR (50)  NOT NULL,
    [Issn]                NVARCHAR (50)  NOT NULL,
    [SJR]                 FLOAT (53)     NOT NULL,
    [SJR_Quartile]        NVARCHAR (50)  NULL,
    [H_index]             NVARCHAR (50)  NOT NULL,
    [Total_Docs_2018]     NVARCHAR (50)  NOT NULL,
    [Total_Docs_3years]   NVARCHAR (50)  NOT NULL,
    [Total_Refs]          NVARCHAR (50)  NOT NULL,
    [Total_Cites_3years]  INT            NOT NULL,
    [Citable_Docs_3years] NVARCHAR (50)  NOT NULL,
    [Cites_Doc_2years]    FLOAT (53)     NOT NULL,
    [Ref_Doc]             FLOAT (53)     NOT NULL,
    [Country]             NVARCHAR (50)  NOT NULL,
    [Publisher]           NVARCHAR (150) NULL,
    [Coverage]            NVARCHAR (150) NOT NULL,
    [Categories]          NVARCHAR (350) NOT NULL
);

