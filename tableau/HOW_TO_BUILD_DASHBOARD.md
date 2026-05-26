# 🎯 How to Build the Tableau Dashboard — Beginner Edition

> Total time: about **45 minutes** the first time. You're doing this for the first time, so go slowly. **There is no rush.**
>
> If you get stuck at any step: screenshot what's on your screen, send it to Claude, and ask "what do I click next?"

---

## What we're going to build

A single page with **4 charts** that tell the story of private vs PSU banks. When recruiters click your Tableau Public link, they'll see something like this:

```
┌────────────────────────────────────────────────────────────┐
│  Private vs PSU Banks in India — FY20–FY25                 │
├──────────────────────────┬─────────────────────────────────┤
│                          │                                 │
│  Chart 1: ROA over time  │  Chart 2: Gross NPA over time   │
│  (line chart)            │  (bar chart)                    │
│                          │                                 │
├──────────────────────────┼─────────────────────────────────┤
│                          │                                 │
│  Chart 3: Loan growth    │  Chart 4: FY25 league table     │
│  (horizontal bars)       │  (colored grid)                 │
│                          │                                 │
└──────────────────────────┴─────────────────────────────────┘
```

---

## 🟢 Part 0 — Get Tableau (5 minutes)

You only do this once.

1. Open your web browser.
2. Go to **<https://public.tableau.com/en-us/s/download>**
3. Click the big blue **Download** button. It'll ask for your email — use yours.
4. The download is a file called `TableauPublicDesktop.dmg` (Mac) or `.exe` (Windows). Open it and follow the install prompts. Click Next, Next, Done.
5. Open Tableau Public (it's now in your Applications folder on Mac, or Start Menu on Windows).
6. First time it opens, it'll ask you to **sign in to Tableau Public**. You already have an account at `public.tableau.com/app/profile/priyanshu.moudgil` — sign in with that.

You're now staring at Tableau Public's home screen. There's a panel on the left that says **"Connect"**. Good.

---

## 🟢 Part 1 — Open the data (3 minutes)

We're going to load the spreadsheet of bank numbers.

1. In the left panel under **"Connect → To a File"**, click **"Text file"**.
2. A file-picker window opens. Navigate to your project folder:
   ```
   Documents → private-vs-psu-banks-india → tableau → banks_wide.csv
   ```
3. Double-click **`banks_wide.csv`**.
4. Tableau opens a new screen showing the data as a table — bank names, years, numbers. **This is correct.**
5. At the bottom of the screen, you'll see a tab called **"Sheet 1"**. Click it.

> *Note: an older version of this guide asked you to right-click `Fy Year Num` and choose "Convert to Discrete". That option was removed from the Data Source tab in newer Tableau versions. **You can safely skip it** — we use the `Financial Year` column (FY20, FY21…) in every chart, and Tableau treats it correctly as a label out of the box.*

You're now on a blank worksheet. Time to build the first chart.

---

## 🟢 Part 2 — Build Chart 1: ROA over time (8 minutes)

**Goal:** A line chart showing how Private and PSU banks' return-on-assets has changed from FY20 to FY25.

**Left side of the screen** has two boxes:
- **Dimensions** (top): contains things like `Bank Name`, `Bank Type`, `Financial Year`. These are *labels*.
- **Measures** (bottom): contains things like `Roa Pct`, `Casa Pct`. These are *numbers*.

The middle and right of the screen has shelves labeled **Columns**, **Rows**, **Filters**, **Marks**, etc.

### Step-by-step

1. **Rename the sheet:** double-click "Sheet 1" at the bottom. Type **"ROA Trend"**. Press Enter.

2. **Drag `Financial Year`** from the left panel onto the **Columns** shelf at the top. *(Drag = click and hold, then drop.)*
   - You should now see FY20, FY21, FY22, FY23, FY24, FY25 listed across the top.

3. **Drag `Roa Pct`** from the left panel onto the **Rows** shelf.
   - You'll see a single bar chart appear. That's fine, we'll change it.

4. **Click the green pill** that just appeared on the Rows shelf (it says `SUM(Roa Pct)`). A menu appears. Hover over **"Measure (Sum)"**, and from the submenu choose **"Average"**. The pill should now say `AVG(Roa Pct)`.

5. **Drag `Bank Type`** from the left panel onto the **Color** card (it's in the "Marks" section in the middle).
   - The bar splits into two — one blue, one orange.

6. **Change Mark Type:** in the "Marks" panel in the middle, there's a dropdown that currently says "Automatic" or "Bar". Click it. Choose **"Line"**.
   - You should now see two lines — one for Private, one for PSU.

7. **Make the colors right:** Click the **Color** card → click **"Edit Colors…"**. A window opens.
   - Click **"Private"** in the list, then click the colored square next to it. Type or paste hex `#1F77B4`. Click OK.
   - Click **"PSU"** in the list, then click the colored square. Type `#D62728`. Click OK.
   - Click OK to close the window. Lines are now blue and red.

8. **Show the numbers on the chart:** Right-click anywhere on the chart area → **"Show Mark Labels"**. The 0.97, 1.36, 1.69, etc. values now appear next to each dot.

9. **Add a title:** Double-click the title bar at the top of the chart (currently says "Sheet" or your sheet name). Type:
   `Return on Assets — Private vs PSU banks (FY20–FY25)`
   Click OK.

### How do you know it's right?

You should see:
- A **blue line** going up from 0.97 (FY20) to 1.98 (FY25)
- A **red line** going up from 0.16 (FY20) to 1.12 (FY25)
- Numbers labeled on every dot

If yes — 🎉 you just built your first Tableau chart. Take a deep breath.

If not — screenshot it and ask Claude what's wrong.

---

## 🟢 Part 3 — Build Chart 2: NPA Clean-up (5 minutes)

**Goal:** Side-by-side blue/red bars showing the PSU NPA clean-up story.

1. At the bottom of the screen, click the **little tab with a "+" icon** next to "ROA Trend". A new blank sheet opens. Rename it **"NPA Clean-up"** (double-click the tab name).

2. **Drag `Financial Year`** to the **Columns** shelf.

3. **Drag `Bank Type`** to the **Columns** shelf (drop it to the RIGHT of `Financial Year`).
   - Now your columns shelf has TWO pills: `Financial Year` then `Bank Type`.

4. **Drag `Gross Npa Pct`** to the **Rows** shelf.

5. Click the green pill `SUM(Gross Npa Pct)` → **Measure (Sum) → Average**. Now it says `AVG(Gross Npa Pct)`.

6. **Drag `Bank Type`** ALSO to the **Color** card (yes, it goes in two places — Columns AND Color). The bars become blue and red side-by-side for each year.

7. **Show the numbers:** right-click chart → **"Show Mark Labels"**.

8. **Format the labels as %:** click on a label → it should already show as e.g. `9.917`. Right-click the label → **"Format…"**. A panel opens on the right. Find **"Pane → Default → Numbers"** → choose **"Percentage"** → set decimal places to 1.
   - Wait — the source data is already a percent number (9.92 not 0.0992), so picking "Percentage" might multiply by 100. **Test it:** if it shows 992% you applied percentage wrong; go back to **"Number (Custom)"** → format `0.0"%"` and it will show 9.9%.

9. **Title:** double-click the chart title → type:
   `Gross NPA — the great PSU clean-up (FY20–FY25)`

### How do you know it's right?

You should see:
- 6 pairs of bars (one pair per year)
- Each pair has a tall **red** bar (PSU) and a shorter **blue** bar (Private)
- The red bars get shorter every year, dropping from ~9.9% (FY20) to ~2.7% (FY25)

---

## 🟢 Part 4 — Build Chart 3: Loan-book CAGR (8 minutes — has one tricky step)

**Goal:** Horizontal bars ranking the 6 banks by their 5-year loan growth.

We need to make a **calculated field** first — this is just Tableau's word for "a number formula".

### Make the calculated field

1. On the left panel, look for the **little dropdown arrow** at the top right of the dimensions/measures list (it might be a tiny down-arrow ▾, or three dots ⋯). Click it → **"Create Calculated Field…"**

2. A formula box opens. In the **Name** box at the top, type:
   ```
   Advances CAGR
   ```

3. In the big formula box below, type or paste this exactly:
   ```
   (POWER(
     { FIXED [Bank Name] : MAX(IF [Financial Year] = "FY25" THEN [Advances Cr] END) }
     /
     { FIXED [Bank Name] : MAX(IF [Financial Year] = "FY20" THEN [Advances Cr] END) }
   , 1/5) - 1) * 100
   ```

4. Below the formula box there should be a message saying **"The calculation is valid."** in green. If you see a red error, double-check spacing and brackets.

5. Click **OK**. You'll now see `Advances CAGR` listed under Measures on the left.

### Now build the chart

1. **New sheet:** click the "+" tab at the bottom → rename it **"Loan-book CAGR"**.

2. **Drag `Advances CAGR`** to the **Columns** shelf.

3. **Drag `Bank Name`** to the **Rows** shelf.
   - You'll see 6 horizontal bars, one per bank.

4. **Drag `Bank Type`** to **Color**. Bars are now blue (private) and red (PSU).

5. **Sort the bars:** hover over the `Bank Name` pill on Rows → a small dropdown arrow appears next to it → click it → **"Sort"**. A window opens.
   - Sort By: **Field**
   - Order: **Descending**
   - Field: **Advances CAGR**
   - Aggregation: **Minimum** (any aggregation works since the CAGR is the same per bank)
   - Click OK.

6. **Labels:** right-click the chart → **"Show Mark Labels"**. Each bar now shows its CAGR value.

7. **Title:** double-click the chart title → type:
   `Loan-book CAGR — FY20 → FY25`

### How do you know it's right?

Expected order from top (highest) to bottom (lowest):
- HDFC Bank: ~22.4%
- PNB: ~18.8%
- ICICI Bank: ~15.8%
- Axis Bank: ~12.7%
- SBI: ~12.7%
- Bank of Baroda: ~12.3%

---

## 🟢 Part 5 — Build Chart 4: FY25 League Table (10 minutes)

**Goal:** A heatmap showing each bank's FY25 performance on 4 key metrics.

This one has the most steps. Go slow.

### Filter to FY25 only

1. **New sheet:** click "+" tab → rename to **"FY25 League Table"**.

2. **Drag `Financial Year`** to the **Filters** shelf (NOT Columns/Rows).
3. A pop-up appears with a checklist of years. **Uncheck everything except FY25.** Click OK.

### Build the heatmap

4. **Drag `Bank Name`** to **Rows**.

5. We want all 4 metrics shown next to each other as columns. Tableau has a magic field for this:
   - In the Dimensions list, find **`Measure Names`** (it might be down at the bottom, in a separate small section). Drag it to **Columns**.
   - Tableau will show ALL measures, which is too many. We'll filter next.

6. **A "Measure Values" card appears** in the middle of your screen (below the Marks card). It lists every numeric field. Right-click any field in there → "Remove" — repeat until only these 4 remain:
   - `AVG(Roa Pct)`
   - `AVG(Gross Npa Pct)`
   - `AVG(Nim Pct)`
   - `AVG(Casa Pct)`

   *(If the aggregations show as SUM, click each pill → Measure → Average.)*

7. **Change to a heatmap:** in the Marks panel, change the dropdown from "Automatic" to **"Square"**.

8. **Drag `Measure Values`** (from the Measure Values card) to **Color**. Squares are now colored by value.

9. **Drag `Measure Values`** to **Label** too. Numbers now appear inside each square.

10. **Fix the color scale:** Click the Color card → **"Edit Colors…"**.
    - Palette: choose **"Red-Green Diverging"**.
    - Click OK.

11. **Fix the Gross NPA inversion:**
    The problem: high NPA is BAD, but the heatmap makes high numbers green. We need to flip NPA.
    - Make a new calculated field (just like we did for CAGR): **Create Calculated Field… → Name:** `Inverse NPA`. **Formula:** `-[Gross Npa Pct]`. Click OK.
    - In the Measure Values card, **remove `AVG(Gross Npa Pct)`** and **add `AVG(Inverse NPA)`** in its place.
    - But we want the LABEL to show the original Gross NPA value, not the inverse. So in the Marks panel: drag `AVG(Gross Npa Pct)` to **Label** instead of `Inverse NPA`.

    *(If this gets confusing, simplest version: leave the original `AVG(Gross Npa Pct)` and just visually remember that "more red on Gross NPA = better". Add a note in the dashboard caption.)*

12. **Sort banks manually best-to-worst:** Right-click the `Bank Name` pill on Rows → **Sort… → Manual**. Drag the names into this order: Axis Bank, ICICI Bank, HDFC Bank, SBI, Bank of Baroda, PNB. Click OK.

13. **Title:** `FY25 league table — banks ranked best (top) to worst (bottom)`.

### How do you know it's right?

You should see a grid:
- 6 rows (banks)
- 4 columns (ROA, Gross NPA, NIM, CASA)
- Mostly GREEN squares in the top rows, mostly RED squares at the bottom
- Numbers inside each square

---

## 🟢 Part 6 — Combine into one Dashboard (5 minutes)

1. At the bottom of the screen there's an icon row. Click the **"New Dashboard"** icon (looks like a grid 🟦🟦/🟦🟦, right next to the "+" tab).

2. A blank dashboard canvas opens. On the left panel you can see your 4 sheets listed.

3. **Set size:** in the "Size" panel on the left, click the dropdown → choose **"Automatic"**.

4. **Drag the 4 sheets onto the canvas:**
   - Drag "ROA Trend" → drop it on the **top-left** area.
   - Drag "NPA Clean-up" → drop it to the **right** of ROA Trend.
   - Drag "Loan-book CAGR" → drop it **below** ROA Trend.
   - Drag "FY25 League Table" → drop it **below** NPA Clean-up.

   You now have a 2×2 grid.

5. **Add a dashboard title:** at the top of the canvas, double-click where it says "Dashboard 1" → type:
   `Private vs PSU Banks in India — FY20–FY25`

6. **(Optional but cool) Make charts filter each other:** click each chart in the dashboard. A small toolbar pops up on the right side of that chart. Click the **funnel icon** ("Use as Filter"). Now clicking a bank/year in one chart will filter the others.

---

## 🟢 Part 7 — Publish to Tableau Public (3 minutes)

1. Top menu: **File → Save to Tableau Public As…**
2. If asked, sign in to Tableau Public with the same account you used in Part 0.
3. Workbook name: **`Private vs PSU Banks in India — A Strategic Analysis`**. Click Save.
4. Tableau uploads your file. After ~30 seconds it'll open the dashboard in your web browser.
5. **Copy the URL** from your browser's address bar. It'll look like:
   ```
   https://public.tableau.com/app/profile/priyanshu.moudgil/viz/PrivateVsPSUBanksInIndia/Dashboard1
   ```
6. **Paste that URL** to Claude in the next chat message and Claude will patch it into your README files.

🎉 **You did it.** You now have an interactive Tableau dashboard live on the public internet.

---

## 🆘 If something breaks

Don't panic. Take a screenshot of what's on your screen. Send it to Claude with a one-line description: *"I'm on Part 3, step 4, and the chart shows X instead of Y."* Claude will tell you the next click.

Most common gotchas:

| Problem | Fix |
|---|---|
| Years sort weird (FY25 before FY20) | Right-click year pill on Columns → Sort → Field → Fy Year Num → Ascending |
| Bars are stacked instead of side-by-side in Chart 2 | You forgot to drag `Bank Type` onto **Columns**, only put it on Color |
| Heatmap colors look backwards on Gross NPA | Use the `Inverse NPA` workaround from Part 5 step 11 |
| `Advances CAGR` shows the same value for every bank — wait that's correct | ✅ each bank gets one CAGR value because the formula is FIXED at Bank Name |
| Tableau won't open | Try restarting Tableau. If still broken, check you're using Tableau Public (free), not Tableau Desktop (paid trial expired) |
| Can't sign in to Tableau Public | Reset password at <https://public.tableau.com> → forgot password |

---

**Pro tip:** before publishing, click around in the dashboard yourself. Make sure tooltips appear on hover, click a year and confirm other charts filter. If it all works on your laptop, it'll work for recruiters too.
