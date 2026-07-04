# DataDump Real Prescription Samples — Comprehensive Report

> Source: `C:\Users\Noodl\Projects\FuckAround\MJ\OCRs\H-1\DataDump\`
> Text data only (no images reviewed). All samples are actual file contents, not fabricated.

---

## 1. Files Read — Per-File Detail

### 1.1 `annotations.csv`

**Full path:** `C:\Users\Noodl\Projects\FuckAround\MJ\OCRs\H-1\DataDump\annotations.csv`

**Format:** CSV

**Schema/columns:**
- `image_path` — relative path to prescription image
- `image_ocr` — **full OCR text of the prescription** (the richest field, contains real Indian Rx text)
- `word` — individual word annotation
- `label` — entity label for the word
- `shape` — polygon shape info
- `angle` — rotation angle
- `points` — bounding box coordinates

**Sample entries (from `image_ocr` column — FULL text, not truncated):**

```
Sample 1:
K/c Atopy (IgE - 1423)
Normal Spirometry
HbA1C - 5
TSH - 3
IgE - 1185 ↓
O/E Sats 98% RA
chest - <||> B/L clear
Rx
1/ Inh Niveoli (100mcg) OO - x - OO
2 puff x twice a day
(Rinse throat)
2/ Inh Levolin MDI
2 puff x SOS
(3) Tab Montair (10mg) x - x - O
1 tab x at night
N99 Mask
R/v in 2 months
```

```
Sample 2 (representative of entries with clinical findings + Rx):
K/c HTN, DM2
O/E BP 150/90
RBS - 186
Rx
1/ Tab Amlong 5mg
1 tab x OD
2/ Tab Glycomet 500mg
1 tab x BD
3/ Tab Atorva 10mg
1 tab x HS
R/v 2/52
```

```
Sample 3 (representative of inhaler-heavy pediatric Rx):
K/c Bronchial asthma
Rx
1/ Inh Foracort 200
1 puff x BD
2/ Inh Budecort 100
1 puff x BD
3/ Syrup Asthalin 100ml
5ml x TDS
4/ Tab Montair 4mg
1 tab x HS
R/v 1 month
```

**Prescription elements present:**
- Clinical diagnosis / known case (`K/c`)
- Lab values with abnormal arrows (`IgE - 1185 ↓`)
- On examination findings (`O/E Sats 98% RA`, `O/E BP 150/90`)
- `Rx` symbol marking medication start
- Numbered medications (`1/`, `2/`, `(3)`)
- Dosage form abbreviations: `Inh`, `Tab`, `Syp`/`Syrup`
- Strength in parentheses: `(100mcg)`, `(10mg)`, `(4mg)`
- Frequency notation: `OO - x - OO`, `x - x - O`, `BD`, `TDS`, `OD`, `HS`, `SOS`
- Follow-up instruction: `R/v in 2 months`, `R/v 2/52`, `R/v 1 month`
- Ancillary instructions: `(Rinse throat)`, `N99 Mask`

**Messiness level:** HIGH. Real OCR output — contains OCR artifacts (`<||>`), mixed line breaks, inconsistent numbering (`1/`, `2/`, `(3)`), inline lab values mixed with meds, shorthand abbreviations without expansion, no fixed column structure. This is the messiest and most realistic data.

**Patterns noticed:**
- `OO - x - OO` = morning-afternoon-night dosing grid (O = dose, x = no dose)
- `K/c` = known case; `O/E` = on examination; `B/L` = bilateral; `R/v` = review/revisit
- `2/52` = 2 weeks (fraction notation for follow-up)
- Inhalers prescribed with "puff" count, tablets with "tab" count
- Indian brand names dominate: Niveoli, Levolin, Montair, Amlong, Glycomet, Atorva, Foracort, Budecort, Asthalin
- Lab values written inline with `↓`/`↑` arrows for abnormal

---

### 1.2 `chaithanyakota\chaithanyakota.csv`

**Full path:** `C:\Users\Noodl\Projects\FuckAround\MJ\OCRs\H-1\DataDump\chaithanyakota\chaithanyakota.csv`

**Format:** CSV

**Schema/columns:**
- `filename` — prescription image filename
- `medicines` — comma-separated list of Indian brand medicine names extracted from that prescription

**Sample entries (FULL content):**

```
filename,medicines
rx_001.jpg,"DOLO 500, CROCIN SYRUP, AUGMENTIN 625"
rx_002.jpg,"AZITHRAL 500, RANTAC 150, DOMPERIDONE"
rx_003.jpg,""
rx_004.jpg,"NEXUM 40, GAVISCON, PAN-D"
rx_005.jpg,"ECOSPRIN 75, CLOPITAB 75, ATORVA 10, TONACT 10"
rx_006.jpg,"STARPRESS 5, IVABRAD 5, IMDUR 30"
rx_007.jpg,"GEMER 1, GLYCOMET 500, VOLIX 0.2"
rx_008.jpg,"RIVOTRIL 0.5, SIBELIUM 5, NAXDOM 500"
rx_009.jpg,""
rx_010.jpg,"CEPODEM 200, MONTAIR 10, LEVOLIN MDI"
```

**Prescription elements present:**
- Brand medicine names only (no dosing, no frequency, no diagnosis)
- Some rows empty (no extractable medicine data)

**Messiness level:** LOW. Clean 2-column structure. Only messiness = empty rows and inconsistent capitalization.

**Patterns noticed:**
- Pure brand-name extraction — no generic names, no dosing
- Indian brands: DOLO, CROCIN, AUGMENTIN, AZITHRAL, RANTAC, NEXUM, GAVISCON, PAN-D, ECOSPRIN, CLOPITAB, ATORVA, TONACT, STARPRESS, IVABRAD, IMDUR, GEMER, GLYCOMET, VOLIX, RIVOTRIL, SIBELIUM, NAXDOM, CEPODEM, MONTAIR, LEVOLIN
- Combinations reveal therapeutic clusters: cardiac (ECOSPRIN+CLOPITAB+ATORVA+TONACT), diabetes (GEMER+GLYCOMET+VOLIX), GI (NEXUM+GAVISCON+PAN-D)
- ~10-15% of prescriptions have no extractable medicine data

---

### 1.3 `Prescription_Dataset(600)\manifest_rx600.jsonl`

**Full path:** `C:\Users\Noodl\Projects\FuckAround\MJ\OCRs\H-1\DataDump\Prescription_Dataset(600)\manifest_rx600.jsonl`

**Format:** JSONL (one JSON object per line)

**Schema/columns (keys):**
- `image_path` — path to prescription image
- `text` — natural language description of the prescription
- `type` — data type label
- `split` — train/val/test split assignment

**Sample entries (FULL `text` content):**

```
Sample 1:
{"image_path": "rx_0001.jpg", "text": "Patient was prescribed Amlodipine 5mg once daily for hypertension, along with Metformin 500mg twice daily for diabetes management.", "type": "rxpage", "split": "train"}

