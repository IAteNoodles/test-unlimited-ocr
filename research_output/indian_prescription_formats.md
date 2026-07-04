# Indian Medical Prescriptions: Real-World Formats for Synthetic OCR Data Generation

*Research report on how Indian prescriptions are actually written in practice — the messy, non-systematic reality. Compiled to feed a synthetic data generator for OCR post-correction.*

---

## Section 1: How Indian Prescriptions Actually Work

Indian prescriptions in the wild bear only a loose resemblance to the "ideal prescription" taught in pharmacology textbooks (which specifies: superscription ℞, inscription with drug name/dose, subscription with instructions to pharmacist, signature, and patient identifiers). In reality, a prescription is a working clinical document that fuses several functions: it is simultaneously a medication order, a mini clinical note, a referral letter, a lab requisition, and a medico-legal record. Doctors under heavy patient load (a government OPD doctor may see 60–120 patients in a 3-hour session; a private GP may see 30–50) write fast, abbreviate heavily, and cram all of this onto whatever stationery is at hand. The result is dense, idiosyncratic, and highly variable from one prescriber to the next.

What textbooks omit is the extent to which patient context bleeds into the prescription. A typical handwritten Indian Rx will carry the chief complaint in shorthand ("c/o fever 3d, cough 5d"), a provisional diagnosis ("? viral fever", "K/c T2DM"), a couple of vitals jotted by a nurse or the doctor ("BP 150/90, PR 96"), and sometimes a fragment of past history ("H/o PTB 2019, on AKT"). These are written in the margins, above the ℞ symbol, or squeezed between drug lines. There is no separate "clinical notes" section in most handwritten prescriptions — everything coexists on one slip. Allergies, when documented at all, are often a single scrawled word ("NKDA" or "no allergy" or just "—"). Weight is frequently absent in adult prescriptions but almost always present in pediatric ones because dosing depends on it.

The medication block itself is non-uniform. Some doctors write only generic names (government/PHC settings, mandated in many states); most private practitioners write brand names (Crocin, Augmentin, Rantac, Monoceff, Azithral). Dosing frequency uses Latin-derived abbreviations that persist decades after they were dropped from Western practice: OD, BD, TDS, QID, HS, SOS, PRN, STAT. Timing relative to food is indicated as "a/c" (before food) or "p/c" (after food), sometimes written in full as "before food"/"after food", sometimes omitted entirely and left to pharmacist counselling. Duration is often vague — "5 days", "1 week", "SOS", or simply a number of tablets with no explicit stop date. The number of tablets is frequently written in the archaic "1–0–0" / "1–0–1" / "1–1–1" matrix notation (morning–afternoon–night) rather than as "BD" or "TDS", and the two notations are mixed within a single prescription.

Physical format varies wildly: a torn page from a ruled notebook with a rubber stamp; a pre-printed letterhead with the doctor's qualifications and registration number; a printed EHR sheet with barcode and patient MRN from a corporate hospital; a government scheme form (CGHS, PMJAY) with pre-printed fields; a digital PDF from a telemedicine app. Handwriting legibility is a genuine and documented problem — multiple Indian studies have measured legibility scores and found a substantial fraction of prescriptions are only partially legible to pharmacists, who routinely call doctors to confirm. This is the core challenge for OCR: the ground truth is often ambiguous even to a human reader, abbreviations are non-standard, and the same drug may appear as "Tab Crocin 650", "T.Crocin(650)", "crocin tab 650mg", or "Paracetamol 650 1BD".

---

## Section 2: Patient Context in Prescriptions

The following patient/disease information is commonly found **on the prescription itself** (not in a separate chart), though presence varies by setting:

- **Patient name** — Almost always present. Often only first name or initials in government OPD ("Ramesh", "S/o Kumar", "F 45"). Full name in private/corporate settings. May be written by registration clerk, nurse, or doctor.
- **Age/sex** — Almost always present, usually as "45/M", "32/F", "M/60". In pediatric prescriptions, age is precise ("1y 3m", "8 months"). Sometimes only age with sex inferred from name.
- **Address** — Rare in OPD slips; present in CGHS/PMJAY/corporate (scheme ID requires it). Sometimes just "village name" in rural settings.
- **Patient ID / MRN / scheme number** — Present in corporate hospitals (MRN), CGHS (beneficiary ID), PMJAY (golden card / PMJAY ID), telemedicine (app ID). Absent in private clinic and government OPD handwritten slips.
- **Date** — Usually present but often only day/month, sometimes only the doctor reuses a pad and the pre-printed year is wrong. Government OPD may have only a hospital stamp date.
- **Chief complaints (c/o)** — Very common in handwritten OPD/private prescriptions. Written as "c/o fever 3 days, headache, bodyache" or "c/o abdominal pain × 2d". Often abbreviated to "c/o". Absent in pure refill/chronic follow-up printed prescriptions.
- **Diagnosis / Provisional diagnosis** — Common. Written as "Dx: Viral fever", "Dx: ? PTB", "Provisional Dx: T2DM", "K/c Acute gastroenteritis". The "? " prefix denotes provisional. "K/c" = "known case of". Sometimes only a working diagnosis with no label.
- **Past history (H/o)** — Present when relevant. "H/o HTN 10y", "H/o DM", "H/o PTB 2018 completed AKT", "H/o MI 2020", "s/o cholecystectomy 2019". Often a single line.
- **Vitals** — BP and pulse frequently written, sometimes by nurse before doctor ("BP 140/90, PR 88"). Temperature in fever cases. RR and SpO2 in respiratory cases. Often only the abnormal ones. In corporate/ER, full vitals set with timestamps.
- **Allergies** — Poorly documented. When present: "NKDA" (no known drug allergy), "no allergy", "allergic to —", or a specific drug ("allergic to penicillin", "sulfa allergy"). Often entirely absent — a major medico-legal gap.
- **Weight** — Almost always present in pediatric prescriptions (dosing depends on it). Sometimes present in adult prescriptions for weight-based drugs (low-molecular-weight heparin, certain antibiotics). In government OPD adult Rx, usually absent.
- **Height/BMI** — Rare except in endocrinology/diabetes follow-up and bariatric clinics.
- **Investigations done / lab values** — In follow-up prescriptions, recent values written in: "HbA1c 8.2", "FBS 142", "PPBS 210", "TSH 6.8", "Cr 1.1", "TLC 11200". Sometimes attached as a separate lab report.
- **Advice / instructions** — Non-drug advice: "plenty of fluids", "rest", "cold sponging", "review after 3 days", "come if no improvement", "diet control", "walk 30 min daily". Often a single line at the bottom.
- **Referral / workup requested** — "Refer to physician", "USG abdomen", "CBC, RBS, LFT, KFT", "X-ray chest PA view", "ECG". May be on the same slip as medications.
- **Follow-up instruction** — "R/v after 3 days", "review 1 week", "SOS consult". Sometimes implicit (number of tablets implies duration).
- **Doctor's signature / stamp** — Signature always (legally required). Stamp with reg number common in private/corporate. In government OPD, often only a hospital stamp + illegible signature.

