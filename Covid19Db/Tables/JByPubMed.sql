CREATE TABLE [dbo].[JByPubMed] (
    [Journal_title]       NVARCHAR (MAX) NOT NULL,
    [NLM_TA]              NVARCHAR (MAX) NOT NULL,
    [pISSN]               NVARCHAR (50)  NULL,
    [eISSN]               NVARCHAR (50)  NULL,
    [Publisher]           NVARCHAR (MAX) NOT NULL,
    [LOCATORplus_ID]      NVARCHAR (50)  NOT NULL,
    [Latest_issue]        NVARCHAR (50)  NOT NULL,
    [Earliest_volume]     NVARCHAR (50)  NOT NULL,
    [Free_access]         NVARCHAR (50)  NULL,
    [Open_access]         NVARCHAR (50)  NOT NULL,
    [Participation_level] NVARCHAR (50)  NOT NULL,
    [Deposit_status]      NVARCHAR (50)  NULL,
    [Journal_URL]         NVARCHAR (150) NOT NULL
);