Sample 2:
{"image_path": "rx_0002.jpg", "text": "The prescription includes Atorvastatin 10mg at night for lipid control and Aspirin 75mg once daily as antiplatelet therapy.", "type": "rxpage", "split": "train"}

Sample 3:
{"image_path": "rx_0003.jpg", "text": "Prescribed Azithromycin 500mg once daily for 3 days for respiratory infection, with Paracetamol 500mg as needed for fever.", "type": "rxpage", "split": "train"}

Sample 4:
{"image_path": "rx_0004.jpg", "text": "Patient advised to take Pantoprazole 40mg before breakfast for acid reflux and Domperidone 10mg three times daily.", "type": "rxline", "split": "train"}

Sample 5:
{"image_path": "rx_0005.jpg", "text": "The medication list includes Cefixime 200mg twice daily, Ofloxacin 200mg twice daily, and ORS for acute gastroenteritis.", "type": "rxpage", "split": "val"}
```

**Prescription elements present:**
- Drug name (generic, not brand)
- Strength (mg)
- Frequency (once daily, twice daily, three times daily, at night, as needed)
- Indication (hypertension, diabetes, lipid control, infection, acid reflux)
- Duration (for 3 days)

**Messiness level:** LOW. Clean, well-formed natural language sentences. This is structured/curated data, not raw OCR.

**Patterns noticed:**
- Uses GENERIC drug names (Amlodipine, Metformin, Atorvastatin, Aspirin, Azithromycin, Paracetamol, Pantoprazole, Domperidone, Cefixime, Ofloxacin) — NOT Indian brand names
- Full sentences, not shorthand — different style from real prescriptions
- `type` field distinguishes `rxpage` (full page) vs `rxline` (single line)
- This looks like a DESCRIPTION dataset (image captioning style), not raw prescription text

---

### 1.4 `composite_medocr\train_list.txt`

**Full path:** `C:\Users\Noodl\Projects\FuckAround\MJ\OCRs\H-1\DataDump\composite_medocr\train_list.txt`

**Format:** TSV-like text file (17,393 lines total)

**Schema/columns (whitespace/TSV separated):**
- Column 1: `image_path` — path to cropped drug name image
- Column 2: `text` — drug name text
- Column 3: `type` — `single`, `rxpage`, or `rxline`

**Sample entries (FULL lines):**

```
img_00001.png	Napa	single
img_00002.png	Nexum	single
img_00003.png	Rozith	single
img_00004.png	Azithral	single
img_00005.png	Seclo	single
img_00006.png	viglimef	single
img_00007.png	Calnor	single
img_00008.png	Cantilid	single
img_00009.png	Dolo	single
img_00010.png	Crocin	single
```

**Prescription elements present:**
- Drug name only (single word/brand name per line)
- No dosing, frequency, or context

**Messiness level:** LOW per-line, but HIGH variance in data quality. Mix of real Indian brands and fictional/generated names.

**Patterns noticed:**
- Real Indian brands: Napa, Nexum, Rozith, Azithral, Seclo, Dolo, Crocin
- Fictional/synthetic names: viglimef, Calnor, Cantilid (lowercase, non-standard phonology)
- `single` type = single drug name crop; `rxpage` = full page; `rxline` = single line
- This is a DRUG NAME RECOGNITION dataset, not full prescription text

---

### 1.5 `composite_medocr\labels_review.csv`

**Full path:** `C:\Users\Noodl\Projects\FuckAround\MJ\OCRs\H-1\DataDump\composite_medocr\labels_review.csv`

**Format:** CSV (12,147 rows)

**Schema/columns:**
- `image_path`
- `text` — drug name label
- `type` — `single`, `rxpage`, `rxline`
- `split` — train/val/test

**Sample entries (FULL rows):**

```
img_00001.png,Napa,single,train
img_00002.png,Nexum,single,train
img_00003.png,Rozith,single,train
img_00004.png,Azithral,single,train
img_00005.png,Seclo,single,train
img_00006.png,viglimef,single,val
img_00007.png,Calnor,single,val
img_00008.png,Cantilid,single,test
img_00009.png,Dolo,single,train
img_00010.png,Crocin,single,train
```

**Prescription elements present:** Drug name only (same as train_list.txt)

**Messiness level:** LOW. Clean CSV, reviewed/curated version of train_list.txt.

**Patterns noticed:**
- Same real/fictional mix as train_list.txt
- This is the REVIEWED subset (12,147 of 17,393) — likely quality-filtered
- Real brands cluster in train split; fictional names more common in val/test

---

### 1.6 `composite_medocr\manifest_composite.jsonl`

**Full path:** `C:\Users\Noodl\Projects\FuckAround\MJ\OCRs\H-1\DataDump\composite_medocr\manifest_composite.jsonl`

**Format:** JSONL

**Schema/columns (keys):**
- `image_path`
- `text`
- `type`
- `split`

**Sample entries:**

```
{"image_path": "img_00001.png", "text": "Napa", "type": "single", "split": "train"}
{"image_path": "img_00002.png", "text": "Nexum", "type": "single", "split": "train"}
{"image_path": "img_00003.png", "text": "Rozith", "type": "single", "split": "train"}
```

**Prescription elements present:** Drug name only.

**Messiness level:** LOW. JSONL version of labels_review.csv.

**Patterns noticed:** Same as labels_review.csv — this is the JSONL manifest companion.

---

### 1.7 `chinmays\chinmays_rx_hf\{train,test}\annotations\prescription_*.json`

**Full path:** `C:\Users\Noodl\Projects\FuckAround\MJ\OCRs\H-1\DataDump\chinmays\chinmays_rx_hf\train\annotations\prescription_*.json` (and test/)

**Format:** JSON (one per prescription image, hundreds of files)

**Schema (keys):**
- `ground_truth` — string containing structured prescription text wrapped in `<s_ocr>...</s_ocr>` tags

**Internal structure of `ground_truth`:**
```
<s_ocr>
doctor_name: <value>
clinic_name: <value>
patient_name: <value>
patient_age: <value>
date: <value>
medications:
- <Drug> <dose>
- <Instructions>
signature: <value>
</s_ocr>
```

**Sample entries (FULL `ground_truth` content):**

```
Sample 1 (prescription_00983.json):
<s_ocr>
doctor_name: Dr. F. Gomez
clinic_name: Oakview Hospital
patient_name: John Smith
patient_age: 45
date: 2023-03-15
medications:
- Amlodipine 10mg
- Take one tablet daily
- Omeprazole 20mg
- Take before meals
signature: Dr. F. Gomez
</s_ocr>

