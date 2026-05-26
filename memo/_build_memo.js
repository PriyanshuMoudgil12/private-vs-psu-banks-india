const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat, HeadingLevel,
  BorderStyle, WidthType, ShadingType, PageNumber, PageBreak,
} = require("docx");

const BLUE = "1F4E79";
const GREY = "595959";
const LIGHT_GREY = "F2F2F2";
const NAVY_TINT = "DCE6F1";
const RED_TINT = "F4CCCC";

const border = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
const borders = { top: border, bottom: border, left: border, right: border };

function H1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 200, after: 120 },
    children: [new TextRun({ text, bold: true, size: 28, color: BLUE })],
  });
}

function H2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 180, after: 80 },
    children: [new TextRun({ text, bold: true, size: 22, color: BLUE })],
  });
}

function P(runs, opts = {}) {
  return new Paragraph({
    spacing: { after: 100, line: 280 },
    alignment: opts.align || AlignmentType.LEFT,
    children: Array.isArray(runs) ? runs : [new TextRun({ text: runs, size: 22 })],
  });
}

function bullet(text) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { after: 60 },
    children: [new TextRun({ text, size: 22 })],
  });
}

function cell(text, opts = {}) {
  return new TableCell({
    borders,
    width: { size: opts.width, type: WidthType.DXA },
    shading: opts.shading ? { fill: opts.shading, type: ShadingType.CLEAR } : undefined,
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [new Paragraph({
      alignment: opts.align || AlignmentType.LEFT,
      children: [new TextRun({ text, bold: !!opts.bold, size: 20, color: opts.color || "000000" })],
    })],
  });
}

// ---- Title block
const titleBlock = [
  new Paragraph({
    spacing: { after: 60 },
    children: [new TextRun({
      text: "CONFIDENTIAL — STRATEGY MEMO",
      bold: true, size: 18, color: GREY,
    })],
  }),
  new Paragraph({
    spacing: { after: 80 },
    children: [new TextRun({
      text: "Why we are losing to private banks — and the three things to fix in 24 months",
      bold: true, size: 32, color: BLUE,
    })],
  }),
  new Paragraph({
    border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: BLUE, space: 4 } },
    spacing: { after: 120 },
    children: [new TextRun({
      text: "Prepared for: PSU Bank CEO   ·   Prepared by: Priyanshu Moudgil   ·   May 2026",
      italics: true, size: 20, color: GREY,
    })],
  }),
];

// ---- Executive summary
const execSummary = [
  H2("Executive summary"),
  P([
    new TextRun({ text: "We analyzed six years of audited financials for India’s six largest banks (HDFC, ICICI, Axis on the private side; SBI, PNB, and Bank of Baroda on the PSU side). The data tells a more nuanced story than the consensus “PSUs are dying” narrative.", size: 22 }),
  ]),
  P([
    new TextRun({ text: "Three facts matter most. ", bold: true, size: 22 }),
    new TextRun({ text: "First, the profitability gap is real and structural — private banks earned 1.98% ROA in FY25 against our 1.12%, a gap that has held at ~1 percentage point through the cycle. Second, our NPA clean-up is the genuine PSU success story: gross NPAs fell from 9.92% to 2.68%, narrowing the gap with private peers from 6.04pp to 1.23pp. Third, ", size: 22 }),
    new TextRun({ text: "the CASA advantage that has anchored the private-bank thesis for two decades just evaporated", bold: true, size: 22 }),
    new TextRun({ text: " — private CASA fell from 47.4% (FY22 peak) to 38.1% (FY25), and in FY25 PSUs (39.6%) actually edged ahead.", size: 22 }),
  ]),
  P([
    new TextRun({ text: "The strategic implication: stop fighting the last war (deposits) and start fighting the next one (asset-side pricing and digital underwriting).", bold: true, size: 22 }),
  ]),
];

