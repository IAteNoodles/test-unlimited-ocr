# Indian Medical Document Formats — Reference for Synthetic OCR Data Generation

## Purpose

Clean text templates for 12 Indian lab report formats and 12 Indian discharge summary formats. These serve as source text for the synthetic OCR error injection pipeline (Section 4.1 of finetuning_plan.md). Each format includes: where used, sections, differentiators, layout style, and a realistic example with Indian reference ranges and clinical content.

---

## Part A: Lab Report Formats (12)

### Common Indian Reference Ranges

These ranges are used across formats below. Individual labs may vary slightly.

| Test | Unit | Male Range | Female Range |
|---|---|---|---|
| Hemoglobin | g/dL | 13.0–17.0 | 11.0–15.0 |
| RBC count | million/cu.mm | 4.5–6.0 | 4.0–5.5 |
| WBC count | /cu.mm | 4000–11000 | 4000–11000 |
| Platelet count | lakh/cu.mm | 1.5–4.5 | 1.5–4.5 |
| PCV (Hematocrit) | % | 40–54 | 36–48 |
| MCV | fL | 80–100 | 80–100 |
| MCH | pg | 27–33 | 27–33 |
| MCHC | g/dL | 32–37 | 32–37 |
| Neutrophils | % | 40–75 | 40–75 |
| Lymphocytes | % | 20–45 | 20–45 |
| Eosinophils | % | 1–6 | 1–6 |
| Monocytes | % | 2–10 | 2–10 |
| Basophils | % | 0–2 | 0–2 |
| Total Cholesterol | mg/dL | <200 | <200 |
| Triglycerides | mg/dL | <150 | <150 |
| HDL | mg/dL | >40 | >50 |
| LDL | mg/dL | <100 | <100 |
| VLDL | mg/dL | <30 | <30 |
| Fasting Blood Sugar | mg/dL | 70–100 | 70–100 |
| PP Blood Sugar | mg/dL | <140 | <140 |
| HbA1c | % | <5.7 | <5.7 |
| Urea | mg/dL | 15–40 | 15–40 |
| Creatinine | mg/dL | 0.6–1.2 | 0.5–1.1 |
| Uric Acid | mg/dL | 3.4–7.0 | 2.4–6.0 |
| Bilirubin Total | mg/dL | 0.2–1.2 | 0.2–1.2 |
| SGPT (ALT) | U/L | 7–56 | 7–56 |
| SGOT (AST) | U/L | 10–40 | 10–40 |
| ALP | U/L | 44–147 | 44–147 |
| Total Protein | g/dL | 6.0–8.3 | 6.0–8.3 |
| Albumin | g/dL | 3.5–5.0 | 3.5–5.0 |
| TSH | µIU/mL | 0.4–4.2 | 0.4–4.2 |
| T3 | ng/dL | 80–200 | 80–200 |
| T4 | µg/dL | 5.0–13.0 | 5.0–13.0 |
| Vitamin D | ng/mL | 20–50 | 20–50 |
| Vitamin B12 | pg/mL | 200–900 | 200–900 |
| Sodium | mmol/L | 135–155 | 135–155 |
| Potassium | mmol/L | 3.5–5.5 | 3.5–5.5 |
| Chloride | mmol/L | 96–109 | 96–109 |

---

### Format 1: Thyrocare (National Chain — Prepaid/Home Collection)

**Where used:** Thyrocare Technologies Ltd. — pan-India, online booking, home collection, prepaid model. Reports delivered via email/app.

**Sections:**
1. Header: Thyrocare logo, lab address (Navi Mumbai HQ), NABL accreditation ID
2. Patient details: Name, age, gender, patient ID, registered mobile
3. Test panel name and code
4. Results table: Test name, result, unit, biological reference range, flag
5. Footer: Method notes, barcode, lab technician signature, NABL disclaimer

**Differentiators:**
- Single-column compact layout (A4 portrait)
- Prepaid booking ID prominently displayed
- "Aarogyam" brand package names
- Minimal clinical commentary — values only
- Standardized national reference ranges (not location-specific)
- Reports often have QR code for verification

**Layout style:** Clean, single-column, compact font (Arial 9pt), light blue header band, results in bordered table with alternating row shading.

**Example:**

```
THYROCARE TECHNOLOGIES LTD.
Plot No. D-37, TTC Area, MIDC, Airoli, Navi Mumbai - 400708
NABL Accredited (MC-2289) | ICMR Approved | CAP Certified

Patient Name: RAJESH KUMAR SHARMA          Patient ID: TC20241187234
Age / Gender: 42 / Male                     Registered Mobile: 98XXXXXX10
Booking ID: ARO2401                          Sample Collected: 15-Jan-2025 07:30
Report Date: 15-Jan-2025 14:22

AAROGYAM 1.2 (60 Parameters)

=================================================================
TEST NAME              RESULT    UNIT       BIOLOGICAL REFERENCE
=================================================================

HEMOGRAM (CBC)
-----------------------------------------------------------------
Hemoglobin (Hb)        14.8      g/dL       13.0 - 17.0
RBC Count              5.12      mill/cu.mm 4.5 - 6.0
WBC Count              7800      /cu.mm     4000 - 11000
Platelet Count         2.45      lakh/cu.mm 1.5 - 4.5
PCV (Hematocrit)       44.2      %          40.0 - 54.0
MCV                    86.3      fL         80.0 - 100.0
MCH                    28.9      pg         27.0 - 33.0
MCHC                   33.5      g/dL       32.0 - 37.0
Neutrophils            62        %          40 - 75
Lymphocytes            28        %          20 - 45
Eosinophils            04        %          1 - 6
Monocytes              05        %          2 - 10
Basophils              01        %          0 - 2

DIABETES
-----------------------------------------------------------------
Fasting Blood Sugar    112  H    mg/dL      70 - 100
HbA1c (Glycosylated    6.2  H    %          < 5.7
  Hemoglobin)

LIPID PROFILE
-----------------------------------------------------------------
Total Cholesterol      182       mg/dL      < 200
Triglycerides          168  H    mg/dL      < 150
HDL Cholesterol        38   L    mg/dL      > 40
LDL Cholesterol        112  H    mg/dL      < 100
VLDL Cholesterol       33    H   mg/dL      < 30

THYROID PROFILE
-----------------------------------------------------------------
TSH                    2.84      µIU/mL     0.4 - 4.2
T3                    128        ng/dL      80 - 200
T4                    8.6        µg/dL      5.0 - 13.0

KIDNEY FUNCTION TEST
-----------------------------------------------------------------
Urea                   28        mg/dL      15 - 40
Creatinine             0.9       mg/dL      0.6 - 1.2
Uric Acid              5.4       mg/dL      3.4 - 7.0

LIVER FUNCTION TEST
-----------------------------------------------------------------
Bilirubin Total        0.7       mg/dL      0.2 - 1.2
SGPT (ALT)             32        U/L        7 - 56
SGOT (AST)             24        U/L        10 - 40
ALP                    88        U/L        44 - 147
Total Protein          7.2       g/dL       6.0 - 8.3
Albumin                4.5       g/dL       3.5 - 5.0

VITAMINS
-----------------------------------------------------------------
Vitamin D              18.5  L   ng/mL      20 - 50
Vitamin B12            412       pg/mL      200 - 900

=================================================================
** End of Report **
Method: Fully Automated Analyser (Cobas c311, Sysmex XN-550)
H = High, L = Low
Results are for clinical correlation by a registered medical practitioner.
Barcode: |||| |||| ||| | ||  ||| | ||||  TC20241187234
Lab Technician: [Signature]
Dr. [Name], MD (Pathology), Pathologist-in-Charge
NABL Ref: MC-2289 | Valid up to 31-Mar-2026
```

---

### Format 2: Dr Lal PathLabs (National Chain — Franchise Model)

**Where used:** Dr Lal PathLabs — pan-India, franchise collection centres, walk-in patients, doctor-referred. Reports via app/email/print.

**Sections:**
1. Header: Dr Lal PathLabs logo, franchise centre address, NABL ID, ICMR approval
2. Patient demographics: Name, age, gender, patient code, referring doctor
3. Specimen details: Collection date/time, sample type
4. Results: Test group headers, test name, result, unit, reference range, abnormal flag
5. Interpreting physician note (if critical values)
6. Footer: Pathologist signature, NABL disclaimer, franchise centre code

**Differentiators:**
- Referring doctor name printed prominently
- Franchise centre code on every page
- "Lal PathLabs" branding with red accent color
- Critical values marked with asterisk and comment
- Age/gender-specific reference ranges (pediatric/geriatric variants)
- Often includes delta check notation (previous value comparison)

**Layout style:** Two-column header (patient left, lab right), results in full-width table, red header band, Times New Roman 10pt.

**Example:**

```
DR LAL PATHLABS
(NABL Accredited: MC-2250 | ICMR Approved | ISO 9001:2015)

Franchise Centre: LPL-DEL-0456, Sector 18, Rohini, New Delhi - 110089
Tel: 011-27XXXXXX | Email: reports@lalpathlabs.com

Patient Name: PRIYA NAIR              Patient Code: LPL25A019872
Age / Gender: 34 / Female             Ref. Doctor: Dr. S. Menon (MD, Med)
Sample Collected: 20-Jan-2025 08:15    Report Generated: 20-Jan-2025 17:40

COMPLETE BLOOD COUNT (CBC)
================================================================================
Test                    Result    Unit       Ref. Range          Flag
================================================================================
Hemoglobin              10.2      g/dL       11.0 - 15.0         L
RBC Count               3.82      mill/cu.mm 4.0 - 5.5           L
WBC Count               6200      /cu.mm     4000 - 11000
Platelet Count          1.98      lakh/cu.mm 1.5 - 4.5
PCV                     31.8      %          36.0 - 48.0         L
MCV                     83.2      fL         80.0 - 100.0
MCH                     26.7      pg         27.0 - 33.0         L
MCHC                    32.1      g/dL       32.0 - 37.0
RDW                     15.8      %          11.6 - 14.0         H
Neutrophils             58        %          40 - 75
Lymphocytes             34        %          20 - 45
Eosinophils             03        %          1 - 6
Monocytes               04        %          2 - 10
Basophils               01        %          0 - 2

IRON STUDIES
================================================================================
Serum Iron              42        µg/dL      60 - 170            L
TIBC                    428       µg/dL      250 - 450           H
Transferrin Saturation  9.8       %          20 - 50             L
Ferritin                8.5       ng/mL      15 - 150            L

THYROID PROFILE
================================================================================
TSH                     4.85      µIU/mL     0.4 - 4.2           H
Free T3                 2.1       pg/mL      2.3 - 4.2           L
Free T4                 0.9       ng/dL      0.8 - 1.8

Note: Low hemoglobin with microcytic hypochromic picture and low ferritin
is consistent with iron deficiency anemia. Elevated TSH with low Free T3
suggests hypothyroidism. Please correlate clinically.

Pathologist: Dr. [Name], MD (Pathology)
Centre Code: LPL-DEL-0456
NABL MC-2250 | Valid up to 28-Feb-2027
*** End of Report ***
```

---

### Format 3: Apollo Diagnostics (Hospital Chain Lab)

**Where used:** Apollo Hospitals Group diagnostic labs — attached to Apollo hospitals and standalone Apollo Diagnostics centres. Reports integrated with Apollo EHR.

**Sections:**
1. Header: Apollo logo, hospital/centre name, address, NABL + JCI accreditation
2. Patient banner: UHID (Unique Hospital ID), name, age, gender, IP/OP number
3. Clinical summary: Brief indication/reason for test
4. Results: Department-grouped (Biochemistry, Hematology, Microbiology)
5. Clinical interpretation / comments
6. Footer: Consultant pathologist signature, NABL + JCI logos

**Differentiators:**
- UHID (hospital patient ID) prominently displayed
- Clinical indication field (reason for ordering test)
- Department-grouped results (Biochem/Hematology/Micro separately headed)
- Clinical interpretation section with pathologist comments
- JCI accreditation alongside NABL
- Integrated with Apollo EHR — may include previous visit delta
- "Apollo" branding with blue/orange accent

**Layout style:** Professional hospital letterhead style, blue header band with Apollo logo, two-tier results table (department header row + test rows), Calibri 10pt.

**Example:**

```
APOLLO DIAGNOSTICS
Apollo Hospitals, Greams Road, Chennai - 600006
NABL: MC-2190 | JCI Accredited | NABH Accredited

UHID: APH-2024-0089172          OP No: OP-25-04512
Patient: SUNDARAM KRISHNAN       Age: 58 / Male
Ref. Consultant: Dr. R. Iyer (Cardiology)
Clinical Indication: Post-CABG follow-up, routine cardiac panel
Collected: 22-Jan-2025 06:00     Reported: 22-Jan-2025 15:30

BIOCHEMISTRY
---------------------------------------------------------------------------
Test                        Result    Unit       Ref. Range        Flag
---------------------------------------------------------------------------
Fasting Blood Sugar         96        mg/dL      70 - 100
HbA1c                      5.8       %          < 5.7             H
Total Cholesterol           154       mg/dL      < 200
Triglycerides               142       mg/dL      < 150
HDL Cholesterol             45        mg/dL      > 40
LDL Cholesterol             82        mg/dL      < 100
VLDL Cholesterol            28        mg/dL      < 30
Creatinine                  1.1       mg/dL      0.6 - 1.2
Urea                        32        mg/dL      15 - 40
Sodium                      138       mmol/L     135 - 155
Potassium                   4.2       mmol/L     3.5 - 5.5
CK-MB                       14        U/L        < 25
Troponin I                  0.02      ng/mL      < 0.04
NT-proBNP                   125       pg/mL      < 300

HEMATOLOGY
---------------------------------------------------------------------------
Hemoglobin                  13.5      g/dL       13.0 - 17.0
WBC Count                   8200      /cu.mm     4000 - 11000
Platelet Count              2.80      lakh/cu.mm 1.5 - 4.5
PT                          12.8      sec        11.0 - 14.0
INR                         1.1                  0.8 - 1.2
APTT                        30.2      sec        25.0 - 35.0

CLINICAL INTERPRETATION:
Cardiac enzymes within normal limits. HbA1c marginally elevated (5.8%),
suggesting pre-diabetes. Lipid profile at target for post-CABG patient
on statin therapy. Renal function normal. INR within therapeutic range.
Continue current management. Repeat HbA1c in 3 months.

Dr. [Name], MD (Biochemistry)
Dr. [Name], MD (Pathology)
Consultant Pathologists, Apollo Hospitals
NABL MC-2190 | JCI Accredited
```

---

### Format 4: Government Hospital Lab (Free/Subsidized)

**Where used:** Government medical college hospitals, district hospitals, CHC labs. Free or nominal fee (Rs. 5-20). High volume, limited automation.

**Sections:**
1. Header: Hospital name (government), "Government of [State]" banner, lab department
2. Patient registration: OP/IP number, name, age, gender (often handwritten or dot-matrix printed)
3. Test name(s) requested
4. Results: Minimal table — test name, result, unit, reference range (sometimes absent)
5. Footer: Lab technician initials, no pathologist signature (often)

