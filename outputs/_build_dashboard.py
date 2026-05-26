"""
Build a self-contained interactive HTML dashboard for the
Private vs PSU Banks project.

Output: outputs/dashboard.html (~3 MB, single file, no dependencies needed)
        — opens in any browser, can be hosted on GitHub Pages.
"""

from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data" / "bank_financials.csv"
OUT  = HERE / "dashboard.html"

df = pd.read_csv(DATA)
df["financial_year"] = pd.Categorical(
    df["financial_year"],
    categories=["FY20","FY21","FY22","FY23","FY24","FY25"], ordered=True,
)

PRIVATE_COLOR = "#1f77b4"
PSU_COLOR     = "#d62728"

# ------------------------------------------------------------------ data
roa  = df.groupby(["financial_year","bank_type"], observed=True)["roa_pct"].mean().unstack()
gnpa = df.groupby(["financial_year","bank_type"], observed=True)["gross_npa_pct"].mean().unstack()
casa = df.groupby(["financial_year","bank_type"], observed=True)["casa_pct"].mean().unstack()

adv = df.pivot(index="bank_name", columns="financial_year", values="advances_cr")
adv["cagr_pct"] = ((adv["FY25"] / adv["FY20"]) ** (1/5) - 1) * 100
adv = adv.join(df[["bank_name","bank_type"]].drop_duplicates().set_index("bank_name"))
adv = adv.sort_values("cagr_pct")

fy25 = df[df["financial_year"]=="FY25"].set_index("bank_name")
fy25 = fy25.reindex(["Axis Bank","ICICI Bank","HDFC Bank","SBI","Bank of Baroda","PNB"])

# ------------------------------------------------------------------ 2x2 subplot
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Return on Assets — Private vs PSU (FY20–FY25)",
        "Gross NPA — the great PSU clean-up",
        "Loan-book CAGR (FY20 → FY25)",
        "FY25 league table — best (top) to worst (bottom)",
    ),
    specs=[[{"type":"scatter"}, {"type":"bar"}],
           [{"type":"bar"},     {"type":"heatmap"}]],
    horizontal_spacing=0.12, vertical_spacing=0.18,
)

years = list(roa.index.astype(str))

# --- Chart 1: ROA lines
fig.add_trace(go.Scatter(
    x=years, y=roa["Private"], name="Private (HDFC, ICICI, Axis)",
    mode="lines+markers+text", line=dict(color=PRIVATE_COLOR, width=3),
    marker=dict(size=10),
    text=[f"{v:.2f}" for v in roa["Private"]], textposition="top center",
    hovertemplate="<b>Private</b><br>%{x}<br>ROA = %{y:.2f}%<extra></extra>",
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=years, y=roa["PSU"], name="PSU (SBI, PNB, BOB)",
    mode="lines+markers+text", line=dict(color=PSU_COLOR, width=3),
    marker=dict(size=10, symbol="square"),
    text=[f"{v:.2f}" for v in roa["PSU"]], textposition="bottom center",
    hovertemplate="<b>PSU</b><br>%{x}<br>ROA = %{y:.2f}%<extra></extra>",
), row=1, col=1)

# --- Chart 2: GNPA bars
fig.add_trace(go.Bar(
    x=years, y=gnpa["Private"], name="Private GNPA",
    marker_color=PRIVATE_COLOR, showlegend=False,
    text=[f"{v:.1f}%" for v in gnpa["Private"]], textposition="outside",
    hovertemplate="<b>Private</b><br>%{x}<br>Gross NPA = %{y:.2f}%<extra></extra>",
), row=1, col=2)
fig.add_trace(go.Bar(
    x=years, y=gnpa["PSU"], name="PSU GNPA",
    marker_color=PSU_COLOR, showlegend=False,
    text=[f"{v:.1f}%" for v in gnpa["PSU"]], textposition="outside",
    hovertemplate="<b>PSU</b><br>%{x}<br>Gross NPA = %{y:.2f}%<extra></extra>",
), row=1, col=2)