// ---- KPI table
const kpiTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [2400, 1750, 1750, 1500, 1960],
  rows: [
    new TableRow({
      tableHeader: true,
      children: [
        cell("FY25 KPI",        { width: 2400, bold: true, shading: BLUE, color: "FFFFFF", align: AlignmentType.LEFT }),
        cell("Private avg",     { width: 1750, bold: true, shading: BLUE, color: "FFFFFF", align: AlignmentType.CENTER }),
        cell("PSU avg",         { width: 1750, bold: true, shading: BLUE, color: "FFFFFF", align: AlignmentType.CENTER }),
        cell("Gap (pp)",        { width: 1500, bold: true, shading: BLUE, color: "FFFFFF", align: AlignmentType.CENTER }),
        cell("Direction",       { width: 1960, bold: true, shading: BLUE, color: "FFFFFF", align: AlignmentType.CENTER }),
      ],
    }),
    new TableRow({ children: [
      cell("ROA (%)",      { width: 2400, bold: true }),
      cell("1.98",         { width: 1750, align: AlignmentType.CENTER, shading: NAVY_TINT }),
      cell("1.12",         { width: 1750, align: AlignmentType.CENTER, shading: RED_TINT }),
      cell("+0.86",        { width: 1500, align: AlignmentType.CENTER }),
      cell("Holding ~1pp", { width: 1960, align: AlignmentType.CENTER }),
    ]}),
    new TableRow({ children: [
      cell("Gross NPA (%)",     { width: 2400, bold: true }),
      cell("1.44",              { width: 1750, align: AlignmentType.CENTER, shading: NAVY_TINT }),
      cell("2.68",              { width: 1750, align: AlignmentType.CENTER, shading: RED_TINT }),
      cell("−1.23",        { width: 1500, align: AlignmentType.CENTER }),
      cell("Narrowing fast",    { width: 1960, align: AlignmentType.CENTER }),
    ]}),
    new TableRow({ children: [
      cell("NIM (%)",      { width: 2400, bold: true }),
      cell("4.09",         { width: 1750, align: AlignmentType.CENTER, shading: NAVY_TINT }),
      cell("3.01",         { width: 1750, align: AlignmentType.CENTER, shading: RED_TINT }),
      cell("+1.08",        { width: 1500, align: AlignmentType.CENTER }),
      cell("Stable spread",{ width: 1960, align: AlignmentType.CENTER }),
    ]}),
    new TableRow({ children: [
      cell("CASA (%)",            { width: 2400, bold: true }),
      cell("38.10",               { width: 1750, align: AlignmentType.CENTER, shading: NAVY_TINT }),
      cell("39.57",               { width: 1750, align: AlignmentType.CENTER, shading: RED_TINT }),
      cell("−1.47",          { width: 1500, align: AlignmentType.CENTER }),
      cell("Flipped — ours", { width: 1960, align: AlignmentType.CENTER }),
    ]}),
  ],
});

// ---- 3 Recommendations
const recs = [
  H2("Three things to fix in the next 24 months"),

  P([
    new TextRun({ text: "1. Stop chasing CASA. Chase NIM. ", bold: true, color: BLUE, size: 24 }),
    new TextRun({ text: "The funding war is over. Private banks lost ~9pp of CASA in three years; we held ours. The deposit-mix battleground does not deserve another rupee of capital. ", size: 22 }),
    new TextRun({ text: "The next war is on the asset side ", bold: true, size: 22 }),
    new TextRun({ text: "— pricing, retail mix, and digital underwriting. Action: shift the loan book mix 5 percentage points from corporate toward high-yield retail (personal, credit card, SMB) over eight quarters; stand up a digital-lending JV with a fintech to underwrite at scale; tie regional-head bonuses to NIM, not asset growth.", size: 22 }),
  ]),

  P([
    new TextRun({ text: "2. Defend the NPA gains by re-engineering underwriting. ", bold: true, color: BLUE, size: 24 }),
    new TextRun({ text: "The IBC won the first NPA war. The second will be won by data — bureau scores, GST flows, real-time monitoring. ", size: 22 }),
    new TextRun({ text: "Action: ", bold: true, size: 22 }),
    new TextRun({ text: "cap manual exception approvals at 10% of new sanctions; mandate model-driven decisioning for every loan under ₹5 crore by Q4 FY27; tie 30% of relationship-manager variable pay to vintage NPA performance, not disbursal volume; publish a quarterly underwriting scorecard to the board.", size: 22 }),
  ]),

  P([
    new TextRun({ text: "3. Become the bank for Bharat’s middle 60%. ", bold: true, color: BLUE, size: 24 }),
    new TextRun({ text: "Private banks own the urban affluent. Fintechs own the digital natives. The 600M middle-income, semi-urban, GST-registered SMB segment is largely under-served — and it is exactly where we have the unfair advantage: branch presence and intergenerational trust. The gap is digital UX. ", size: 22 }),
    new TextRun({ text: "Action: ", bold: true, size: 22 }),
    new TextRun({ text: "rebuild mobile + chat account opening to a 90-second flow; partner with two regional payment-aggregators for SMB collections; target ₹5 lakh crore of new SMB advances by FY28.", size: 22 }),
  ]),
];

