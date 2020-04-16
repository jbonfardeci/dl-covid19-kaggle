﻿CREATE procedure dbo.usp_UpdatePaperRanks as

/*
	Normalize numbers from 0-1
	z = (x - min(x)) / (max(x) - min(x)) 
*/
; with auth as (
	select 
		paper_id
		, (x - min(x) over()) / (max(x) over() - min(x) over()) as AuthorRank 
	from (
		select 
			p.paper_id
			, convert(decimal(12,4), sum(r.aif_rank)) as x
		from
			dbo.Authored as a 

			inner join dbo.AllPapers as p 
				on a.paper_id = p.paper_id

			inner join dbo.vw_author_ranked_aif as r 
				on a.author_hash = r.hash_id
		where 
			r.aif_rank is not null
		group by 
			p.paper_id
	) as t1
)

, jrnl as (
	select 
		paper_id
		, Journal
		, (x - min(x) over()) / (max(x) over() - min(x) over()) as JournalRank 
	from (
		select 
			p.paper_id
			, jr.Journal
			, convert(decimal(12,4), isnull(jr.ImpactFactor,0)) as x
		from 
			dbo.AllPapers as p 

			left join dbo.vw_journals_ranked_combined as jr
				on p.JournalId = jr.JournalId
	) as t
)

, recency as (
	select 
		paper_id
		, (x - min(x) over()) / (max(x) over() - min(x) over()) as Recency
	from (
		select 
			paper_id 
			, convert(decimal(18,5), (case 
				when p.publish_date is null then 0 
				else Datediff_big(MS, '1970-01-01', p.publish_date) 
			end)) as x
		from 
			dbo.AllPapers as p
		where 
			publish_date is not null
	) as t1
)

, cited_authors as (
    select 
        paper_id
        , (x - min(x) over()) / (max(x) over() - min(x) over()) as CitedAuthorsRank
    from (
        select 
            p.paper_id
            , convert(decimal(12,5), sum(a.aif_rank)) as x --CitedAuthorsRank
        from 
            dbo.AllPapers as p

            inner join dbo.Citation as c 
                on p.paper_id = c.paper_id

            inner join dbo.vw_author_ranked_aif as a 
                on c.author_hash = a.hash_id
        group by 
            p.paper_id
    ) as t
)

, cited_inst as (
    select 
        paper_id
        , (x - min(x) over()) / (max(x) over() - min(x) over()) as CitedInstitutionRank
    from (
        select 
            p.paper_id
            , convert(decimal(12,5), sum(ins.Global_Rank)) as x --CitedInstitutionRank
        from 
            dbo.AllPapers as p

            inner join dbo.Citation as c 
                on p.paper_id = c.paper_id

            inner join dbo.Affiliation as af 
                on c.author_hash = af.author_hash

            inner join dbo.vw_institutitions_ranked_sir as ins 
                on af.institution_hash = ins.hash_id
        group by 
            p.paper_id
    ) as t
)

, all_ranks as (
    select 
        p.paper_id
        , convert(decimal(12, 5), a.AuthorRank) as AuthorRank
        , convert(decimal(12, 5), jrnl.JournalRank) as JournalRank
        , convert(decimal(12, 5), r.Recency) as Recency
		, convert(decimal(12, 5), ca.CitedAuthorsRank) as CitedAuthorsRank
		, convert(decimal(12, 5), ci.CitedInstitutionRank) as CitedInstitutionRank
    from 
        dbo.AllPapers as p 

        left join auth as a
            on p.paper_id = a.paper_id

        left join jrnl 
            on p.paper_id = jrnl.paper_id

        left join recency as r
            on r.paper_id = p.paper_id

		left join cited_authors as ca 
			on p.paper_id = ca.paper_id 

		left join cited_inst as ci
			on p.paper_id = ci.paper_id
)

update dbo.AllPapers set 
		AuthorRank = ar.AuthorRank
		, JournalRank = ar.JournalRank
		, Recency = ar.Recency
		, CitedAuthorsRank = ar.CitedAuthorsRank
		, CitedInstitutionRank = ar.CitedInstitutionRank
from all_ranks as ar
where dbo.AllPapers.paper_id = ar.paper_id
;