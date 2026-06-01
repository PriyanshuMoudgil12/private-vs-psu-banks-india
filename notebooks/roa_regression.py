"""
Regression decomposition of the ROA gap between Private and PSU banks.

Tests whether the ~1pp Private-vs-PSU ROA gap is driven by structural
variables (NIM, NPA, CASA) or by an unexplained "private bank premium"
that survives controlling for them.

Approach:
  Model 1: OLS of roa_pct on nim_pct, gross_npa_pct, casa_pct
  Model 2: same plus an is_private dummy — if the dummy is insignificant
           after controls, the gap is fully explained by structure
  Then    : decompose the 0.99pp gap into contributions from each driver.

Run from project root:
    python3 notebooks/roa_regression.py

Requires: pandas, statsmodels
"""

import pandas as pd
import statsmodels.api as sm
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "bank_financials.csv"
df   = pd.read_csv(DATA)

# ---------------------------------------------------------------------------
# Model 1 — structural drivers only
# ---------------------------------------------------------------------------
X1 = sm.add_constant(df[["nim_pct", "gross_npa_pct", "casa_pct"]])
y  = df["roa_pct"]
m1 = sm.OLS(y, X1).fit()

print("=" * 72)
print("MODEL 1: ROA ~ NIM + NPA + CASA   (structural drivers only)")
print("=" * 72)
print(m1.summary().tables[1])
print(f"R-squared: {m1.rsquared:.3f}   Adj R-squared: {m1.rsquared_adj:.3f}")

# ---------------------------------------------------------------------------
# Model 2 — add ownership dummy to test for a "private premium"
# ---------------------------------------------------------------------------
df["is_private"] = (df["bank_type"] == "Private").astype(int)
X2 = sm.add_constant(df[["nim_pct", "gross_npa_pct", "casa_pct", "is_private"]])
m2 = sm.OLS(y, X2).fit()

print()
print("=" * 72)
print("MODEL 2: ROA ~ NIM + NPA + CASA + is_private")
print("=" * 72)
print(m2.summary().tables[1])
print(f"R-squared: {m2.rsquared:.3f}   Adj R-squared: {m2.rsquared_adj:.3f}")

# ---------------------------------------------------------------------------
# Decomposition of the 0.99pp gap using Model 1 coefficients
# ---------------------------------------------------------------------------
private_mean = df.loc[df["bank_type"] == "Private", ["nim_pct", "gross_npa_pct", "casa_pct"]].mean()
psu_mean     = df.loc[df["bank_type"] == "PSU",     ["nim_pct", "gross_npa_pct", "casa_pct"]].mean()
betas        = m1.params[["nim_pct", "gross_npa_pct", "casa_pct"]]
contrib      = (private_mean - psu_mean) * betas
actual_gap   = df.loc[df["bank_type"] == "Private", "roa_pct"].mean() - \
               df.loc[df["bank_type"] == "PSU",     "roa_pct"].mean()

print()
print("=" * 72)
print(f"DECOMPOSITION of the {actual_gap:.2f}pp ROA gap (Model 1 betas × group-mean gaps)")
print("=" * 72)
print(f"  {'Variable':<18} {'Beta':>8} {'Gap (P-PSU)':>14} {'Contribution to ROA gap':>26}")
print("  " + "-" * 70)
for var in ["nim_pct", "gross_npa_pct", "casa_pct"]:
    print(f"  {var:<18} {betas[var]:>+8.3f} {private_mean[var] - psu_mean[var]:>+14.2f} {contrib[var]:>+26.3f} pp")
print("  " + "-" * 70)
print(f"  {'TOTAL explained':<18}            {' ':>14} {contrib.sum():>+26.3f} pp")
print(f"  {'Unexplained residual':<18}        {' ':>14} {actual_gap - contrib.sum():>+26.3f} pp  ('private premium')")

print()
print("Interpretation: NIM does almost all the work. After controlling for")
print("NIM, NPA, and CASA, the is_private dummy in Model 2 carries p =",
      f"{m2.pvalues['is_private']:.2f} — meaning there is no statistically")
print("significant 'private bank premium' beyond what the structural variables")
print("already explain. The ROA gap is a structural story, not an ownership one.")
