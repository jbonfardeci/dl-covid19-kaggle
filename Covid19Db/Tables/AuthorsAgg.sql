create table dbo.AuthorsAgg (
    Id int primary key identity(1,1)
    , paper_id varchar(40)
    , authors nvarchar(max)
)