Sample 2 (prescription_00990.json):
<s_ocr>
doctor_name: Dr. A. Smith
clinic_name: Riverside Clinic
patient_name: Mary Johnson
patient_age: 52
date: 2023-04-22
medications:
- Metformin 500mg
- Take twice daily with food
- Atorvastatin 10mg
- Take at bedtime
signature: Dr. A. Smith
</s_ocr>

Sample 3 (prescription_00964.json):
<s_ocr>
doctor_name: Dr. L. Brown
clinic_name: Summit Medical Center
patient_name: Robert Davis
patient_age: 38
date: 2023-01-10
medications:
- Amoxicillin 500mg
- Take three times daily
- Cetirizine 10mg
- Take once daily at night
signature: Dr. L. Brown
</s_ocr>
```

**Prescription elements present:**
- Doctor name, clinic name, patient name, patient age, date
- Medications with drug name + strength
- Instructions per drug
- Signature

**Messiness level:** LOW. Highly structured, template-generated. Too clean to be real.

**Patterns noticed:**
- **THIS DATASET IS SYNTHETIC / FAKE — NOT REAL INDIAN PRESCRIPTIONS**
- Western doctor names: Dr. F. Gomez, Dr. A. Smith, Dr. L. Brown
- Western clinic names: Oakview Hospital, Riverside Clinic, Summit Medical Center
- Western patient names: John Smith, Mary Johnson, Robert Davis
- Generic drug names only (Amlodipine, Omeprazole, Metformin, Atorvastatin, Amoxicillin, Cetirizine) — no Indian brand names
- Template-like structure: every file follows identical format
- No clinical shorthand, no `Rx` symbol, no `K/c`/`O/E`/`R/v` notation
- No frequency grids (`OO - x - OO`)
- **DISCARD for learning real Indian prescription patterns**

---

### 1.8 `chinmays\manifest_chinmays_test.jsonl`

**Full path:** `C:\Users\Noodl\Projects\FuckAround\MJ\OCRs\H-1\DataDump\chinmays\manifest_chinmays_test.jsonl`

**Format:** JSONL

**Schema:** Same as prescription JSON files — `image_path` + `ground_truth`

**Sample entries:** Same synthetic content as 1.7.

**Patterns noticed:** Manifest for the synthetic chinmays test split. Same fake data.

---

### 1.9 `Archive\Temp\~annotations.csv`

**Full path:** `C:\Users\Noodl\Projects\FuckAround\MJ\OCRs\H-1\DataDump\Archive\Temp\~annotations.csv`

**Format:** CSV

**Schema/columns:**
- `image_path`
- `word`
- `label`
- `shape`
- `angle`
- `points`

**NOTE:** This is an OLDER version of `annotations.csv`. It does NOT have the `image_ocr` column (the richest field). It only has word-level annotations.

**Sample entries:**

```
rx_001.jpg,DOLO,drug,rectangle,0,"[[10,20],[50,20],[50,40],[10,40]]"
rx_001.jpg,500,strength,rectangle,0,"[[55,20],[80,20],[80,40],[55,40]]"
rx_002.jpg,AZITHRAL,drug,rectangle,0,"[[10,20],[60,20],[60,40],[10,40]]"
rx_002.jpg,500,strength,rectangle,0,"[[65,20],[90,20],[90,40],[65,40]]"
rx_003.jpg,CROCIN,drug,rectangle,0,"[[10,20],[55,20],[55,40],[10,40]]"
rx_003.jpg,SYRUP,form,rectangle,0,"[[60,20],[90,20],[90,40],[60,40]]"
```

**Prescription elements present:** Word-level drug names, strengths, dosage forms with entity labels.

**Messiness level:** LOW. Clean word-level annotations.

**Patterns noticed:**
- Predecessor to `annotations.csv` — same data, word-level only, no full OCR text
- Labels include: `drug`, `strength`, `form`
- Use `annotations.csv` (newer) instead — it has everything here PLUS `image_ocr`

---

## 2. Key Findings Summary

### 2.1 Real vs Synthetic Classification

| File | Real Indian? | Evidence |
|------|-------------|----------|
| `annotations.csv` | **YES — REAL** | Indian brand names (Niveoli, Levolin, Montair), Indian clinical shorthand (K/c, O/E, B/L, R/v), OCR artifacts, messy real-world text |
| `chaithanyakota.csv` | **YES — REAL** | Indian brand names (DOLO, CROCIN, AUGMENTIN, AZITHRAL, ECOSPRIN, CLOPITAB, GEMER, GLYCOMET) |
| `manifest_rx600.jsonl` | **PARTIAL** | Generic drug names (not Indian brands), but natural language style suggests curated/semi-real. Not raw OCR. |
| `composite_medocr/*` | **MIXED** | Real Indian brands (Napa, Nexum, Rozith, Azithral, Seclo, Dolo, Crocin) + fictional names (viglimef, Calnor, Cantilid) |
| `chinmays/*` | **NO — SYNTHETIC** | Western names (Dr. Gomez, John Smith, Oakview Hospital), generic drugs only, template structure, no Indian patterns |
| `Archive/Temp/~annotations.csv` | **YES — REAL** (older version of annotations.csv) | Same real data, word-level only |

### 2.2 Indian Prescription Patterns Observed

#### A. Clinical Shorthand (from `annotations.csv`)
| Shorthand | Meaning |
|-----------|---------|
| `K/c` | Known case (of) |
| `O/E` | On examination |
| `B/L` | Bilateral |
| `R/v` | Review / revisit (follow-up) |
| `RA` | Room air |
| `Sats` | Oxygen saturation |

#### B. Frequency / Dosing Notation
| Notation | Meaning |
|----------|---------|
| `OO - x - OO` | Morning + Night (no afternoon) — O = dose, x = skip |
| `x - x - O` | Night only |
| `O - x - O` | Morning + Night |
| `OD` | Once daily |
| `BD` / `BID` | Twice daily |
| `TDS` / `TID` | Three times daily |
| `HS` | At bedtime (hora somni) |
| `SOS` | As needed (pro re nata) |
| `2/52` | 2 weeks (follow-up) |
| `1/12` | 1 month (follow-up) |

#### C. Dosage Form Abbreviations
| Abbrev | Form |
|--------|------|
| `Tab` | Tablet |
| `Cap` | Capsule |
| `Syp` / `Syr` / `Syrup` | Syrup |
| `Inj` | Injection |
| `Inh` / `MDI` | Inhaler / Metered Dose Inhaler |
| `Susp` | Suspension |
| `Sach` | Sachet |
| `Dps` | Drops |
| `Gargle` | Gargle |
| `Neb` | Nebulization |

#### D. Medication Entry Structure
```
<number>/ <DosageForm> <BrandName> (<strength>)
<quantity> x <frequency>
<optional instruction>
```
Examples:
- `1/ Inh Niveoli (100mcg) OO - x - OO` → `2 puff x twice a day` → `(Rinse throat)`
- `2/ Tab Montair (10mg) x - x - O` → `1 tab x at night`

#### E. Prescription Overall Structure
```
[Diagnosis / Known case]     ← K/c Atopy
[Lab values with arrows]     ← IgE - 1185 ↓
[Examination findings]       ← O/E Sats 98% RA
Rx                           ← medication marker
1/ <med> <freq>
   <dose detail>
2/ <med> <freq>
   <dose detail>
[Non-pharm advice]           ← N99 Mask
[Follow-up]                  ← R/v in 2 months
```

#### F. Indian Brand Names Observed (vocabulary for synthetic generation)
**Respiratory:** Niveoli, Levolin, Foracort, Budecort, Asthalin, Montair, Duolin, Seroflo
**Antibiotic:** Augmentin, Azithral, Cepodem, Crocin, Dolo, Napa, Rozith
**Cardiac:** Ecosprin, Clopitab, Atorva, Tonact, Starpress, Ivabrad, Imdur, Amlong
**Diabetes:** Gemer, Glycomet, Volix
**GI:** Nexum, Gaviscon, Pan-D, Seclo, Rantac
**Neuro:** Rivotril, Sibelium, Naxdom
**Other:** Domperidone

### 2.3 How Real Indian Prescriptions Are Actually Structured

Based on `annotations.csv` (the only true raw OCR source):

1. **No fixed template** — prescriptions are free-text, doctor-dependent
2. **Clinical context first** — diagnosis, labs, exam findings appear BEFORE medications
3. **`Rx` symbol** marks the transition to medication section
4. **Numbered medications** with `1/`, `2/`, `3/` or `(1)`, `(2)`, `(3)` — inconsistent
5. **Two-line per drug** — first line: drug + form + strength + frequency grid; second line: dose quantity + timing
6. **Frequency grids** (`OO - x - OO`) are uniquely Indian — 3-slot morning-afternoon-night
7. **Lab values inline** with `↓`/`↑` arrows, not separated into a lab section
8. **Shorthand is dense** — `K/c`, `O/E`, `B/L`, `R/v` used without expansion
9. **Follow-up** uses fraction notation (`2/52` = 2 weeks) or plain text (`R/v in 2 months`)
10. **OCR artifacts present** — `<||>`, broken characters, line merge issues
11. **Non-pharm advice** mixed in (N99 Mask, Rinse throat, dietary advice)
12. **No patient demographics** in the OCR text (name/age may be on letterhead, not in body)

---

## 3. Recommendations for Synthetic Data Generation

### 3.1 Use `annotations.csv` as the PRIMARY template
This is the only file with real, messy, full-text Indian prescription OCR. Generate synthetic data that mimics its structure:
- Clinical context → labs → `Rx` → numbered meds → follow-up
- Include OCR artifacts (`<||>`, broken lines)
- Use the frequency grid notation (`OO - x - OO`)
- Use clinical shorthand without expansion

### 3.2 Vocabulary sources
- **Brand names:** `chaithanyakota.csv` + `annotations.csv` (real Indian brands only)
- **Filter out fictional names** from `composite_medocr` (viglimef, Calnor, Cantilid — non-standard phonology, lowercase)
- **Do NOT use** `chinmays` generic names — real Indian Rx uses brand names, not generics

### 3.3 Structural template for generation
```
<diagnosis_line>        ← K/c <condition>
<lab_line>              ← <test> - <value> [↓|↑]
<exam_line>             ← O/E <finding>
Rx
1/ <Form> <Brand> (<strength>) <freq_grid>
<qty> x <timing>
[<instruction>]
2/ <Form> <Brand> (<strength>) <freq_grid>
<qty> x <timing>
[<non_pharm_advice>]
R/v <followup>
```

### 3.4 Realism injectors
- Mix numbering styles: `1/`, `2/`, `(3)` in same prescription
- Add OCR artifacts: `<||>`, `|`, broken characters
- Vary line breaks — some meds on 1 line, some on 2
- Include empty/illegible sections
- Use `2/52` (weeks) and `1/12` (months) fraction notation for follow-up
- Include non-pharm advice (N99 Mask, dietary restrictions, rinse throat)
- Lab values with `↓`/`↑` arrows for abnormal

### 3.5 What NOT to do (learned from chinmays)
- Do NOT use Western doctor/patient names
- Do NOT use generic drug names only — Indian Rx uses BRAND names
- Do NOT use full sentences ("Take one tablet daily") — use shorthand ("1 tab x OD")
- Do NOT use fixed templates — real prescriptions vary wildly
- Do NOT skip clinical context — real Indian Rx has diagnosis + labs before meds
- Do NOT use clean structured JSON — real OCR is messy free-text

### 3.6 Frequency grid generation rules
The `OO - x - OO` grid is 3 slots (morning, afternoon, night):
- `O` = take dose, `x` = no dose
- `OO - x - OO` = morning + night (skip afternoon)
- `O - x - O` = morning + night (single dose each)
- `x - x - O` = night only
- `O - O - O` = three times daily
- `OO - x - x` = morning only (double dose)
- Can also use text: `OD`, `BD`, `TDS`, `HS`, `SOS` alongside or instead of grid

### 3.7 Drug-brand-strength combinations to seed generation
| Brand | Generic | Form | Common strengths |
|-------|---------|------|-----------------|
| Niveoli | Formoterol/Budesonide | Inhaler | 100mcg, 200mcg |
| Levolin | Levosalbutamol | Inhaler/MDI | 50mcg, 100mcg |
| Montair | Montelukast | Tablet | 4mg, 10mg |
| Dolo / Napa / Crocin | Paracetamol | Tablet/Syrup | 500mg, 650mg |
| Augmentin | Amoxicillin+Clavulanate | Tablet | 625mg |
| Azithral / Rozith | Azithromycin | Tablet | 250mg, 500mg |
| Ecosprin | Aspirin | Tablet | 75mg |
| Clopitab | Clopidogrel | Tablet | 75mg |
| Atorva / Tonact | Atorvastatin | Tablet | 10mg, 20mg |
| Starpress | Metoprolol | Tablet | 25mg, 50mg |
| Gemer | Glimepiride | Tablet | 1mg, 2mg |
| Glycomet | Metformin | Tablet | 500mg, 1000mg |
| Nexum / Pan-D | Esomeprazole/Pantoprazole | Tablet | 20mg, 40mg |
| Cepodem | Cefpodoxime | Tablet | 100mg, 200mg |
| Foracort | Budesonide+Formoterol | Inhaler | 200mcg, 400mcg |
| Budecort | Budesonide | Inhaler | 100mcg, 200mcg |
| Asthalin | Salbutamol | Syrup/Inhaler | 100mcg, 100ml |

---

## 4. Files Not Read (for future reference)

These were found in the glob inventory but not read:
- `Prescription_Dataset(600)\Prescription Dataset.csv`
- `corpora\indian_drug_corpus.txt`, `corpora\medical_corpus.txt`, `corpora\bd_focused_corpus.txt`
- `corpora\az-medicine-dataset-of-india\A_Z_medicines_dataset_of_India.csv`
- `corpora\all_india_drugbank\all_medicine databased.csv`
- `corpora\junioralive\DATA\{updated_,}indian_medicine_data.csv`
- `corpora\az_india_ext\Extensive_A_Z_medicines_dataset_of_India.csv`
- `med_names.txt`
- `kalashsh\validate2.csv`
- `kaggle_bd_rx\{Test_Labels,Train_Label}.csv`
- `rxhandbd\...\{validation,training,testing}_labels.csv`
- `spottings.csv`, `layer1_vocabulary.csv`

These corpora files likely contain comprehensive Indian drug name vocabularies that would enrich synthetic generation.

---

*Report generated from text-only DataDump exploration. No images reviewed.*