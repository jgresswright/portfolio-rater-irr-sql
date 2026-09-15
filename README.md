# SQL/DuckDB Rater-IRR Analytics

## Executive Summary

This project analyzes inter-rater agreement and disagreement patterns in a synthetic LLM-evaluation dataset (12 raters, 900 evaluations, 2,700 ratings across 6 batches) using SQL against a local DuckDB database — a second, independent portfolio piece built to demonstrate SQL depth (CTEs, window functions, joins) as a companion to an earlier R-based statistical analysis of the same domain.

**Key Cross-Dataset Finding:** This project independently reproduces the earlier R portfolio project's core finding — opinion-based evaluations show the lowest rater agreement of any domain — this time on a fully separate synthetic dataset, giving that pattern a validated, cross-dataset result rather than a single-dataset observation.

**Key Technical Achievement:** A full SQL analytics pipeline covering four distinct query patterns — aggregation/joins, CTE-based window functions, CASE-based cohort bucketing, and RANK()-based tie-aware ranking — all hand-written and debugged without code generation, consistent with an own-work-first approach to skill-building.

## Project Overview

Where the companion R project asked *"how reliable is rater agreement overall, and what predicts disagreement?"* using statistical modeling, this project asks a narrower, SQL-native question: *"what can raw query logic alone surface about agreement, rater volatility, and batch drift — without a statistics library in the loop?"* It's a deliberate constraint: no `dplyr`, no `irr` package, just SQL against a relational schema.

## Business Context

Large-scale LLM evaluation pipelines generate exactly this kind of data — multiple raters scoring the same items over time, in batches, with quality and consistency questions that operations teams (not just researchers) need to answer directly from the data warehouse. This project mirrors that operational reality: the questions are the kind a quality lead would run against a live annotation database, not just what a statistician would run in a notebook.

## Technical Approach

### Data

Synthetic dataset generated for this project (independent of the R project's dataset):
- 12 raters
- 900 evaluations
- 2,700 individual ratings
- 6 batches (early: B1–B2, mid: B3, late: B4–B6)

### Query Categories

1. **Aggregation & Joins** — Per-evaluation agreement computed as a MAX−MIN spread across raters, broken down by domain. Replicates the R project's finding that opinion evaluations show the lowest agreement of any domain, this time via direct SQL aggregation rather than Fleiss' Kappa.

2. **CTEs & Window Functions (LAG)** — Per-rater rolling volatility, computed as the average absolute delta between a rater's consecutive ratings. Surfaces a real spread between the most-volatile rater (R008, ~1.76 average delta) and the most-consistent (R007, ~1.54).

3. **CASE-Based Cohort Bucketing** — Early-batch (B1–B2) vs. late-batch (B4–B6) comparison of disagreement levels. Found a small but real increase in disagreement in later batches — flagged as a pattern worth monitoring rather than over-interpreted, given the modest size of the gap.

4. **RANK() with Tie Handling** — Most-disagreed-upon evaluation per rater per batch, using `RANK()` rather than `ROW_NUMBER()` specifically to surface multi-way ties correctly (e.g., a four-way tie for maximum deviation in batch B1) rather than arbitrarily picking one result.

### Technologies Used

- **DuckDB** (local, no cloud warehouse dependency)
- **SQL**: CTEs, window functions (`LAG`, `RANK`), `CASE` expressions, multi-table joins
- **Reproducible, hand-written queries** — no query generation; all four categories were written cold and debugged independently

## Key Findings

- **Opinion evaluations remain the hardest to agree on** — this holds across two independently generated synthetic datasets and two entirely different analytical approaches (R/statistical vs. SQL/aggregation), which is a stronger claim than either project could make alone.
- **Rater volatility is measurable and meaningfully different across raters** — a ~0.22-point gap in average consecutive-rating delta between the most- and least-volatile raters in this dataset.
- **A modest late-batch drift in disagreement appeared** — real, but small enough that it's presented here as a flag for further monitoring rather than a strong conclusion.
- **Tie-aware ranking matters** — a naive `ROW_NUMBER()` approach would have silently discarded three of four genuinely tied "most disagreed" evaluations in one batch; `RANK()` preserves them.

## Scope Note

A dashboard/visualization layer was deliberately scoped **out** of this project to keep the focus on SQL query depth rather than presentation tooling. All results here come directly from SQL output.

## Repository Structure

```
sql-duckdb-rater-irr/
│
├── README.md                          # This file
├── data/
│   └── generate_data.py   # synthetic dataset creation
│
├── queries/
│   ├── 01_aggregation_joins.sql       # Agreement spread by domain
│   ├── 02_cte_window_volatility.sql   # Rater volatility via LAG
│   ├── 03_case_cohort_comparison.sql  # Early vs. late batch comparison
│   └── 04_rank_tie_handling.sql       # Most-disagreed evaluation per rater/batch
│
└── db/
    └── rater_irr.duckdb                # Local DuckDB database file
```

## Running the Analysis

```bash
# 1. Generate the synthetic dataset
duckdb rater_irr.duckdb < data/generate_data.py

# 2. Run each query category
duckdb rater_irr.duckdb < queries/01_aggregation_joins.sql
duckdb rater_irr.duckdb < queries/02_cte_window_volatility.sql
duckdb rater_irr.duckdb < queries/03_case_cohort_comparison.sql
duckdb rater_irr.duckdb < queries/04_rank_tie_handling.sql
```

## Skills Demonstrated

- **SQL Depth**: Multi-table joins, chained CTEs, window functions (`LAG`, `RANK`), `CASE`-based bucketing
- **Data Modeling**: Designing a relational schema for rater/evaluation/batch data
- **Cross-Project Validation**: Independently confirming a finding from a separate portfolio project using a different tool and dataset
- **Reproducible, Own-Work Analysis**: All queries hand-written and debugged without code generation
- **Domain Expertise**: LLM evaluation quality and inter-rater reliability

## Related Work

This project is a companion piece to [Statistical Analysis of LLM Evaluation Quality Patterns](../portfolio-llm-eval-quality) — the R/tidyverse project that first surfaced the opinion-agreement finding this project independently reproduces.

## About This Project

Developed to demonstrate SQL analytics capability in the context of large-scale LLM evaluation systems, as a complement to statistical (R-based) analysis of the same domain. All data is synthetically generated; no proprietary or confidential information is included.

## Contact

**Jonathan Gress-Wright**

- LinkedIn: <https://www.linkedin.com/in/jonathan-gress-wright/>
- GitHub: <https://github.com/jgresswright/>
- Email: gressmeister@gmail.com

---

*All data in this project is synthetically generated. No proprietary or confidential information is included.*
