CREATE TABLE [dbo].[Author] (
    [hash_id]    VARCHAR (40)   NOT NULL,
    [first_name] NVARCHAR (255) NULL,
    [last_name]  NVARCHAR (255) NULL,
    [middle]     NVARCHAR (25)  NULL,
    [suffix]     NVARCHAR (10)  NULL,
    [email]      NVARCHAR (255) NULL,
    PRIMARY KEY CLUSTERED ([hash_id] ASC)
);

