-- Verification query for structured allopurinol table.
-- Expected:
-- total_patients = 4985
-- unique_patients = 4985
-- structured_treated = 1849
-- structured_not_treated = 3136

SELECT
    COUNT(*) AS total_patients,
    COUNT(DISTINCT person_id) AS unique_patients,
    SUM(structured_allopurinol) AS structured_treated,
    COUNT(*) - SUM(structured_allopurinol) AS structured_not_treated
FROM eou.gout_nlp_structured_allopurinol;