**Differentiators:**
- Dot-matrix or thermal printer output (low quality — important for OCR training)
- Minimal formatting, no color, no logos
- Reference ranges often missing or handwritten
- No abnormal flags — just raw values
- Patient name may be in regional language + English
- Often smudged, carbon-copy quality
- No NABL accreditation typically
- High noise: stamps, signatures overlapping text, fold marks

**Layout style:** Dot-matrix print on continuous tractor-feed paper or thermal paper, monospace font (Courier), no tables/borders, plain text columns.

**Example:**

```
GOVERNMENT MEDICAL COLLEGE HOSPITAL
DEPARTMENT OF BIOCHEMISTRY
[State] Government | [City]

OP No: 2025/045872          Date: 25-Jan-2025
Name: LAKSHMI DEVI          Age: 45/F
Beds/OP: Medicine OP

Tests Requested: FBS, PPBS, Urea, Creatinine

========================================
Test            Value    Unit
========================================
FBS             134      mg/dL
PPBS            198      mg/dL
Urea            38       mg/dL
Creatinine      1.0      mg/dL
========================================

[Lab Technician Initials: RK]
[Round Stamp: Govt Medical College, Biochemistry Dept]
[Date Stamp: 25 JAN 2025]

Note: Report to be collected from counter. Valid for 7 days.
```

---

### Format 5: Standalone Diagnostic Centre (Mid-Tier Private)

**Where used:** Independent private diagnostic centres (not chain-affiliated). Common in tier-2/tier-3 cities. Walk-in patients, doctor referrals.

**Sections:**
1. Header: Centre name, address, phone, NABL ID (if accredited)
2. Patient details: Name, age, gender, phone, referring doctor
3. Bill/invoice section (often on same page as report)
4. Results: Test name, result, unit, reference range
5. Footer: Technician signature, centre stamp

**Differentiators:**
- Invoice and report often on same page (unique OCR challenge)
- Local language mixed with English
- Variable formatting — no standardized template
- May include handwritten notes/annotations by technician
- Centre stamp/seal overlapping text
- Often printed on inkjet printer (lower quality than laser)
- Reference ranges may be from textbook (not lab-validated)
- Smaller test panels (5-15 tests typical)

**Layout style:** Custom layout, often designed in MS Word/Tally, mixed fonts, no consistent table structure, A5 or A4.

**Example:**

```
SRI VINAYAKA DIAGNOSTIC CENTRE
Beside Bus Stand, Tumkur Road, [Town] - 572XXX
Ph: 0816-22XXXXX | Mob: 9448XXXXXX
NABL: (Applied For) | GST: 29ABCDE1234F1Z5

Bill No: 2025/0142          Date: 28-Jan-2025
Patient: NAGARAJ M          Age: 52/M
Phone: 9900XXXXXX           Ref. Dr: Dr. Prakash

===================================================
TEST                RESULT    UNIT     REF RANGE
===================================================

BLOOD SUGAR
Fasting             146       mg/dL    70-100
PP                  224       mg/dL    <140

UREA & CREATININE
Urea                42        mg/dL    15-40
Creatinine          1.3       mg/dL    0.6-1.2

LIPID PROFILE
Cholesterol         210       mg/dL    <200
TG                  190       mg/dL    <150
HDL                 35        mg/dL    >40
LDL                 138       mg/dL    <100

URINE ROUTINE
Colour              Pale Yellow
Appearance          Clear
pH                  6.0
Specific Gravity     1.020
Protein             Nil
Sugar               +2
Pus Cells           2-3/hpf
RBC                 Nil
Crystals            Nil

===================================================
Amount: Rs. 450/-    Paid: Cash
[Centre Stamp: Sri Vinayaka Diagnostic Centre, [Town]]
Tech: [Signature]
*** Thank You ***
```

---

### Format 6: Metropolis Healthcare (National Chain — NABL Premium)

**Where used:** Metropolis Healthcare Ltd. — pan-India, urban focus, premium positioning. Specialized tests, advanced panels. Reports via app/email.

**Sections:**
1. Header: Metropolis logo, lab address, NABL + CAP + ICMR accreditations
2. Patient demographics: Name, age, gender, patient ID, referring physician
3. Specimen info: Collection date/time, sample type, accession number
4. Results: Grouped by panel, test name, result, unit, reference range, flag
5. Technical notes: Methodology, interferences, limitations
6. Clinical comments (for specialized tests)
7. Footer: Pathologist signature, accreditation logos, barcode

**Differentiators:**
- Premium layout with high-quality formatting
- Technical notes section (methodology, interferences)
- Clinical comments for specialized tests
- Age/gender-specific reference ranges clearly labeled
- Delta check with previous result (if available)
- "Metropolis" branding with green accent
- Critical value alert box (if applicable)
- Often includes chromatogram/graph for HPLC/electrophoresis

**Layout style:** Professional multi-column layout, green header band, bordered tables with color-coded flags (red H, blue L), Calibri/Arial 9pt, A4 portrait.

**Example:**

```
METROPOLIS HEALTHCARE LTD.
NABL: MC-2412 | CAP: 9024715 | ICMR Approved
Corporate Office: A-101, MIDC, Andheri (E), Mumbai - 400093

Patient: ANITA DESAI              Patient ID: MHC25B007845
Age / Gender: 29 / Female         Accession: 25-01-88421
Ref. Physician: Dr. K. Shah       Collected: 30-Jan-2025 07:45
                                  Reported: 30-Jan-2025 16:10

+-----------------------------------------------------------------------+
| CRITICAL VALUE ALERT                                                  |
| Potassium: 5.9 mmol/L (Ref: 3.5 - 5.5) — CRITICAL HIGH               |
| Notified to Dr. K. Shah at 15:45 on 30-Jan-2025                       |
+-----------------------------------------------------------------------+

ELECTROLYTES
---------------------------------------------------------------------------
Test                    Result    Unit       Ref. Range         Flag
---------------------------------------------------------------------------
Sodium                  142       mmol/L     135 - 155
Potassium               5.9   *H  mmol/L     3.5 - 5.5          CRITICAL
Chloride                108       mmol/L     96 - 109
Ionized Calcium         1.05      mmol/L     1.10 - 1.35        L
Phosphorus              4.8       mg/dL      2.5 - 4.5          H
Magnesium               2.1       mg/dL      1.7 - 2.2

RENAL FUNCTION
---------------------------------------------------------------------------
Urea                    68   H    mg/dL      15 - 40
Creatinine              1.8  H    mg/dL      0.5 - 1.1
eGFR                    38   L    mL/min     > 90

HEMATOLOGY
---------------------------------------------------------------------------
Hemoglobin              8.2  L    g/dL       11.0 - 15.0
WBC Count               11200 H   /cu.mm     4000 - 11000
Platelet Count          1.20  L   lakh/cu.mm 1.5 - 4.5

TECHNICAL NOTES:
- Potassium measured by ion-selective electrode (ISE)
- Sample hemolysis index: 1+ (mild) — potassium may be falsely elevated
- Recommend repeat sample with proper venipuncture technique
- eGFR calculated by CKD-EPI (2021) equation

CLINICAL COMMENTS:
Findings suggestive of acute kidney injury with hyperkalemia.
Mild hemolysis may contribute to elevated potassium; however, the
clinical picture is consistent with true hyperkalemia given the
elevated creatinine and low eGFR. Recommend ECG evaluation and
urgent clinical correlation.

Dr. [Name], MD (Pathology)          Dr. [Name], MD (Biochemistry)
Consultant Pathologist              Consultant Biochemist

Metropolis Healthcare Ltd.
NABL MC-2412 | CAP 9024715
Barcode: |||| ||| | |||| ||  ||| |  25-01-88421
```

---

### Format 7: SRL Diagnostics (National Chain — Reference Lab)

**Where used:** SRL Ltd. (formerly SRL Ranbaxy) — pan-India, reference lab for complex/specialized tests. Also has front-end collection centres.

**Sections:**
1. Header: SRL logo, lab address (Goregaon, Mumbai HQ), NABL + CAP + ICMR
2. Patient demographics: Name, age, gender, patient ID, referring doctor
3. Specimen details: Collection date, sample type, accession number
4. Results: Panel-grouped, test name, result, unit, reference range, flag
5. Methodology notes
6. Footer: Pathologist signature, accreditation logos

**Differentiators:**
- Reference lab — handles complex/specialized tests other labs can't do
- Detailed methodology notes for each test
- Sub-specialty pathologist signatures (histopath, hematology, etc.)
- "SRL" branding with blue accent
- Often includes interpretive comments for complex panels
- May include flow cytometry graphs, electrophoresis traces
- Longer turnaround time noted on report

**Layout style:** Clean professional layout, blue header, two-column results for short tests, full-width for long panels, Arial 9pt.

**Example:**

```
SRL DIAGNOSTICS
(A Fortis Company)
NABL: MC-2335 | CAP: 9024698 | ICMR Approved
Reference Lab: Plot No. 1, MIDC, Goregaon (E), Mumbai - 400063

Patient: MOHAMMED FASIL          Patient ID: SRL25C004512
Age / Gender: 6 / Male           Accession: SRL-25-998712
Ref. Doctor: Dr. A. Reddy        Collected: 02-Feb-2025 09:00
(Pediatric Hemato-Oncology)      Reported: 04-Feb-2025 14:30

HEMOGLOBIN ELECTROPHORESIS (HPLC)
===========================================================================
Test                        Result    Unit       Ref. Range        Flag
===========================================================================
Hemoglobin A2               5.8   H   %          2.0 - 3.2
Hemoglobin F                1.2       %          < 1.0
Hemoglobin A                93.0      %          95.0 - 98.0      L
Hb D                        0.0       %          Not Detected
Hb S                        0.0       %          Not Detected
Hb C                        0.0       %          Not Detected
Hb E                        0.0       %          Not Detected

COMPLETE BLOOD COUNT
===========================================================================
Hemoglobin                  7.8   L   g/dL       11.0 - 14.0
RBC Count                   4.20      mill/cu.mm 4.0 - 5.5
WBC Count                   9500      /cu.mm     4500 - 13500
Platelet Count              3.10      lakh/cu.mm 1.5 - 4.5
MCV                        62.0   L   fL         75.0 - 87.0
MCH                        18.5   L   pg         24.0 - 30.0
MCHC                       29.8   L   g/dL       30.0 - 36.0
RDW                        22.5   H   %          11.5 - 14.5

PERIPHERAL SMEAR EXAMINATION
===========================================================================
RBC: Microcytic, hypochromic, anisopoikilocytosis (+), target cells
     seen, basophilic stippling present.
WBC: Normocellular, no abnormal cells seen.
Platelets: Adequate on smear.

IRON STUDIES
===========================================================================
Serum Iron                  35    L   µg/dL      50 - 120
TIBC                       480    H   µg/dL      250 - 450
Ferritin                   6.2    L   ng/mL      7 - 140

METHODOLOGY:
- Hb Electrophoresis: HPLC (Bio-Rad D-10)
- CBC: Automated (Sysmex XN-1000)
- Peripheral Smear: Manual review by hematopathologist
- Iron Studies: Immunoturbidimetry

INTERPRETATION:
Hemoglobin A2 of 5.8% is elevated, consistent with beta-thalassemia
trait. Low MCV, MCH, and elevated RDW support the diagnosis. Iron
studies show coexisting iron deficiency anemia. Peripheral smear
shows microcytic hypochromic picture with target cells, consistent
with thalassemia trait. Genetic counseling recommended for parents.

Dr. [Name], MD (Pathology)           Dr. [Name], MD (Hematology)
Consultant Hematopathologist         Consultant Hematologist

SRL Diagnostics | NABL MC-2335 | CAP 9024698
```

---

### Format 8: Point-of-Care Testing (POCT) Report

**Where used:** Bedside POCT devices in ICUs, ERs, ambulances. Blood gas analyzers, glucometers, portable analyzers. Rapid results, minimal formatting.

**Sections:**
1. Device header: Analyzer model, hospital/department
2. Patient ID: Minimal (often just IP number or barcode)
3. Timestamp: Date/time of analysis
4. Results: Compact list — parameter, value, unit, range
5. Operator initials

**Differentiators:**
- Thermal paper printout (narrow, ~80mm width)
- Very compact — 5-10 parameters only
- No patient name (privacy — barcode only)
- Printed at point of care, not lab
- Blood gas, electrolytes, glucose, lactate common
- No pathologist signature — operator initials only
- Quality: thermal print fades, susceptible to heat damage
- Often taped into patient chart (OCR challenge: tape marks, folds)

**Layout style:** Narrow thermal paper (~80mm), monospace, very small font (6-7pt), no tables, plain text columns.

**Example:**

```
RAPIDPOINT 500 - BLOOD GAS ANALYZER
Apollo Hospitals - ICU-2

ID: 25-0287-ICU2     03-Feb-2025 14:22
Sample: Arterial     Op: RN

pH        7.28    L   (7.35-7.45)
pCO2      52      H   (35-45 mmHg)
pO2       68      L   (80-100 mmHg)
HCO3      24          (22-26 mmol/L)
BE        -2.0        (-2 to +2)
SO2       91      L   (95-100 %)
Na+       136         (135-155 mmol/L)
K+        5.4     H   (3.5-5.5 mmol/L)
Cl-       104         (96-109 mmol/L)
Glu       248     H   (70-140 mg/dL)
Lactate   3.2     H   (0.5-2.0 mmol/L)
Hb        9.2     L   (13-17 g/dL)
Hct       27.5    L   (40-54 %)

Interp: Uncompensated respiratory
acidosis with hypoxemia.

[Operator: RN]
[Auto-printed]
```

---

### Format 9: Microbiology Culture & Sensitivity Report

**Where used:** Microbiology departments in hospitals and reference labs. Culture, identification, antibiotic sensitivity testing. Takes 48-72 hours.

**Sections:**
1. Header: Lab/hospital name, department (Microbiology)
2. Patient demographics: Name, age, gender, IP/OP number, ward/bed
3. Specimen details: Sample type (urine/blood/sputum/wound), collection date, method
4. Culture result: Growth/no growth, organism identified
5. Colony count (for urine/quantitative cultures)
6. Antibiotic Sensitivity Pattern (AST): Organism, antibiotic, zone size, S/I/R
7. Comments: Interpretation, contamination notes
8. Footer: Microbiologist signature

**Differentiators:**
- Takes 48-72 hours — report date differs from collection date
- Antibiotic sensitivity table is unique format (S/I/R pattern)
- Organism identification with scientific names (italicized)
- Colony count for quantitative cultures (CFU/mL)
- "Mixed growth" / "Contaminated sample" notes common
- May include preliminary report (24h) + final report (72h)
- Antibiotic abbreviations: AMP, AMC, CTR, CIP, GEN, etc.
- S = Sensitive, I = Intermediate, R = Resistant

**Layout style:** Two-section layout — upper section (culture result), lower section (AST table). AST table has antibiotic name, disk potency, zone diameter, interpretation columns.

**Example:**