---

## Section 3: Distinct Prescription Formats

### Format 1: Government Hospital OPD Prescription (Handwritten, Dense, Minimal)

- **Where used:** District hospital, civil hospital, medical college OPD, government general hospital. Doctor sees 60–120 patients per session.
- **Sections included (in order of appearance):**
  1. Hospital name (pre-printed on slip or rubber stamp)
  2. Date (often only the stamp date)
  3. Patient name + age/sex (one line, written by clerk or doctor)
  4. OPD registration number (sometimes)
  5. Chief complaint + vitals (squeezed in, 1–2 lines)
  6. Provisional diagnosis (1 line, often with "?")
  7. ℞ symbol
  8. Medications (generic names, abbreviated, 3–6 lines)
  9. Advice (1 line)
  10. Follow-up ("R/v")
  11. Doctor signature + hospital stamp
- **What makes it different:** Minimal stationery (often a 1/4 page slip), generic names mandated, no letterhead per doctor, heavy abbreviation, vitals may be written by nurse in different handwriting, diagnosis often provisional and abbreviated. No patient ID beyond OPD serial. Extremely time-pressured.
- **Example:**

```
   GOVT DISTRICT HOSPITAL, JALGAON          OPD Reg: 4421
   Date: 25/6/26

   Ramesh s/o Suresh  45/M
   c/o fever 5d, cough with sputum 3d, breathlessness 1d
   BP 110/70  PR 104  Temp 101°F  SpO2 95%
   Dx: ? LRTI / ? CAP

   ℞
   Tab Azithromycin 500mg 1OD x 5d
   Tab Paracetamol 500mg 1SOS fever
   Tab Levocetirizine 5mg 1HS
   Syr Ambroxol 10ml TDS
   Tab Ranitidine 150mg 1BD a/c
   Inhaler Salbutamol 2 puffs SOS

   - plenty fluids, rest
   - if no relief in 3d come back
   R/v 3/7

   [illegible signature]
   [GOVT DISTRICT HOSPITAL JALGAON stamp]
```

- **How messy/systematic:** 2/5 (low structure, high density, generic names, abbreviated)

---

### Format 2: Private Clinic Prescription (Letterhead, Semi-Structured)

- **Where used:** Solo or small-group private practitioner clinic, MBBS/MD general physician, pediatrician, physician in semi-urban/urban practice.
- **Sections included:**
  1. Pre-printed letterhead: doctor name, qualifications (MD, DCH, etc.), registration number, clinic address, phone, timings
  2. Date
  3. Patient name, age/sex (handwritten)
  4. Chief complaints (1–2 lines)
  5. Vitals (BP, weight sometimes)
  6. Provisional diagnosis
  7. ℞
  8. Medications (mix of brand and generic, often brand-heavy)
  9. Investigations requested (if any)
  10. Advice
  11. Follow-up
  12. Doctor signature + clinic stamp
- **What makes it different:** Personal letterhead with doctor's branding. Brand names common (Crocin, Augmentin, Rantac). More legible than government OPD but still handwritten. Patient relationship ongoing — doctor remembers patient. Often a "refill" pattern for chronic patients. May include phone follow-up.
- **Example:**

```
   Dr. S. K. Deshpande, MD (General Medicine)
   Reg No: 67890 (Maharashtra Medical Council)
   Deshpande Clinic, Shop 4, Sai Plaza, Station Road, Kalyan
   Ph: 98xxxxxxxx  Timings: 10–1, 6–9

   25/06/2026

   Mrs. Sunita Patil  52/F   Wt 68kg
   c/o burning urination 2d, frequency, lower abd pain
   BP 130/80   PR 88
   Dx: Acute UTI

   ℞
   Tab Augmentin 625 1BD x 5d
   Tab Citralka 2tsp TDS in water
   Tab Rantac 150 1BD a/c
   Tab Urispas 1TDS p/c
   Tab Dolo 650 1SOS fever/pain
   Syr Cofdex 10ml HS SOS

   - urine routine + culture
   - 3L water/day
   - review with report 3d

   S. K. Deshpande
   [stamp]
```

- **How messy/systematic:** 3/5 (letterhead gives structure, body semi-structured, brand names)

---

### Format 3: Corporate Hospital Prescription (Printed, Systematic, EHR-Generated)

- **Where used:** Multi-specialty corporate hospital (Apollo, Fortis, Manipal, Max, Narayana, Aster), OPD consultation. Generated by hospital EHR/HIS.
- **Sections included:**
  1. Hospital logo + name + address header (printed)
  2. Patient details block: MRN, name, age/sex, address, phone
  3. Visit details: OPD no, department, consultant name, date/time
  4. Allergies field (explicit, "No Known Allergies" if none)
  5. Chief complaints (structured)
  6. Vitals (structured table: BP, PR, RR, Temp, SpO2, height, weight, BMI)
  7. Diagnosis (provisional / final, ICD code sometimes)
  8. Investigations advised
  9. ℞ Medications (structured: drug, dose, frequency, duration, quantity, route)
  10. Advice / patient instructions
  11. Follow-up date
  12. Digital signature + consultant stamp + hospital stamp
  13. Barcode (patient ID)
- **What makes it different:** Fully printed, systematic, EHR-generated. Structured medication table. Allergies always documented. ICD codes may appear. Barcode for pharmacy. Often 1–2 pages. Legible. May include generic + brand name both. Follow-up as explicit date.
- **Example:**

```
   ┌──────────────────────────────────────────────┐
   │  APOLLO HOSPITALS, BENGALURU                 │
   │  154/1, Bannerghatta Road, Bengaluru 560076  │
   └──────────────────────────────────────────────┘
   MRN: APH-22-88412          OPD Reg: 00347721
   Patient: Anjali Rao        Age/Sex: 38/F
   Dept: General Medicine     Consultant: Dr. R. Menon, MD
   Date: 25-Jun-2026  10:42   Allergies: No Known Allergies

   CHIEF COMPLAINTS:
   - Headache for 7 days, throbbing, frontal
   - Nausea, photophobia

   VITALS:
   BP 118/76   PR 82   RR 16   Temp 98.4°F   SpO2 99%
   Ht 162cm   Wt 58kg   BMI 22.1

   DIAGNOSIS: Migraine without aura (ICD G43.009)

   INVESTIGATIONS ADVISED: Nil

   ℞
   1. Tab Naproxen 500mg     1 BD after food     x 3 days    Qty 6
   2. Tab Domperidone 10mg   1 TDS before food   x 3 days    Qty 9
   3. Tab Propranolol 40mg   1 OD morning        x 30 days   Qty 30
   4. Tab Rizatriptan 10mg   1 SOS at onset      Qty 4

   ADVICE:
   - Maintain headache diary
   - Adequate sleep, regular meals
   - Avoid triggers (chocolate, cheese, sunlight)
   - Review after 1 month or SOS

   FOLLOW-UP: 25-Jul-2026

   Digitally signed by
   Dr. R. Menon, MD (General Medicine)
   Reg No: KMC-45678
   [barcode] [hospital stamp]
```

