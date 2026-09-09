-- Structured allopurinol indicator for the same 4,985 NLP-analysis patients.
-- Mirrors the treatment logic from the ATLAS treated cohort:
-- allopurinol codeset ancestor concept 1167322, with >=1 exposure
-- during the observation period containing cohort entry.

CREATE TABLE eou.gout_nlp_structured_allopurinol AS

WITH cohort_patients AS (
    SELECT DISTINCT
        person_id,
        cohort_start_date
    FROM eou.gout_notes_nlp_subset
),

allopurinol_concepts AS (
    SELECT 1167322 AS concept_id

    UNION

    SELECT ca.descendant_concept_id
    FROM deid_omop.concept_ancestor ca
    JOIN deid_omop.concept c
        ON ca.descendant_concept_id = c.concept_id
    WHERE ca.ancestor_concept_id = 1167322
      AND c.invalid_reason IS NULL
),

index_observation_period AS (
    SELECT
        c.person_id,
        c.cohort_start_date,
        op.observation_period_start_date,
        op.observation_period_end_date
    FROM cohort_patients c
    JOIN deid_omop.observation_period op
        ON c.person_id = op.person_id
       AND c.cohort_start_date >= op.observation_period_start_date
       AND c.cohort_start_date <= op.observation_period_end_date
),

treated AS (
    SELECT DISTINCT
        c.person_id
    FROM index_observation_period c
    JOIN deid_omop.drug_exposure d
        ON c.person_id = d.person_id
    JOIN allopurinol_concepts a
        ON d.drug_concept_id = a.concept_id
    WHERE d.drug_exposure_start_date >= c.observation_period_start_date
      AND d.drug_exposure_start_date <= c.observation_period_end_date
)

SELECT
    c.person_id,
    c.cohort_start_date,
    CASE
        WHEN t.person_id IS NOT NULL THEN 1
        ELSE 0
    END AS structured_allopurinol
FROM cohort_patients c
LEFT JOIN treated t
    ON c.person_id = t.person_id;