```
MICROBIOLOGY DEPARTMENT
Manipal Hospital, Bengaluru - 560017

Patient: KAVITHA R               IP No: IP-25-3398
Age / Gender: 62 / Female        Ward: 4A, Bed 12
Ref. Doctor: Dr. S. Nair          Sample: Urine (Mid-stream)
Collected: 05-Feb-2025 08:00      Reported: 07-Feb-2025 11:00

CULTURE & SENSITIVITY - URINE
===========================================================================

SPECIMEN: Urine (Mid-stream clean catch)
COLONY COUNT: > 10^5 CFU/mL

CULTURE RESULT:
Significant growth of Escherichia coli

ANTIBIOTIC SENSITIVITY PATTERN:
===========================================================================
Antibiotic          Disc    Zone(mm)   Interpretation
===========================================================================
Amikacin            AK-30   20         S
Amoxicillin-Clav    AMC-30  14         R
Ampicillin          AMP-10  11         R
Cefepime            CPM-30  18         S
Cefotaxime          CTX-30  16         I
Ceftriaxone         CTR-30  17         S
Ciprofloxacin       CIP-5   12         R
Co-trimoxazole      COT-25  10         R
Gentamicin          GEN-10  16         S
Imipenem            IPM-10  24         S
Levofloxacin        LE-5    14         R
Nitrofurantoin      NIT-300 18         S
Norfloxacin         NX-10   13         R
Piperacillin-Taz    PIT-100 20         S
Tobramycin          TOB-10  15         S

S = Sensitive, I = Intermediate, R = Resistant

COMMENTS:
Significant bacteriuria with E. coli resistant to fluoroquinolones
and co-trimoxazole. Sensitive to cephalosporins (cefepime,
ceftriaxone), carbapenems (imipenem), and nitrofurantoin.
Recommend: Injection Ceftriaxone 1g IV BD as per renal function.
Repeat culture after 5 days of antibiotic therapy.

Dr. [Name], MD (Microbiology)
Consultant Microbiologist
```

---

### Format 10: Histopathology Report

**Where used:** Histopathology departments in hospitals and reference labs. Tissue biopsy processing, H&E staining, microscopic examination. Reports are descriptive text (not tabular).

**Sections:**
1. Header: Lab/hospital name, department (Histopathology)
2. Patient demographics: Name, age, gender, IP/OP number
3. Specimen details: Tissue/site, biopsy type, clinical history
4. Gross description: Macroscopic findings (specimen size, appearance)
5. Microscopic description: Histological findings (cellular level)
6. Diagnosis: Final histopathological diagnosis
7. TNM staging (if applicable — cancer specimens)
8. Comments / prognostic markers
9. Footer: Pathologist signature

**Differentiators:**
- Primarily narrative text (not tabular) — unique OCR challenge
- Medical terminology: architectural patterns, cellular atypia, mitotic figures
- TNM staging notation (T2 N1 M0, etc.)
- Immunohistochemistry (IHC) results may be appended
- Gross + Microscopic sections are long descriptive paragraphs
- Diagnosis is the key field — usually 1-3 lines
- Turnaround: 3-7 days (tissue processing takes time)
- May include "Provisional" and "Final" reports

**Layout style:** Letter-style report, no tables (except IHC results), justified text paragraphs, bold section headers, Times New Roman 11pt.

**Example:**

```
DEPARTMENT OF HISTOPATHOLOGY
Tata Memorial Hospital, Mumbai - 400012

Histopathology Report No: H/25/04872

Patient: RAMESH PATEL              IP No: IP-25-4456
Age / Gender: 54 / Male            Date Received: 08-Feb-2025
Ref. Surgeon: Dr. A. Mehta         Date Reported: 12-Feb-2025

CLINICAL HISTORY:
Lumpectomy for right breast lump. Clinically suspected fibroadenoma.

SPECIMEN:
Right breast lumpectomy specimen received in 10% neutral buffered
formalin.

GROSS DESCRIPTION:
Received a single irregular grey-white tissue piece measuring
3.5 x 2.5 x 2.0 cm. External surface irregular. Cut section shows
a firm grey-white area measuring 2.0 x 1.5 cm with irregular margins.
Rest of the tissue appears yellow and lobulated. Entire lesion
submitted for processing (5 cassettes, A1-A5).

MICROSCOPIC DESCRIPTION:
Sections show a tumor composed of infiltrating nests and cords of
malignant epithelial cells with moderate cytoplasm and pleomorphic
hyperchromatic nuclei. Tumor cells are arranged in tubular and
cribriform patterns. Mitotic activity is 8-10 per 10 hpf. Areas
of necrosis and calcification are present. Tumor infiltrates into
surrounding fibroadipose tissue. Surgical margins are free of tumor
(clearance > 5 mm). No lymphovascular invasion identified. Adjacent
breast tissue shows fibrocystic changes with apocrine metaplasia.

DIAGNOSIS:
Right breast lumpectomy:
Infiltrating Ductal Carcinoma - Not Otherwise Specified (NOS),
Histological Grade II (Modified Bloom-Richardson Score: 7/9:
Tubule formation 2, Nuclear pleomorphism 3, Mitotic count 2)

pTNM Staging: pT2 pN0 (sn) Mx
(Not assessed for nodal status — sentinel node biopsy separate)

IMMUNOHISTOCHEMISTRY:
Estrogen Receptor (ER): Positive (Allred Score: 7/8)
Progesterone Receptor (PR): Positive (Allred Score: 6/8)
HER2/neu: Negative (Score 1+)
Ki-67: 15% (low proliferative index)

COMMENTS:
Infiltrating ductal carcinoma, Grade II, ER/PR positive, HER2
negative. Luminal A molecular subtype. Favorable prognosis.
Recommend endocrine therapy consideration.

Dr. [Name], MD (Pathology)
Consultant Histopathologist
```

---

### Format 11: Radiology Report

**Where used:** Radiology departments in hospitals and diagnostic centres. X-ray, USG, CT, MRI reports. Descriptive text with impression.

**Sections:**
1. Header: Hospital/lab name, department (Radiology/Imaging)
2. Patient demographics: Name, age, gender, IP/OP number
3. Study details: Modality (X-ray/USG/CT/MRI), body part, date
4. Clinical indication: Reason for study
5. Technique: Modality details (e.g., "3T MRI with contrast")
6. Findings: Descriptive text by anatomical region
7. Impression: Concluding diagnosis/differential
8. Footer: Radiologist signature

**Differentiators:**
- Descriptive text (not tabular)
- Anatomical region-based findings (brain, chest, abdomen, etc.)
- Measurements included in text (e.g., "lesion measuring 2.3 x 1.8 cm")
- Impression section is the key field (1-5 lines)
- May reference prior imaging ("compared to previous CT dated...")
- Technical parameters mentioned (slice thickness, contrast, sequence)
- Radiologist may add recommendation for further imaging

**Layout style:** Letter-style report, justified paragraphs, bold section headers, no tables, Times New Roman 11pt.

**Example:**

```
DEPARTMENT OF RADIOLOGY & IMAGING
Fortis Hospital, Bannerghatta Road, Bengaluru - 560076

Radiology Report No: R/25/12890

Patient: SUNIL AGARWAL              OP No: OP-25-8821
Age / Gender: 47 / Male             Date: 15-Feb-2025
Ref. Doctor: Dr. P. Kumar (Neuro)   Modality: MRI

STUDY: MRI Brain with Contrast (Gadolinium)
CLINICAL INDICATION: Headaches for 3 months, occasional blurred vision.
TECHNIQUE: MRI performed on 1.5T scanner. Sequences: T1, T2, FLAIR,
DWI, SWI, pre and post-contrast T1 in axial, sagittal and coronal
planes. 15 mL Dotarem (Gadoteric acid) administered IV.

FINDINGS:
Brain parenchyma shows normal signal intensity in bilateral cerebral
and cerebellar hemispheres. No evidence of acute infarct or
hemorrhage. Diffusion restriction is not identified.

A well-defined extra-axial lesion is seen in the right frontal
parasagittal region, measuring approximately 2.8 x 2.3 x 2.1 cm.
The lesion appears isointense on T1 and slightly hypointense on T2
with homogeneous intense post-contrast enhancement. A dural tail
sign is noted. There is mass effect on the adjacent right frontal
lobe with minimal vasogenic edema. No midline shift. Ventricular
system is normal in size and configuration. Basal cisterns are
unremarkable.

Bilateral internal carotid arteries show normal flow void signals.
Visualized paranasal sinuses are clear. Orbits are unremarkable.

IMPRESSION:
Well-defined homogeneously enhancing extra-axial lesion in the right
frontal parasagittal region with dural tail sign — imaging features
are suggestive of meningioma.

No evidence of acute infarct, hemorrhage or mass effect requiring
urgent intervention.

Recommend: Neurosurgical consultation for further management.
Follow-up MRI in 6 months if conservative management planned.

Dr. [Name], MD (Radiology)
Consultant Radiologist
```

---

### Format 12: Health Checkup Package Report

**Where used:** Health checkup packages at hospitals and diagnostic chains (Apollo Whole Health, Thyrocare Aarogyam, Metropolis TruHealth). Multi-panel reports with summary page.

**Sections:**
1. Cover page: Package name, patient photo (sometimes), summary
2. Patient demographics: Name, age, gender, package code
3. Summary page: Overall health status, abnormal tests highlighted
4. Detailed results: Multiple panels (CBC, Biochem, Lipid, Thyroid, Vitamins, Urine)
5. ECG summary (if included)
6. TMT/Echo summary (if included)
7. USG abdomen summary (if included)
8. Physician consultation notes (if included)
9. Recommendations: Lifestyle, diet, follow-up
10. Footer: Medical officer signature

**Differentiators:**
- Multi-page report (3-5 pages typical)
- Summary page with color-coded status (green/amber/red)
- Combines lab + imaging + cardiac + physician notes
- "Health Score" or "Wellness Index" may be included
- Lifestyle/diet recommendations section
- Package branding (e.g., "Apollo Whole Health 360")
- Patient photo on cover page (OCR challenge)
- Often includes BMI, BP readings from physical exam

**Layout style:** Professional multi-page layout, color-coded summary page, detailed results in subsequent pages, branded cover page, Calibri 10pt.

**Example:**

```
APOLLO WHOLE HEALTH 360 — EXECUTIVE HEALTH CHECK
Apollo Hospitals, Jubilee Hills, Hyderabad - 500033

Patient: VENKATESH REDDY           Package: WH360-E
Age / Gender: 45 / Male            Date: 18-Feb-2025
UHID: APH-2024-0098234             Consultant: Dr. N. Rao

HEALTH SUMMARY
===========================================================================
Overall Status: ATTENTION REQUIRED
Tests Abnormal: 6 out of 42 parameters
===========================================================================

AREA                    STATUS      KEY FINDING
---------------------------------------------------------------------------
Hematology              NORMAL      CBC within normal limits
Diabetes                ATTENTION   HbA1c 6.1% (Pre-diabetes)
Lipid Profile           ATTENTION   LDL 138 mg/dL (Above target)
Thyroid                 NORMAL      TSH 2.1 µIU/mL
Kidney Function         NORMAL      Creatinine 0.9 mg/dL
Liver Function          NORMAL      All parameters normal
Vitamins                ATTENTION   Vitamin D 16 ng/mL (Deficient)
Cardiac (ECG)           NORMAL      Sinus rhythm, rate 72/min
Cardiac (TMT)           NORMAL      Negative for inducible ischemia
USG Abdomen             ATTENTION   Fatty liver (Grade I)
                        ATTENTION   Renal calculus 4mm (left)

DETAILED RESULTS — LABORATORY
===========================================================================

HEMOGRAM
Hemoglobin              15.2       g/dL       13.0 - 17.0
RBC Count               5.28       mill/cu.mm 4.5 - 6.0
WBC Count               7200       /cu.mm     4000 - 11000
Platelet Count          2.65       lakh/cu.mm 1.5 - 4.5
Neutrophils             60         %          40 - 75
Lymphocytes             32         %          20 - 45
Eosinophils             03         %          1 - 6
Monocytes               04         %          2 - 10
Basophils               01         %          0 - 2

DIABETES PANEL
Fasting Blood Sugar     108   H    mg/dL      70 - 100
HbA1c                   6.1   H    %          < 5.7
PP Blood Sugar          162   H    mg/dL      < 140

LIPID PROFILE
Total Cholesterol       195        mg/dL      < 200
Triglycerides           175   H    mg/dL      < 150
HDL Cholesterol         38    L    mg/dL      > 40
LDL Cholesterol         138   H    mg/dL      < 100
VLDL Cholesterol        35    H    mg/dL      < 30

THYROID PROFILE
TSH                     2.1        µIU/mL     0.4 - 4.2
Free T3                 3.2        pg/mL      2.3 - 4.2
Free T4                 1.2        ng/dL      0.8 - 1.8

KIDNEY FUNCTION
Urea                    26         mg/dL      15 - 40
Creatinine              0.9        mg/dL      0.6 - 1.2
Uric Acid               5.8        mg/dL      3.4 - 7.0
Sodium                  140        mmol/L     135 - 155
Potassium               4.3        mmol/L     3.5 - 5.5

LIVER FUNCTION
Bilirubin Total         0.6        mg/dL      0.2 - 1.2
SGPT (ALT)              28         U/L        7 - 56
SGOT (AST)              22         U/L        10 - 40
ALP                     82         U/L        44 - 147
Total Protein           7.0        g/dL       6.0 - 8.3
Albumin                 4.3        g/dL       3.5 - 5.0

VITAMINS
Vitamin D               16.0  L    ng/mL      20 - 50
Vitamin B12             385        pg/mL      200 - 900

URINE ROUTINE
Colour                  Pale Yellow
Appearance              Clear
pH                      6.0
Specific Gravity         1.020
Protein                 Nil
Sugar                   Nil
Pus Cells               1-2/hpf
RBC                     Nil

ECG: Sinus rhythm, rate 72/min, normal axis, no ST-T changes.
TMT: Exercise for 9.2 minutes (Bruce protocol). Achieved 96% of
     target heart rate. No chest pain. No significant ST changes.
     Negative for inducible ischemia.

USG ABDOMEN:
Liver: Enlarged (15.5 cm), increased echogenicity — Grade I fatty
       liver. No focal lesion.
Gallbladder: Well-distended, no calculi, wall thickness normal.
Pancreas: Normal in size and echogenicity.
Spleen: Normal (10.2 cm).
Kidneys: Right 10.1 cm, Left 10.5 cm. Cortical echogenicity normal.
         A 4 mm calculus in lower pole of left kidney. No
         hydronephrosis.
Bladder: Normal, no mass or calculus.

PHYSICIAN CONSULTATION:
Patient is a 45-year-old male, executive, with sedentary lifestyle.
BMI: 27.8 (overweight). BP: 138/88 mmHg. Pre-diabetic (HbA1c 6.1%),
dyslipidemia (high LDL, low HDL), Vitamin D deficiency, Grade I
fatty liver, small renal calculus.

RECOMMENDATIONS:
1. Lifestyle: 30 min brisk walk daily, target weight reduction 5 kg
2. Diet: Low carbohydrate, low fat. Reduce sugar and fried foods.
   Increase fiber, vegetables, fruits.
3. Vitamin D: Sachet 60,000 IU once weekly x 8 weeks, then monthly
4. Lipid: Repeat lipid profile in 3 months. Consider statin if
   lifestyle modification insufficient.
5. Diabetes: Repeat HbA1c in 3 months. Monitor blood sugar.
6. Fatty liver: USG repeat in 6 months. LFT monitoring.
7. Renal calculus: Increase fluid intake (3L/day). USG in 6 months.
8. Follow-up: Comprehensive review in 3 months.

Dr. [Name], MD (General Medicine)
Consultant Physician
Apollo Hospitals, Hyderabad
```

