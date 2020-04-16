create table dbo.KeywordCountsUnpivot(
    paper_id varchar(40)
    , KeywordCount int
    , Keyword varchar(100)
);

insert into dbo.KeywordCountsUnpivot(paper_id, KeywordCount, Keyword)
select 
    paper_id, KeywordCount, Keyword
from (
select paper_id
      ,count_transmission as transmission
      ,count_incubation as incubation
      ,count_environmental_stability as [environmental stability]
      ,count_risk as risk
      ,count_virus as virus
      ,count_genetics as genetics
      ,count_origin as origin
      ,count_evolution as evolution
      ,count_vaccines as vaccines
      ,count_therapeutics as therapeutics
      ,count_non_pharmaceutical_interventions as [non pharmaceutical interventions]
      ,count_published as published
      ,count_medical_care as [medical care]
      ,count_ethical as ethical
      ,count_social_science as [social science]
      ,count_diagnostics as diagnostics
      ,count_surveillance as surveillance
      ,count_information_sharing as [information sharing]
      ,count_inter_sectoral_collaboration as [inter sectoral collaboration]
      ,count_covid19 as [covid 19]
      ,count_sarscov2 as [sars cov2]
  from 
    covid19.dbo.KeywordCounts
) as p
unpivot(KeywordCount for Keyword in (transmission
      ,incubation
      ,[environmental stability]
      ,risk
      ,virus
      ,genetics
      ,origin
      ,evolution
      ,vaccines
      ,therapeutics
      ,[non pharmaceutical interventions]
      ,published
      ,[medical care]
      ,ethical
      ,[social science]
      ,diagnostics
      ,surveillance
      ,[information sharing]
      ,[inter sectoral collaboration]
      ,[covid 19]
      ,[sars cov2])
) as up;

alter table dbo.KeywordCountsUnpivot with check add constraint fk_KeywordCountsUnpivot_paper_id foreign key(paper_id) references dbo.AllPapers(paper_id);

create nonclustered index ix_KeywordCountsUnpivot_paper_id on dbo.KeywordCountsUnpivot(paper_id);