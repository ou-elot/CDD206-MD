# Project Milestone 2: Clinical Note Validation of a Gout Cohort

**Name:** Elliott Ou  
**Drug:** Allopurinol  
**Clinical condition:** Gout

## Study Purpose

In Milestone 1, I created a structured EHR cohort of patients with gout who met the study eligibility criteria and evaluated allopurinol treatment using structured OMOP data. Milestone 2 evaluates how well information documented in clinical notes can recover the same cohort concepts and treatment information.

The goals of this milestone were to:

1. identify a reproducible and computationally feasible clinical-note sample;
2. detect the cohort concepts in notes using pattern matching and at least three LLMs;
3. identify allopurinol treatment from the notes;
4. compare the demographics of the sampled cohort and note-derived treated patients; and
5. compare note-derived allopurinol identification with structured EHR drug exposure.

---

# Step 1. Clinical Note Extraction

## Full extracted note population

Clinical notes were extracted in Athena for the structured gout cohort.

The structured Milestone 1 cohort contained **5,664 patients**. The note extraction contained **433,821 clinical notes** and **5,498 unique patients**.

Therefore, 166 patients in the structured cohort did not have an extracted clinical note available in this dataset.

The extracted note fields included:

```text
person_id
cohort_start_date
cohort_end_date
person_source_value
patientepicid
deid_note_key
deid_service_date
note_type
note_text
```

## Clinical Note Extraction

The clinical notes extracted had multiple types:

| Note type | Notes |
|---|---:|
| Progress Notes | 73,684 |
| Consults | 36,797 |
| Assessment & Plan Note | 13,809 |
| H&P | 6,458 |
| Discharge Summary | 4,825 |
| **Total** | **135,573** |


A full LLM inference run analyzing all 135,573 notes with three LLMs would be computationally expensive.

## Final NLP analysis sample

The final notes subset included only types **Progress Notes** and **Assessment & Plan Notes**, since I thought they would have the most mentions of the cohort concepts.

For each patient, notes were sorted by time from cohort entry. The 3 notes closest to cohort entry date were kept.

The final sample contained:

- **13,481 notes**
- **4,985 unique patients**
- **12,487 Progress Notes**
- **994 Assessment & Plan Notes**

Thirteen selected notes were null or blank, leaving **13,468 nonblank notes** eligible for model inference.
---

# Step 2. Cohort Concept Extraction From Notes

Three concepts were used for this cohort:

- `gout_mentioned`
- `urate_mentioned`
- `allopurinol_mentioned`

The same overall classification definitions and structured output format were used for all LLMs.

The three LLMs models used were **Qwen/Qwen3-8B-AWQ**, **meta-llama/Llama-3.1-8B-Instruct**, **mistralai/Mistral-7B-Instruct-v0.3**

A text/pattern-matching baseline was also applied. If a word was found in the note, regardless of context, pattern-matching considers this positive. 

A patient was considered positive for a concept if at least one successfully evaluated selected note was positive for that concept.

## Patient-level concept counts

| Concept           |   Pattern matching patient count |   Mistral patient count |   Llama patient count |   Qwen patient count |
|:------------------|---------------------------------:|------------------------:|----------------------:|---------------------:|
| Gout              |                             2514 |                    1943 |                  2567 |                 2236 |
| Urate / uric acid |                             2189 |                     888 |                  1811 |                 1860 |
| Allopurinol       |                             1285 |                     968 |                  1289 |                 1138 |

There was substantial variation across methods, especially for urate. Mistral identified considerably fewer patients with urate documentation than the other methods. Gout and allopurinol counts were more consistent across Pattern, Llama, and Qwen, although Mistral generally identified fewer positives.

---

# Step 3. Allopurinol Identification From Clinical Notes

Within the **4,985-patient NLP sample**, the number of patients identified as having an allopurinol mention was:

| Method | Allopurinol-positive patients | Percent of NLP sample |
|---|---:|---:|
| Pattern matching | 1,285 | 25.8% |
| Mistral | 968 | 19.4% |
| Llama | 1,289 | 25.9% |
| Qwen | 1,138 | 22.8% |

All four note-based methods identified a lower proportion of treated patients than structured EHR data when evaluated in the same patient sample.

---

# Step 4. Demographics of the Sampled and Note-Derived Treated Groups

A demographic table was created in Athena for the same **4,985 patients** in the NLP sample and joined to the patient-level extraction outputs by `person_id`.