- **How messy/systematic:** 5/5 (highly systematic, printed, structured)

---

### Format 4: CGHS Wellness Center Prescription

- **Where used:** CGHS (Central Government Health Scheme) wellness centers for central government employees, pensioners, and dependents. Across India in CGHS-covered cities.
- **Sections included:**
  1. CGHS logo + wellness center name (pre-printed)
  2. CGHS beneficiary ID + beneficiary name
  3. Age/sex, relation to card holder
  4. Date
  5. Medical officer / specialist name
  6. Diagnosis
  7. ℞ Medicines (from CGHS formulary / AI list)
  8. "Issued from CGHS pharmacy" indication
  9. Referral to CGHS empaneled hospital if needed
  10. Signature + CGHS stamp
- **What makes it different:** CGHS beneficiary ID is central. Medicines drawn from CGHS wellness center pharmacy (free). Formulary-driven — branded equivalents from CGHS rate contract. Pensioner-heavy population (chronic disease common). Often a refill slip. May have "AI" (advance investigation) or "referral" stamp. Printed format with handwritten additions.
- **Example:**

```
   ┌────────────────────────────────────────────┐
   │  CGHS WELLNESS CENTRE, RK PURAM, NEW DELHI │
   │  [CGHS logo]                               │
   └────────────────────────────────────────────┘
   Beneficiary ID: 1100000000456789
   Name: Sh. R. K. Sharma (Pensioner)
   Age/Sex: 68/M    Card: Self
   Date: 25.06.2026
   MO: Dr. P. Gupta

   Dx: T2DM, HTN, IHD — stable

   ℞
   Tab Metformin 500mg        1 BD
   Tab Glimepiride 2mg        1 OD
   Tab Telmisartan 40mg       1 OD
   Tab Atorvastatin 10mg      1 HS
   Tab Clopidogrel 75mg       1 OD
   Tab Aspirin 75mg           1 OD after lunch
   Insulin Glargine 16u       SC HS

   - HbA1c, FBS, lipid profile, KFT next visit
   - ECG
   - Referral to cardiology OPD (CGHS empaneled)

   Issued: CGHS Pharmacy, RK Puram
   [signature] [CGHS stamp]
```

- **How messy/systematic:** 4/5 (pre-printed form, semi-structured, formulary-driven)

---

### Format 5: PMJAY / Ayushman Bharat Hospital Prescription

- **Where used:** Empaneled hospitals under Ayushman Bharat PMJAY (up to ₹5 lakh family cover). Used at empaneled private and government hospitals for covered beneficiaries.
- **Sections included:**
  1. Hospital name + "Empaneled under PMJAY" / Ayushman Bharat logo
  2. PMJAY ID (golden card number) + beneficiary name
  3. Family ID, relation
  4. Age/sex
  5. Date of admission/visit
  6. Treating doctor
  7. Diagnosis (primary + secondary, ICD)
  8. Package / procedure code (if admitted)
  9. ℞ Medications
  10. Investigations (pre-authorization may be referenced)
  11. Discharge summary reference (if inpatient)
  12. Doctor signature + hospital NABH/PMJAY stamp
- **What makes it different:** PMJAY ID is mandatory. Scheme-driven documentation for claim processing. Diagnosis must be coded for package eligibility. Often printed from PMJAY portal (NHA). Mix of OPD and IPD. Medicines may be from hospital pharmacy (covered) or outside. Pre-authorization number for procedures.
- **Example:**

```
   ┌────────────────────────────────────────────────┐
   │  SARVODAYA HOSPITAL                            │
   │  Empaneled under Ayushman Bharat PMJAY         │
   │  [Ayushman logo]                               │
   └────────────────────────────────────────────────┘
   PMJAY ID: 23123456789012      Family ID: 23123456789
   Beneficiary: Meena Devi       Age/Sex: 45/F
   Relation: Self
   Date: 25/06/2026   OPD
   Treating: Dr. A. Verma, MD

   Dx (Primary): Cholelithiasis (ICD K80.2)
   Dx (Secondary): T2DM (ICD E11.9)
   Package: Lap Cholecystectomy — Pre-auth #AB-998877

   ℞
   Tab Augmentin 625 1BD x 5d
   Tab Dolo 650 1SOS
   Tab Rantac 150 1BD
   Tab Metformin 500 1BD
   Inj Tramadol 50mg IM SOS

   - USG abdomen done (gallstones confirmed)
   - Pre-anesthetic checkup
   - Surgery scheduled 28/06
   - Discharge meds per package

   [signature]
   [SARVODAYA HOSPITAL PMJAY stamp]
```

- **How messy/systematic:** 4/5 (portal-printed, scheme-structured, claim-driven)

---

### Format 6: Telemedicine / E-Prescription (Digital)

- **Where used:** Telemedicine consults via apps (Practo, Lybrate, mfine, Apollo 24|7, eSanjeevani, Tata 1mg). Also WhatsApp/email consults (technically non-compliant but common).
- **Sections included:**
  1. App/platform header or doctor's digital letterhead
  2. Doctor name, qualification, reg number (mandatory per Telemedicine Guidelines 2020)
  3. Patient name, age/sex
  4. Consult ID / order ID
  5. Date/time of consult
  6. Mode (video/audio/text)
  7. Chief complaints (patient-typed or doctor-entered)
  8. Diagnosis
  9. ℞ Medications (structured, often with generic+brand)
  10. Advice
  11. Follow-up
  12. Digital signature / QR code for verification
  13. Pharmacy partner link (for delivery)
- **What makes it different:** Fully digital, no handwriting. Structured fields. QR code for authenticity. Often auto-formatted. Medication list may have drug-interaction warnings auto-generated. Patient may receive via SMS/email/app. Compliant format per Telemedicine Practice Guidelines 2020 (requires reg number, mode of consult). R-group drugs (Schedule X, etc.) not allowed via text/audio consult.
- **Example:**

