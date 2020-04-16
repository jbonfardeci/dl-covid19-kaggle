-- Takes ~50 minutes to run (create) with ~30K papers.
SELECT S1.*
      ,count_transmission + count_incubation + count_environmental_stability + count_risk + count_virus + count_genetics + count_origin + count_evolution + count_vaccines
     + count_therapeutics + count_non_pharmaceutical_interventions + count_published + count_medical_care + count_ethical + count_social_science + count_diagnostics
     + count_surveillance + count_information_sharing + count_inter_sectoral_collaboration + count_covid19 + count_sarscov2 AS count_total_keywords
  --INTO dbo.KeywordCounts2
  FROM (SELECT paper_id
            ,CASE WHEN title     IS NULL OR title     = '' OR title     = ' ' THEN 'N' ELSE 'Y' END AS title_avail
            ,CASE WHEN abstract  IS NULL OR abstract  = '' OR abstract  = ' ' THEN 'N' ELSE 'Y' END AS abstract_avail
            ,CASE WHEN body_text IS NULL OR body_text = '' OR body_text = ' ' THEN 'N' ELSE 'Y' END AS body_text_avail
            ,ISNULL(dbo.fn_GetKeywordCounts(ISNULL(title, '') + ' ' + ISNULL(abstract, '') + ' ' + ' ' + ISNULL(body_text, ''), 'transmission'), 0)                     AS count_transmission
            ,ISNULL(dbo.fn_GetKeywordCounts(ISNULL(title, '') + ' ' + ISNULL(abstract, '') + ' ' + ' ' + ISNULL(body_text, ''), 'incubation'), 0)                       AS count_incubation
            ,ISNULL(dbo.fn_GetKeywordCounts(ISNULL(title, '') + ' ' + ISNULL(abstract, '') + ' ' + ' ' + ISNULL(body_text, ''), 'environmental stability'), 0)          AS count_environmental_stability
            ,ISNULL(dbo.fn_GetKeywordCounts(ISNULL(title, '') + ' ' + ISNULL(abstract, '') + ' ' + ' ' + ISNULL(body_text, ''), 'risk'), 0)                             AS count_risk
            ,ISNULL(dbo.fn_GetKeywordCounts(ISNULL(title, '') + ' ' + ISNULL(abstract, '') + ' ' + ' ' + ISNULL(body_text, ''), 'virus'), 0)                            AS count_virus
            ,ISNULL(dbo.fn_GetKeywordCounts(ISNULL(title, '') + ' ' + ISNULL(abstract, '') + ' ' + ' ' + ISNULL(body_text, ''), 'genetics'), 0)                         AS count_genetics
            ,ISNULL(dbo.fn_GetKeywordCounts(ISNULL(title, '') + ' ' + ISNULL(abstract, '') + ' ' + ' ' + ISNULL(body_text, ''), 'origin'), 0)                           AS count_origin
            ,ISNULL(dbo.fn_GetKeywordCounts(ISNULL(title, '') + ' ' + ISNULL(abstract, '') + ' ' + ' ' + ISNULL(body_text, ''), 'evolution'), 0)                        AS count_evolution
            ,ISNULL(dbo.fn_GetKeywordCounts(ISNULL(title, '') + ' ' + ISNULL(abstract, '') + ' ' + ' ' + ISNULL(body_text, ''), 'vaccines'), 0)                         AS count_vaccines
            ,ISNULL(dbo.fn_GetKeywordCounts(ISNULL(title, '') + ' ' + ISNULL(abstract, '') + ' ' + ' ' + ISNULL(body_text, ''), 'therapeutics'), 0)                     AS count_therapeutics
            ,ISNULL(dbo.fn_GetKeywordCounts(ISNULL(title, '') + ' ' + ISNULL(abstract, '') + ' ' + ' ' + ISNULL(body_text, ''), 'non-pharmaceutical interventions'), 0) AS count_non_pharmaceutical_interventions
            ,ISNULL(dbo.fn_GetKeywordCounts(ISNULL(title, '') + ' ' + ISNULL(abstract, '') + ' ' + ' ' + ISNULL(body_text, ''), 'published'), 0)                        AS count_published
            ,ISNULL(dbo.fn_GetKeywordCounts(ISNULL(title, '') + ' ' + ISNULL(abstract, '') + ' ' + ' ' + ISNULL(body_text, ''), 'medical care'), 0)                     AS count_medical_care
            ,ISNULL(dbo.fn_GetKeywordCounts(ISNULL(title, '') + ' ' + ISNULL(abstract, '') + ' ' + ' ' + ISNULL(body_text, ''), 'ethical'), 0)                          AS count_ethical
            ,ISNULL(dbo.fn_GetKeywordCounts(ISNULL(title, '') + ' ' + ISNULL(abstract, '') + ' ' + ' ' + ISNULL(body_text, ''), 'social science'), 0)                   AS count_social_science
            ,ISNULL(dbo.fn_GetKeywordCounts(ISNULL(title, '') + ' ' + ISNULL(abstract, '') + ' ' + ' ' + ISNULL(body_text, ''), 'diagnostics'), 0)                      AS count_diagnostics
            ,ISNULL(dbo.fn_GetKeywordCounts(ISNULL(title, '') + ' ' + ISNULL(abstract, '') + ' ' + ' ' + ISNULL(body_text, ''), 'surveillance'), 0)                     AS count_surveillance
            ,ISNULL(dbo.fn_GetKeywordCounts(ISNULL(title, '') + ' ' + ISNULL(abstract, '') + ' ' + ' ' + ISNULL(body_text, ''), 'information sharing'), 0)              AS count_information_sharing
            ,ISNULL(dbo.fn_GetKeywordCounts(ISNULL(title, '') + ' ' + ISNULL(abstract, '') + ' ' + ' ' + ISNULL(body_text, ''), 'inter-sectoral collaboration'), 0)     AS count_inter_sectoral_collaboration
            ,ISNULL(dbo.fn_GetKeywordCounts(ISNULL(title, '') + ' ' + ISNULL(abstract, '') + ' ' + ' ' + ISNULL(body_text, ''), 'COVID-19'), 0)                         AS count_covid19
            ,ISNULL(dbo.fn_GetKeywordCounts(ISNULL(title, '') + ' ' + ISNULL(abstract, '') + ' ' + ' ' + ISNULL(body_text, ''), 'SARS-CoV-2'), 0)                       AS count_sarscov2
       FROM dbo.AllPapers) S1