---

## Part B: Discharge Summary Formats (12)

### Format 1: NABH-Accredited Hospital (Standard Format)

**Where used:** NABH-accredited private hospitals (multi-specialty). Follows NABH mandated discharge summary structure.

**Sections:**
1. Header: Hospital name, NABH logo, patient demographics (UHID, IP number)
2. Admission details: Date of admission, date of discharge, LOS (length of stay)
3. Consulting doctor / treating team
4. Chief complaint
5. History of present illness (HPI)
6. Past history (medical, surgical, drug, allergy)
7. Personal history (smoking, alcohol, diet, sleep, bowel, bladder)
8. Family history
9. Examination findings (general, systemic)
10. Investigations (lab + imaging summary)
11. Diagnosis (primary + secondary + co-morbidities)
12. Procedures performed (if any)
13. Treatment summary (medications during stay)
14. Condition at discharge
15. Discharge medications (with dose, frequency, duration)
16. Advice on discharge (diet, activity, follow-up)
17. Review date
18. Footer: Treating consultant signature, NABH accreditation ID

**Differentiators:**
- Structured, comprehensive, follows NABH template
- All sections clearly headed and numbered
- Diagnosis coded (ICD-10 where applicable)
- Discharge medications in tabular format
- Follow-up date specified
- Condition at discharge explicitly stated
- NABH logo and accreditation number on header

**Layout style:** Professional hospital letterhead, structured numbered sections, discharge medications in bordered table, A4 portrait, Calibri 11pt.

**Example:**

```
KOKILABEN DHIRUBHAI AMBANI HOSPITAL
NABH Accredited (Hospital ID: NABH/H-2019-0234)
Andheri (W), Mumbai - 400053

DISCHARGE SUMMARY

Patient Name: SURESH BHATIA              UHID: KDA-2024-008912
IP No: IP-25-04567                       Age / Gender: 67 / Male
Date of Admission: 10-Feb-2025           Date of Discharge: 16-Feb-2025
Length of Stay: 6 days
Consultant: Dr. R. Sharma (Cardiology)

CHIEF COMPLAINT:
Chest pain and sweating for 2 hours.

HISTORY OF PRESENT ILLNESS:
Patient was apparently well 2 hours before admission when he
developed sudden onset retrosternal chest pain, compressive in
nature, radiating to left arm, associated with sweating and
palpitations. No breathlessness, no syncope. Brought to ER by
family. ECG showed ST elevation in leads II, III, aVF. Diagnosed
as acute inferior wall MI. Thrombolysed with Tenecteplase. Shifted
to CCU for monitoring. Coronary angiography done on day 2 showed
100% occlusion of right coronary artery (RCA). Primary PCI with
drug-eluting stent to RCA done. Patient stabilized over 6 days.

PAST HISTORY:
- Hypertension for 12 years (on Telmisartan 40mg OD)
- Type 2 Diabetes Mellitus for 8 years (on Metformin 500mg BD)
- Dyslipidemia for 5 years (on Rosuvastatin 10mg OD)
- No prior cardiac events
- No surgical history

PERSONAL HISTORY:
- Smoking: Non-smoker
- Alcohol: Occasional (once a month)
- Diet: Mixed diet, high in fried foods
- Sleep: 6-7 hours, disturbed
- Bowel/Bladder: Normal

FAMILY HISTORY:
Father had CAD, died at 72. Mother hypertensive. One sibling with
diabetes. No family history of premature CAD.

EXAMINATION ON ADMISSION:
General: Conscious, oriented, anxious. Pulse 96/min, regular.
         BP 150/90 mmHg. RR 22/min. SpO2 96% on room air.
         Pallor: mild. Icterus: nil. Edema: nil.
Systemic:
  CVS: S1 S2 normal, no murmur, no gallop
  RS: Bilateral vesicular breath sounds, no crepitations
  CNS: Conscious, oriented, no focal deficit
  P/A: Soft, non-tender, no organomegaly

INVESTIGATIONS:
Hemoglobin: 12.8 g/dL | WBC: 9800 /cu.mm | Platelets: 2.4 lakh/cu.mm
Troponin I: 8.5 ng/mL (H) | CK-MB: 85 U/L (H)
Total Cholesterol: 210 mg/dL | LDL: 142 mg/dL | HDL: 35 mg/dL
HbA1c: 7.8%
Creatinine: 1.1 mg/dL | Urea: 32 mg/dL
ECG: Acute inferior wall STEMI (ST elevation II, III, aVF,
     reciprocal depression in I, aVL)
Echo: LVEF 45%, hypokinesia of inferior wall, no clot, no PE.
CAG: 100% occlusion of mid RCA, 70% stenosis in LAD, 30% in LCX.
     Primary PCI to RCA with 3.0 x 24mm DES. TIMI 3 flow restored.

DIAGNOSIS:
Primary: Acute Inferior Wall ST-Elevation Myocardial Infarction
         (STEMI) — Post primary PCI to RCA with DES
Secondary: Coronary Artery Disease (Triple Vessel Disease)
Co-morbidities:
  - Hypertension (ICD-10: I10)
  - Type 2 Diabetes Mellitus (ICD-10: E11.9)
  - Dyslipidemia (ICD-10: E78.5)

PROCEDURES PERFORMED:
1. Coronary Angiography (10-Feb-2025)
2. Primary PCI with DES to RCA (10-Feb-2025)

TREATMENT SUMMARY DURING STAY:
- Loading dose: Aspirin 325mg, Ticagrelor 180mg, Atorvastatin 80mg
- Thrombolysis: Tenecteplase 35mg IV bolus
- Antiplatelet: Aspirin 150mg OD, Ticagrelor 90mg BD
- Anticoagulation: Enoxaparin 0.6mg SC BD (for 48h)
- Statin: Atorvastatin 80mg HS
- Beta-blocker: Metoprolol 25mg BD
- ACE inhibitor: Ramipril 2.5mg OD
- Anti-diabetic: Insulin (sliding scale), Metformin 500mg BD
- Antiemetic: Ondansetron 4mg IV PRN
- IV fluids: Normal saline as needed

CONDITION AT DISCHARGE:
Stable. Afebrile. Pulse 72/min, regular. BP 130/80 mmHg.
No chest pain. No breathlessness. Ambulating independently.

DISCHARGE MEDICATIONS:
+-----------------------------------------------------------------------+
| Medication            | Dose      | Frequency | Duration              |
+-----------------------------------------------------------------------+
| Aspirin               | 150 mg    | OD        | Lifelong              |
| Ticagrelor            | 90 mg     | BD        | 1 year                |
| Atorvastatin          | 80 mg     | HS        | Lifelong              |
| Metoprolol            | 25 mg     | BD        | Lifelong              |
| Ramipril              | 2.5 mg    | OD        | Lifelong              |
| Metformin             | 500 mg    | BD        | Continue              |
| Pantoprazole          | 40 mg     | OD        | 1 month               |
+-----------------------------------------------------------------------+

ADVICE ON DISCHARGE:
1. Diet: Low salt, low fat, diabetic diet. Avoid fried foods.
2. Activity: Gradual increase. No heavy lifting for 4 weeks.
   Cardiac rehabilitation after 4 weeks.
3. Avoid: Smoking, alcohol. Restrict caffeine.
4. Monitor: Blood pressure daily, blood sugar as advised.
5. Warning signs: Report immediately if chest pain, breathlessness,
   palpitations, syncope, or bleeding.

FOLLOW-UP:
- Cardiology OPD: 24-Feb-2025 (1 week)
- Repeat Echo: After 1 month
- Lipid profile: After 1 month
- HbA1c: After 3 months

Dr. R. Sharma, MD, DM (Cardiology)
Consultant Cardiologist
Kokilaben Dhirubhai Ambani Hospital
NABH/H-2019-0234
```

---

### Format 2: AIIMS / Government Medical College (Structured, Detailed)

**Where used:** AIIMS, JIPMER, PGI, government medical colleges. Structured academic format, detailed, teaching hospital style.

**Sections:**
1. Header: Hospital name (government), "Government of India" banner, department
2. Patient demographics: CR No (hospital registration), IP No, ward/bed
3. Admission details: Date/time of admission, discharge, LOS
4. Brought by (relative/police)
5. Chief complaint (with duration)
6. History of present illness (detailed, narrative)
7. Review of systems
8. Past history (medical/surgical/drug/allergy)
9. Personal history (with occupational details)
10. Menstrual/obstetric history (if female)
11. Family history
12. General examination (vitals + built, nourishment, etc.)
13. Systemic examination (CVS, RS, CNS, P/A — detailed)
14. Provisional diagnosis
15. Investigations (lab + imaging — detailed)
16. Final diagnosis
17. Treatment in hospital (day-by-day or summary)
18. Course in hospital
19. Condition at discharge
20. Discharge advice (medications + non-pharmacological)
21. Follow-up date and clinic
22. Footer: Senior resident + Professor signatures

**Differentiators:**
- Very detailed (2-4 pages typical)
- Academic teaching hospital format — includes provisional diagnosis
- Review of systems section (unique to teaching hospitals)
- Day-by-day treatment course (unique)
- Senior resident + Professor dual signature
- CR No (hospital registration number) used instead of UHID
- Government hospital banner
- No NABH logo (government hospitals may not be NABH accredited)
- ICD-10 coding may be present
- Social history detailed (occupation, socioeconomic status)

**Layout style:** Government hospital letterhead, dense text, minimal formatting, Times New Roman 11pt, A4 portrait, may be dot-matrix printed.

**Example:**

```
ALL INDIA INSTITUTE OF MEDICAL SCIENCES (AIIMS)
New Delhi - 110029 | Government of India

DEPARTMENT OF GENERAL MEDICINE

DISCHARGE SUMMARY

CR No: 2024-045872              IP No: 25-MED-3398
Name: GEETA KUMARI              Age / Gender: 38 / Female
Ward/Bed: 5A, Bed 14            Brought by: Husband
Date of Admission: 12-Feb-2025  Date of Discharge: 20-Feb-2025
Length of Stay: 8 days
Unit: Prof. [Name] Unit

CHIEF COMPLAINTS:
1. Fever for 10 days
2. Yellowish discoloration of eyes for 5 days
3. Abdominal pain for 3 days
4. Decreased urine output for 2 days

HISTORY OF PRESENT ILLNESS:
Patient was apparently well 10 days back when she developed
intermittent fever, high grade, not associated with chills/rigor,
initially relieved by paracetamol. Five days ago, family noticed
yellowish discoloration of eyes and dark-colored urine. Three days
ago, she developed dull aching pain in right upper abdomen, non-
radiating, not related to food intake. Two days ago, urine output
decreased to approximately 400 mL/day. No history of vomiting,
hematemesis, melena, altered sensorium, bleeding, rash, joint pain,
or breathlessness. No history of blood transfusion, IV drug abuse,
or high-risk behavior. Admitted for evaluation and management.

REVIEW OF SYSTEMS:
CNS: No headache, no seizures, no altered sensorium
CVS: No palpitations, no chest pain, no orthopnea
RS: No cough, no breathlessness
GIS: As per HPI. No constipation/diarrhea. No dysphagia
GUS: Decreased urine output as per HPI. No burning micturition
     Menstrual history: Regular cycles, LMP 2 weeks ago

PAST HISTORY:
- No history of diabetes, hypertension, TB, asthma
- No prior hospitalization
- No surgical history
- No known allergies
- Immunization: Hepatitis B — not vaccinated

PERSONAL HISTORY:
- Occupation: Housewife
- Diet: Vegetarian
- No smoking, no alcohol, no tobacco chewing
- Socioeconomic status: Lower middle class

OBSTETRIC HISTORY:
P3+0A0, all full-term normal deliveries, last child 8 years old.

FAMILY HISTORY:
Husband is alcoholic. No family history of liver disease.
No family history of diabetes, hypertension, or malignancy.

GENERAL EXAMINATION ON ADMISSION:
Conscious, oriented, moderately built, poorly nourished.
Temp: 100.2°F | Pulse: 108/min | BP: 100/60 mmHg | RR: 24/min
Pallor: ++ | Icterus: +++ | Clubbing: nil
Lymphadenopathy: nil | Edema: bilateral pitting, up to ankle
Spider naevi: present on upper chest | Palmar erythema: present
Flapping tremor: present

SYSTEMIC EXAMINATION:
CVS: S1 S2 normal, no murmur
RS: Bilateral vesicular breath sounds, basal crepitations
CNS: Conscious, oriented to time/place/person. No focal deficit.
     Asterixis present.
P/A: Inspection: Distended, visible veins
     Palpation: Liver palpable 4 cm below costal margin, tender,
                span 14 cm. Spleen palpable 2 cm. Shifting
                dullness present (ascites).
     Percussion: Dull in flanks

PROVISIONAL DIAGNOSIS:
Acute viral hepatitis with hepatic failure (? Hepatitis E)
with hepatorenal syndrome

INVESTIGATIONS:
CBC: Hb 9.2 g/dL, WBC 14200 /cu.mm (N 78), Platelets 1.2 lakh/cu.mm
LFT: Bilirubin Total 18.5 mg/dL, Direct 12.2 mg/dL
     SGPT 820 U/L, SGOT 1120 U/L, ALP 280 U/L
     Total Protein 5.8 g/dL, Albumin 2.4 g/dL
     PT 22 sec (Control 13), INR 2.1
RFT: Urea 88 mg/dL, Creatinine 2.8 mg/dL
     Na+ 132 mmol/L, K+ 5.2 mmol/L
Viral Markers:
     HBsAg: Negative
     Anti-HCV: Negative
     Anti-HEV IgM: Positive
     Anti-HAV IgM: Negative
USG Abdomen: Hepatomegaly with coarse echotexture, splenomegaly,
     moderate ascites, bilateral pleural effusion
Ascitic Fluid Analysis: Serum-ascites albumin gradient 2.1
     (consistent with portal hypertension), cell count 120/cu.mm
     (lymphocyte predominant), culture sterile

FINAL DIAGNOSIS:
Acute Liver Failure secondary to Hepatitis E virus infection
(ICD-10: B17.2) with Hepatorenal Syndrome (ICD-10: N17.8)
and Coagulopathy (ICD-10: D68.8)

TREATMENT IN HOSPITAL:
Day 1-8: IV fluids (DNS + RL), restricted as per urine output
Day 1-8: Injection Cefotaxime 1g IV BD (prophylaxis)
Day 1-8: Injection Vitamin K 10mg IV OD
Day 1-8: Injection Pantoprazole 40mg IV OD
Day 1-8: Injection Furosemide 20mg IV (as needed for edema)
Day 1-8: Lactulose 30mL TID (for hepatic encephalopathy)
Day 1-8: Rifaximin 550mg BD
Day 3-8: Norepinephrine infusion (for hepatorenal syndrome)
Day 5-8: Fresh Frozen Plasma 4 units (for coagulopathy)
Day 6-8: Albumin 20% 100mL OD (for hepatorenal syndrome)

COURSE IN HOSPITAL:
Day 1-3: Patient deteriorated — encephalopathy progressed from
  Grade I to Grade II, renal function worsened (creatinine 1.4 to
  2.8), INR increased to 2.1. Started on norepinephrine, albumin,
  and FFP.
Day 4-6: Gradual improvement. Encephalopathy resolved. Urine
  output improved to 800 mL/day. Bilirubin decreased from 22 to 15.
Day 7-8: Stable. Conscious, oriented. Bilirubin 12.5, Creatinine
  1.8, INR 1.6. Tolerating oral diet. Discharged on Day 8.

CONDITION AT DISCHARGE:
Conscious, oriented. Afebrile. Pulse 88/min, BP 110/70 mmHg.
Icterus ++. No encephalopathy. Tolerating oral diet. Urine output
  1200 mL/day.

DISCHARGE ADVICE:
Medications:
1. Tab Lactulose 30 mL TID — 2 weeks
2. Tab Rifaximin 550mg BD — 2 weeks
3. Tab Propranolol 20mg BD — lifelong (for portal hypertension)
4. Tab Spironolactone 50mg OD — review in 2 weeks
5. Tab Vitamin K 5mg OD — 2 weeks
6. Syrup Multivitamin 1 spoon OD — 1 month

Non-pharmacological:
1. Low salt, low protein diet (40g/day) initially, gradually increase
2. Avoid hepatotoxic drugs (paracetamol, NSAIDs)
3. Avoid alcohol (patient is non-alcoholic)
4. Adequate rest, gradual mobilization
5. Monitor urine output, weight daily

FOLLOW-UP:
Medicine OPD (Prof. [Name] Unit) on 06-Mar-2025
Repeat LFT, RFT, PT/INR before OPD visit
USG abdomen after 2 weeks

Senior Resident: Dr. [Name], MD (Medicine)
Professor: Dr. [Name], MD, DM (Gastroenterology)
Department of General Medicine, AIIMS New Delhi
```