```
   ┌─────────────────────────────────────────────┐
   │  e-PRESCRIPTION                              │
   │  Dr. Kavita Nair, MBBS, MD (Internal Med)    │
   │  Reg No: TSMC-55432 (Telangana)              │
   │  Platform: Apollo 24|7                       │
   └─────────────────────────────────────────────┘
   Consult ID: AP247-2026-0098123
   Patient: Arjun Mehta    Age/Sex: 29/M
   Date: 25 Jun 2026  14:15
   Mode: Video consultation

   CHIEF COMPLAINTS:
   Sore throat, mild fever 2 days, body ache

   DIAGNOSIS: Acute pharyngitis

   ℞
   1. Tablet Azithromycin 500mg
      1 tablet once daily for 3 days
   2. Tablet Paracetamol 650mg
      1 tablet SOS if fever > 100°F
   3. Tablet Betadine gargle
      10ml in warm water, gargle BD
   4. Tablet Vitamin C 500mg
      1 tablet OD for 7 days

   ADVICE:
   - Warm saline gargles
   - Voice rest, hydration
   - Isolate, wear mask
   - Review if breathing difficulty / no relief in 3 days

   FOLLOW-UP: Tele-consult after 3 days

   [QR code]
   Digitally signed: Dr. Kavita Nair
   Verify at apollo247.com/verify
```

- **How messy/systematic:** 5/5 (fully structured, digital, no handwriting)

---

### Format 7: Pediatric Prescription (Weight-Based Dosing)

- **Where used:** Pediatrician OPD (private or hospital), pediatric OPD in medical college. Children <12 typically.
- **Sections included:**
  1. Doctor letterhead / hospital header
  2. Date
  3. Child's name, age (precise — months), sex, **weight (prominent)**
  4. Chief complaints
  5. Vitals (temp, weight, sometimes height, head circumference in infants)
  6. Diagnosis
  7. ℞ Medications — **dose calculated per kg, often shown**
  8. Advice (feeding, fluids, danger signs)
  9. Follow-up / "come immediately if..." list
  10. Doctor signature
- **What makes it different:** Weight is mandatory and prominent. Doses are weight-based (mg/kg) and the calculation is sometimes visible ("Paracetamol 15mg/kg = 180mg"). Syrups/drops with ml dosing. Dosing by age-bands common when weight unknown. Immunization status may be noted. "Danger signs" advice explicit (lethargy, not feeding, fast breathing). Often more detailed advice than adult Rx.
- **Example:**

```
   Dr. Meena Kulkarni, MD (Pediatrics), DCH
   Reg No: MMC-33210
   Kulkarni Children's Clinic, Pune

   25/06/2026

   Aarav s/o Nikhil   1y 6m   M   Wt: 11 kg
   c/o fever 2d, runny nose, decreased feeding
   Temp 101.2°F   RR 38   (no chest indrawing)
   Dx: Viral URTI

   ℞
   Syr Crocin (Paracetamol 250mg/5ml)
       3.5ml (=175mg) SOS fever >100°F  max 4 doses/d
   Syr Azithral (Azithromycin 200mg/5ml)
       2.5ml OD x 3d   (10mg/kg)
   Syr Maxtra (chlorpheniramine+phenylephrine)
       2.5ml TDS x 3d
   Nasoclear saline drops 2 drops each nostril TDS
   Syr Zinc 20mg/5ml  2.5ml OD x 14d

   - continue breastfeeding, ORS if loose stool
   - tepid sponging for fever
   - COME IMMEDIATELY if: not feeding, lethargy,
     fast breathing, convulsion, non-blanching rash
   R/v 3d

   Meena Kulkarni
   [stamp]
```

- **How messy/systematic:** 4/5 (structured, weight prominent, dose calc visible)

---

### Format 8: Chronic Disease Follow-Up Prescription (Diabetes / Hypertension)

- **Where used:** Physician/endocrinologist/cardiologist OPD for established T2DM, HTN, hypothyroidism, CKD. Private clinic, corporate hospital, or CGHS.
- **Sections included:**
  1. Doctor letterhead / hospital header
  2. Date
  3. Patient name, age/sex
  4. Diagnosis (chronic, established)
  5. **Recent lab values** (HbA1c, FBS, PPBS, lipid profile, KFT, urine albumin)
  6. **Current vitals** (BP, weight, BMI)
  7. **Current medications** (full list, often with doses)
  8. ℞ Changes (titration — ↑/↓ dose, add/stop)
  9. New investigations advised
  10. Advice (diet, exercise, foot care)
  11. Follow-up (3-monthly for diabetes)
  12. Doctor signature
- **What makes it different:** Lab values and vitals are central, not the prescription itself. Medication changes are incremental ("↑ Glimepiride to 4mg", "stop Metformin temporarily"). Often a "refill + titration" document. Foot examination, eye examination reminders. May reference previous visit values. Printed follow-up sheet common in corporate.
- **Example:**

```
   Dr. R. Subramanian, MD, DM (Endocrinology)
   Reg No: TNDMC-77841
   Diabetes & Endocrine Centre, Chennai

   25/06/2026

   Mr. K. Murugan   61/M
   Dx: T2DM (since 2014), HTN, Diabetic neuropathy

   LAST VISIT (28/03/26)          TODAY
   HbA1c  8.4%                    HbA1c 7.9%  (↓)
   FBS    156                     FBS 132
   PPBS   244                     PPBS 198
   S.Cr   1.2                     S.Cr 1.3
   Urine ACR 38                   —
   LDL    112                     LDL 98
   BP     144/86                  BP 138/82   Wt 74kg

   CURRENT MEDS:
   Tab Metformin 1000 BD, Glimepiride 2 OD, Telmisartan 40 OD,
   Atorvastatin 10 HS, Pregabalin 75 HS

   ℞ CHANGES:
   ↑ Glimepiride 2 → 3mg OD
   + Tab Empagliflozin 10mg 1 OD morning
   continue rest
   Pregabalin 75 → 150 HS

   INVESTIGATIONS (next visit):
   HbA1c, FBS, PPBS, KFT, urine ACR, ECG, foot screening
   Fundus examination (ophthalmology)

   ADVICE:
   - diet review (diabetic educator)
   - daily walk 40 min
   - daily foot inspection, proper footwear
   - home glucose monitoring log

   FOLLOW-UP: 3 months (25/09/26)

   R. Subramanian
   [stamp]
```

- **How messy/systematic:** 4/5 (structured follow-up, lab table, titration)

---

### Format 9: Emergency / ER Prescription (Terse, Abbreviated)

