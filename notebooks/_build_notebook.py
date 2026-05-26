"""Programmatically build the Jupyter notebook for the project."""
from pathlib import Path
import json

NB_PATH = Path(__file__).resolve().parent / "private_vs_psu_banks_analysis.ipynb"

def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}

def code(text, outputs=None):
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": outputs or [], "source": text.splitlines(keepends=True)}

cells = [
md("""# Private vs PSU Banks in India — A Strategic Analysis (FY20–FY25)

*Author: Priyanshu Moudgil · BBA · Business Analyst Portfolio*

**Business question**: *You are advising the CEO of a major Indian PSU bank.
The board has asked — why are we losing ground to private banks year after year,
and what 3 things must change in the next 24 months?*

**Banks analyzed (6 banks × 6 years = 36 observations)**

| Private (winners) | PSU (laggards we're advising) |
|---|---|
| HDFC Bank | State Bank of India (SBI) |
| ICICI Bank | Punjab National Bank (PNB) |
| Axis Bank | Bank of Baroda (BOB) |

These 6 banks hold roughly 60–70% of all Indian banking assets.

**Metrics**

- **Total assets, deposits, advances, net profit** (in ₹ crore)
- **Gross NPA %** — loan-book quality (lower = better)
- **ROA %** — return on assets (higher = better)
- **NIM %** — net interest margin / pricing power (higher = better)
- **CASA %** — share of cheap current+savings deposits (higher = better)
"""),

md("## 1. Setup"),
code("""import sqlite3
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

DATA = Path("../data/bank_financials.csv")
DB   = Path("../data/bank_financials.db")
OUT  = Path("../outputs")
OUT.mkdir(exist_ok=True)

sns.set_style("whitegrid")
plt.rcParams.update({"axes.titleweight": "bold", "figure.dpi": 110})

df = pd.read_csv(DATA)
df["financial_year"] = pd.Categorical(
    df["financial_year"],
    categories=["FY20","FY21","FY22","FY23","FY24","FY25"], ordered=True,
)
print("rows:", len(df), "| banks:", df['bank_name'].nunique(), "| years:", df['financial_year'].nunique())
df.head()"""),

md("## 2. Data quality check"),
code("""print("Missing values:")
print(df.isna().sum())
print()
print("Per-bank row counts (should all be 6):")
print(df.groupby('bank_name').size())
print()
print("Summary stats:")
df.describe().round(2)"""),

md("""## 3. Finding #1 — The profitability gap held at ~1 percentage point

ROA (Return on Assets) is the cleanest single profitability metric — net profit divided by total assets.
A 1pp gap may sound small, but on a ₹50 lakh crore balance sheet that's ₹50,000 crore of foregone profit.
"""),
code("""roa = df.groupby(['financial_year','bank_type'], observed=True)['roa_pct'].mean().unstack()
roa['gap_pp'] = roa['Private'] - roa['PSU']
roa.round(2)"""),

md("""**Insight.** Private ROA roughly doubled (0.97% → 1.98%). PSU ROA grew ~7x but from a tiny base (0.16% → 1.12%).
The gap has held at ~1pp across the cycle. PSUs *are* catching up — but slowly, and only because their
NPA clean-up is finally feeding through to the bottom line.
"""),

md("""## 4. Finding #2 — The PSU NPA clean-up is real (and almost over)

This is the most flattering story PSU banks can tell. Six years ago, every ₹100 of PSU loans had
₹10 sitting in non-performing buckets. Today that figure is below ₹3.
"""),
code("""gnpa = df.groupby(['financial_year','bank_type'], observed=True)['gross_npa_pct'].mean().unstack()
gnpa['psu_excess_pp'] = gnpa['PSU'] - gnpa['Private']
gnpa.round(2)"""),

md("""**Insight.** The PSU "excess NPA" gap narrowed from **6.04pp (FY20) → 1.23pp (FY25)** — a ~5pp
improvement. The IBC, write-offs, and credit cycle did most of the work. **But** the easy gains are gone;
from here, PSU asset quality has to be earned through better underwriting, not bankruptcy court.
"""),

md("## 5. Finding #3 — Growth: PSUs aren't shrinking, they're just smaller"),
code("""adv = df.pivot(index='bank_name', columns='financial_year', values='advances_cr')
adv['cagr_pct'] = ((adv['FY25'] / adv['FY20']) ** (1/5) - 1) * 100
adv = adv.join(df[['bank_name','bank_type']].drop_duplicates().set_index('bank_name'))
adv[['FY20','FY25','cagr_pct','bank_type']].sort_values('cagr_pct', ascending=False).round(1)"""),

md("""**Insight.** Loan-book CAGR over FY20–FY25:

- HDFC **22.4%** — but inflated by the FY24 HDFC Ltd merger; underlying organic growth is ~14–15%
- PNB **18.8%**, ICICI **15.8%** — PSUs aren't growth-laggards, they're growing at private-bank pace
- Axis = SBI = **12.7%** — large-bank base effects

The narrative that "PSUs are dying" is wrong. They're growing the loan book — they just earn less on it.
"""),

md("""## 6. Finding #4 — The CASA advantage just evaporated

CASA = Current + Savings Accounts. It's the cheapest funding a bank has — current accounts pay 0% interest,
savings 3–4%. Private banks have always claimed a structural CASA edge. The data says: not anymore.
"""),
code("""casa = df.groupby(['financial_year','bank_type'], observed=True)['casa_pct'].mean().unstack()
casa['private_advantage_pp'] = casa['Private'] - casa['PSU']
casa.round(2)"""),

md("""**Insight.** Private CASA peaked at 47.4% in FY22 and has fallen to **38.1%** in FY25.
PSU CASA also fell, but less violently. For the first time in the dataset, in FY25 **PSUs (39.6%) actually
beat private banks (38.1%) on CASA**. The reason: customers moved cash into 7–8% fixed deposits as
interest rates rose. Private banks lost their structural funding advantage — at least for now.

**This is the surprise of the analysis.** It says PSU CEOs shouldn't waste capital chasing CASA share —
the war is over and the rate cycle decided it.
"""),

md("## 7. Finding #5 — NIM: the persistent ~90bps spread"),
code("""nim_by_bank = df.groupby(['bank_name','bank_type'], observed=True)['nim_pct'].mean().reset_index()
nim_by_bank.sort_values(['bank_type','nim_pct'], ascending=[True, False]).round(2)"""),

code("""nim_by_type = df.groupby('bank_type')['nim_pct'].mean()
print(f"Avg private NIM: {nim_by_type['Private']:.2f}%")
print(f"Avg PSU     NIM: {nim_by_type['PSU']:.2f}%")
print(f"Spread:           {nim_by_type['Private'] - nim_by_type['PSU']:.2f}pp")"""),

md("""**Insight.** Private banks earn ~90bps more on every rupee they lend. This isn't a CASA story
(see Finding #4 — CASA gap is gone). It is a **pricing-power and asset-mix story**: private banks
lend more to retail and unsecured segments where yields are 200–300bps higher than corporate.
NIM is the single best predictor of long-run ROA, and it explains most of the residual profitability gap.
"""),

md("""## 8. FY25 league table — synthesizing everything

Rank every bank on each KPI, then average the ranks for a single bottom-line ordering.
"""),
code("""fy25 = df[df['financial_year']=='FY25'].copy()
fy25['rk_npa']    = fy25['gross_npa_pct'].rank(ascending=True)
fy25['rk_roa']    = fy25['roa_pct'].rank(ascending=False)
fy25['rk_nim']    = fy25['nim_pct'].rank(ascending=False)
fy25['rk_casa']   = fy25['casa_pct'].rank(ascending=False)
fy25['rk_profit'] = fy25['net_profit_cr'].rank(ascending=False)
fy25['avg_rank']  = fy25[['rk_npa','rk_roa','rk_nim','rk_casa','rk_profit']].mean(axis=1)
cols = ['bank_name','bank_type','total_assets_cr','net_profit_cr','roa_pct',
        'gross_npa_pct','nim_pct','casa_pct','avg_rank']
fy25[cols].sort_values('avg_rank').round(2)"""),

md("""**Take-away.** All three private banks lead. SBI ties HDFC on combined ranks — its NPA clean-up
and sheer scale make it the only PSU that competes with the top private banks on every dimension.
PNB still occupies the bottom.
"""),

md("""## 9. Strategic recommendations

Three things the PSU CEO should commit to in the next 24 months.

### 1. **Stop chasing CASA. Chase NIM.**
The data is brutal: private CASA fell faster than PSU CASA. The funding war is over.
The real war is on the **asset** side — pricing, retail mix, and digital underwriting.
*Action*: shift the loan book mix by 5pp from corporate to high-yield retail (personal,
credit card, small-business) over 8 quarters. Stand up a digital-lending JV with a fintech
to underwrite at scale.

### 2. **Defend the NPA gains by re-engineering underwriting, not by lending less.**
The IBC won the first NPA war. The second will be won by data: bureau scores, GST flows,
real-time monitoring. *Action*: cap manual exception approvals at 10% of new sanctions,
mandate model-driven decisioning for every loan under ₹5 crore by Q4 FY27, and tie 30% of
relationship-manager variable pay to vintage NPA performance, not disbursal volume.

### 3. **Become the bank for Bharat's middle 60%.**
Private banks own urban affluent; fintechs own digital natives. The 600M middle-income,
semi-urban, GST-registered SMB segment is largely under-served. PSUs have the branch network
and trust — they just don't have the digital onboarding. *Action*: rebuild mobile + chat
account opening to a 90-second flow, partner with two regional payment-aggregators for
SMB collections, and target ₹5 lakh crore of new SMB advances by FY28.

### What this means for fintechs

A re-rated PSU is the most underpriced distribution channel in India. The bank with 23,000
branches and 50 crore accounts has 90% of the customer file and 10% of the digital UX.
A fintech that productizes underwriting, KYC, or collections **as infrastructure that SBI/PNB/BOB
can rent** captures the upside without funding the balance sheet. The winners of the next
decade in BFSI may not be the bank or the fintech — they'll be the picks-and-shovels providers
sitting between them.
"""),
]

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.10"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

NB_PATH.write_text(json.dumps(nb, indent=1))
print("wrote", NB_PATH)