---

### Format 3: Apollo Hospitals (Corporate Hospital)

**Where used:** Apollo Hospitals Group (corporate, multi-specialty). Standardized across Apollo hospitals. Integrated with Apollo EHR.

**Sections:**
1. Header: Apollo logo, hospital name, NABH + JCI accreditation
2. Patient banner: UHID, IP number, name, age, gender
3. Admission/discharge dates, LOS, consultant
4. Diagnosis (primary + co-morbidities) — at top, not bottom
5. Brief history
6. Examination findings
7. Investigations summary
8. Procedures
9. Treatment summary
10. Hospital course
11. Condition at discharge
12. Discharge medications (table)
13. Advice
14. Follow-up
15. Footer: Consultant signature

**Differentiators:**
- Diagnosis at TOP of summary (not bottom) — corporate style
- JCI accreditation alongside NABH
- UHID prominently displayed
- Concise format (1-2 pages) — corporate efficiency
- Discharge medications in clean table
- Apollo branding with blue/orange
- Integrated with EHR — may auto-populate from electronic records
- "Apollo" logo and branding throughout

**Layout style:** Professional corporate letterhead, blue header band, clean tables, Calibri 10pt, A4 portrait.

**Example:**

```
APOLLO HOSPITALS
Greams Road, Chennai - 600006
NABH Accredited | JCI Accredited

DISCHARGE SUMMARY

UHID: APH-2024-0091452          IP No: IP-25-4478
Patient: ARUN PRAKASH            Age / Gender: 55 / Male
Admitted: 14-Feb-2025            Discharged: 18-Feb-2025
LOS: 4 days                      Consultant: Dr. S. Krishnan
                                 (Gastroenterology)

DIAGNOSIS:
Primary: Acute Calculous Cholecystitis (ICD-10: K81.0)
Procedure: Laparoscopic Cholecystectomy (ICD-9-CM: 51.23)
Co-morbidities: Type 2 Diabetes Mellitus (E11.9),
                Hypertension (I10)

BRIEF HISTORY:
55-year-old male, known diabetic and hypertensive, presented with
right upper quadrant abdominal pain for 3 days, fever, and vomiting.
USG showed gallstones with thickened gallbladder wall. Admitted for
laparoscopic cholecystectomy.

EXAMINATION:
General: Conscious, afebrile on admission. Pulse 92/min, BP 140/90.
P/A: Right upper quadrant tenderness, positive Murphy's sign.
     No organomegaly.

INVESTIGATIONS:
WBC: 13400 /cu.mm (N 82) | Hb: 13.5 g/dL | Platelets: 2.8 lakh
LFT: Bilirubin 1.8 mg/dL, SGPT 85 U/L, ALP 180 U/L
RFT: Creatinine 0.9 mg/dL, Urea 28 mg/dL
FBS: 142 mg/dL, HbA1c: 7.2%
USG Abdomen: Multiple gallstones, GB wall 5mm thick, no CBD dilation

PROCEDURES:
Laparoscopic Cholecystectomy (15-Feb-2025) — uneventful.
Specimen sent for histopathology.

TREATMENT SUMMARY:
- IV antibiotics: Injection Ceftriaxone 1g IV BD (Day 1-4)
- Analgesia: Injection Tramadol 50mg IV TID (Day 1-2),
  then Tab Diclofenac 50mg BD (Day 3-4)
- Antiemetic: Injection Ondansetron 4mg IV PRN
- Insulin: Sliding scale (Day 1-3), then oral hypoglycemics
- DVT prophylaxis: Injection Enoxaparin 0.4mg SC OD
- IV fluids: Normal saline + Dextrose as needed

HOSPITAL COURSE:
Day 1: Admission, workup, antibiotic coverage, pain control.
Day 2: Laparoscopic cholecystectomy. Post-op recovery in ward.
Day 3: Tolerating oral liquids. Ambulating. Pain well controlled.
Day 4: Tolerating solid diet. Wound healthy. Discharged.

CONDITION AT DISCHARGE:
Stable. Afebrile. Tolerating oral diet. Wound healthy.
Discharged with advice.

DISCHARGE MEDICATIONS:
+-----------------------------------------------------------------------+
| Medication            | Dose      | Frequency | Duration              |
+-----------------------------------------------------------------------+
| Amoxicillin-Clav      | 625 mg    | TID        | 5 days               |
| Diclofenac            | 50 mg     | BD         | 3 days               |
| Pantoprazole          | 40 mg     | OD         | 2 weeks              |
| Metformin             | 500 mg    | BD         | Continue             |
| Glimepiride           | 2 mg      | OD         | Continue             |
| Telmisartan           | 40 mg     | OD         | Continue             |
| Rosuvastatin          | 10 mg     | OD         | Continue             |
+-----------------------------------------------------------------------+

ADVICE:
1. Wound care: Keep clean and dry. Suture removal after 7 days.
2. Diet: Low fat diet for 2 weeks, then normal diet.
3. Activity: No heavy lifting for 2 weeks. Gradual mobilization.
4. Monitor blood sugar regularly.
5. Report if: fever, wound discharge, severe abdominal pain, jaundice.

FOLLOW-UP:
Surgical Gastroenterology OPD on 25-Feb-2025 (1 week)
Histopathology report to be reviewed at follow-up.

Dr. S. Krishnan, MS, MCh (Surgical Gastroenterology)
Consultant, Apollo Hospitals, Chennai
NABH | JCI Accredited
```

---

### Format 4: Government District Hospital (Basic, Minimal)

**Where used:** District hospitals, sub-divisional hospitals, CHCs. Minimal format, often handwritten or typed on typewriter. Free treatment.

**Sections:**
1. Header: Hospital name (government), district
2. Patient: Name, age, gender, IP number
3. Admission/discharge dates
4. Diagnosis (1-2 lines)
5. Treatment given (brief)
6. Discharge medications (brief list)
7. Follow-up date
8. Footer: Medical officer signature

**Differentiators:**
- Very brief (half page to 1 page)
- No detailed history/examination
- Diagnosis in 1-2 lines
- Treatment in 2-3 lines
- Medications as simple list (no table)
- May be handwritten
- Government hospital stamp
- No NABH/JCI accreditation
- Often in regional language + English
- No structured sections — free text

**Layout style:** Plain text on government letterhead, no tables, no formatting, may be handwritten, A5 or A4.

**Example:**

```
DISTRICT HOSPITAL, [TOWN NAME]
[District], [State]

DISCHARGE CARD

Name: RAMULU              Age: 48 / Male
IP No: 2025/3398          Bed: 7, Male Ward
Admitted: 16-Feb-2025     Discharged: 19-Feb-2025

Diagnosis: Right lower lobe pneumonia with pleural effusion

Treatment given:
- IV antibiotics (Ceftriaxone) for 3 days
- Oral antibiotics (Amoxicillin) for 1 day
- Antipyretics (Paracetamol)
- IV fluids
- Oxygen support (Day 1)
- Chest physiotherapy

Condition at discharge: Improved. Afebrile. No breathlessness.

Discharge medicines:
1. Tab Amoxicillin 500mg TID x 5 days
2. Tab Paracetamol 500mg PRN for fever
3. Tab Pantoprazole 40mg OD x 1 week
4. Cough syrup 1 spoon TID x 5 days

Advice:
- Take medicines regularly
- Come to OPD after 1 week
- Chest X-ray to be repeated after 2 weeks
- If breathlessness or fever comes back, come immediately

Review: 26-Feb-2025 (Medicine OPD)

[Medical Officer Signature]
[Government District Hospital Stamp]
```

---

### Format 5: Nursing Home (Small Private, Brief)

**Where used:** Small private nursing homes (10-50 beds). General practitioner or general surgeon run. Brief, informal format.

**Sections:**
1. Header: Nursing home name, address, phone
2. Patient: Name, age, gender
3. Admission/discharge dates
4. Procedure (if surgical)
5. Diagnosis
6. Treatment
7. Discharge medications
8. Advice
9. Footer: Doctor signature

**Differentiators:**
- Very brief (half page)
- No structured sections — letter format
- Doctor's personal letterhead
- No NABH accreditation
- Medications as simple list
- May include doctor's personal phone number
- Informal tone
- Often printed on dot-matrix or inkjet
- Nursing home stamp

**Layout style:** Personal letterhead, free text, no tables, A5 or A4, informal.

**Example:**

```
SRI LAKSHMI NURSING HOME
[Street], [Town] - 560XXX
Ph: 080-26XXXXXX | Mob: 9845XXXXX

Discharge Summary

Patient: LAKSHMI          Age: 28 / Female
Admitted: 18-Feb-2025     Discharged: 20-Feb-2025

Diagnosis: Normal delivery (Full term vaginal delivery)
           Female baby, 2.8 kg

Procedure: Episiotomy and forceps delivery

Treatment during stay:
- IV fluids
- Injection Oxytocin for labor augmentation
- Episiotomy repair under local anesthesia
- Antibiotics (Injection Cefotaxime)
- Analgesics
- Iron and calcium supplements

Discharge medicines:
1. Tab Amoxicillin 500mg TID x 5 days
2. Tab Ibuprofen 400mg TID x 3 days
3. Tab Iron + Folic acid OD x 3 months
4. Tab Calcium OD x 3 months
5. Syrup Vitamin drops for baby

Advice:
- Breastfeed exclusively for 6 months
- Keep episiotomy site clean
- Perineal exercises
- Avoid heavy work for 6 weeks
- Immunization: BCG, OPV-0, Hep-B at birth (done)
- Next immunization: 6 weeks (Pentavalent, OPV-1, Rota-1)

Review: 04-Mar-2025 (2 weeks) — for episiotomy suture removal
        and baby check-up

Dr. [Name], MBBS, MS (OBG)
Sri Lakshmi Nursing Home
[Nursing Home Stamp]
```

---

### Format 6: Tertiary Care Centre (Specialty, Detailed)

**Where used:** Tertiary care specialty hospitals (cardiac, neuro, oncology, transplant). Detailed, specialty-specific format.

**Sections:**
1. Header: Hospital name, specialty department, NABH
2. Patient demographics: UHID, IP number
3. Admission/discharge dates, LOS
4. Consultant + team
5. Referring diagnosis
6. Detailed history (specialty-specific)
7. Examination (specialty-specific detailed)
8. Investigations (specialty-specific panels)
9. Final diagnosis (specialty-specific)
10. Procedures/interventions (detailed)
11. Treatment course (day-by-day for complex cases)
12. Complications (if any)
13. Condition at discharge
14. Discharge medications (specialty-specific)
15. Specialty-specific advice
16. Follow-up plan (detailed)
17. Footer: Consultant + fellow signatures

**Differentiators:**
- Specialty-specific sections (e.g., cardiac: echo details, cath report; neuro: GCS, neurological exam)
- Very detailed (3-5 pages)
- Day-by-day treatment course for complex cases
- Complications section explicitly listed
- Multi-disciplinary team mentioned
- Procedure details (e.g., stent size, valve type, graft details)
- Follow-up plan with specific investigations
- Fellow/senior resident co-signature

**Layout style:** Professional hospital letterhead, detailed structured sections, tables for medications and investigations, A4 portrait, Calibri 10pt.

**Example:**

