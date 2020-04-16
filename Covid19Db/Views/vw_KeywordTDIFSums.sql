CREATE   VIEW dbo.vw_KeywordTDIFSums AS
SELECT SUM(count_total_words)                      AS sum_count_total_words
      ,SUM(tfidf_transmission)                     AS sum_tfidf_transmission
      ,SUM(tfidf_incubation)                       AS sum_tfidf_incubation
      ,SUM(tfidf_environmental_stability)          AS sum_tfidf_environmental_stability
      ,SUM(tfidf_risk)                             AS sum_tfidf_risk
      ,SUM(tfidf_virus)                            AS sum_tfidf_virus
      ,SUM(tfidf_genetics)                         AS sum_tfidf_genetics
      ,SUM(tfidf_origin)                           AS sum_tfidf_origin
      ,SUM(tfidf_evolution)                        AS sum_tfidf_evolution
      ,SUM(tfidf_vaccines)                         AS sum_tfidf_vaccines
      ,SUM(tfidf_therapeutics)                     AS sum_tfidf_therapeutics
      ,SUM(tfidf_non_pharmaceutical_interventions) AS sum_tfidf_non_pharmaceutical_interventions
      ,SUM(tfidf_published)                        AS sum_tfidf_published
      ,SUM(tfidf_medical_care)                     AS sum_tfidf_medical_care
      ,SUM(tfidf_ethical)                          AS sum_tfidf_ethical
      ,SUM(tfidf_social_science)                   AS sum_tfidf_social_science
      ,SUM(tfidf_diagnostics)                      AS sum_tfidf_diagnostics
      ,SUM(tfidf_surveillance)                     AS sum_tfidf_surveillance
      ,SUM(tfidf_information_sharing)              AS sum_tfidf_information_sharing
      ,SUM(tfidf_inter_sectoral_collaboration)     AS sum_tfidf_inter_sectoral_collaboration
      ,SUM(tfidf_covid19)                          AS sum_tfidf_covid19
      ,SUM(tfidf_sarscov2)                         AS sum_tfidf_sarscov2
  FROM dbo.KeywordTFIDF
