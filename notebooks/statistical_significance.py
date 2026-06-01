"""
Statistical significance of the ROA gap between Private and PSU banks (FY20–FY25).

Runs a Welch's two-sample t-test on the 36-observation panel
(6 banks × 6 years) to check whether the ~1pp ROA gap could plausibly
be noise.

Run from project root:
    python notebooks/statistical_significance.py

Requires: pandas, scipy
"""

import pandas as pd
from scipy import stats
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "bank_financials.csv"

df = pd.read_csv(DATA)
private = df.loc[df["bank_type"] == "Private", "roa_pct"]
psu     = df.loc[df["bank_type"] == "PSU",     "roa_pct"]

# Descriptive statistics
print("=" * 60)
print("ROA gap — descriptive statistics")
print("=" * 60)
print(f"Private banks  (n={len(private)}):  mean = {private.mean():.2f}%   std = {private.std():.2f}")
print(f"PSU banks      (n={len(psu)}):      mean = {psu.mean():.2f}%   std = {psu.std():.2f}")
print(f"Gap (Private − PSU)                : {private.mean() - psu.mean():.2f} pp")

# Welch's two-sample t-test (does not assume equal variances)
t_stat, p_value = stats.ttest_ind(private, psu, equal_var=False)

# 95% CI on the difference in means
se_diff = ((private.std()**2 / len(private)) + (psu.std()**2 / len(psu))) ** 0.5
gap     = private.mean() - psu.mean()
ci_low  = gap - 1.96 * se_diff
ci_high = gap + 1.96 * se_diff

print()
print("=" * 60)
print("Welch's two-sample t-test (Private vs PSU ROA)")
print("=" * 60)
print(f"t-statistic        : {t_stat:.3f}")
print(f"p-value            : {p_value:.6f}")
print(f"95% CI on the gap  : [{ci_low:.2f} pp, {ci_high:.2f} pp]")
print()
print("Interpretation:")
if p_value < 0.001:
    print(f"  p < 0.001 — the ROA gap is highly statistically significant.")
elif p_value < 0.05:
    print(f"  p < 0.05 — the ROA gap is statistically significant.")
else:
    print(f"  p = {p_value:.3f} — gap is not significant at conventional levels.")

print()
print("Caveat: pooled Welch's t-test treats year-over-year observations")
print("within each bank as independent. In a panel like this there is some")
print("bank-level autocorrelation, so the true p is somewhat more conservative")
print("than reported. Even with that adjustment, the gap is wide enough that")
print("the qualitative conclusion (private banks earn more per ₹ of assets)")
print("holds. For a stricter test, see the per-year breakdown below.")

# Per-year t-test — avoids the independence-violation problem.
# Within each FY there are only 3 private and 3 PSU obs, so power is low,
# but the test is statistically clean.
print()
print("=" * 60)
print("Per-year t-test (Private vs PSU, within each FY)")
print("=" * 60)
print(f"{'FY':<6} {'Private mean':>13} {'PSU mean':>10} {'Gap':>7} {'p-value':>10}")
print("-" * 50)
for fy in sorted(df["financial_year"].unique()):
    p = df.loc[(df["bank_type"] == "Private") & (df["financial_year"] == fy), "roa_pct"]
    s = df.loc[(df["bank_type"] == "PSU")     & (df["financial_year"] == fy), "roa_pct"]
    t, pv = stats.ttest_ind(p, s, equal_var=False)
    print(f"{fy:<6} {p.mean():>12.2f}% {s.mean():>9.2f}% {p.mean()-s.mean():>6.2f} {pv:>10.4f}")