```
NARAYANA HEALTH — CARDIAC SCIENCES
NABH Accredited | NH Health City, Bengaluru - 560099

DISCHARGE SUMMARY — CARDIOLOGY

UHID: NH-2024-0078451          IP No: IP-25-8821
Patient: PRAKASH MENON         Age / Gender: 61 / Male
Admitted: 20-Feb-2025          Discharged: 27-Feb-2025
LOS: 7 days
Consultant: Dr. C.N. Manjunath  Team: Dr. [Name] (Fellow)

REFERRING DIAGNOSIS:
Severe aortic stenosis with LV dysfunction — for aortic valve
replacement.

HISTORY:
61-year-old male, known hypertensive, presented with progressive
exertional dyspnea (NYHA Class III) for 6 months, two episodes of
presyncope in last month. No chest pain, no palpitations, no
orthopnea, no PND. Evaluated as outpatient — Echo showed severe
aortic stenosis (AVA 0.7 cm², mean gradient 48 mmHg, LVEF 40%).
Advised surgical aortic valve replacement.

EXAMINATION:
General: Conscious, oriented. Pulse 78/min, irregular (AF).
         BP 140/80 mmHg. JVP not raised.
CVS: Ejection systolic murmur at aortic area, radiating to carotids,
     grade 4/6. S2 soft. No diastolic murmur.
RS: Bilateral vesicular breath sounds, no crepitations.
P/A: Soft, non-tender, no organomegaly.

INVESTIGATIONS:
CBC: Hb 12.1 g/dL, WBC 7800, Platelets 2.6 lakh
RFT: Creatinine 1.0 mg/dL, Urea 30 mg/dL
LFT: Normal
Coagulation: PT 13.2 sec, INR 1.1
Echo (Pre-op):
  LVEF: 40% (Simpson's)
  Aortic valve: Calcified, severely stenotic
  AVA: 0.7 cm² | Mean gradient: 48 mmHg | Peak gradient: 72 mmHg
  Mitral valve: Mild MR
  LA: 42 mm | LV ESD 42 mm | LV EDD 56 mm
  No clot, no pericardial effusion
Coronary Angiography:
  LAD: 30% stenosis | LCX: normal | RCA: 20% stenosis
  No significant CAD. Mild disease only.

FINAL DIAGNOSIS:
1. Severe Calcific Aortic Stenosis (ICD-10: I35.0)
   with LV systolic dysfunction (LVEF 40%)
2. Atrial Fibrillation (ICD-10: I48)
3. Systemic Hypertension (ICD-10: I10)
4. Mild Coronary Artery Disease (ICD-10: I25.10)

PROCEDURE:
Elective Surgical Aortic Valve Replacement (22-Feb-2025)
- Valve: 23mm St. Jude Mechanical Valve (Regent)
- Technique: Median sternotomy, CPB, aortic cross-clamp
- Cross-clamp time: 78 minutes | CPB time: 112 minutes
- Intra-op TEE: Valve functioning well, no paravalvular leak
- Procedure uneventful

TREATMENT COURSE:
Day 1 (20-Feb): Admission, workup, pre-anesthesia evaluation
Day 2 (21-Feb): Pre-op optimization. Started on amiodarone for AF
Day 3 (22-Feb): SAVR. Post-op shifted to CVTS ICU, intubated,
                on inotropes (noradrenaline 0.05 mcg/kg/min),
                sedated. Chest tubes 2, pacing wires in situ.
Day 4 (23-Feb): Extubated. Inotropes weaned. Chest tubes removed.
                Shifted to step-down. Started oral feeds.
Day 5 (24-Feb): Transferred to ward. Ambulating. Echo: LVEF 45%,
                valve well seated, mean gradient 8 mmHg.
Day 6 (25-Feb): Progressive ambulation. NSR maintained on amiodarone.
Day 7 (27-Feb): Stable. Discharged.

COMPLICATIONS:
- Post-op atrial fibrillation (managed with amiodarone, reverted
  to sinus rhythm on Day 5)
- No other complications

CONDITION AT DISCHARGE:
Stable. Conscious, oriented. NSR. Pulse 72/min. BP 130/80.
Afebrile. Wound healthy. Ambulating independently. Tolerating
oral diet.

DISCHARGE MEDICATIONS:
+-----------------------------------------------------------------------+
| Medication            | Dose      | Frequency | Duration              |
+-----------------------------------------------------------------------+
| Warfarin              | 5 mg      | OD (6PM)  | Lifelong              |
| Aspirin               | 75 mg     | OD        | 3 months              |
| Metoprolol            | 25 mg     | BD        | Lifelong              |
| Amiodarone            | 200 mg    | OD        | 3 months              |
| Ramipril              | 2.5 mg    | OD        | Lifelong              |
| Atorvastatin          | 40 mg     | HS        | Lifelong              |
| Pantoprazole          | 40 mg     | OD        | 1 month               |
+-----------------------------------------------------------------------+

ADVICE:
1. Warfarin: STRICT compliance. INR target 2.5-3.5 (mechanical
   valve). Check INR twice weekly for 2 weeks, then weekly, then
   monthly. Adjust dose as per INR.
2. Diet: Avoid vitamin K-rich foods (spinach, broccoli, cabbage)
   in large quantities. Maintain consistent intake.
3. Activity: Gradual increase. Cardiac rehab after 6 weeks.
   No driving for 4 weeks. No heavy lifting for 8 weeks.
4. Wound care: Keep clean. Suture removal after 10 days.
5. Dental prophylaxis: Required before any dental procedure
   (lifelong — mechanical valve).
6. Warning signs: Bleeding, chest pain, breathlessness, syncope,
   fever, wound discharge — report immediately.

FOLLOW-UP:
- CVTS OPD: 06-Mar-2025 (1 week) — wound check, suture removal
- Cardiology OPD: 13-Mar-2025 (2 weeks) — INR review, Echo
- INR check: 28-Feb-2025, 02-Mar-2025, 05-Mar-2025
- Echo: After 1 month, then 6 months, then yearly
- Lifelong cardiac follow-up

Dr. C.N. Manjunath, MS, MCh (CVTS)
Dr. [Name], DNB (Cardiology) — Fellow
Narayana Health, Bengaluru
NABH Accredited
```

---

### Format 7: Maternity Hospital Discharge

**Where used:** Maternity hospitals, OBG departments. Post-natal discharge after normal delivery or C-section.

**Sections:**
1. Header: Hospital name, OBG department
2. Patient demographics: Name, age, IP number
3. Obstetric details: Gravida/Para, LMP, EDD, mode of delivery
4. Baby details: Weight, gender, APGAR, immunization status
5. Delivery details: Date/time, mode, complications
6. Post-natal course
7. Condition at discharge (mother + baby)
8. Discharge medications (mother + baby)
9. Post-natal advice
10. Family planning advice
11. Immunization schedule
12. Follow-up dates
13. Footer: Obstetrician signature

**Differentiators:**
- Baby details included alongside mother
- Obstetric terminology (Gravida, Para, LMP, EDD, APGAR)
- Immunization schedule for baby
- Family planning advice section
- Post-natal care instructions (breastfeeding, perineal/abdominal care)
- Two follow-up dates (mother + baby)
- Baby weight and feeding details

**Layout style:** Hospital letterhead, structured sections, baby and mother details side by side, A4 portrait.

**Example:**

```
CLOUDNINE HOSPITAL — MATERNITY
Old Airport Road, Bengaluru - 560017

POST-NATAL DISCHARGE SUMMARY

Mother: DEEPIKA RAGHU        Age: 29 / Female
IP No: IP-25-2298            UHID: C9-2024-004512
Admitted: 24-Feb-2025        Discharged: 27-Feb-2025
Consultant: Dr. [Name] (OBG)

OBSTETRIC DETAILS:
Gravida 2 Para 1+0+0+1      LMP: 17-May-2024
EDD: 21-Feb-2025            Gestation: 40 weeks + 3 days
Mode of Delivery: LSCS (Repeat)
Indication: Previous LSCS

BABY DETAILS:
Gender: Male                Weight: 3.1 kg
APGAR: 8 (1 min), 9 (5 min) Cry: Good
Breastfeeding: Established   Jaundice: Nil
Immunization at birth: BCG, OPV-0, Hep-B (given)

DELIVERY DETAILS:
Elective repeat LSCS done on 24-Feb-2025 under spinal anesthesia.
Intra-op: Clear liquor, baby cried immediately, placenta delivered
complete. Uterine closure done. Hemostasis secured. Blood loss:
~400 mL. Procedure uneventful.

POST-NATAL COURSE:
Day 1: Post-op recovery. IV fluids, antibiotics, analgesics.
       Catheter removed. Breastfeeding initiated.
Day 2: Tolerating oral diet. Ambulating. Baby feeding well.
Day 3: Wound healthy. Stitches intact. Baby active.
Day 4: Stable. Discharged.

CONDITION AT DISCHARGE:
Mother: Stable. Afebrile. Wound healthy. Lochia normal.
        Breastfeeding established. Ambulating.
Baby: Active, feeding well. No jaundice. Weight 2.95 kg.

DISCHARGE MEDICATIONS — MOTHER:
1. Tab Amoxicillin-Clav 625mg BD x 5 days
2. Tab Diclofenac 50mg BD x 5 days
3. Tab Iron + Folic acid OD x 3 months
4. Tab Calcium 500mg BD x 3 months
5. Tab Pantoprazole 40mg OD x 2 weeks
6. Syrup Lactulose 15mL HS x 1 week

DISCHARGE MEDICATIONS — BABY:
1. Syrup Vitamin D3 400 IU OD (1 drop) — daily for 1 year
2. Nothing else required at present

POST-NATAL ADVICE:
1. Breastfeeding: Exclusive for 6 months. Feed on demand.
   Proper latching technique. Both breasts each feed.
2. Wound care: Keep clean and dry. No bath for 7 days.
   Suture removal after 7 days.
3. Diet: High protein, high iron. Continue calcium and iron.
   Adequate fluids (3L/day).
4. Activity: Gradual mobilization. No heavy lifting for 6 weeks.
   No intercourse for 6 weeks. Pelvic floor exercises.
5. Baby care: Cord care (keep dry, clean with spirit).
   Bath after cord falls off (7-10 days).

FAMILY PLANNING:
Lactational amenorrhea method (LAM) effective for 6 months if
exclusive breastfeeding and no menses. Discuss contraception at
6-week follow-up. Options: IUCD, OCP, barrier methods.

IMMUNIZATION SCHEDULE FOR BABY:
Birth: BCG, OPV-0, Hep-B (DONE)
6 weeks: Pentavalent (DPT+HepB+Hib), OPV-1, IPV-1, Rota-1, PCV-1
10 weeks: Pentavalent-2, OPV-2, IPV-2, Rota-2, PCV-2
14 weeks: Pentavalent-3, OPV-3, IPV-3, Rota-3, PCV-3
9 months: MR (Measles-Rubella), JE, PCV booster
15-18 months: DPT booster, OPV booster, MR-2
2 years: Typhoid

FOLLOW-UP:
Mother: 06-Mar-2025 (10 days) — suture removal, wound check
        10-Apr-2025 (6 weeks) — post-natal check, family planning
Baby: 06-Mar-2025 (10 days) — weight, jaundice, feeding check
      10-Apr-2025 (6 weeks) — first immunization

Dr. [Name], MS (OBG)
Consultant Obstetrician
Cloudnine Hospital, Bengaluru
```

---

### Format 8: Cardiac Hospital Discharge

**Where used:** Cardiac specialty hospitals (Fortis Escorts, Manipal Heart Institute, Narayana Hrudayalaya). Post-cardiac procedure discharge.

**Sections:**
1. Header: Hospital name, cardiology department
2. Patient demographics
3. Admission/discharge dates, LOS
4. Cardiac diagnosis (detailed)
5. Procedure details (PCI/CABG/valve — with device details)
6. Pre-procedure workup
7. Procedure note (cath report / surgical note)
8. Post-procedure course
9. Complications
10. Echo summary
11. Discharge medications (cardiac-specific)
12. Cardiac rehab advice
13. Follow-up plan (with specific investigations)
14. Footer: Cardiologist signature

**Differentiators:**
- Detailed cardiac procedure note (stent type, size, location)
- Echo findings included in discharge summary
- Cardiac rehab plan
- Antiplatelet duration specified (DAPT)
- INR monitoring plan (if mechanical valve)
- Cardiac risk factor modification advice
- Specific follow-up investigations (echo, stress test)

**Layout style:** Cardiac hospital letterhead, structured sections, procedure details in semi-tabular format, A4 portrait.

**Example:**

```
FORTIS ESCORTS HEART INSTITUTE
NABH Accredited | Okhla Road, New Delhi - 110025

CARDIOLOGY DISCHARGE SUMMARY

UHID: FEHI-2024-006712        IP No: IP-25-3390
Patient: HARPREET SINGH       Age / Gender: 58 / Male
Admitted: 01-Mar-2025         Discharged: 04-Mar-2025
LOS: 3 days
Consultant: Dr. [Name] (Interventional Cardiology)

DIAGNOSIS:
1. Chronic Stable Angina (CCS Class III) (ICD-10: I20.8)
2. Coronary Artery Disease — Double Vessel Disease
3. Type 2 Diabetes Mellitus (E11.9)
4. Hypertension (I10)
5. Dyslipidemia (E78.5)

PROCEDURE:
Coronary Angiography + PCI to LAD (02-Mar-2025)

PRE-PROCEDURE WORKUP:
CBC: Hb 13.8, WBC 7600, Platelets 2.5 lakh
RFT: Creatinine 0.9, Urea 26
Coagulation: PT 12.8, INR 1.0
ECG: Normal sinus rhythm, rate 74/min, T wave inversion in V1-V3
Echo: LVEF 55%, mild hypokinesia of anterior wall, no clot,
      no pericardial effusion, no significant valvular lesion

CORONARY ANGIOGRAPHY:
LAD: 90% stenosis in mid segment, TIMI 2 flow
LCX: 30% stenosis in proximal segment
RCA: 20% stenosis, dominant
Left Main: Normal
LV: LVEF 55%, anterior hypokinesia

PCI DETAILS:
Access: Right Radial (6Fr sheath)
Catheter: JL 3.5, JR 4
Guidewire: Sion Blue (0.014")
Balloon: 2.5 x 15mm (pre-dilatation at 10 atm)
Stent: 3.0 x 24mm Drug-Eluting Stent (Xience Prime) to mid LAD
       deployed at 14 atm
Post-dilatation: 3.5 x 8mm NC balloon at 16 atm
Result: 0% residual stenosis, TIMI 3 flow, no dissection,
        no distal embolization
Contrast volume: 80 mL | Fluoroscopy time: 7.2 minutes

POST-PROCEDURE COURSE:
Day 1 (01-Mar): Admission, workup, pre-procedure preparation.
                Loading: Aspirin 325mg, Ticagrelor 180mg.
Day 2 (02-Mar): CAG + PCI to LAD. Uneventful. Sheath removed.
                Monitoring in CCU. No chest pain.
Day 3 (03-Mar): Shifted to ward. Ambulating. Tolerating oral diet.
                Echo: LVEF 55%, stent well placed.
Day 4 (04-Mar): Stable. Discharged.

COMPLICATIONS: None

ECHO SUMMARY:
LVEF: 55% (Simpson's)
Anterior wall: Mild hypokinesia (improved from pre-procedure)
Valves: Normal
No clot, no pericardial effusion

DISCHARGE MEDICATIONS:
+-----------------------------------------------------------------------+
| Medication            | Dose      | Frequency | Duration              |
+-----------------------------------------------------------------------+
| Aspirin               | 75 mg     | OD        | Lifelong              |
| Ticagrelor            | 90 mg     | BD        | 1 year (DAPT)         |
| Atorvastatin          | 80 mg     | HS        | Lifelong              |
| Metoprolol            | 25 mg     | BD        | Lifelong              |
| Ramipril              | 5 mg      | OD        | Lifelong              |
| Metformin             | 500 mg    | BD        | Continue              |
| Glimepiride           | 2 mg      | OD        | Continue              |
| Pantoprazole          | 40 mg     | OD        | 1 month               |
+-----------------------------------------------------------------------+

CARDIAC REHAB ADVICE:
1. Medications: STRICT compliance. Do not stop dual antiplatelet
   therapy (Aspirin + Ticagrelor) for 1 year — risk of stent
   thrombosis.
2. Statin: Continue even if cholesterol is normal — stabilizes
   plaque.
3. Diet: Low fat, low salt, diabetic diet. Mediterranean diet
   preferred. Avoid fried foods, red meat.
4. Exercise: Gradual cardiac rehab program after 1 week.
   Start with 15 min walk, increase to 45 min daily.
   Target: 150 min/week moderate exercise.
5. Risk factors: Stop smoking (if applicable). Control BP
   (<130/80), blood sugar (HbA1c <7), LDL (<70).
6. Warning signs: Chest pain, breathlessness, palpitations,
   syncope — report to ER immediately.

FOLLOW-UP:
- Cardiology OPD: 11-Mar-2025 (1 week)
- Echo: After 1 month
- TMT: After 3 months
- Lipid profile, HbA1c: After 1 month
- Coronary angiography: Only if symptoms recur

Dr. [Name], MD, DM (Cardiology)
Interventional Cardiologist
Fortis Escorts Heart Institute, New Delhi
NABH Accredited
```

