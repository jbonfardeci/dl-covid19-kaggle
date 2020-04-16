-- Takes ~40 minutes to run.
SELECT KC.paper_id, KC.title_avail, KC.abstract_avail, KC.body_text_avail, AP.count_total_words
      ,(CAST(KC.count_transmission AS FLOAT)/AP.count_total_words) * (LOG10(CAST(29748 AS FLOAT)/(SELECT COUNT(1) FROM dbo.KeywordCounts WHERE count_transmission > 0)))                                         AS tfidf_transmission
      ,(CAST(KC.count_incubation AS FLOAT)/AP.count_total_words) * (LOG10(CAST(29748 AS FLOAT)/(SELECT COUNT(1) FROM dbo.KeywordCounts WHERE count_incubation > 0)))                                             AS tfidf_incubation
      ,(CAST(KC.count_environmental_stability AS FLOAT)/AP.count_total_words) * (LOG10(CAST(29748 AS FLOAT)/(SELECT COUNT(1) FROM dbo.KeywordCounts WHERE count_environmental_stability > 0)))                   AS tfidf_environmental_stability
      ,(CAST(KC.count_risk AS FLOAT)/AP.count_total_words) * (LOG10(CAST(29748 AS FLOAT)/(SELECT COUNT(1) FROM dbo.KeywordCounts WHERE count_risk > 0)))                                                         AS tfidf_risk
      ,(CAST(KC.count_virus AS FLOAT)/AP.count_total_words) * (LOG10(CAST(29748 AS FLOAT)/(SELECT COUNT(1) FROM dbo.KeywordCounts WHERE count_virus > 0)))                                                       AS tfidf_virus
      ,(CAST(KC.count_genetics AS FLOAT)/AP.count_total_words) * (LOG10(CAST(29748 AS FLOAT)/(SELECT COUNT(1) FROM dbo.KeywordCounts WHERE count_genetics > 0)))                                                 AS tfidf_genetics
      ,(CAST(KC.count_origin AS FLOAT)/AP.count_total_words) * (LOG10(CAST(29748 AS FLOAT)/(SELECT COUNT(1) FROM dbo.KeywordCounts WHERE count_origin > 0)))                                                     AS tfidf_origin
      ,(CAST(KC.count_evolution AS FLOAT)/AP.count_total_words) * (LOG10(CAST(29748 AS FLOAT)/(SELECT COUNT(1) FROM dbo.KeywordCounts WHERE count_evolution > 0)))                                               AS tfidf_evolution
      ,(CAST(KC.count_vaccines AS FLOAT)/AP.count_total_words) * (LOG10(CAST(29748 AS FLOAT)/(SELECT COUNT(1) FROM dbo.KeywordCounts WHERE count_vaccines > 0)))                                                 AS tfidf_vaccines
      ,(CAST(KC.count_therapeutics AS FLOAT)/AP.count_total_words) * (LOG10(CAST(29748 AS FLOAT)/(SELECT COUNT(1) FROM dbo.KeywordCounts WHERE count_therapeutics > 0)))                                         AS tfidf_therapeutics
      ,(CAST(KC.count_non_pharmaceutical_interventions AS FLOAT)/AP.count_total_words) * (LOG10(CAST(29748 AS FLOAT)/(SELECT COUNT(1) FROM dbo.KeywordCounts WHERE count_non_pharmaceutical_interventions > 0))) AS tfidf_non_pharmaceutical_interventions
      ,(CAST(KC.count_published AS FLOAT)/AP.count_total_words) * (LOG10(CAST(29748 AS FLOAT)/(SELECT COUNT(1) FROM dbo.KeywordCounts WHERE count_published > 0)))                                               AS tfidf_published
      ,(CAST(KC.count_medical_care AS FLOAT)/AP.count_total_words) * (LOG10(CAST(29748 AS FLOAT)/(SELECT COUNT(1) FROM dbo.KeywordCounts WHERE count_medical_care > 0)))                                         AS tfidf_medical_care
      ,(CAST(KC.count_ethical AS FLOAT)/AP.count_total_words) * (LOG10(CAST(29748 AS FLOAT)/(SELECT COUNT(1) FROM dbo.KeywordCounts WHERE count_ethical > 0)))                                                   AS tfidf_ethical
      ,(CAST(KC.count_social_science AS FLOAT)/AP.count_total_words) * (LOG10(CAST(29748 AS FLOAT)/(SELECT COUNT(1) FROM dbo.KeywordCounts WHERE count_social_science > 0)))                                     AS tfidf_social_science
      ,(CAST(KC.count_diagnostics AS FLOAT)/AP.count_total_words) * (LOG10(CAST(29748 AS FLOAT)/(SELECT COUNT(1) FROM dbo.KeywordCounts WHERE count_diagnostics > 0)))                                           AS tfidf_diagnostics
      ,(CAST(KC.count_surveillance AS FLOAT)/AP.count_total_words) * (LOG10(CAST(29748 AS FLOAT)/(SELECT COUNT(1) FROM dbo.KeywordCounts WHERE count_surveillance > 0)))                                         AS tfidf_surveillance
      ,(CAST(KC.count_information_sharing AS FLOAT)/AP.count_total_words) * (LOG10(CAST(29748 AS FLOAT)/(SELECT COUNT(1) FROM dbo.KeywordCounts WHERE count_information_sharing > 0)))                           AS tfidf_information_sharing
      ,(CAST(KC.count_inter_sectoral_collaboration AS FLOAT)/AP.count_total_words) * (LOG10(CAST(29748 AS FLOAT)/(SELECT COUNT(1) FROM dbo.KeywordCounts WHERE count_inter_sectoral_collaboration > 0)))         AS tfidf_inter_sectoral_collaboration
      ,(CAST(KC.count_covid19 AS FLOAT)/AP.count_total_words) * (LOG10(CAST(29748 AS FLOAT)/(SELECT COUNT(1) FROM dbo.KeywordCounts WHERE count_covid19 > 0)))                                                   AS tfidf_covid19
      ,(CAST(KC.count_sarscov2 AS FLOAT)/AP.count_total_words) * (LOG10(CAST(29748 AS FLOAT)/(SELECT COUNT(1) FROM dbo.KeywordCounts WHERE count_sarscov2 > 0)))                                                 AS tfidf_sarscov2
INTO dbo.KeywordTFIDF2
FROM dbo.KeywordCounts KC
JOIN (SELECT paper_id
            ,SUM(LEN(ISNULL(title, '') + ' ' + ISNULL(abstract, '') + ' ' + ISNULL(body_text, '')) - LEN(REPLACE(ISNULL(title, '') + ' ' + ISNULL(abstract, '') + ' ' + ISNULL(body_text, ''), ' ', ''))) + 1 AS count_total_words
        FROM dbo.AllPapers
    GROUP BY paper_id) AP ON (KC.paper_id = AP.paper_id)