- **Where used:** Hospital emergency department / casualty. Time-critical.
- **Sections included:**
  1. ER header (hospital name, "EMERGENCY")
  2. Patient name, age/sex, MRN (if known; "UNKNOWN" if brought unconscious)
  3. Date/time of arrival (precise)
  4. Mode of arrival (ambulance/walk-in/referred)
  5. Presenting complaint (one line, terse)
  6. Vitals (full set, time-stamped)
  7. Working diagnosis
  8. ℞ STAT orders (IV fluids, injections, O2)
  9. Investigations (STAT)
  10. Plan (admit / observe / discharge)
  11. Doctor signature
- **What makes it different:** Terse, time-stamped, STAT-heavy. IV/IM routes dominant initially. Fluid orders with rates. "Triage" category may be noted. Often written on ER-specific colored paper. Abbreviated to the extreme. May transition to admission orders. Legibility often poor due to urgency.
- **Example:**

```
   ┌──────────────────────────────────────────┐
   │  FORTIS HOSPITAL — EMERGENCY             │
   └──────────────────────────────────────────┘
   Pt: Gopal R   58/M   MRN: F-44712
   Arrived: 25/06/26  23:40   Brought by ambulance
   C/O: severe chest pain 1h, sweating, breathless
   Vitals 23:42: BP 90/60  PR 110  RR 24  SpO2 92% RA
   Dx: ? ACS — anterior MI

   ℞ STAT
   O2 4L nasal prong → tgt SpO2 >94
   Inj Aspirin 325mg chewable STAT
   Inj Clopidogrel 300mg PO STAT
   Inj Atorvastatin 80mg PO STAT
   Inj Morphine 3mg IV STAT (repeat SOS)
   Inj Pantop 40mg IV STAT
   IV NS bolus 250ml STAT
   Shift to Cath Lab — primary PCI

   INVESTIGATIONS STAT:
   ECG, Troponin, CBC, RBS, KFT, LFT, PT/INR, Na/K,
   CXR, 2D Echo

   Plan: ADMIT — CCU, cardiology consult urgent

   [ER MO signature]
   [FORTIS EMERGENCY stamp]
```

- **How messy/systematic:** 2/5 (terse, STAT-heavy, time-pressured, abbreviated)

---

### Format 10: Nursing Home Prescription (Mixed Handwritten + Printed)

- **Where used:** Small private nursing homes (10–30 beds), semi-urban/urban. Run by 1–3 doctors. Maternity homes, surgical centers.
- **Sections included:**
  1. Nursing home letterhead (printed, with name + phone)
  2. Date
  3. Patient name, age/sex
  4. IPD/OPD + bed number (if admitted)
  5. Diagnosis
  6. ℞ Medications (handwritten, brand names)
  7. IV fluids / injections (if inpatient)
  8. Investigations
  9. Advice
  10. Doctor signature + nursing home stamp
- **What makes it different:** Mixes OPD and IPD on same stationery. May include IV fluid orders, injection schedules, nursing instructions ("I/V fluid DNS 1L over 6h"). Handwritten on printed letterhead. Often a single doctor's practice. Maternity homes have obstetric specifics (LMP, EDD, gravida/para). Less systematic than corporate, more than government OPD.
- **Example:**

```
   ┌────────────────────────────────────────────┐
   │  SAI NURSING HOME                          │
   │  Dr. V. Joshi, MS                          │
   │  Station Road, Ahmednagar  Ph: 0241-xxxxxx │
   └────────────────────────────────────────────┘
   25/6/26   IPD Bed 4

   Smt. Lata Jadhav   30/F
   Dx: P3 LSCS (post-op day 1)

   ℞
   Inj Cefotaxime 1g IV BD x 5d
   Inj Metronidazole 500mg IV TDS x 3d
   Inj Tramadol 50mg IM SOS
   Inj Pantop 40mg IV OD
   Tab Rantac 150 1BD
   IV Fluid DNS 500ml + RL 500ml over 8h
   Syr Lactulose 15ml HS
   Tab Iron+Folic acid 1OD

   - clear fluids today, soft diet tomorrow
   - ambulate evening
   - wound dressing
   - breast feeding encouraged

   V. Joshi
   [SAI NURSING HOME stamp]
```

- **How messy/systematic:** 3/5 (letterhead + handwritten, IPD/OPD mix, IV orders)

---

### Format 11: Specialist Referral Prescription (With Workup Requested)

- **Where used:** GP/family physician refers to specialist (physician, cardiologist, neurologist, surgeon). Also inter-specialist referrals within a hospital.
- **Sections included:**
  1. Referring doctor letterhead
  2. Date
  3. Patient name, age/sex
  4. Brief history (chief complaint + duration)
  5. Examination findings (relevant)
  6. Investigations done so far (with values)
  7. Provisional diagnosis
  8. **Reason for referral** (explicit)
  9. ℞ Symptomatic / interim medications
  10. Workup requested from specialist
  11. Referring doctor signature
- **What makes it different:** It's a referral letter as much as a prescription. Emphasis on what's been done and what's being asked. Interim meds may be minimal. Workup list prominent. May be addressed to a named specialist ("To Dr. X, Cardiologist"). Often the patient carries this + reports to the specialist.
- **Example:**

```
   Dr. Anil Banerjee, MBBS, MD (Family Med)
   Reg No: WBMC-12087
   Banerjee Family Clinic, Kolkata

   25/06/2026

   To: Dr. S. Chatterjee, DM (Cardiology)

   Patient: Mr. Subhash Dutta   55/M
   H/o: central chest pain on exertion 2 months,
        relieved by rest, now occurring at rest since 3d.
        K/c HTN 8y, smoker 30 pack-years.

   O/E: BP 150/90, PR 92, S1S2 normal, no murmur,
        lungs clear, no pedal edema.

   ECG (done today): T wave inversion V1–V4
   RBS 112, Troponin I 0.03 (negative)

   Provisional Dx: Unstable angina / ? NSTEMI

   REASON FOR REFERRAL:
   For urgent cardiology evaluation, risk stratification,
   coronary angiography.

   ℞ (interim)
   Tab Aspirin 300mg chew STAT then 75mg OD
   Tab Clopidogrel 300mg STAT then 75mg OD
   Tab Atorvastatin 40mg HS
   Tab Pantop 40 1OD
   SL GTN spray SOS chest pain

   - shift to ER if pain persists/worsens

   Anil Banerjee
   [stamp]
```

- **How messy/systematic:** 4/5 (structured referral, history + workup, addressed)

---

### Format 12: Rural / PHC Prescription (Minimal Resources, Generic Names)

- **Where used:** Primary Health Centre (PHC), Community Health Centre (CHC), sub-centre. Rural areas. Medical officer (MBBS) or specialist on visit. ANM for minor ailments.
- **Sections included:**
  1. PHC name (pre-printed government slip or stamp)
  2. Date
  3. Patient name, age/sex, village
  4. Chief complaint (brief)
  5. Vitals (if equipment available — BP may be absent)
  6. Diagnosis
  7. ℞ Medications (generic names, from PHC formulary / essential list)
  8. Advice
  9. Referral to CHC/district hospital if needed
  10. MO signature + PHC stamp
