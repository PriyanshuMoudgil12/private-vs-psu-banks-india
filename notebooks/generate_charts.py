"""
Generate all 6 publication-quality charts for the Private vs PSU Banks project.

Reads:   ../data/bank_financials.csv
Writes:  ../outputs/01_roa_gap.png
         ../outputs/02_gnpa_clean_up.png
         ../outputs/03_advances_growth_cagr.png
         ../outputs/04_casa_squeeze.png
         ../outputs/05_nim_spread.png
         ../outputs/06_fy25_league_table.png
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data" / "bank_financials.csv"
OUT  = HERE.parent / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA)
df["financial_year"] = pd.Categorical(
    df["financial_year"],
    categories=["FY20", "FY21", "FY22", "FY23", "FY24", "FY25"],
    ordered=True,
)

PRIVATE_COLOR = "#1f77b4"   # blue
PSU_COLOR     = "#d62728"   # red
sns.set_style("whitegrid")
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 130,
})

# -------------------------------------------------------------------- #
# CHART 1 — ROA gap                                                    #
# -------------------------------------------------------------------- #
g = df.groupby(["financial_year", "bank_type"], observed=True)["roa_pct"].mean().unstack()

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(g.index.astype(str), g["Private"], marker="o", lw=2.5,
        color=PRIVATE_COLOR, label="Private (HDFC, ICICI, Axis)")
ax.plot(g.index.astype(str), g["PSU"],     marker="s", lw=2.5,
        color=PSU_COLOR,     label="PSU (SBI, PNB, BOB)")

for i, fy in enumerate(g.index.astype(str)):
    ax.annotate(f"{g['Private'].iloc[i]:.2f}", (i, g['Private'].iloc[i]),
                textcoords="offset points", xytext=(0, 10), ha="center",
                fontsize=9, color=PRIVATE_COLOR)
    ax.annotate(f"{g['PSU'].iloc[i]:.2f}", (i, g['PSU'].iloc[i]),
                textcoords="offset points", xytext=(0, -15), ha="center",
                fontsize=9, color=PSU_COLOR)

ax.set_title("Return on Assets — Private vs PSU banks (FY20–FY25)")
ax.set_ylabel("ROA (%)")
ax.set_xlabel("")
ax.set_ylim(0, 2.3)
ax.legend(loc="upper left")
fig.text(0.5, -0.02,
         "Private banks earn ~2× more per rupee of assets. Gap held ~1pp; PSUs are catching up but slowly.",
         ha="center", fontsize=9, style="italic", color="#555")
fig.tight_layout()
fig.savefig(OUT / "01_roa_gap.png", bbox_inches="tight")
plt.close(fig)

# -------------------------------------------------------------------- #
# CHART 2 — GNPA clean-up                                              #
# -------------------------------------------------------------------- #
g = df.groupby(["financial_year", "bank_type"], observed=True)["gross_npa_pct"].mean().unstack()

fig, ax = plt.subplots(figsize=(9, 5))
x = range(len(g.index))
width = 0.38
ax.bar([i - width/2 for i in x], g["Private"], width,
       label="Private", color=PRIVATE_COLOR)
ax.bar([i + width/2 for i in x], g["PSU"],     width,
       label="PSU",     color=PSU_COLOR)

for i in x:
    ax.text(i - width/2, g["Private"].iloc[i] + 0.15, f"{g['Private'].iloc[i]:.1f}%",
            ha="center", fontsize=9)
    ax.text(i + width/2, g["PSU"].iloc[i] + 0.15, f"{g['PSU'].iloc[i]:.1f}%",
            ha="center", fontsize=9)

ax.set_xticks(list(x))
ax.set_xticklabels(g.index.astype(str))
ax.set_title("Gross NPA — the great PSU clean-up (FY20–FY25)")
ax.set_ylabel("Gross NPA (%)")
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax.legend(loc="upper right")
fig.text(0.5, -0.02,
         "PSU gross NPAs fell from 9.9% → 2.7%. The 6pp gap with private peers narrowed to just 1.2pp.",
         ha="center", fontsize=9, style="italic", color="#555")
fig.tight_layout()
fig.savefig(OUT / "02_gnpa_clean_up.png", bbox_inches="tight")
plt.close(fig)

# -------------------------------------------------------------------- #
# CHART 3 — Advances growth CAGR FY20→FY25                             #
# -------------------------------------------------------------------- #
adv = df.pivot(index="bank_name", columns="financial_year", values="advances_cr")
adv["cagr_pct"] = ((adv["FY25"] / adv["FY20"]) ** (1/5) - 1) * 100
adv = adv.merge(df[["bank_name", "bank_type"]].drop_duplicates(), on="bank_name")
adv = adv.sort_values("cagr_pct", ascending=True)

fig, ax = plt.subplots(figsize=(9, 5))
colors = [PRIVATE_COLOR if t == "Private" else PSU_COLOR for t in adv["bank_type"]]
bars = ax.barh(adv["bank_name"], adv["cagr_pct"], color=colors)
for bar, v in zip(bars, adv["cagr_pct"]):
    ax.text(v + 0.3, bar.get_y() + bar.get_height()/2, f"{v:.1f}%",
            va="center", fontsize=10)

ax.set_title("Loan-book CAGR — FY20 → FY25")
ax.set_xlabel("Advances 5-year CAGR (%)")
ax.set_xlim(0, max(adv["cagr_pct"]) * 1.15)

# legend
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=PRIVATE_COLOR, label="Private"),
                   Patch(color=PSU_COLOR,     label="PSU")], loc="lower right")
fig.text(0.5, -0.02,
         "HDFC's 22% CAGR is inflated by the FY24 HDFC Ltd merger; ex-merger growth is closer to 14–15%.",
         ha="center", fontsize=9, style="italic", color="#555")
fig.tight_layout()
fig.savefig(OUT / "03_advances_growth_cagr.png", bbox_inches="tight")
plt.close(fig)

# -------------------------------------------------------------------- #
# CHART 4 — CASA squeeze                                               #
# -------------------------------------------------------------------- #
g = df.groupby(["financial_year", "bank_type"], observed=True)["casa_pct"].mean().unstack()

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(g.index.astype(str), g["Private"], marker="o", lw=2.5,
        color=PRIVATE_COLOR, label="Private")
ax.plot(g.index.astype(str), g["PSU"],     marker="s", lw=2.5,
        color=PSU_COLOR,     label="PSU")
ax.fill_between(g.index.astype(str), g["Private"], g["PSU"],
                where=(g["Private"] >= g["PSU"]),
                interpolate=True, alpha=0.10, color=PRIVATE_COLOR)

for i, fy in enumerate(g.index.astype(str)):
    ax.annotate(f"{g['Private'].iloc[i]:.1f}", (i, g['Private'].iloc[i]),
                textcoords="offset points", xytext=(0, 10), ha="center",
                fontsize=9, color=PRIVATE_COLOR)
    ax.annotate(f"{g['PSU'].iloc[i]:.1f}", (i, g['PSU'].iloc[i]),
                textcoords="offset points", xytext=(0, -15), ha="center",
                fontsize=9, color=PSU_COLOR)

ax.set_title("CASA ratio — the funding advantage that just evaporated")
ax.set_ylabel("CASA (%) of deposits")
ax.set_xlabel("")
ax.set_ylim(34, 50)
ax.legend(loc="lower left")
fig.text(0.5, -0.02,
         "Private CASA fell from 47% (FY22 peak) to 38% (FY25). For the first time in FY25, PSUs edge ahead.",
         ha="center", fontsize=9, style="italic", color="#555")
fig.tight_layout()
fig.savefig(OUT / "04_casa_squeeze.png", bbox_inches="tight")
plt.close(fig)

# -------------------------------------------------------------------- #
# CHART 5 — NIM spread, bank-by-bank average                           #
# -------------------------------------------------------------------- #
nim = df.groupby(["bank_name", "bank_type"], observed=True)["nim_pct"].mean().reset_index()
nim = nim.sort_values("nim_pct", ascending=True)

fig, ax = plt.subplots(figsize=(9, 5))
colors = [PRIVATE_COLOR if t == "Private" else PSU_COLOR for t in nim["bank_type"]]
bars = ax.barh(nim["bank_name"], nim["nim_pct"], color=colors)
for bar, v in zip(bars, nim["nim_pct"]):
    ax.text(v + 0.05, bar.get_y() + bar.get_height()/2, f"{v:.2f}%",
            va="center", fontsize=10)

ax.set_title("Net Interest Margin — 6-year average (FY20–FY25)")
ax.set_xlabel("Avg NIM (%)")
ax.set_xlim(0, max(nim["nim_pct"]) * 1.15)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=PRIVATE_COLOR, label="Private"),
                   Patch(color=PSU_COLOR,     label="PSU")], loc="lower right")
fig.text(0.5, -0.02,
         "Private banks earn ~90bps more on every rupee they lend — structural pricing power, not luck.",
         ha="center", fontsize=9, style="italic", color="#555")
fig.tight_layout()
fig.savefig(OUT / "05_nim_spread.png", bbox_inches="tight")
plt.close(fig)

# -------------------------------------------------------------------- #
# CHART 6 — FY25 league table (heatmap)                                #
# -------------------------------------------------------------------- #
fy25 = df[df["financial_year"] == "FY25"].copy()
fy25 = fy25.set_index("bank_name")[["roa_pct", "gross_npa_pct", "nim_pct",
                                    "casa_pct"]]
# Lower is better for NPAs — invert for heatmap scoring
score = fy25.copy()
score["gross_npa_pct"] = -score["gross_npa_pct"]
# normalize each column 0–1 (higher = better)
norm = (score - score.min()) / (score.max() - score.min())

fig, ax = plt.subplots(figsize=(9, 5))
sns.heatmap(
    norm.reindex(["Axis Bank", "ICICI Bank", "HDFC Bank",
                  "SBI", "Bank of Baroda", "PNB"]),
    annot=fy25.reindex(["Axis Bank", "ICICI Bank", "HDFC Bank",
                        "SBI", "Bank of Baroda", "PNB"]).round(2).astype(str).values,
    fmt="", cmap="RdYlGn", cbar=False, linewidths=1, linecolor="white",
    annot_kws={"fontsize": 11, "fontweight": "bold"},
    xticklabels=["ROA (%)", "Gross NPA (%)", "NIM (%)", "CASA (%)"],
    ax=ax,
)
ax.set_title("FY25 league table — banks ranked best to worst (top to bottom)")
ax.set_ylabel("")
fig.text(0.5, -0.02,
         "All three private banks lead. SBI matches HDFC on ranks (cleaner book + scale). PNB still last.",
         ha="center", fontsize=9, style="italic", color="#555")
fig.tight_layout()
fig.savefig(OUT / "06_fy25_league_table.png", bbox_inches="tight")
plt.close(fig)

print("All 6 charts written to:", OUT)
for p in sorted(OUT.glob("*.png")):
    print(" -", p.name)
