"""
Synthetic data generator: SQL/DuckDB Rater-IRR Analytics Pipeline
Same conceptual domain as the R portfolio project (LLM evaluation quality),
but generated fresh and shaped specifically for SQL window-function /
CTE / cohort-join practice rather than reused from the R project.

Design choices made deliberately to give the SQL project real teeth:
  - Ratings are spread across BATCHES (cohorts) over time, so LAG/LEAD
    and per-rater rolling comparisons are meaningful, not decorative.
  - Raters have persistent profiles (tendency, consistency, expertise)
    that drift slightly batch-to-batch, so cohort comparison joins
    surface real signal (e.g. "did rater drift after batch 4?").
  - Each evaluation is rated by exactly 3 raters (matches golden-set
    methodology), enabling agreement/adjudication queries.
  - Timestamps are staggered within each batch so ROW_NUMBER/RANK by
    rater-and-time and gaps-and-islands-style streak logic both work.
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

LOCAL_DIR = os.path.dirname(__file__)

rng = np.random.default_rng(42)

N_RATERS = 12
N_BATCHES = 6
EVALS_PER_BATCH = 150
DOMAINS = ["technical", "factual", "creative", "opinion"]
COMPLEXITIES = ["simple", "moderate", "complex"]

# ---------------------------------------------------------------------------
# 1. Rater profiles (persistent identity + per-batch drift)
# ---------------------------------------------------------------------------
tendencies = rng.choice(["strict", "moderate", "lenient"], size=N_RATERS, p=[0.3, 0.4, 0.3])
base_consistency = rng.uniform(0.65, 0.92, size=N_RATERS)
expertise_domain = rng.choice(DOMAINS, size=N_RATERS)

raters = pd.DataFrame({
    "rater_id": [f"R{str(i+1).zfill(3)}" for i in range(N_RATERS)],
    "tendency": tendencies,
    "base_consistency": base_consistency.round(3),
    "expertise_domain": expertise_domain,
})

# ---------------------------------------------------------------------------
# 2. Evaluations (the items being rated), spread across batches
# ---------------------------------------------------------------------------
eval_rows = []
eval_counter = 1
batch_start_dates = [datetime(2026, 3, 2) + timedelta(weeks=2 * b) for b in range(N_BATCHES)]

for batch_idx in range(N_BATCHES):
    batch_id = f"B{batch_idx + 1}"
    for _ in range(EVALS_PER_BATCH):
        domain = rng.choice(DOMAINS)
        complexity = rng.choice(COMPLEXITIES, p=[0.35, 0.4, 0.25])
        true_quality = int(rng.integers(1, 6))
        eval_rows.append({
            "evaluation_id": f"E{str(eval_counter).zfill(5)}",
            "batch_id": batch_id,
            "domain": domain,
            "complexity": complexity,
            "true_quality": true_quality,
        })
        eval_counter += 1

evaluations = pd.DataFrame(eval_rows)

# ---------------------------------------------------------------------------
# 3. Ratings (long format: 3 raters assigned per evaluation)
# ---------------------------------------------------------------------------
def sample_rating(true_quality, tendency, consistency, is_expert):
    """Simulate a rater's score around the true quality, with noise
    shaped by consistency, a tendency bias, and an expertise bonus."""
    noise_sd = (1.0 - consistency) * 2.2
    bias = {"strict": -0.35, "moderate": 0.0, "lenient": 0.35}[tendency]
    expertise_bonus = 0.4 if is_expert else 0.0
    raw = true_quality + bias + rng.normal(0, noise_sd) + rng.normal(0, max(0.05, 0.3 - expertise_bonus))
    return int(np.clip(round(raw), 1, 5))

rating_rows = []
rating_counter = 1

for batch_idx in range(N_BATCHES):
    batch_id = f"B{batch_idx + 1}"
    batch_start = batch_start_dates[batch_idx]
    batch_evals = evaluations[evaluations.batch_id == batch_id]

    # Slight per-batch consistency drift per rater (some raters fatigue
    # or improve over the project; this is what makes cohort comparison
    # joins interesting instead of flat).
    batch_consistency_adj = rng.normal(0, 0.03, size=N_RATERS)

    for eval_pos, (_, ev) in enumerate(batch_evals.iterrows()):
        assigned = rng.choice(raters.rater_id, size=3, replace=False)
        # Stagger timestamps through the two-week batch window, roughly
        # in evaluation order but with realistic jitter.
        ts_base = batch_start + timedelta(
            hours=eval_pos * 2.2 + float(rng.uniform(-1, 1))
        )
        for r_offset, rater_id in enumerate(assigned):
            r_idx = raters.index[raters.rater_id == rater_id][0]
            tendency = raters.loc[r_idx, "tendency"]
            consistency = float(np.clip(
                raters.loc[r_idx, "base_consistency"] + batch_consistency_adj[r_idx],
                0.4, 0.98
            ))
            is_expert = raters.loc[r_idx, "expertise_domain"] == ev["domain"]
            rating = sample_rating(ev["true_quality"], tendency, consistency, is_expert)
            rating_ts = ts_base + timedelta(minutes=int(rng.integers(0, 90)) * r_offset)

            rating_rows.append({
                "rating_id": f"RT{str(rating_counter).zfill(6)}",
                "evaluation_id": ev["evaluation_id"],
                "rater_id": rater_id,
                "batch_id": batch_id,
                "rating": rating,
                "rated_at": rating_ts,
            })
            rating_counter += 1

ratings = pd.DataFrame(rating_rows)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
raters.to_csv(os.path.join(LOCAL_DIR, "raters.csv"), index=False)
evaluations.to_csv(os.path.join(LOCAL_DIR, "evaluations.csv"), index=False)
ratings.to_csv(os.path.join(LOCAL_DIR, "ratings.csv"), index=False)

print("Raters:", raters.shape)
print("Evaluations:", evaluations.shape)
print("Ratings:", ratings.shape)
print("\nSample ratings:")
print(ratings.head(10).to_string(index=False))