- **What makes it different:** Generic names only (government mandate + formulary constraint). Limited drug availability — what's in PHC stock. Minimal investigations (maybe Hb, urine albumin, RBS). Referral to higher center common for anything serious. Free medicines from PHC pharmacy. Often printed government slip with handwritten entries. Village name used as identifier. ANM may handle follow-up.
- **Example:**

```
   ┌────────────────────────────────────────────┐
   │  PRIMARY HEALTH CENTRE, KOTHUR             │
   │  [Govt of Telangana logo]                  │
   └────────────────────────────────────────────┘
   25/06/2026

   Lakshmi   25/F   V/o: Kothur
   c/o white discharge pv 1 week, itching
   (BP not recorded — instrument under repair)
   Dx: ? vaginal candidiasis

   ℞
   Tab Fluconazole 150mg 1OD single dose
   Tab Metronidazole 400mg 1TDS x 7d
   Tab Albendazole 400mg 1 stat
   Clotrimazole vaginal pessary 1 OD HS x 6d
   Tab Paracetamol 500mg 1SOS pain

   - maintain hygiene
   - husband also to take treatment if symptoms
   - R/v 1 week; if no relief refer CHC

   [MO signature]
   [PHC KOTHUR stamp]
```

- **How messy/systematic:** 2/5 (minimal, generic, formulary-limited, resource-constrained)

---

## Section 4: Common Abbreviations & Shorthand

### Dosing Frequency
| Abbrev | Meaning | Notes |
|---|---|---|
| OD | once daily (omne in die) | Universal in India |
| BD / BID | twice daily (bis in die) | BD more common than BID |
| TDS / TID | three times daily (ter in die) | TDS dominant |
| QID / QDS | four times daily (quater in die) | |
| HS | at bedtime (hora somni) | |
| SOS | if required (si opus sit) | Single dose available; "PRN" similar but implies ongoing |
| PRN | as needed (pro re nata) | |
| STAT | immediately / single dose now | ER heavy |
| Q4H / Q6H / Q8H | every 4/6/8 hours | |
| QD | every day | Less common than OD |
| QOD / Q2D | every other day | |
| QWK | once weekly | e.g., methotrexate |
| 1–0–0 / 1–0–1 / 1–1–1 | morning–afternoon–night tablet matrix | Very Indian; the "0" = no dose that time |
| 0–0–1 | night only | |
| 2–0–2 | two morning, two night | |
| Alt days | alternate days | |
| Weekly once | once a week | |

### Routes of Administration
| Abbrev | Meaning |
|---|---|
| PO / per oral | by mouth |
| IV | intravenous |
| IM | intramuscular |
| SC / subcut | subcutaneous |
| PR | per rectum |
| SL | sublingual |
| INH / inh | inhalation |
| TOP | topical |
| OD (ophth) | right eye (oculus dexter) — context-dependent, conflicts with "once daily" |
| OS (ophth) | left eye (oculus sinister) |
| OU (ophth) | both eyes (oculus uterque) |
| PV | per vagina |
| Pess | pessary (vaginal) |
| Supp | suppository |
| GTN SL | glyceryl trinitrate sublingual |
| Neb | nebulization |
| S/C | subcutaneous (also written) |

### Timing Relative to Food
| Abbrev | Meaning |
|---|---|
| a/c / ac | before food (ante cibum) |
| p/c / pc | after food (post cibum) |
| before food | (written in full) |
| after food | (written in full) |
| with food | |
| empty stomach | e.g., levothyroxine, alendronate |
| HS | at bedtime (often implies empty stomach) |
| 1h before food | |
| morning | |
| night | |

### Diagnosis & History Shorthand
| Abbrev | Meaning |
|---|---|
| K/c / KCO | known case of |
| H/o | history of |
| c/o | complains of |
| C/O | complains of (caps variant) |
| O/E | on examination |
| P/A | per abdomen (examination) |
| P/R | per rectum (examination) |
| P/V | per vagina (examination) |
| R/v / Rv | review (follow-up) |
| R/o | rule out |
| s/o | suggestive of / son of (context) |
| d/o | daughter of |
| w/o | wife of |
| h/o | history of |
| NKDA | no known drug allergy |
| NAD | no abnormality detected |
| S/O | suggestive of |
| D/D | differential diagnosis |
| ?Dx | provisional diagnosis |
| Dx | diagnosis |
| ? | provisional / query (prefix) |
| # | fracture (e.g., "# NOF" = fracture neck of femur) |
| Pt | patient |
| y / yr | years |
| m / mo | months |
| d | days |

### Disease Abbreviations (common in Indian Rx)
| Abbrev | Meaning |
|---|---|
| HTN | hypertension |
| DM / T2DM | diabetes mellitus / type 2 |
| T1DM | type 1 diabetes |
| IHD | ischemic heart disease |
| CAD | coronary artery disease |
| ACS | acute coronary syndrome |
| MI | myocardial infarction |
| NSTEMI / STEMI | non-ST / ST elevation MI |
| CVA | cerebrovascular accident (stroke) |
| TIA | transient ischemic attack |
| CKD | chronic kidney disease |
| AKI | acute kidney injury |
| CLD | chronic liver disease |
| COPD | chronic obstructive pulmonary disease |
| BA | bronchial asthma |
| PTB | pulmonary tuberculosis |
| AKT / ATT | anti-tubercular therapy |
| LRTI / URTI | lower / upper respiratory tract infection |
| CAP | community-acquired pneumonia |
| UTI | urinary tract infection |
| GE | gastroenteritis |
| AP | acute pancreatitis |
| GERD | gastroesophageal reflux disease |
| IBD | inflammatory bowel disease |
| IBS | irritable bowel syndrome |
| NAFLD | non-alcoholic fatty liver disease |
| DKA | diabetic ketoacidosis |
| HHS | hyperosmolar hyperglycemic state |
| UTI | urinary tract infection |
| ARF | acute renal failure |
| ESRD | end-stage renal disease |
| BPH | benign prostatic hyperplasia |
| PID | pelvic inflammatory disease |
| PCOS | polycystic ovarian syndrome |
| DUB | dysfunctional uterine bleeding |
| LSCS | lower segment cesarean section |
| PV / P1 / P2 | para (obstetric) |
| G1 / G2 | gravida |
| LMP | last menstrual period |
| EDD | expected date of delivery |
| ITP | immune thrombocytopenia |
| SLE | systemic lupus erythematosus |
| RA | rheumatoid arthritis |
| OA | osteoarthritis |
| CVA | cerebrovascular accident |

