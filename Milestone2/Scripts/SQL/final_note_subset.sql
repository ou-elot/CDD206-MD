-- Final NLP note subset
-- Keeps Progress Notes and Assessment & Plan Notes.
-- Retains up to 3 notes per patient, ranked by proximity to cohort entry.

CREATE TABLE eou.gout_notes_nlp_subset AS
WITH ranked_notes AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY person_id
            ORDER BY
                ABS(
                    date_diff(
                        'day',
                        cohort_start_date,
                        CAST(deid_service_date AS DATE)
                    )
                ),
                CAST(deid_service_date AS DATE),
                deid_note_key
        ) AS note_rank
    FROM eou.gout_extracted_notes
    WHERE note_type IN (
        'Progress Notes',
        'Assessment & Plan Note'
    )
)
SELECT *
FROM ranked_notes
WHERE note_rank <= 3;
