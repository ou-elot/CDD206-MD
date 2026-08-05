
# Effectiveness of Allopurinol in Patients With Gout

 Elliott Ou
 Albert Lee
 UCSF ACID3

## Study Purpose

This retrospective cohort study evaluated whether recorded allopurinol treatment was associated with achievement of the recommended serum urate treatment target among adults with gout in UCSF's de-identified OMOP data.

Allopurinol is a urate-lowering medication used for the long-term management of gout. It reduces uric acid production and is intended to lower serum urate and reduce future gout-related complications. It is not primarily used to relieve pain during an acute gout flare.

The study question was:

Among adults with gout, were patients with a recorded allopurinol exposure more likely to achieve a follow-up serum urate level below 6 mg/dL than patients without a recorded allopurinol exposure?

## Data Source

The primary analysis used the OMOP DEID UCSF data source in ATLAS.

A secondary feasibility check was also performed using the combined UCSF and SFDPH data source, but the UCSF-only cohort was used for the primary results and Table 1.

## Cohort Definition

### Cohort Entry

The cohort entry event was the first qualifying diagnosis of gout during the patient's observation period.

The date of the qualifying gout diagnosis was used as the index date.

### Inclusion Criteria

Patients were required to:

1. Be 18 years of age or older on the index date.
2. Have a recorded diagnosis of gout.
3. Have at least one blood or serum urate measurement from 90 days before through 14 days after the index date.

Previous use of gout medications was not used as an exclusion criterion.

### Allopurinol-Treated Group

Patients were classified as allopurinol-treated if they had at least one recorded allopurinol drug exposure.

### No-Recorded-Allopurinol Group

The comparison cohort consisted of patients who met the cohort criteria but had no recorded allopurinol exposures.

The allopurinol-treated and no-recorded-allopurinol groups were therefore mutually exclusive and together accounted for the full qualifying cohort.

## Follow-Up and Effectiveness Outcome

Patients were followed for up to 180 days after cohort entry.

A 180-day follow-up period was selected because allopurinol is commonly initiated at a low dose and adjusted over time using repeated serum urate measurements. The outcome window of days 90 through 180 allowed approximately three to six months for treatment initiation, dose adjustment, and measurement of the patient's serum urate response.

The effectiveness outcome was achievement of a blood or serum urate value below 6 mg/dL between days 90 and 180 after cohort entry.

This value represents achievement of the recommended serum urate treatment target. It does not mean that the patient was cured of gout.

For both treatment groups, two separate outcome cohorts were generated directly:

1. Patients with at least one blood or serum urate measurement between days 90 and 180.
2. Patients with at least one blood or serum urate measurement below 6 mg/dL during the same period.

The comparison-group outcome counts were generated directly from the no-recorded-allopurinol cohort rather than being estimated by subtraction.

## Cohort Sizes

| Cohort | Number of patients |
|---|---:|
| Full qualifying UCSF gout cohort | 5,664 |
| Allopurinol-treated group | 1,915 |
| No recorded allopurinol group | 3,749 |

The treated and no-recorded-allopurinol groups account for the full cohort:

`1,915 + 3,749 = 5,664`

The percentage of the full cohort with recorded allopurinol exposure was:

`(1,915 / 5,664) × 100 = 33.81%`


## Table 1. Baseline Characteristics of the UCSF Gout Cohort

| Characteristic | Full cohort (n = 5,664) | Allopurinol-treated (n = 1,915) | No recorded allopurinol (n = 3,749) |
|---|---:|---:|---:|
| **Age, years** |  |  |  |
| Mean (SD) | 60.03 (14.42) | 60.59 (14.63) | 59.75 (14.30) |
| Median | 62 | 62 | 61 |
| 25th–75th percentile | 51–71 | 51–72 | 51–70 |
| Range | 18–90 | 18–90 | 19–90 |
| **Sex, n (%)** |  |  |  |
| Male | 4,063 (71.73%) | 1,498 (78.22%) | 2,565 (68.42%) |
| Female | 1,601 (28.27%) | 417 (21.78%) | 1,184 (31.58%) |
| **Ethnicity, n (%)** |  |  |  |
| Not Hispanic or Latino | 4,925 (86.95%) | 1,698 (88.67%) | 3,227 (86.08%) |
| Hispanic or Latino | 442 (7.80%) | 171 (8.93%) | 271 (7.23%) |
| Unknown or not reported | 297 (5.24%) | 46 (2.40%) | 251 (6.70%) |
| **Race, n (%)** |  |  |  |
| White | 2,550 (45.02%) | 852 (44.49%) | 1,698 (45.29%) |
| Asian | 1,441 (25.44%) | 594 (31.02%) | 847 (22.59%) |
| Black or African American | 532 (9.39%) | 182 (9.50%) | 354 (9.44%) |
| Native Hawaiian or Other Pacific Islander | 358 (6.32%) | 43 (2.25%) | 315 (8.40%) |
| Other race | 609 (10.75%) | 201 (10.50%) | 408 (10.88%) |
| Unknown or not reported | 174 (3.07%) | 43 (2.25%) | 115 (3.07%) |
| **Baseline clinical characteristics, n (%)** |  |  |  |
| Chronic gout | 957 (16.90%) | 677 (35.35%) | 280 (7.47%) |
| Type 2 diabetes | 1,832 (32.34%) | 793 (41.41%) | 1,039 (27.71%) |
| Chronic kidney disease | 2,807 (49.56%) | 1,153 (60.21%) | 1,654 (44.12%) |

The allopurinol-treated group had a similar average age to the no-recorded-allopurinol group but contained a larger proportion of male and Asian patients.

The allopurinol-treated group also had a higher recorded prevalence of chronic gout, type 2 diabetes, and chronic kidney disease than the no-recorded-allopurinol group.