### Vitals & Investigation Shorthand
| Abbrev | Meaning |
|---|---|
| BP | blood pressure |
| PR | pulse rate (also per rectum — context) |
| RR | respiratory rate |
| SpO2 | oxygen saturation |
| Temp / T° | temperature |
| CVS | cardiovascular system |
| RS | respiratory system |
| CNS | central nervous system |
| PA / P/A | per abdomen |
| FBS | fasting blood sugar |
| PPBS | post-prandial blood sugar |
| RBS | random blood sugar |
| HbA1c | glycated hemoglobin |
| CBC | complete blood count |
| TLC / DLC | total / differential leukocyte count |
| Hb | hemoglobin |
| PLT | platelets |
| LFT | liver function test |
| KFT / RFT | kidney / renal function test |
| Na / K | sodium / potassium |
| Ca / Phos | calcium / phosphate |
| TSH | thyroid stimulating hormone |
| T3 / T4 | thyroid hormones |
| ECG | electrocardiogram |
| 2D Echo | echocardiography |
| CXR | chest X-ray |
| USG | ultrasonography |
| CT / MRI | computed tomography / magnetic resonance imaging |
| ESR | erythrocyte sedimentation rate |
| CRP | C-reactive protein |
| PT / INR | prothrombin time / international normalized ratio |
| ACR | albumin:creatinine ratio |
| ABG | arterial blood gas |
| CSF | cerebrospinal fluid |

### Latin Abbreviations Still in Use
| Abbrev | Meaning |
|---|---|
| ℞ | recipe (take) — the prescription symbol |
| OD | omne in die (once daily) |
| BD | bis in die (twice daily) |
| TDS | ter in die (three times daily) |
| QID | quater in die (four times daily) |
| HS | hora somni (at bedtime) |
| SOS | si opus sit (if required) |
| PRN | pro re nata (as needed) |
| ac | ante cibum (before food) |
| pc | post cibum (after food) |
| STAT | statim (immediately) |
| aq | aqua (water) |
| gtts | guttae (drops) |
| ad lib | ad libitum (as desired) |
| q.s. | quantum satis (sufficient quantity) |
| aa | ana (of each) |
| fiat | let it be made (compounding) |
| mist | mistura (mixture) |
| cap | capsula (capsule) |
| tab | tabella (tablet) |
| syr | syrupus (syrup) |
| tinct | tinctura (tincture) |

### Indian-Specific / Regional Shorthand
| Abbrev / Term | Meaning | Notes |
|---|---|---|
| 1–0–0 / 1–0–1 / 1–1–1 | morning–afternoon–night dosing matrix | Distinctly Indian; ubiquitous |
| R/v | review (follow-up) | Indian shorthand for "review" |
| K/c | known case of | Indian clinical shorthand |
| c/o | complains of | Universal Indian |
| H/o | history of | Universal Indian |
| s/o, d/o, w/o | son of, daughter of, wife of | Indian address/identity convention |
| V/o | village of | Rural identifier |
| NKDA | no known drug allergy | |
| SOS | if required | Used far more than PRN in India |
| BD, TDS | twice/thrice daily | Preferred over BID/TID |
| Tab / Cap / Syr / Inj | tablet / capsule / syrup / injection | Indian standard |
| Inj | injection | |
| Drops | pediatric | |
| Pess | pessary | |
| Crema / cream | topical | |
| Oint | ointment | |
| GTT / gtts | drops | |
| M / F | male / female | |
| Pt | patient | |
| R/O | rule out | |
| D/D | differential diagnosis | |
| # | fracture | Orthopedic shorthand |
| @ | at (e.g., "@ 4L") | |
| → | leading to / progressing to | |
| ↑ / ↓ | increased / decreased | Titration |
| x 5d / x 1wk | for 5 days / for 1 week | Duration |
| OD, BD written as "1OD", "1BD" | 1 tablet once/twice daily | Number prefix = tablets per dose |
| "1–0–1" | one morning, none afternoon, one night | |
| "2–0–2" | two morning, two night | |
| "SOS fever" | take if fever occurs | |
| "SOS pain" | take if pain occurs | |
| "continue" | keep taking existing meds | |
| "stop" | discontinue | |
| "taper" | gradually reduce (steroids) | |
| AKT / ATT | anti-tubercular therapy | India-specific prominence |
| DOTS | directly observed therapy (TB) | |
| RNTCP / NTEP | national TB program | |
| CGHS | Central Government Health Scheme | |
| PMJAY | Pradhan Mantri Jan Arogya Yojana | |
| MO | medical officer | Government setup |
| ANM | auxiliary nurse midwife | Rural |
| OPD / IPD | outpatient / inpatient department | |
| CCU / ICU | coronary / intensive care unit | |
| LSCS | lower segment cesarean section | |
| PV / P1 / P2 | para (obstetric history) | |
| G1P0 / G2P1 | gravida/para notation | |
| LMP / EDD | last menstrual period / expected delivery date | |
| PNC / ANC | postnatal / antenatal care | |
| MTP | medical termination of pregnancy | |
| D&C | dilation and curettage | |
| HSG | hysterosalpingography | |
| IUI / IVF | intrauterine insemination / in vitro fertilization | |
| IUD | intrauterine device | |
| OCP | oral contraceptive pill | |
| POP | progestin-only pill | |
| DMPA | depot medroxyprogesterone | |
| ECP | emergency contraceptive pill | |
| MMR | measles-mumps-rubella | |
| DPT | diphtheria-pertussis-tetanus | |
| OPV | oral polio vaccine | |
| BCG | bacillus Calmette-Guérin | |
| Hep B | hepatitis B | |
| Hib | Haemophilus influenzae type b | |
| RV | rotavirus vaccine | |
| PCV | pneumococcal conjugate vaccine | |
| MR | measles-rubella | |
| JE | Japanese encephalitis | |
| TT | tetanus toxoid | |
| Td | tetanus-diphtheria | |

---

## Section 5: Key Observations for Synthetic Data Generation