The demographic fields included:

- age at cohort entry;
- sex;
- race; and
- ethnicity.

## Table 1

| Characteristic                                  | Qualified/sample cohort   | Pattern treated   | Mistral treated   | Llama treated   | Qwen treated   |
|:------------------------------------------------|:--------------------------|:------------------|:------------------|:----------------|:---------------|
| N                                               | 4985                      | 1285              | 968               | 1289            | 1138           |
| Age, mean (SD)                                  | 60.3 (14.5)               | 60.4 (15.0)       | 60.2 (14.8)       | 60.5 (15.0)     | 60.9 (14.7)    |
| Age, median                                     | 62.0                      | 62.0              | 62.0              | 62.0            | 63.0           |
| Sex: FEMALE                                     | 1402 (28.1%)              | 280 (21.8%)       | 214 (22.1%)       | 300 (23.3%)     | 273 (24.0%)    |
| Sex: MALE                                       | 3583 (71.9%)              | 1005 (78.2%)      | 754 (77.9%)       | 989 (76.7%)     | 865 (76.0%)    |
| Race: Asian                                     | 1357 (27.2%)              | 388 (30.2%)       | 271 (28.0%)       | 383 (29.7%)     | 309 (27.2%)    |
| Race: Black or African American                 | 470 (9.4%)                | 109 (8.5%)        | 75 (7.7%)         | 112 (8.7%)      | 110 (9.7%)     |
| Race: Native Hawaiian or Other Pacific Islander | 260 (5.2%)                | 39 (3.0%)         | 30 (3.1%)         | 41 (3.2%)       | 34 (3.0%)      |
| Race: Other Race                                | 552 (11.1%)               | 131 (10.2%)       | 98 (10.1%)        | 126 (9.8%)      | 117 (10.3%)    |
| Race: Unknown                                   | 131 (2.6%)                | 41 (3.2%)         | 31 (3.2%)         | 43 (3.3%)       | 42 (3.7%)      |
| Race: White                                     | 2199 (44.1%)              | 574 (44.7%)       | 462 (47.7%)       | 580 (45.0%)     | 523 (46.0%)    |
| Ethnicity: Hispanic or Latino                   | 410 (8.2%)                | 93 (7.2%)         | 74 (7.6%)         | 95 (7.4%)       | 87 (7.6%)      |
| Ethnicity: Not Hispanic or Latino               | 4365 (87.6%)              | 1135 (88.3%)      | 846 (87.4%)       | 1131 (87.7%)    | 994 (87.3%)    |
| Ethnicity: Unknown                              | 210 (4.2%)                | 57 (4.4%)         | 48 (5.0%)         | 63 (4.9%)       | 57 (5.0%)      |

Across methods, the note-derived allopurinol-treated groups were demographically similar to one another and broadly consistent with the treated cohort from Milestone 1.

The full NLP sample had a mean age of **60.3 years** and was **71.9% male**. The note-derived treated groups were more heavily male, ranging from **76.0% to 78.2% male** across methods. This was similar to the structured allopurinol-treated cohort in Milestone 1, which was approximately **78.2% male**.

Age distributions were also highly similar across methods, with mean ages around 60 to 61 years. Race and ethnicity distributions did not show large shifts across the extraction methods.

Overall, the demographic patterns were consistent with the expectation from Milestone 1 that patients identified as receiving allopurinol would be more frequently male while having a similar age distribution to the overall gout cohort.

---

# Step 5. Structured EHR vs Clinical-Note Identification of Allopurinol

To make a direct patient-level comparison, the structured allopurinol treatment definition from Milestone 1 was applied to the same **4,985 NLP-analysis patients**.

Within this common population:

- **1,849** patients were structured-EHR treated
- **3,136** patients were structured-EHR not treated
- structured treatment prevalence was **37.1%**

The structured indicator was then compared patient-by-patient with the note-derived `allopurinol_mentioned` result from each method.

## Agreement with structured EHR treatment

| Method | TP | FN | FP | TN | Sensitivity | Specificity | PPV | NPV | Agreement |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Pattern matching | 910 | 939 | 375 | 2,761 | 49.2% | 88.0% | 70.8% | 74.6% | 73.6% |
| Mistral | 731 | 1,118 | 237 | 2,899 | 39.5% | 92.4% | 75.5% | 72.2% | 72.8% |
| Llama | 891 | 958 | 398 | 2,738 | 48.2% | 87.3% | 69.1% | 74.1% | 72.8% |
| Qwen | 835 | 1,014 | 303 | 2,833 | 45.2% | 90.3% | 73.4% | 73.6% | 73.6% |