---

### Format 9: Oncology Hospital Discharge

**Where used:** Cancer specialty hospitals (Tata Memorial, HCG, Apollo Cancer Institute). Post-chemotherapy/surgery/radiation discharge.

**Sections:**
1. Header: Hospital name, oncology department
2. Patient demographics
3. Admission/discharge dates, LOS
4. Oncology diagnosis (with staging)
5. Treatment intent (curative/palliative)
6. Current cycle/phase of treatment
7. Treatment administered (chemo regimen with doses)
8. Toxicity summary (hematologic, GI, etc.)
9. Supportive care given
10. Condition at discharge
11. Discharge medications (antiemetics, growth factors, etc.)
12. Precautions (neutropenic precautions)
13. Next cycle date
14. Follow-up plan
15. Footer: Oncologist signature

**Differentiators:**
- Cancer staging (TNM) prominently displayed
- Chemotherapy regimen name and cycle number
- Drug doses per BSA (body surface area)
- Toxicity grading (CTCAE)
- Neutropenic precautions
- Next cycle date explicitly stated
- Treatment intent (curative vs palliative)
- Port/PICC line care instructions

**Layout style:** Oncology hospital letterhead, structured sections, chemo regimen in table, A4 portrait.

**Example:**

```
TATA MEMORIAL HOSPITAL
Department of Medical Oncology
Parel, Mumbai - 400012

DISCHARGE SUMMARY — ONCOLOGY

CR No: TMH-2024-045678        IP No: 25-MO-882
Patient: FATEMA BEGUM         Age / Gender: 48 / Female
Admitted: 03-Mar-2025         Discharged: 06-Mar-2025
LOS: 3 days
Consultant: Dr. [Name] (Medical Oncology)

DIAGNOSIS:
Carcinoma Left Breast — pT2 pN1 M0 (Stage IIA)
ER Positive, PR Positive, HER2 Negative
Post-surgery (MRM done 15-Jan-2025)
Adjuvant Chemotherapy — Cycle 2 of 4

TREATMENT INTENT: Curative (Adjuvant)

CHEMOTHERAPY REGIMEN: AC (Doxorubicin + Cyclophosphamide)
Cycle: 2 of 4 (Q3 weekly)

DOSE CALCULATION:
BSA: 1.62 m²
Doxorubicin: 60 mg/m² = 97 mg IV
Cyclophosphamide: 600 mg/m² = 972 mg IV

CHEMOTHERAPY ADMINISTERED:
Date: 04-Mar-2025
- Pre-medication: Ondansetron 8mg IV, Dexamethasone 8mg IV,
  Ranitidine 50mg IV, Phenergan 12.5mg IV
- Doxorubicin 97mg IV bolus (via chemoport) at 10:30 AM
- Cyclophosphamide 972mg IV in 250mL NS over 30 min at 11:00 AM
- Hydration: 1L NS over 2 hours post-chemo
- Tolerated well. No immediate hypersensitivity reaction.

TOXICITY SUMMARY (CTCAE v5.0):
Hematologic: WBC 4.2 (Grade 1), Hb 10.8 (Grade 1), Platelets 220 (Grade 0)
GI: Mild nausea Day 1 (Grade 1), controlled with ondansetron
   No vomiting, no mucositis, no diarrhea
Other: No alopecia yet (expected after cycle 2-3)
       No fatigue, no neuropathy

SUPPORTIVE CARE GIVEN:
- G-CSF (Pegfilgrastim 6mg SC) — to be given on Day 2 (05-Mar)
- Antiemetics: Ondansetron + Dexamethasone + Aprepitant
- Mouth care: Chlorhexidine gargles
- Tab Iron + Folic acid (for anemia)

CONDITION AT DISCHARGE:
Stable. Afebrile. No nausea/vomiting. Tolerating oral diet.
WBC 4.2, Hb 10.8, Platelets 220. Chemoport patent.

DISCHARGE MEDICATIONS:
1. Tab Ondansetron 8mg TID PRN (for nausea) x 5 days
2. Tab Domperidone 10mg TID PRN x 5 days
3. Tab Loperamide 2mg PRN (for diarrhea)
4. Tab Paracetamol 500mg PRN (for fever) — BUT if fever >100.4°F,
   report to emergency IMMEDIATELY (neutropenic fever)
5. Syrup Chlorhexidine gargles 10mL TID x 7 days
6. Tab Iron + Folic acid OD x 1 month
7. Tab Calcium + Vitamin D OD x 1 month
8. Inj Pegfilgrastim 6mg SC — to be taken on 05-Mar-2025 (Day 2)
   at local clinic/hospital

NEUTROPENIC PRECAUTIONS:
1. Avoid crowds, sick people, raw foods (salads, fruits with skin
   removed, uncooked eggs/meat)
2. Hand hygiene: frequent hand washing
3. If fever >100.4°F (38°C): Report to Tata Memorial Emergency
   IMMEDIATELY. Do not take paracetamol and wait. Neutropenic
   fever is a medical emergency.
4. Watch for: bleeding, unusual bruising, mouth ulcers, diarrhea,
   burning urination, cough, breathlessness.
5. Chemoport care: Keep dry. No heavy lifting on that side.
   Flush every 4 weeks if not in use.

NEXT CYCLE:
Cycle 3 of 4 (AC): 25-Mar-2025
- CBC before next cycle: WBC >3000, Platelets >100,000 required
- If counts low, cycle may be delayed by 1 week
- After 4 cycles of AC: Switch to Paclitaxel (4 cycles) or
  start hormone therapy (Tamoxifen/Aromatase inhibitor)

FOLLOW-UP:
- Medical Oncology OPD: 10-Mar-2025 (Day 7) — CBC check
- CBC: Twice weekly (Mon/Thu) at local lab
- Medical Oncology OPD: 24-Mar-2025 — pre-cycle assessment
- Admission for Cycle 3: 25-Mar-2025

Dr. [Name], MD, DM (Medical Oncology)
Tata Memorial Hospital, Mumbai
```

---

### Format 10: Pediatric Hospital Discharge

**Where used:** Pediatric specialty hospitals, pediatric wards. Child discharge with parent instructions.

**Sections:**
1. Header: Hospital name, pediatrics department
2. Patient demographics: Child name, age, gender, weight
3. Parent/guardian name
4. Admission/discharge dates, LOS
5. Immunization status
6. History (from parent)
7. Examination findings (pediatric-specific)
8. Investigations
9. Diagnosis
10. Treatment given
11. Condition at discharge
12. Discharge medications (weight-based dosing)
13. Parent advice (home care, feeding, warning signs)
14. Follow-up
15. Footer: Pediatrician signature

**Differentiators:**
- Weight-based medication dosing (mg/kg)
- Immunization status checked
- Parent/guardian name (not just patient)
- Feeding advice (breast/formula/solid based on age)
- Developmental milestones mentioned
- Warning signs explained for parents
- Pediatric-specific dosing (syrups, drops)

**Layout style:** Pediatric hospital letterhead, child-friendly formatting, weight-based dosing in table, A4 portrait.

**Example:**

```
RAINBOW CHILDREN'S HOSPITAL
Pediatrics Department
Marathahalli, Bengaluru - 560037

PEDIATRIC DISCHARGE SUMMARY

Patient: AARAV REDDY            Age: 2 years 3 months
Weight: 11.5 kg                 Gender: Male
Parent: [Father's Name]         UHID: RCH-2024-003389
IP No: IP-25-067                Bed: 4, Pediatric Ward
Admitted: 05-Mar-2025           Discharged: 08-Mar-2025
LOS: 3 days
Consultant: Dr. [Name] (Pediatrics)

IMMUNIZATION STATUS: Up to date (as per IAP schedule)
BCG, OPV-0/1/2/3, Pentavalent-1/2/3, MR-1, PCV-1/2/3, Rota-1/2/3
Next due: MR-2 + DPT booster at 18 months (overdue — advise)

CHIEF COMPLAINT (per parent):
Fever for 4 days, fast breathing for 2 days, not feeding well.

HISTORY:
2-year-old boy, previously healthy, developed fever 4 days ago
(max 102°F), treated with paracetamol at home. 2 days ago, parents
noticed fast breathing and reduced oral intake. No cough, no
vomiting, no diarrhea, no seizures, no rash. Admitted for
evaluation and management.

EXAMINATION ON ADMISSION:
General: Conscious, irritable. Temp 101°F. RR 52/min (tachypnea).
         SpO2 94% on room air. Cap refill 2 sec. No cyanosis.
Weight: 11.5 kg (50th centile)
RS: Bilateral crepitations, subcostal retractions (+)
CVS: S1 S2 normal, no murmur. Pulse 140/min.
CNS: Conscious, irritable but consolable. No meningeal signs.
P/A: Soft, non-tender. Liver 2 cm below costal margin. Spleen
     not palpable.

INVESTIGATIONS:
CBC: Hb 10.5 g/dL, WBC 18500 /cu.mm (N 72, L 22), Platelets 3.2 lakh
CRP: 48 mg/L (H)
Blood culture: Pending (will report if positive)
Chest X-ray: Right lower lobe consolidation — consistent with
             pneumonia
RSV/Influenza/COVID rapid panel: Negative

DIAGNOSIS:
Severe Community-Acquired Pneumonia (Right Lower Lobe)
(ICD-10: J18.1)

TREATMENT GIVEN:
- IV Antibiotics: Injection Ceftriaxone 575mg IV BD (50mg/kg/day)
  (Day 1-3)
- Oxygen: Nasal prongs 2L/min (Day 1-2), weaned off Day 3
- Nebulization: Salbutamol 2.5mg + Ipratropium 250mcg QID (Day 1-2),
  then BD (Day 3)
- Antipyretic: Syrup Paracetamol 160mg (10mg/kg/dose) PRN
- IV fluids: DNS + KCl 66 mL/hr (Day 1-2), stopped when tolerating
  oral feeds
- Chest physiotherapy: Day 2-3

COURSE:
Day 1: Admission, started on IV antibiotics + oxygen. Tachypneic
       but maintaining SpO2 94% on 2L O2.
Day 2: Fever settled. RR decreased to 40/min. SpO2 97% on 1L O2.
       Started oral feeds.
Day 3: Afebrile. RR 32/min. SpO2 98% on room air. Tolerating
       oral feeds. Active. Discharged.

CONDITION AT DISCHARGE:
Afebrile. Active. SpO2 98% on room air. Tolerating oral feeds.
RR 30/min. No retractions. Chest clear.

DISCHARGE MEDICATIONS:
+-----------------------------------------------------------------------+
| Medication            | Dose      | Frequency | Duration              |
+-----------------------------------------------------------------------+
| Syrup Amoxicillin     | 230 mg    | BD         | 5 days (oral)        |
|   (20mg/kg/dose)      | (5.75 mL) |            |                      |
| Syrup Paracetamol     | 160 mg    | QID PRN    | 3 days (fever/pain)  |
|   (10mg/kg/dose)      | (8 mL)    |            |                      |
| Syrup Salbutamol      | 2.5 mg    | TID        | 5 days               |
|   (0.15mg/kg/dose)    | (2.5 mL)  |            |                      |
+-----------------------------------------------------------------------+

PARENT ADVICE:
1. Complete full antibiotic course (5 days) even if child improves.
2. Fever: Give paracetamol if fever >100°F. Tepid sponging.
   Do NOT give ibuprofen without consulting doctor.
3. Feeding: Continue normal diet. Give plenty of fluids (water,
   ORS, soups). Breastfeeding if still breastfeeding.
4. Breathing: If child breathes fast or has chest indrawing, or
   lips turn blue — bring to hospital immediately.
5. Hygiene: Hand washing. Avoid contact with sick people.
6. Complete rest for 3 days, then gradual return to normal activity.

WARNING SIGNS — REPORT IMMEDIATELY IF:
- Fast breathing or chest indrawing
- Fever >102°F not responding to paracetamol
- Not feeding or drinking at all
- Lethargy or excessive sleepiness
- Bluish lips or fingers
- Convulsions/seizures

FOLLOW-UP:
- Pediatric OPD: 12-Mar-2025 (4 days) — review, check recovery
- Chest X-ray repeat: After 2 weeks (to confirm clearance)
- Immunization: MR-2 + DPT booster — at next visit
- Growth monitoring: At each visit

Dr. [Name], MD (Pediatrics)
Consultant Pediatrician
Rainbow Children's Hospital, Bengaluru
```

---

### Format 11: Psychiatric Facility Discharge

**Where used:** Psychiatric hospitals, mental health facilities. Post-acute psychiatric admission discharge.

**Sections:**
1. Header: Hospital name, psychiatry department
2. Patient demographics: Name, age, gender, IP number
3. Admission details: Date, legal status (voluntary/involuntary)
4. Presenting complaint (with duration)
5. History of present illness (psychiatric)
6. Past psychiatric history
7. Family psychiatric history
8. Pre-morbid personality
9. Mental status examination (MSE)
10. Investigations (including psychological tests)
11. Diagnosis (ICD-10 psychiatric)
12. Treatment during stay (medications + therapy)
13. Treatment response
14. Condition at discharge
15. Discharge medications (psychiatric)
16. Side effects to watch
17. Advice to patient and family
18. Follow-up plan
19. Footer: Psychiatrist signature

**Differentiators:**
- Mental Status Examination (MSE) section — unique to psychiatry
- Pre-morbid personality section
- Legal status (voluntary/admitted under Mental Health Act)
- Family psychiatric history
- Psychological test results (if done)
- Treatment response described qualitatively
- Side effects monitoring (antipsychotic/antidepressant specific)
- Family education advice
- Community mental health resources

**Layout style:** Psychiatric hospital letterhead, structured sections, MSE in semi-structured format, A4 portrait.

**Example:**

