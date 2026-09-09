-- Demographics for the 4,985 NLP-analysis patients

CREATE TABLE eou.gout_nlp_demographics AS
WITH cohort_patients AS (
    SELECT DISTINCT
        person_id,
        cohort_start_date
    FROM eou.gout_notes_nlp_subset
)
SELECT
    c.person_id,
    c.cohort_start_date,
    YEAR(c.cohort_start_date) - p.year_of_birth AS age_at_index,
    gender.concept_name AS sex,
    race.concept_name AS race,
    ethnicity.concept_name AS ethnicity
FROM cohort_patients c
JOIN deid_omop.person p
    ON c.person_id = p.person_id
LEFT JOIN deid_omop.concept gender
    ON p.gender_concept_id = gender.concept_id
LEFT JOIN deid_omop.concept race
    ON p.race_concept_id = race.concept_id
LEFT JOIN deid_omop.concept ethnicity
    ON p.ethnicity_concept_id = ethnicity.concept_id;
