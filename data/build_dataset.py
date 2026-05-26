"""
Build the master bank-financials dataset for the Private vs PSU Banks project.

DATA SOURCES (per bank, in priority order):
  1. Each bank's published Annual Report (FY20-FY25)
  2. Each bank's Q4 Investor Presentation (FY24, FY25)
  3. Equitymaster Annual Report Analysis (https://www.equitymaster.com/research-it/annual-results-analysis/)
  4. Bank-specific press releases and analyst notes

VERIFICATION STATUS:
  - FY24 + FY25 values cross-checked against May 2026 web search results
    against official press releases (HDFC, SBI, PNB, ICICI, BoB, Axis).
  - FY20-FY23 values from each bank's historical annual reports.
  - Numbers are approximate to 0.01 precision where reported; some
    secondary metrics (CASA, NIM) may differ by 10-30 bps depending
    on whether bank uses standalone vs consolidated figures.

UNITS:
  - All absolute values in ₹ crore (1 crore = 10 million = ₹1,00,00,000)
  - All ratios (gross_npa_pct, roa_pct, nim_pct, casa_pct) in percentage
"""

import csv
from pathlib import Path

# Each row = one bank-year observation.
DATA = [
    # ========== HDFC BANK (Private) ==========
    # Note: HDFC Ltd merged INTO HDFC Bank effective July 2023, causing
    # the large jump in total assets / advances between FY23 and FY24.
    {"bank_name": "HDFC Bank", "bank_type": "Private", "financial_year": "FY20",
     "total_assets_cr": 1530511, "deposits_cr": 1147502, "advances_cr": 993703,
     "net_profit_cr": 26257, "gross_npa_pct": 1.26, "roa_pct": 1.89,
     "nim_pct": 4.20, "casa_pct": 42.2},
    {"bank_name": "HDFC Bank", "bank_type": "Private", "financial_year": "FY21",
     "total_assets_cr": 1746870, "deposits_cr": 1335060, "advances_cr": 1132837,
     "net_profit_cr": 31116, "gross_npa_pct": 1.32, "roa_pct": 1.97,
     "nim_pct": 4.10, "casa_pct": 46.1},
    {"bank_name": "HDFC Bank", "bank_type": "Private", "financial_year": "FY22",
     "total_assets_cr": 2068535, "deposits_cr": 1559217, "advances_cr": 1368821,
     "net_profit_cr": 36961, "gross_npa_pct": 1.17, "roa_pct": 2.03,
     "nim_pct": 4.00, "casa_pct": 48.2},
    {"bank_name": "HDFC Bank", "bank_type": "Private", "financial_year": "FY23",
     "total_assets_cr": 2466081, "deposits_cr": 1883394, "advances_cr": 1600586,
     "net_profit_cr": 44109, "gross_npa_pct": 1.12, "roa_pct": 2.07,
     "nim_pct": 4.10, "casa_pct": 44.4},
    {"bank_name": "HDFC Bank", "bank_type": "Private", "financial_year": "FY24",
     "total_assets_cr": 4030190, "deposits_cr": 2376888, "advances_cr": 2571920,
     "net_profit_cr": 64062, "gross_npa_pct": 1.24, "roa_pct": 1.59,
     "nim_pct": 3.60, "casa_pct": 38.2},
    {"bank_name": "HDFC Bank", "bank_type": "Private", "financial_year": "FY25",
     "total_assets_cr": 4392420, "deposits_cr": 2710900, "advances_cr": 2724940,
     "net_profit_cr": 70792, "gross_npa_pct": 1.33, "roa_pct": 1.61,
     "nim_pct": 3.90, "casa_pct": 34.9},

    # ========== ICICI BANK (Private) ==========
    {"bank_name": "ICICI Bank", "bank_type": "Private", "financial_year": "FY20",
     "total_assets_cr": 1098365, "deposits_cr": 770968, "advances_cr": 645289,
     "net_profit_cr": 7931, "gross_npa_pct": 5.53, "roa_pct": 0.81,
     "nim_pct": 3.73, "casa_pct": 45.1},
    {"bank_name": "ICICI Bank", "bank_type": "Private", "financial_year": "FY21",
     "total_assets_cr": 1230433, "deposits_cr": 932522, "advances_cr": 733729,
     "net_profit_cr": 16193, "gross_npa_pct": 4.96, "roa_pct": 1.42,
     "nim_pct": 3.69, "casa_pct": 46.3},
    {"bank_name": "ICICI Bank", "bank_type": "Private", "financial_year": "FY22",
     "total_assets_cr": 1411297, "deposits_cr": 1064571, "advances_cr": 859020,
     "net_profit_cr": 23339, "gross_npa_pct": 3.60, "roa_pct": 1.84,
     "nim_pct": 3.96, "casa_pct": 48.9},
    {"bank_name": "ICICI Bank", "bank_type": "Private", "financial_year": "FY23",
     "total_assets_cr": 1584207, "deposits_cr": 1180840, "advances_cr": 1019638,
     "net_profit_cr": 31896, "gross_npa_pct": 2.81, "roa_pct": 2.13,
     "nim_pct": 4.48, "casa_pct": 45.8},
    {"bank_name": "ICICI Bank", "bank_type": "Private", "financial_year": "FY24",
     "total_assets_cr": 1729021, "deposits_cr": 1412825, "advances_cr": 1184406,
     "net_profit_cr": 40888, "gross_npa_pct": 2.30, "roa_pct": 2.37,
     "nim_pct": 4.10, "casa_pct": 42.0},
    {"bank_name": "ICICI Bank", "bank_type": "Private", "financial_year": "FY25",
     "total_assets_cr": 1918233, "deposits_cr": 1610348, "advances_cr": 1341766,
     "net_profit_cr": 47227, "gross_npa_pct": 1.70, "roa_pct": 2.46,
     "nim_pct": 4.40, "casa_pct": 38.4},

    # ========== AXIS BANK (Private) ==========
    {"bank_name": "Axis Bank", "bank_type": "Private", "financial_year": "FY20",
     "total_assets_cr": 915166, "deposits_cr": 640105, "advances_cr": 571424,
     "net_profit_cr": 1627, "gross_npa_pct": 4.86, "roa_pct": 0.20,
     "nim_pct": 3.51, "casa_pct": 41.2},
    {"bank_name": "Axis Bank", "bank_type": "Private", "financial_year": "FY21",
     "total_assets_cr": 996118, "deposits_cr": 707306, "advances_cr": 623720,
     "net_profit_cr": 6588, "gross_npa_pct": 3.70, "roa_pct": 0.70,
     "nim_pct": 3.53, "casa_pct": 45.0},
    {"bank_name": "Axis Bank", "bank_type": "Private", "financial_year": "FY22",
     "total_assets_cr": 1175178, "deposits_cr": 821721, "advances_cr": 707696,
     "net_profit_cr": 13025, "gross_npa_pct": 2.82, "roa_pct": 1.21,
     "nim_pct": 3.47, "casa_pct": 45.0},
    {"bank_name": "Axis Bank", "bank_type": "Private", "financial_year": "FY23",
     "total_assets_cr": 1317326, "deposits_cr": 946945, "advances_cr": 845303,
     "net_profit_cr": 9580, "gross_npa_pct": 2.02, "roa_pct": 0.81,
     "nim_pct": 4.02, "casa_pct": 47.0},
    {"bank_name": "Axis Bank", "bank_type": "Private", "financial_year": "FY24",
     "total_assets_cr": 1477209, "deposits_cr": 1068641, "advances_cr": 965068,
     "net_profit_cr": 26386, "gross_npa_pct": 1.50, "roa_pct": 1.83,
     "nim_pct": 3.90, "casa_pct": 42.0},
    {"bank_name": "Axis Bank", "bank_type": "Private", "financial_year": "FY25",
     "total_assets_cr": 1610327, "deposits_cr": 1172952, "advances_cr": 1040810,
     "net_profit_cr": 28055, "gross_npa_pct": 1.30, "roa_pct": 1.88,
     "nim_pct": 3.98, "casa_pct": 41.0},

    # ========== STATE BANK OF INDIA (PSU) ==========
    {"bank_name": "SBI", "bank_type": "PSU", "financial_year": "FY20",
     "total_assets_cr": 3951393, "deposits_cr": 3241621, "advances_cr": 2325290,
     "net_profit_cr": 14488, "gross_npa_pct": 6.15, "roa_pct": 0.38,
     "nim_pct": 3.19, "casa_pct": 45.2},
    {"bank_name": "SBI", "bank_type": "PSU", "financial_year": "FY21",
     "total_assets_cr": 4534430, "deposits_cr": 3681277, "advances_cr": 2449498,
     "net_profit_cr": 20410, "gross_npa_pct": 4.98, "roa_pct": 0.48,
     "nim_pct": 3.11, "casa_pct": 46.1},
    {"bank_name": "SBI", "bank_type": "PSU", "financial_year": "FY22",
     "total_assets_cr": 4987597, "deposits_cr": 4051534, "advances_cr": 2733966,
     "net_profit_cr": 31676, "gross_npa_pct": 3.97, "roa_pct": 0.67,
     "nim_pct": 3.12, "casa_pct": 45.3},
    {"bank_name": "SBI", "bank_type": "PSU", "financial_year": "FY23",
     "total_assets_cr": 5516979, "deposits_cr": 4423778, "advances_cr": 3199269,
     "net_profit_cr": 50232, "gross_npa_pct": 2.78, "roa_pct": 0.96,
     "nim_pct": 3.37, "casa_pct": 43.8},
    {"bank_name": "SBI", "bank_type": "PSU", "financial_year": "FY24",
     "total_assets_cr": 6165707, "deposits_cr": 4916077, "advances_cr": 3767535,
     "net_profit_cr": 61077, "gross_npa_pct": 2.24, "roa_pct": 1.04,
     "nim_pct": 3.28, "casa_pct": 41.1},
    {"bank_name": "SBI", "bank_type": "PSU", "financial_year": "FY25",
     "total_assets_cr": 6606290, "deposits_cr": 5382190, "advances_cr": 4221000,
     "net_profit_cr": 70901, "gross_npa_pct": 1.82, "roa_pct": 1.10,
     "nim_pct": 3.09, "casa_pct": 39.97},

    # ========== PUNJAB NATIONAL BANK (PSU) ==========
    # Note: PNB amalgamated with United Bank and Oriental Bank of Commerce on
    # April 1, 2020. FY21 onwards reflects the merged entity, hence the jump.
    {"bank_name": "PNB", "bank_type": "PSU", "financial_year": "FY20",
     "total_assets_cr": 830657, "deposits_cr": 703846, "advances_cr": 471827,
     "net_profit_cr": 336, "gross_npa_pct": 14.21, "roa_pct": 0.04,
     "nim_pct": 2.59, "casa_pct": 43.0},
    {"bank_name": "PNB", "bank_type": "PSU", "financial_year": "FY21",
     "total_assets_cr": 1262283, "deposits_cr": 1106332, "advances_cr": 674230,
     "net_profit_cr": 2022, "gross_npa_pct": 14.12, "roa_pct": 0.15,
     "nim_pct": 3.07, "casa_pct": 45.5},
    {"bank_name": "PNB", "bank_type": "PSU", "financial_year": "FY22",
     "total_assets_cr": 1310643, "deposits_cr": 1146219, "advances_cr": 728185,
     "net_profit_cr": 3457, "gross_npa_pct": 11.78, "roa_pct": 0.26,
     "nim_pct": 2.71, "casa_pct": 47.4},
    {"bank_name": "PNB", "bank_type": "PSU", "financial_year": "FY23",
     "total_assets_cr": 1406018, "deposits_cr": 1280815, "advances_cr": 830153,
     "net_profit_cr": 2507, "gross_npa_pct": 8.74, "roa_pct": 0.18,
     "nim_pct": 3.06, "casa_pct": 43.0},
    {"bank_name": "PNB", "bank_type": "PSU", "financial_year": "FY24",
     "total_assets_cr": 1492894, "deposits_cr": 1371800, "advances_cr": 934432,
     "net_profit_cr": 8245, "gross_npa_pct": 5.73, "roa_pct": 0.55,
     "nim_pct": 3.09, "casa_pct": 41.1},
    {"bank_name": "PNB", "bank_type": "PSU", "financial_year": "FY25",
     "total_assets_cr": 1650000, "deposits_cr": 1568000, "advances_cr": 1116000,
     "net_profit_cr": 16630, "gross_npa_pct": 3.95, "roa_pct": 1.00,
     "nim_pct": 2.93, "casa_pct": 38.8},

    # ========== BANK OF BARODA (PSU) ==========
    # Note: BoB amalgamated with Vijaya Bank and Dena Bank on April 1, 2019.
    # FY20 onwards reflects the merged entity.
    {"bank_name": "Bank of Baroda", "bank_type": "PSU", "financial_year": "FY20",
     "total_assets_cr": 1157915, "deposits_cr": 945985, "advances_cr": 690121,
     "net_profit_cr": 546, "gross_npa_pct": 9.40, "roa_pct": 0.06,
     "nim_pct": 2.61, "casa_pct": 38.8},
    {"bank_name": "Bank of Baroda", "bank_type": "PSU", "financial_year": "FY21",
     "total_assets_cr": 1155365, "deposits_cr": 966997, "advances_cr": 706300,
     "net_profit_cr": 828, "gross_npa_pct": 8.87, "roa_pct": 0.07,
     "nim_pct": 2.81, "casa_pct": 41.9},
    {"bank_name": "Bank of Baroda", "bank_type": "PSU", "financial_year": "FY22",
     "total_assets_cr": 1277998, "deposits_cr": 1045939, "advances_cr": 777008,
     "net_profit_cr": 7272, "gross_npa_pct": 6.61, "roa_pct": 0.60,
     "nim_pct": 3.03, "casa_pct": 42.1},
    {"bank_name": "Bank of Baroda", "bank_type": "PSU", "financial_year": "FY23",
     "total_assets_cr": 1473828, "deposits_cr": 1203688, "advances_cr": 940998,
     "net_profit_cr": 14110, "gross_npa_pct": 3.79, "roa_pct": 1.03,
     "nim_pct": 3.31, "casa_pct": 40.3},
    {"bank_name": "Bank of Baroda", "bank_type": "PSU", "financial_year": "FY24",
     "total_assets_cr": 1565835, "deposits_cr": 1326958, "advances_cr": 1090608,
     "net_profit_cr": 17789, "gross_npa_pct": 2.92, "roa_pct": 1.17,
     "nim_pct": 3.27, "casa_pct": 39.8},
    {"bank_name": "Bank of Baroda", "bank_type": "PSU", "financial_year": "FY25",
     "total_assets_cr": 1710000, "deposits_cr": 1472000, "advances_cr": 1230000,
     "net_profit_cr": 20716, "gross_npa_pct": 2.26, "roa_pct": 1.26,
     "nim_pct": 3.02, "casa_pct": 39.95},
]


def build_csv():
    out_path = Path(__file__).parent / "bank_financials.csv"
    fieldnames = [
        "bank_name", "bank_type", "financial_year",
        "total_assets_cr", "deposits_cr", "advances_cr", "net_profit_cr",
        "gross_npa_pct", "roa_pct", "nim_pct", "casa_pct",
    ]
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(DATA)
    print(f"wrote {out_path}  ({len(DATA)} rows)")


if __name__ == "__main__":
    build_csv()
