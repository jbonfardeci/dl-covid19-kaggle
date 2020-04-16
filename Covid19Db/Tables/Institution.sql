CREATE TABLE [dbo].[Institution] (
    [hash_id]          VARCHAR (40)   NOT NULL,
    [institution_name] NVARCHAR (255) NULL,
    [laboratory]       NVARCHAR (255) NULL,
    [addrLine]         NVARCHAR (255) NULL,
    [postCode]         NVARCHAR (50)  NULL,
    [settlement]       NVARCHAR (255) NULL,
    [country]          NVARCHAR (255) NULL,
    [region]           NVARCHAR (255) NULL,
    PRIMARY KEY CLUSTERED ([hash_id] ASC)
);