These differences indicate that the two exposure groups were not fully comparable at baseline and suggest potential confounding by indication and underlying disease complexity.

## Effectiveness Analysis

Only patients with at least one follow-up blood or serum urate measurement between days 90 and 180 could be evaluated for the effectiveness outcome.

The outcome cohorts were generated directly for the allopurinol-treated and no-recorded-allopurinol groups.

### Allopurinol-Treated Group

Among the 1,915 allopurinol-treated patients:

- 536 had at least one follow-up urate measurement between days 90 and 180.
- 190 had at least one follow-up urate measurement below 6 mg/dL during that period.
- 346 did not have a recorded follow-up value below 6 mg/dL.

### No-Recorded-Allopurinol Group

Among the 3,749 patients without recorded allopurinol:

- 471 had at least one follow-up urate measurement between days 90 and 180.
- 161 had at least one follow-up urate measurement below 6 mg/dL during that period.
- 310 did not have a recorded follow-up value below 6 mg/dL.

### Outcome Table

| Treatment group | Follow-up urate available | Urate <6 mg/dL, n (%) | No recorded urate <6 mg/dL, n (%) |
|---|---:|---:|---:|
| Allopurinol-treated | 536 | 190 (35.45%) | 346 (64.55%) |
| No recorded allopurinol | 471 | 161 (34.18%) | 310 (65.82%) |
| **Total** | **1,007** | **351 (34.86%)** | **656 (65.14%)** |

The target achievement rate was calculated as:

**Target achievement rate = (number of patients with a follow-up urate below 6 mg/dL / number of patients with any follow-up urate measurement) × 100**

For the allopurinol-treated group:

`(190 / 536) × 100 = 35.45%`

For the no-recorded-allopurinol group:

`(161 / 471) × 100 = 34.18%`

The absolute difference between the groups was:

`35.45% − 34.18% = 1.27 percentage points`

## Statistical Analysis

A Pearson chi-square test of independence was used to compare the proportion of patients achieving serum urate below 6 mg/dL between the two exposure groups.

The hypotheses were:

- **Null hypothesis:** Achievement of serum urate below 6 mg/dL is independent of recorded allopurinol exposure.
- **Alternative hypothesis:** Achievement of serum urate below 6 mg/dL differs between the allopurinol-treated and no-recorded-allopurinol groups.

The observed contingency table was:

| Treatment group | Urate <6 mg/dL | No recorded urate <6 mg/dL |
|---|---:|---:|
| Allopurinol-treated | 190 | 346 |
| No recorded allopurinol | 161 | 310 |

The Pearson chi-square test produced:

**χ²(1) = 0.18, p = 0.67**

Because the p-value was greater than 0.05, the null hypothesis was not rejected.

## Conclusion

Among patients with an available follow-up urate measurement, 35.45% of allopurinol-treated patients and 34.18% of patients without recorded allopurinol achieved a serum urate value below 6 mg/dL.

The difference of 1.27 percentage points was not statistically significant.

Therefore, this unadjusted analysis did not find evidence that recorded allopurinol exposure was associated with a greater likelihood of achieving the serum urate treatment target between days 90 and 180.

This finding should not be interpreted as proof that allopurinol is ineffective.

The allopurinol-treated group had substantially higher recorded prevalence of chronic gout, type 2 diabetes, and chronic kidney disease. These differences suggest that treated patients may have had more severe gout or greater underlying disease complexity.

Because these baseline factors may affect both the likelihood of receiving allopurinol and the likelihood of reaching the serum urate target, the crude comparison may be affected by confounding by indication.

A more complete analysis would adjust for these baseline differences using methods such as multivariable regression, matching, stratification, or propensity score adjustment.

## Limitations

This study has several limitations:

1. Allopurinol exposure was based on recorded drug exposure and does not confirm that patients took the medication as prescribed.
2. Patients were not required to be new users of allopurinol, so some treated patients may have been continuing an existing prescription.
3. Information on medication dose, dose escalation, adherence, and treatment discontinuation was not included.
4. Only patients with a recorded follow-up urate measurement between days 90 and 180 could be included in the effectiveness analysis. Allopurinol may take longer to reach desired outcomes. 
5. Patients with follow-up measurements may differ from patients without follow-up laboratory testing.
6. The outcome definition identified whether a patient had at least one urate value below 6 mg/dL during follow-up rather than selecting one standardized measurement per patient.
7. A patient with multiple measurements could qualify based on one value below 6 mg/dL even if another value during the same period was higher.
8. The analysis was unadjusted and did not control for differences in chronic gout, type 2 diabetes, chronic kidney disease, age, sex, race, ethnicity, or other potential confounding factors.
9. The study used data from one healthcare system, which may limit generalizability to other populations.

## Rubric and Self-Assessment

| Component | Your Score | Albert Score | Points | Additional Justification (if needed) | Comments from Albert |
|---|---:|---:|---:|---|---|
| There is a markdown file in Project Milestone 1 Submissions, and it includes a project title and my name. | 1 |  | 1 | The submission is written in Markdown and includes the project title and author name at the top of the page. |  |
| The page adequately describes the purpose of the study. | 3 |  | 3 | The study purpose, selected treatment, clinical role of allopurinol, research question, treatment definition, and effectiveness outcome are described. |  |
| The page adequately describes the cohort definition. | 3 |  | 3 | The page defines the cohort entry event, age requirement, gout diagnosis, baseline urate requirement, treatment-assignment window, comparison group, follow-up period, and outcome window. |  |
| The page includes a Table 1 for the cohort within UCSF. | 3 |  | 3 | Table 1 reports age, sex, race, ethnicity, and relevant baseline clinical characteristics for the full UCSF cohort and both exposure groups. |  |
| **Total** | **10** |  | **10** |  |  |
