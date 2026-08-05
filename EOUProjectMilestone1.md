
# Effectiveness of Allopurinol in Patients With Gout

 Elliott Ou
 
 Albert Lee
 
 UCSF ACID3

## Study Purpose

This cohort study determined if allopurinol treatment was effective in lowering serum urate levels to target in adults with gout in UCSF's de-identified OMOP dataset.

Allopurinol is a urate-lowering medication used for the long-term management of gout. It reduces uric acid production and is intended to lower serum urate and reduce future gout-related complications. It is not primarily used to relieve pain during an acute gout flare.

Among adults with gout, were patients with a recorded allopurinol exposure more likely to achieve a follow-up serum urate level below 6 mg/dL than patients without a recorded allopurinol exposure?

## Data Source

The primary analysis used the OMOP DEID UCSF data source in ATLAS.
## Cohort Definition

### Cohort Entry

The cohort entry event was the patient's first diagnosis of gout. This date is used as the index date in this study. 

### Inclusion Criteria

Patients were required to:
1. Be 18 years of age or older on the index date.
2. Have a recorded diagnosis of gout.

Previous use of gout medications was not used as an exclusion criterion.

Patients were classified as allopurinol-treated if they had at least one recorded allopurinol drug exposure. The comparison cohort consisted of patients with gout but had no recorded allopurinol exposures.

## Follow-Up and Effectiveness Outcome

Patient data up to 180 days after cohort entry was used to determine effectiveness. 

An 180-day follow-up period was selected because allopurinol is commonly initiated at a low dose and adjusted over time. The effectiveness outcome was determined by lowering the blood or serum urate value below 6 mg/dL. 6 mg/dL is the recommended serum urate treatment target. Patients with more severe gout cases may have lower targets.

For both treatments, two separate outcome groups were generated:

1. Patients with at least one blood or serum urate measurement between days 90 and 180.
2. Patients with at least one blood or serum urate measurement below 6 mg/dL during the same 90-180 day period. 

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

## Effectiveness Analysis

Only patients with at least one follow-up blood or serum urate measurement between days 90 and 180 could be evaluated for the effectiveness outcome.

### Allopurinol-Treated Group

In the 1,915 allopurinol-treated patients:

- 536 had at least one follow-up urate measurement between days 90 and 180.
- 190 had at least one follow-up urate measurement below 6 mg/dL during that period.
- 346 did not have a recorded follow-up value below 6 mg/dL.

### No-Recorded-Allopurinol Group

In the 3,749 patients without treatment:

- 471 had at least one follow-up urate measurement between days 90 and 180.
- 161 had at least one follow-up urate measurement below 6 mg/dL during that period.
- 310 did not have a recorded follow-up value below 6 mg/dL.

### Outcome Table

| Treatment group | Follow-up available | Urate <6 mg/dL, n (%) | 
|---|---:|---:|
| Allopurinol-treated | 536 | 190 (35.45%) |
| No recorded allopurinol | 471 | 161 (34.18%) |
| **Total** | **1,007** | **351 (34.86%)** |

The target achievement rate was calculated as number of patients with successful outcome divided by all follow up measurements.

For the allopurinol-treated group:

`190/536 = 35.45%`

For the no-recorded-allopurinol group:

`161/471 = 34.18%`

The difference between the groups was:

`35.45% − 34.18% = 1.27%`

## Statistical Analysis

A Pearson chi-square test of independence was used to compare the proportion of patients achieving serum urate below 6 mg/dL between the two exposure groups.

The hypotheses were:

- **Null hypothesis:** Achievement of serum urate below 6 mg/dL is independent of treatment
- **Alternative hypothesis:** Achievement of serum urate below 6 mg/dL differs between the treatment and control group. 

Observed results:

| Treatment group | Urate <6 mg/dL | No recorded urate <6 mg/dL |
|---|---:|---:|
| Allopurinol-treated | 190 | 346 |
| No recorded allopurinol | 161 | 310 |

The Pearson chi-square test produced:

**χ²(1) = 0.18, p = 0.67**

Because the p-value was greater than 0.05, the null hypothesis was not rejected. The treatment does not have a significant effect in lowering serum urate levels. 

## Conclusion

Among patients with an available follow-up urate measurement, 35.45% of allopurinol-treated patients and 34.18% of patients without recorded allopurinol achieved a serum urate value below 6 mg/dL. The difference was not statistically significant.

Therefore, analysis determined that recorded allopurinol exposure had no association with a greater likelihood of achieving the serum urate treatment target between days 90 and 180.

## Limitations

This study has several limitations:

1. Allopurinol exposure was based on recorded drug exposure and does not confirm that patients took the medication as prescribed.
2. Information on medication dose, dose escalation, adherence, and treatment discontinuation was not included.
3. Only patients with a recorded follow-up urate measurement between days 90 and 180 could be included in the effectiveness analysis. Allopurinol may take longer to reach desired outcomes. 
5. The outcome definition used a value to judge success, instead of change in urate levels. 
5. The analysis was unadjusted and did not control for differences in chronic gout, type 2 diabetes, chronic kidney disease, age, sex, race, ethnicity, or other potential confounding factors.
6. The study used only one dataset, which may limit generalizability to the general population.

## Rubric and Self-Assessment

| Component | Your Score | Albert Score | Points | Additional Justification (if needed) | Comments from Albert |
|---|---:|---:|---:|---|---|
| There is a markdown file in Project Milestone 1 Submissions, and it includes a project title and my name. | 1 |  | 1 | The submission is written in Markdown and includes the project title and author name at the top of the page. |  |
| The page adequately describes the purpose of the study. | 3 |  | 3 | The study purpose, selected treatment, clinical role of allopurinol, research question, treatment definition, and effectiveness outcome are described. |  |
| The page adequately describes the cohort definition. | 3 |  | 3 | The page defines the cohort entry event, age requirement, gout diagnosis, baseline urate requirement, treatment-assignment window, comparison group, follow-up period, and outcome window. |  |
| The page includes a Table 1 for the cohort within UCSF. | 3 |  | 3 | Table 1 reports age, sex, race, ethnicity, and relevant baseline clinical characteristics for the full UCSF cohort and both exposure groups. |  |
| **Total** | **10** |  | **10** |  |  |
