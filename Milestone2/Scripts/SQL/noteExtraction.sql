-- extract_clinical_notes.sql
-- Milestone 2 clinical-note extraction for the gout cohort.
--
-- Replace <COHORT_TABLE> with the Athena table containing your
-- Milestone 1 cohort and these columns:
--   person_id
--   cohort_start_date
--   cohort_end_date

CREATE TABLE eou.gout_extracted_notes AS

WITH cohort AS (
    SELECT DISTINCT
        person_id,
        cohort_start_date,
        cohort_end_date
    FROM <COHORT_TABLE>
)

SELECT
    c.person_id,
    c.cohort_start_date,
    c.cohort_end_date,
    p.person_source_value,
    nm.patientepicid,
    nm.deid_note_key,
    nm.deid_service_date,
    nm.note_type,
    nt.note_text
FROM cohort c

JOIN deid_omop.person p
    ON c.person_id = p.person_id

JOIN deid_cdw.note_metadata nm
    ON CAST(p.person_source_value AS VARCHAR)
     = CAST(nm.patientepicid AS VARCHAR)

JOIN deid_cdw.note_text nt
    ON nm.deid_note_key = nt.deid_note_key
;

-- Verify full extraction
SELECT
    COUNT(*) AS total_notes,
    COUNT(DISTINCT deid_note_key) AS unique_notes,
    COUNT(DISTINCT person_id) AS patients_with_notes
FROM eou.gout_extracted_notes
;

-- Note-type distribution
SELECT
    note_type,
    COUNT(*) AS note_count,
    COUNT(DISTINCT person_id) AS patient_count
FROM eou.gout_extracted_notes
GROUP BY note_type
ORDER BY note_count DESC
;

-- Initial clinically relevant candidate subset
CREATE TABLE eou.gout_notes_candidate_subset AS

SELECT *
FROM eou.gout_extracted_notes
WHERE note_type IN (
    'Progress Notes',
    'Consults',
    'Assessment & Plan Note',
    'H&P',
    'Discharge Summary'
)
;

SELECT
    COUNT(*) AS total_candidate_notes,
    COUNT(DISTINCT person_id) AS candidate_patients
FROM eou.gout_notes_candidate_subset
;
