create view [vw_institutitions_ranked_sir] as
select hash_id, institution_name, laboratory, IRankBySIR.Global_Rank, Institution.Country
from dbo.Institution
inner join dbo.IRankBySIR on institution_hash = hash_id;