- **No single canonical format exists.** The 12 formats above (and hybrids) all appear in real Indian medical data. A synthetic generator must produce all of them, not one "ideal" prescription.
- **Handwriting legibility is a first-class variable.** Even within "handwritten" formats, legibility ranges from neat to near-illegible. The generator must model a legibility spectrum, not assume clean text. This is the core OCR challenge.
- **Abbreviation density is extreme and non-standard.** OD/BD/TD/QID, the 1–0–1 matrix, K/c, c/o, H/o, R/v, SOS, and disease abbreviations (HTN, T2DM, PTB) appear constantly. The same concept has multiple written forms ("1BD", "1–0–0", "once daily", "OD"). The generator must emit all variants.
- **Generic vs. brand names coexist.** Government/PHC = generic (Paracetamol, Metformin). Private = brand (Crocin, Glycomet). Corporate = often both. The generator must know brand-generic pairings for common Indian drugs (Crocin=Paracetamol, Augmentin=Amoxicillin+Clavulanate, Rantac=Ranitidine, Azithral=Azithromycin, Monoceff=Cefpodoxime, Glycomet=Metformin, Glimestar=Glimepiride, Telma=Telmisartan, Atorva=Atorvastatin, Ecosprin=Aspirin, Clavam=Amoxicillin+Clavulanate, Calpol=Paracetamol, Dolo=Paracetamol, Novamox=Amoxicillin, Oflox=Ofloxacin, Cifran=Ciprofloxacin, Zifi=Cefixime, Monoceff=Cefpodoxime, Advent=Amoxicillin+Clavulanate, Meftal=Mefenamic acid, Voveran=Diclofenac, Signoflam, Pan=Pantoprazole, Pan-D, Razo=Rabeprazole, Ocid=Omeprazole, Domstal=Domperidone, Ondem=Ondansetron, Emset=Ondansetron, Vertin=Betahistine, Stugeron=Cinnarizine, Phenergan=Promethazine, Avil=Pheniramine, Cetzine=Cetirizine, Alerid=Cetirizine, Montek=Montelukast, Seroflo=Fluticasone+Salmeterol, Foracort=Budesonide+Formoterol, Duolin=Ipratropium+Salbutamol, Asthalin=Salbutamol, Budecort=Budesonide).
- **Patient context bleeds into the prescription.** Chief complaints, vitals, diagnosis, and history are written on the same slip as medications — not in a separate note. The generator must interleave clinical context with drug orders, not produce a clean "drug-only" Rx.
- **The 1–0–1 matrix notation is distinctly Indian and ubiquitous.** It must be generated alongside OD/BD/TDS. Variants: 1–0–0, 1–0–1, 1–1–1, 0–0–1, 2–0–2, 1–0–2. Sometimes written with dots (1.0.1) or slashes (1/0/1).
- **Dose units are often omitted or inconsistent.** "Tab Crocin 650" (mg implied), "Syr 5ml", "2 puffs", "1 tsp". The generator must produce both explicit-unit and implicit-unit forms.
- **Duration is frequently vague.** "x 5d", "1 week", "SOS", "continue", or just a tablet count with no stop date. The generator must produce vague durations, not always clean "x 7 days".
- **Allergies are often absent.** When present, "NKDA" or "no allergy" or a specific drug. The generator must model the absence (most common) as well as presence.
- **Weight is present in pediatric, absent in most adult Rx.** The generator must condition weight presence on setting and patient type.
- **Vitals are partial and setting-dependent.** Government OPD: maybe BP + temp. Corporate: full vitals table. ER: full set + timestamps. The generator must produce partial vitals, not always complete.
- **Diagnosis is often provisional ("?").** "? viral fever", "? PTB", "? ACS". The generator must emit provisional diagnoses with the "?" prefix, not only confirmed diagnoses.
- **Multiple handwriting styles on one slip.** In government OPD, clerk writes name, nurse writes vitals, doctor writes Rx — three hands. The generator (if rendering images) must model multi-handwriter slips.
- **Stationery variety is large.** Torn notebook page, pre-printed letterhead, government scheme form, EHR printout, telemedicine PDF, ER colored paper. The generator must model stationery as a variable, not assume blank paper.
- **Stamps and letterheads introduce noise.** Hospital stamps, doctor stamps, CGHS/PMJAY logos, barcodes, QR codes — all overlap text and degrade OCR. The generator must include stamp/logo noise.
- **Refill patterns differ from new-Rx patterns.** Chronic follow-ups show titration (↑/↓), "continue", lab-value tables. The generator must produce refill/titration prescriptions, not only new prescriptions.
- **Indian English spellings and conventions.** "colour", "diarrhoea", "oesophagus", "paediatrics", "gynaecology", "orthopaedics". Drug spellings: "Paracetamol" (not "Paracetamol" US), "Cefuroxime", "Amoxicillin". The generator must use Indian/British spellings, not American.
- **Currency and units are Indian.** ₹ for costs (rare on Rx), kg/cm for weight/height, °F for temperature (India uses Fahrenheit for body temp, unlike °C in most of the world), mmHg for BP, mg/dL for glucose/creatinine (not mmol/L). The generator must use Indian units.
- **Names follow Indian conventions.** First name + father/husband name ("Ramesh s/o Suresh", "Smt. Sunita w/o Rajesh"), initials ("R. K. Sharma"), village name in rural ("V/o Kothur"), caste/community surnames (Patel, Reddy, Nair, Iyer, Singh, Khan, Das, Bose). The generator must produce realistic Indian name patterns across regions.
- **Age notation varies.** "45/M", "M/45", "45y male", "1y 6m" (pediatric), "8 months" (infant), "68y" (elderly). The generator must produce all age/sex notations.
- **Telemedicine prescriptions have mandatory fields.** Per Telemedicine Practice Guidelines 2020: doctor reg number, mode of consult (video/audio/text), date/time, digital signature/QR. R-group drugs (Schedule X, narcotics, etc.) cannot be prescribed via audio/text. The generator must produce compliant e-prescriptions.
- **Scheme IDs are mandatory in CGHS/PMJAY.** CGHS beneficiary ID (16-digit), PMJAY ID (golden card). The generator must include these in the relevant formats.
- **The same drug appears in many textual forms.** "Tab Crocin 650", "T.Crocin(650)", "crocin tab 650mg", "Crocin 650mg 1BD", "Paracetamol 650 1–0–1". The generator must produce all surface forms for each drug to train OCR post-correction on variation.
- **Marginalia and insertions are common.** A dose change scrawled above a line, an added drug in the margin, a crossed-out drug. The generator must model insertions, deletions, and corrections — not only clean linear text.
- **Follow-up instructions vary.** "R/v 3d", "R/v 3/7", "review 1 week", "review after 1 month", "SOS consult", "come if no relief". The generator must produce all follow-up notations including the Indian "3/7" (3 days) and "3/52" (3 weeks) shorthand.
- **Advice is often non-drug and terse.** "plenty fluids", "rest", "cold sponging", "diet control", "walk 30 min", "avoid oily food". The generator must include lifestyle advice lines, not only medications.

---

*End of report. This document is intended as ground-truth reference for building a synthetic Indian prescription generator targeting OCR post-correction. All drug names, dosing, and examples are illustrative of real-world Indian prescription practice and should be validated against current clinical guidelines before any clinical use.*