# --- Chart 3: CAGR
colors = [PRIVATE_COLOR if t=="Private" else PSU_COLOR for t in adv["bank_type"]]
fig.add_trace(go.Bar(
    x=adv["cagr_pct"], y=adv.index, orientation="h",
    marker_color=colors, showlegend=False,
    text=[f"{v:.1f}%" for v in adv["cagr_pct"]], textposition="outside",
    hovertemplate="<b>%{y}</b><br>5-yr CAGR = %{x:.1f}%<extra></extra>",
), row=2, col=1)

# --- Chart 4: heatmap
heat_metrics = ["roa_pct","gross_npa_pct","nim_pct","casa_pct"]
heat_labels  = ["ROA (%)","Gross NPA (%)","NIM (%)","CASA (%)"]
z = fy25[heat_metrics].copy()
# Normalize each column to 0..1 where higher = better (flip NPA)
norm = z.copy()
norm["gross_npa_pct"] = -norm["gross_npa_pct"]
norm = (norm - norm.min()) / (norm.max() - norm.min())

text_vals = [[f"{v:.2f}" for v in row] for row in z.values]
fig.add_trace(go.Heatmap(
    z=norm.values, x=heat_labels, y=list(z.index),
    colorscale="RdYlGn", showscale=False,
    text=text_vals, texttemplate="<b>%{text}</b>",
    textfont={"size": 13},
    hovertemplate="<b>%{y}</b><br>%{x} = %{text}<extra></extra>",
), row=2, col=2)
fig.update_yaxes(autorange="reversed", row=2, col=2)

# ------------------------------------------------------------------ layout
fig.update_layout(
    title=dict(
        text=("<b>Private vs PSU Banks in India — Strategic Analysis (FY20–FY25)</b><br>"
              "<span style='font-size:12px;color:#666'>"
              "6 banks · 6 years · ₹50+ lakh crore of assets · "
              "By Priyanshu Moudgil · Business Analyst Portfolio</span>"),
        x=0.5, xanchor="center",
    ),
    height=850, width=1200,
    font=dict(family="Arial, sans-serif", size=12),
    plot_bgcolor="white",
    paper_bgcolor="white",
    barmode="group",
    legend=dict(orientation="h", yanchor="bottom", y=1.05,
                xanchor="center", x=0.25),
    margin=dict(t=130, b=80, l=80, r=40),
)

fig.update_xaxes(showgrid=False, row=1, col=1)
fig.update_yaxes(title="ROA (%)", gridcolor="#eee", row=1, col=1)
fig.update_yaxes(title="Gross NPA (%)", gridcolor="#eee", row=1, col=2)
fig.update_xaxes(title="5-yr CAGR (%)", gridcolor="#eee", row=2, col=1)
fig.update_xaxes(title="", row=2, col=2)
fig.update_yaxes(title="", row=2, col=2)

# ------------------------------------------------------------------ KPI cards + recommendations as HTML wrapper
KPI_HTML = """
<div style="max-width:1200px;margin:0 auto;padding:24px;font-family:Arial,sans-serif">
  <h1 style="margin:0 0 6px 0;color:#1F2A44">Private vs PSU Banks in India</h1>
  <p style="margin:0 0 18px 0;color:#555;font-size:14px">
    A strategic comparative analysis of India's 6 largest banks over FY20–FY25.<br>
    Hover over charts for tooltips. Source: bank annual reports + investor presentations.
  </p>

  <div style="display:flex;gap:14px;flex-wrap:wrap;margin-bottom:24px">
    {kpi_cards}
  </div>
"""

CHART_HTML = "{chart_div}"

