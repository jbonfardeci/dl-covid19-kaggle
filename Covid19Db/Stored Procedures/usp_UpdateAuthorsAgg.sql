create procedure dbo.usp_UpdateAuthorsAgg as
truncate table dbo.AuthorsAgg;

insert into dbo.AuthorsAgg(paper_id, authors)
select
    paper_id
    , string_agg(trim(concat(a.last_name, ', ', a.first_name, ' ', a.middle)), '; ') as authors
from    
    dbo.Authored as auth 

    inner join dbo.Author as a 
        on auth.author_hash = a.hash_id
group by 
    paper_id
;