// ---- What this means for fintechs
const fintech = [
  H2("Coda — what this means for fintechs"),
  P([
    new TextRun({ text: "A re-rated PSU is the most underpriced distribution channel in India. The bank with 23,000 branches and 50 crore accounts has 90% of the customer file and roughly 10% of the digital UX. A fintech that productizes underwriting, KYC, or collections ", size: 22 }),
    new TextRun({ text: "as infrastructure that SBI, PNB, or BOB can rent ", italics: true, size: 22 }),
    new TextRun({ text: "captures the upside without funding the balance sheet. The winners of the next decade in BFSI may not be the bank or the fintech — they’ll be the picks-and-shovels providers sitting between them.", size: 22 }),
  ]),
];

// ---- Methods footnote
const methods = [
  new Paragraph({
    border: { top: { style: BorderStyle.SINGLE, size: 6, color: "BFBFBF", space: 4 } },
    spacing: { before: 200, after: 60 },
    children: [new TextRun({ text: " ", size: 16 })],
  }),
  new Paragraph({
    spacing: { after: 40 },
    children: [new TextRun({
      text: "Methodology & sources",
      bold: true, size: 18, color: GREY,
    })],
  }),
  new Paragraph({
    spacing: { after: 40 },
    children: [new TextRun({
      text: ("36 bank-year observations (6 banks × 6 years). Absolute values in ₹ crore. Ratios " +
             "in percentage. Data compiled from each bank’s annual report (FY20–FY25), Q4 investor " +
             "presentations, Equitymaster Annual Results Analysis, and press releases; cross-checked " +
             "via May 2026 web search. Full SQL queries, Python notebook, and Excel workbook in the " +
             "accompanying GitHub repository."),
      size: 18, italics: true, color: GREY,
    })],
  }),
];

// ---- Document
const doc = new Document({
  creator: "Priyanshu Moudgil",
  title: "Private vs PSU Banks — Strategy Memo",
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial", color: BLUE },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial", color: BLUE },
        paragraph: { spacing: { before: 180, after: 80 }, outlineLevel: 1 } },
    ],
  },
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 },
      },
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({
            text: "Private vs PSU Banks — Strategy Memo",
            italics: true, size: 16, color: GREY,
          })],
        })],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "Priyanshu Moudgil  —  May 2026  —  Page ",
                          size: 16, color: GREY }),
            new TextRun({ children: [PageNumber.CURRENT], size: 16, color: GREY }),
          ],
        })],
      }),
    },
    children: [
      ...titleBlock,
      ...execSummary,
      new Paragraph({ spacing: { after: 80 }, children: [new TextRun(" ")] }),
      kpiTable,
      ...recs,
      ...fintech,
      ...methods,
    ],
  }],
});

Packer.toBuffer(doc).then(buf => {
  const out = path.join(__dirname, "Private_vs_PSU_Banks_Strategy_Memo.docx");
  fs.writeFileSync(out, buf);
  console.log("wrote " + out);
});