```
NIMHANS (National Institute of Mental Health & Neuro Sciences)
Department of Psychiatry
Bengaluru - 560029

PSYCHIATRIC DISCHARGE SUMMARY

CR No: NIM-2024-008912        IP No: 25-PSY-445
Patient: [Name withheld]       Age / Gender: 27 / Male
Admitted: 20-Feb-2025          Discharged: 06-Mar-2025
LOS: 14 days
Legal Status: Voluntary admission
Consultant: Dr. [Name] (Psychiatry)

PRESENTING COMPLAINTS (per patient and family):
1. Hearing voices when no one is around — 6 months
2. Belief that people are trying to harm him — 4 months
3. Reduced sleep and talking to self — 3 months
4. Social withdrawal and not going to work — 2 months
5. Aggressive behavior when confronted — 1 month

HISTORY OF PRESENT ILLNESS:
27-year-old male, software engineer, premorbidly well-adjusted,
started hearing voices of 2-3 men commenting on his actions and
threatening him, 6 months ago. Voices were continuous, worse at
night. 4 months ago, developed belief that colleagues at office
were plotting to kill him, that his phone was tapped, and that
cameras were installed in his room. Stopped going to work. Sleep
reduced to 2-3 hours. Started talking to self. 1 month ago, became
aggressive when family tried to take him to hospital. Brought by
family and admitted voluntarily after psychiatric evaluation.

No history of substance use, no medical illness, no head trauma,
no seizures. No history of mania or depression.

PAST PSYCHIATRIC HISTORY:
No prior psychiatric treatment. No prior hospitalization.

FAMILY PSYCHIATRIC HISTORY:
Maternal uncle — diagnosed with schizophrenia, on treatment.
No other family history of mental illness.

PRE-MORBID PERSONALITY:
Well-adjusted, sociable, good academic record. No premorbid
personality traits suggestive of schizoid/paranoid personality.
Good occupational functioning.

MENTAL STATUS EXAMINATION (on admission):
General appearance: Disheveled, poor self-care, eye contact poor
Psychomotor: Mild agitation
Speech: Relevant but occasionally interrupted by responding to
         internal stimuli (hallucinations)
Mood: Anxious, dysphoric
Affect: Congruent with mood, restricted range
Thought: Thought alienation present (thought broadcasting)
         Delusions of persecution and reference
         No delusions of grandeur, no obsessions, no phobias
         No suicidal/homicidal ideation
Perception: Auditory hallucinations (second person, threatening
            content, running commentary)
Cognition: Conscious, oriented to time/place/person
           Attention and concentration: impaired
           Memory: intact (immediate, recent, remote)
Intelligence: Average
Insight: Partial (accepts illness but attributes to external causes)
Judgment: Impaired

INVESTIGATIONS:
CBC: Normal | RFT: Normal | LFT: Normal | TSH: 2.1 µIU/mL (Normal)
RPR: Non-reactive | HIV: Non-reactive
MRI Brain: No structural abnormality
EEG: Normal
Psychological testing: PANSS score 95 (Positive: 28, Negative: 18,
                       General: 49) — consistent with schizophrenia

DIAGNOSIS:
Paranoid Schizophrenia (ICD-10: F20.0)
First episode, acute phase

TREATMENT DURING STAY:
Pharmacological:
- Tab Olanzapine: Started 5mg OD, increased to 10mg OD (Day 3),
  then 15mg OD (Day 7). Tolerated well.
- Tab Lorazepam 2mg HS: For sleep and agitation (Day 1-7),
  tapered and stopped by Day 10.
- Tab Trihexyphenidyl 2mg BD: For EPS prophylaxis (Day 7 onwards)

Non-pharmacological:
- Supportive psychotherapy (daily, individual sessions)
- Family psychoeducation (2 sessions with parents)
- Activity therapy (group activities, art therapy)
- Relaxation exercises

TREATMENT RESPONSE:
Day 3: Sleep improved to 6-7 hours. Agitation reduced.
Day 7: Auditory hallucinations decreased in frequency and intensity.
       Delusional ideas less preoccupying.
Day 10: No overt hallucinations. Delusions of persecution still
        present but with less conviction. Started engaging in
        ward activities.
Day 14: No hallucinations. Delusions significantly attenuated.
        Insight improved (accepts illness, agrees to treatment).
        PANSS score 52 (Positive: 12, Negative: 14, General: 26).

CONDITION AT DISCHARGE:
Stable. No hallucinations. No delusional ideation. Sleep adequate.
Eating well. Engaging in activities. Insight partial-improved.
PANSS: 52 (reduced from 95).

DISCHARGE MEDICATIONS:
1. Tab Olanzapine 15mg HS — continue
2. Tab Trihexyphenidyl 2mg BD — continue
3. Tab Multivitamin OD — 1 month

SIDE EFFECTS TO WATCH (Olanzapine):
- Weight gain: Monitor weight weekly. Diet control, exercise.
- Sedation: Take at bedtime. Avoid driving if drowsy.
- Extrapyramidal symptoms: Tremor, rigidity, restlessness —
  report if occurs.
- Metabolic: Check blood sugar and lipid profile monthly.
- Do NOT stop medication suddenly — risk of relapse.

ADVICE TO PATIENT AND FAMILY:
1. Medications: Take regularly. Do not stop without doctor's
   advice. Relapse risk is high if medications are stopped.
2. Follow-up: Regular OPD visits as scheduled. Medications will
   be adjusted as needed.
3. Family support: Be supportive. Do not argue with delusional
   beliefs. Encourage medication compliance and activity.
4. Activity: Gradual return to normal activities. Start with
   simple tasks. May need leave from work for 2-4 weeks.
5. Avoid: Alcohol, cannabis, and other substances — can worsen
   illness and interact with medications.
6. Warning signs: Report immediately if — sleep disturbance,
   hearing voices, suspiciousness, aggressive behavior, refusal
   to take medications, suicidal thoughts.
7. Emergency: NIMHANS Emergency Department available 24x7.

FOLLOW-UP:
- Psychiatry OPD: 13-Mar-2025 (1 week)
- Then every 2 weeks for 2 months, then monthly
- CBC, FBS, Lipid profile: After 1 month (metabolic monitoring)
- Weight: Weekly at home, record in diary
- PANSS: At 6 weeks, 3 months, 6 months
- Vocational rehabilitation assessment: After 1 month

Dr. [Name], MD (Psychiatry)
Professor, Department of Psychiatry
NIMHANS, Bengaluru
```

---

### Format 12: Day Care Procedure Discharge

**Where used:** Day care units for minor procedures (endoscopy, colonoscopy, cataract, minor surgery). Same-day discharge, brief format.

**Sections:**
1. Header: Hospital name, day care unit
2. Patient demographics: Name, age, gender
3. Procedure date, discharge date (same day)
4. Procedure performed
5. Anesthesia type
6. Procedure findings
7. Post-procedure course (brief — few hours)
8. Condition at discharge
9. Discharge medications
10. Post-procedure advice
11. Warning signs
12. Follow-up
13. Footer: Doctor signature

**Differentiators:**
- Same-day admission and discharge (LOS: few hours)
- Very brief (half page to 1 page)
- Anesthesia recovery notes
- Post-procedure advice specific to procedure
- "Day Care" or "Ambulatory" label
- No detailed history/examination
- Focus on procedure and immediate recovery

**Layout style:** Brief format, day care unit letterhead, concise sections, A5 or A4.

**Example:**

```
SANKARA NETHRALAYA — DAY CARE
Nungambakkam, Chennai - 600006

DAY CARE DISCHARGE SUMMARY

Patient: LAKSHMI NARAYANAN     Age / Gender: 65 / Male
UHID: SN-2024-005678           IP No: DC-25-0234
Procedure Date: 08-Mar-2025    Discharge: 08-Mar-2025 (Same Day)
Consultant: Dr. [Name] (Ophthalmology)

PROCEDURE: Right Eye Phacoemulsification with IOL Implantation
ANESTHESIA: Topical (Proparacaine 0.5% eye drops) + Peribulbar block

PROCEDURE DETAILS:
- Phacoemulsification of right eye cataract (Nuclear sclerosis Grade 3)
- IOL: Foldable posterior chamber IOL (AcrySof IQ, +21.0 D)
  implanted in the bag
- Incision: 2.2mm clear corneal, self-sealing
- Viscoelastic: Used and thoroughly removed
- Antibiotic: Intracameral Moxifloxacin injected
- Procedure duration: 25 minutes
- Uneventful

POST-PROCEDURE COURSE:
- Recovery in day care for 2 hours
- Eye checked: IOP 16 mmHg, cornea clear, IOL well centered
- Tolerating oral fluids
- No pain, no nausea, no vomiting
- Discharged after recovery assessment

CONDITION AT DISCHARGE:
Stable. Right eye: patch removed, vision 6/18 (unaided), IOP 16,
cornea clear, IOL in position. Left eye: no change (6/6 with
glasses). No pain. Tolerating oral diet. Ambulating independently.

DISCHARGE MEDICATIONS — RIGHT EYE:
1. Gatifloxacin 0.3% eye drops — 1 drop QID x 2 weeks
2. Prednisolone acetate 1% eye drops — 1 drop 2-hourly x 1 week,
   then QID x 1 week, then BD x 1 week, then stop
3. Ketorolac 0.4% eye drops — 1 drop TID x 2 weeks
4. Lubricant (Carboxymethylcellulose 0.5%) — 1 drop QID x 1 month
5. Tab Paracetamol 500mg PRN (for pain) x 3 days

POST-PROCEDURE ADVICE:
1. Eye care:
   - Do NOT rub or press the eye
   - Keep eye closed at night (eye shield provided)
   - Wear dark glasses outdoors
   - No water in the eye for 1 week (wipe face with damp cloth)
2. Activity:
   - No heavy lifting (>5 kg) for 2 weeks
   - No bending forward for 1 week
   - No swimming for 1 month
   - Can watch TV, read after 2 days (in moderation)
3. Face wash: Avoid for 1 week. Wipe face with damp cloth.
4. Hair wash: After 1 week, head tilted backwards.
5. Diet: Normal. Avoid very hard foods for 2 days.

WARNING SIGNS — REPORT IMMEDIATELY IF:
- Severe eye pain not relieved by paracetamol
- Sudden loss of vision or decrease in vision
- Flashes of light or floaters
- Curtain or shadow in vision
- Discharge from eye, swelling, redness increasing

FOLLOW-UP:
- Day 1 post-op: 09-Mar-2025 (tomorrow morning) — mandatory
- Day 7 post-op: 15-Mar-2025 — suture check, IOP, refraction
- 1 month: 08-Apr-2025 — refraction, glasses prescription
- 3 months: 08-Jun-2025 — final check

Note: Left eye cataract surgery to be scheduled after right eye
stabilizes (approximately 4-6 weeks).

Dr. [Name], MS, FRCS (Ophthalmology)
Sankara Nethralaya, Chennai
```

---

## Appendix: OCR-Specific Notes for Synthetic Data Generation

### Layout Characteristics by Format (for OCR noise modeling)

| Format | Print Quality | Paper | Font | Tables | Stamps/Seals | Noise Level |
|---|---|---|---|---|---|---|
| Thyrocare | Laser (high) | A4 white | Arial 9pt | Yes (bordered) | QR code | Low |
| Dr Lal PathLabs | Laser (high) | A4 white | Times 10pt | Yes (bordered) | None | Low |
| Apollo Diagnostics | Laser (high) | A4 white | Calibri 10pt | Yes (bordered) | None | Low |
| Govt Hospital | Dot-matrix/thermal | Continuous/thermal | Courier 8pt | No (plain text) | Multiple stamps | High |
| Standalone Centre | Inkjet (medium) | A4/A5 | Mixed | Minimal | Centre stamp | Medium |
| Metropolis | Laser (high) | A4 white | Calibri 9pt | Yes (color-coded) | None | Low |
| SRL | Laser (high) | A4 white | Arial 9pt | Yes (bordered) | None | Low |
| POCT | Thermal | 80mm thermal | Monospace 6pt | No | None | High (fading) |
| Microbiology | Laser (medium) | A4 white | Times 10pt | Yes (AST table) | None | Low-Medium |
| Histopathology | Laser (medium) | A4 white | Times 11pt | No (narrative) | None | Low |
| Radiology | Laser (medium) | A4 white | Times 11pt | No (narrative) | None | Low |
| Health Checkup | Laser (high) | A4 white (multi-page) | Calibri 10pt | Yes (color) | None | Low |

### Discharge Summary Layout Characteristics

| Format | Print Quality | Length | Font | Tables | Stamps/Seals | Noise Level |
|---|---|---|---|---|---|---|
| NABH Hospital | Laser (high) | 2-3 pages | Calibri 11pt | Yes (meds) | Hospital seal | Low |
| AIIMS/Govt Med College | Dot-matrix/laser | 3-5 pages | Times 11pt | No | Govt stamp | Medium-High |
| Apollo (Corporate) | Laser (high) | 1-2 pages | Calibri 10pt | Yes (meds) | None | Low |
| District Hospital | Typewriter/handwritten | 1 page | Mixed/none | No | Govt stamp | High |
| Nursing Home | Inkjet/dot-matrix | Half page | Mixed | No | Nursing home stamp | High |
| Tertiary Care | Laser (high) | 3-5 pages | Calibri 10pt | Yes (meds) | Hospital seal | Low |
| Maternity | Laser (medium) | 1-2 pages | Calibri 10pt | Yes (meds) | Hospital seal | Low-Medium |
| Cardiac Hospital | Laser (high) | 2-3 pages | Calibri 10pt | Yes (meds) | Hospital seal | Low |
| Oncology Hospital | Laser (high) | 2-3 pages | Calibri 10pt | Yes (chemo) | Hospital seal | Low |
| Pediatric Hospital | Laser (high) | 1-2 pages | Calibri 10pt | Yes (meds) | Hospital seal | Low |
| Psychiatric Facility | Laser (medium) | 2-3 pages | Times 11pt | No | Hospital seal | Low-Medium |
| Day Care | Laser (medium) | 1 page | Calibri 10pt | Yes (meds) | Hospital seal | Low |

### Recommended OCR Error Profiles by Format

For synthetic error injection, apply different error rates based on document quality:

**High noise (Govt Hospital, District Hospital, Nursing Home, POCT):**
- Character substitution: 8-12%
- Deletion: 4-6%
- Insertion: 3-5%
- Word merge: 8-10%
- Transposition: 2-3%
- Additional: stamp overlap, fold marks, ink smudge simulation

**Medium noise (Standalone Centre, Microbiology, Histopathology, Radiology):**
- Character substitution: 4-6%
- Deletion: 2-3%
- Insertion: 1-2%
- Word merge: 3-5%
- Transposition: 1%

**Low noise (Thyrocare, Dr Lal, Apollo, Metropolis, SRL, Health Checkup):**
- Character substitution: 1-3%
- Deletion: 1%
- Insertion: 0.5-1%
- Word merge: 1-2%
- Transposition: 0.5%

### Indian-Specific OCR Challenges

1. **Multi-lingual content:** Patient names may include regional language characters transliterated to English (e.g., "Dhanalakshmi", "Srinivasulu", "Mohammed", "Gurpreet")
2. **Abbreviations:** Indian medical abbreviations (BD = twice daily, OD = once daily, TID = thrice daily, HS = at bedtime, PRN = as needed)
3. **Units:** Indian labs use lakh/cu.mm (not K/µL) for platelets, mill/cu.mm (not M/µL) for RBC
4. **Currency:** Rs. or ₹ in billing sections
5. **Dates:** DD-MM-YYYY format (Indian), sometimes DD/MM/YY
6. **Names:** Initials before names (e.g., "K. Ramesh", "S. Priya") — common in South India
7. **Doctor qualifications:** MD, MS, DM, MCh, DNB — Indian medical degrees
8. **Hospital types:** Government, Private, Trust, Corporate — different formatting standards
9. **Accreditation:** NABL (labs), NABH (hospitals), JCI (international), ICMR (research)
10. **ICD coding:** ICD-10 codes may appear in discharge summaries (not always present in smaller hospitals)

---

## Summary

| Category | Formats | Total Examples |
|---|---|---|
| Lab Reports | 12 | 12 full examples |
| Discharge Summaries | 12 | 12 full examples |
| **Total** | **24** | **24 full examples** |

All examples use Indian reference ranges, Indian clinical content, Indian hospital/lab names, and Indian medical conventions. Ready for use as clean source text in the synthetic OCR error injection pipeline.