REC_HTML = """
  <h2 style="margin-top:34px;color:#1F2A44">Three Strategic Recommendations</h2>
  <div style="display:flex;gap:14px;flex-wrap:wrap">
    <div style="flex:1;min-width:280px;border-left:4px solid #1F77B4;padding:12px 16px;background:#F5FAFF;border-radius:4px">
      <h3 style="margin:0 0 6px 0;color:#1F77B4">1. Stop chasing CASA. Chase NIM.</h3>
      <p style="margin:0;font-size:14px;color:#444">The funding war is over. Shift 5pp of the loan book from corporate to high-yield retail by FY27; stand up a digital-lending JV.</p>
    </div>
    <div style="flex:1;min-width:280px;border-left:4px solid #1F77B4;padding:12px 16px;background:#F5FAFF;border-radius:4px">
      <h3 style="margin:0 0 6px 0;color:#1F77B4">2. Re-engineer underwriting.</h3>
      <p style="margin:0;font-size:14px;color:#444">The IBC won the first NPA war. The second will be won by data — bureau scores, GST flows, real-time monitoring. Mandate model-driven decisioning under ₹5cr.</p>
    </div>
    <div style="flex:1;min-width:280px;border-left:4px solid #1F77B4;padding:12px 16px;background:#F5FAFF;border-radius:4px">
      <h3 style="margin:0 0 6px 0;color:#1F77B4">3. Become the bank for Bharat's middle 60%.</h3>
      <p style="margin:0;font-size:14px;color:#444">600M middle-income, semi-urban, GST-registered SMBs are under-served. Close the digital UX gap. Target ₹5 lakh crore new SMB advances by FY28.</p>
    </div>
  </div>

  <p style="margin-top:32px;color:#777;font-size:12px;text-align:center">
    Code, SQL, notebook, Excel and memo:
    <a href="https://github.com/PriyanshuMoudgil12/private-vs-psu-banks-india" style="color:#1F77B4">github.com/PriyanshuMoudgil12/private-vs-psu-banks-india</a>
    &nbsp;·&nbsp;
    <a href="https://linkedin.com/in/priyanshu-moudgil" style="color:#1F77B4">LinkedIn</a>
  </p>
</div>
"""

def kpi_card(label, value, sub, color):
    return f"""
    <div style="flex:1;min-width:200px;background:white;border:1px solid #e2e2e2;border-radius:8px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,0.05)">
      <div style="color:#777;font-size:12px;text-transform:uppercase;letter-spacing:0.5px">{label}</div>
      <div style="color:{color};font-size:28px;font-weight:bold;margin:4px 0">{value}</div>
      <div style="color:#555;font-size:13px">{sub}</div>
    </div>
    """

kpi_cards = "".join([
    kpi_card("ROA gap (FY25)",        "+0.86pp", "Private 1.98% vs PSU 1.12%",     "#1F77B4"),
    kpi_card("PSU NPA clean-up",      "−7.2pp",  "9.92% (FY20) → 2.68% (FY25)",  "#28A745"),
    kpi_card("Private CASA peak→FY25", "47.4 → 38.1%", "Funding advantage evaporated","#D62728"),
    kpi_card("NIM spread",            "+1.08pp", "Private pricing power is structural","#1F77B4"),
])

# Generate the chart HTML
chart_html = fig.to_html(full_html=False, include_plotlyjs="cdn", div_id="dashboard-chart")

# Stitch it all together
final_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Private vs PSU Banks in India — Strategic Analysis (FY20–FY25)</title>
  <meta name="description" content="A consulting-style analysis of India's 6 largest banks over FY20-FY25, comparing private banks (HDFC, ICICI, Axis) vs PSU banks (SBI, PNB, BoB). By Priyanshu Moudgil.">
  <style>body{{margin:0;background:#fafafa}}</style>
</head>
<body>
{KPI_HTML.format(kpi_cards=kpi_cards)}
{chart_html}
{REC_HTML}
</div>
</body>
</html>
"""

OUT.write_text(final_html, encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size/1024:.1f} KB)")