## Interpretation

For identifying whether a patient received allopurinol, the **structured EHR appears more reliable than relying only on the sampled clinical notes**.

The main evidence is the relatively low sensitivity of all note-based methods. Only **39.5% to 49.2%** of patients with structured allopurinol treatment were identified as allopurinol-positive in the selected notes. Even the highest-sensitivity method, pattern matching, missed **939 of 1,849** structured-treated patients.

At the same time, specificity was relatively high (**87.3% to 92.4%**) and PPV ranged from **69.1% to 75.5%**. This means a positive allopurinol mention in a note was often consistent with structured treatment, but absence of a mention was not strong evidence that the patient was untreated.

The most likely explanation is that a structured medication exposure can exist without allopurinol being explicitly discussed in one of the patient's three selected notes. Clinical notes also provide information that structured drug exposure does not capture as easily, including whether treatment was being discussed, continued, stopped, held, or considered in a particular clinical context.

Therefore, for the narrow question of **whether a patient received allopurinol**, I would rely primarily on structured EHR drug exposure. Clinical-note extraction is better used as a complementary source for validating treatment and understanding clinical context.

---

# Exploratory Note-Type Check

Because Assessment & Plan notes might be expected to contain more medication information, I also examined the frequency of allopurinol-positive notes by note type using existing note-level outputs.

For the methods with complete results available in this check:

| Method | Progress Notes positive | Assessment & Plan positive |
|---|---:|---:|
| Pattern matching | 15.3% | 7.5% |
| Mistral | 11.0% | 6.0% |
| Llama | 15.3% | 8.0% |

Contrary to the initial expectation, Progress Notes had a higher allopurinol-positive rate than Assessment & Plan Notes in these results. Therefore, the relatively small number of Assessment & Plan notes alone is unlikely to explain the low sensitivity of note-based treatment identification.

This does not eliminate sampling as a limitation: allopurinol may still have been documented in other note types or in Progress/A&P notes that were not among the three selected notes for a patient.

---

# Limitations

1. **Incomplete note availability.** The structured cohort contained 5,664 patients, but only 5,498 had extracted clinical notes.
2. **Note-type restriction.** The final NLP analysis used only Progress Notes and Assessment & Plan Notes.
3. **Maximum three notes per patient.** Relevant treatment documentation may have appeared in an unselected note.
4. **Sampling by proximity to cohort entry.** This prioritized documentation near index but may omit later or earlier medication information.
5. **Narrative documentation is not equivalent to medication exposure.** A patient may receive allopurinol without the drug being mentioned in a selected note.
6. **Positive note mentions can have temporal ambiguity.** A mention may describe historical use, discontinuation, or discussion rather than treatment during the structured exposure period.
7. **Model disagreement.** The models differed substantially for some concepts, particularly urate.
8. **Parsing failures.** A small number of Llama and Qwen outputs failed parsing; failures were tracked separately rather than automatically treated as negative predictions.
9. **Single health-system data source.** Results may not generalize to other institutions or documentation practices.

---

# Conclusion

Clinical notes were useful for recovering gout, urate, and allopurinol information, but note-based extraction alone did not identify all patients with structured allopurinol exposure.

Across Pattern, Mistral, Llama, and Qwen, note-based allopurinol extraction showed high specificity but limited sensitivity. The results support using **structured EHR medication data as the primary source for determining whether allopurinol treatment occurred**, while using clinical notes as a complementary source for contextual information and validation.

---

# Reproducibility

Key analysis outputs include:

```text
outputs/patient_level_positive_counts_all_methods.csv
outputs/table1_all_methods_allopurinol_treated.csv
outputs/structured_vs_note_allopurinol_summary.csv
outputs/structured_vs_note_allopurinol_summary.md
```

Key scripts include:

```text
scripts/create_demographic_table1.py
scripts/compare_structured_allopurinol.py
```

The repository should also include the SQL used for:

- clinical-note extraction;
- final note subset selection;
- demographic extraction;
- structured allopurinol extraction;
- and Athena exports.

No new LLM inference is required to reproduce the downstream demographic and structured-vs-note comparisons if the note-level prediction files are retained.
