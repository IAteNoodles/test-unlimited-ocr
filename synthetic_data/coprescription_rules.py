# =============================================================================
# Co-prescription Rules for Indian Medical Prescriptions
# =============================================================================
# Purpose:
#   Defines co-prescription patterns for common Indian outpatient conditions.
#   Drugs that are prescribed together for a given condition are clubbed into
#   "prescription lines" (primary / adjunct / symptomatic / prophylaxis) so that
#   a synthetic prescription generator can assemble realistic medication bundles.
#
# Contents:
#   - CONDITIONS        : condition -> prescription pattern (lines of drug options)
#   - ADVICE_TEMPLATES  : condition -> list of non-drug advice strings
#   - FOLLOWUP_DAYS     : condition -> follow-up window + note
#   - DOSAGE_FORMS      : abbreviation -> full form + route
#   - FREQUENCY_CODES   : Indian dosing notation -> meaning + times per day
#   - DURATION_OPTIONS  : common duration strings used in Indian prescriptions
#
# Notes:
#   - All medicine keys referenced in `options` lists match keys defined in the
#     MEDICINES and FDCS dicts of medicines_db.py (snake_case).
#   - Pure data declarations only: no functions, no imports.
#   - File is self-contained and importable.
# =============================================================================


CONDITIONS = {
    # ------------------------------------------------------------------
    # RESPIRATORY / ENT
    # ------------------------------------------------------------------
    "fever_viral": {
        "name": "Viral Fever",
        "icd_code": "R50.9",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["paracetamol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "symptomatic",
                "options": ["cetirizine", "levocetirizine"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "symptomatic",
                "options": ["domperidone", "ondansetron"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
            {
                "type": "symptomatic",
                "options": ["oral_rehydration_salts"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
        ],
    },
    "common_cold": {
        "name": "Common Cold",
        "icd_code": "J00",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": [
                    "phenylephrine_chlorpheniramine_paracetamol",
                    "caffeine_paracetamol_phenylephrine",
                ],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "symptomatic",
                "options": ["cetirizine", "levocetirizine"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.5,
            },
            {
                "type": "symptomatic",
                "options": ["vitamin_c"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
        ],
    },
    "pharyngitis": {
        "name": "Acute Pharyngitis",
        "icd_code": "J02.9",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["amoxicillin", "azithromycin", "amoxicillin_clavulanate"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.7,
            },
            {
                "type": "symptomatic",
                "options": ["paracetamol", "ibuprofen_paracetamol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "symptomatic",
                "options": ["ambroxol", "herbal_cough_syrups"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "symptomatic",
                "options": ["levocetirizine", "cetirizine"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "adjunct",
                "options": ["pantoprazole"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.5,
            },
        ],
    },
    "tonsillitis": {
        "name": "Acute Tonsillitis",
        "icd_code": "J03.9",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["amoxicillin", "amoxicillin_clavulanate", "azithromycin", "cephalexin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.9,
            },
            {
                "type": "symptomatic",
                "options": ["paracetamol", "ibuprofen_paracetamol", "diclofenac_paracetamol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "symptomatic",
                "options": ["ambroxol", "herbal_cough_syrups"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
            {
                "type": "adjunct",
                "options": ["pantoprazole"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.5,
            },
        ],
    },
    "acute_bronchitis": {
        "name": "Acute Bronchitis",
        "icd_code": "J20.9",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["amoxicillin", "azithromycin", "doxycycline"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.6,
            },
            {
                "type": "symptomatic",
                "options": ["ambroxol", "guaifenesin", "bromhexine", "salbutamol_guaifenesin_bromhexine"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "symptomatic",
                "options": ["salbutamol", "levosalbutamol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "symptomatic",
                "options": ["paracetamol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.5,
            },
            {
                "type": "symptomatic",
                "options": ["levocetirizine", "cetirizine"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "adjunct",
                "options": ["pantoprazole"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
        ],
    },
    "pneumonia": {
        "name": "Pneumonia",
        "icd_code": "J18.9",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["amoxicillin", "amoxicillin_clavulanate", "azithromycin", "ceftriaxone"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.9,
            },
            {
                "type": "symptomatic",
                "options": ["ambroxol", "guaifenesin", "salbutamol_guaifenesin_bromhexine"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.9,
            },
            {
                "type": "symptomatic",
                "options": ["levosalbutamol", "salbutamol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "symptomatic",
                "options": ["paracetamol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.6,
            },
            {
                "type": "adjunct",
                "options": ["pantoprazole"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.5,
            },
        ],
    },

    # ------------------------------------------------------------------
    # GASTROINTESTINAL
    # ------------------------------------------------------------------
    "uti": {
        "name": "Urinary Tract Infection",
        "icd_code": "N39.0",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["ciprofloxacin", "norfloxacin", "ofloxacin", "levofloxacin", "cotrimoxazole"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "symptomatic",
                "options": ["paracetamol", "ibuprofen_paracetamol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.5,
            },
            {
                "type": "symptomatic",
                "options": ["oral_rehydration_salts"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "adjunct",
                "options": ["pantoprazole"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
        ],
    },
    "gastroenteritis": {
        "name": "Acute Gastroenteritis",
        "icd_code": "A09",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["ofloxacin_ornidazole", "metronidazole", "ciprofloxacin", "ofloxacin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.7,
            },
            {
                "type": "symptomatic",
                "options": ["oral_rehydration_salts"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "symptomatic",
                "options": ["loperamide"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "symptomatic",
                "options": ["ondansetron", "domperidone"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.5,
            },
            {
                "type": "symptomatic",
                "options": ["paracetamol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
            {
                "type": "adjunct",
                "options": ["zinc"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "adjunct",
                "options": ["b_complex"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.2,
            },
        ],
    },
    "dyspepsia": {
        "name": "Dyspepsia",
        "icd_code": "K30",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["pantoprazole", "rabeprazole", "omeprazole", "esomeprazole"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["pantoprazole_domperidone", "rabeprazole_domperidone"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.6,
            },
            {
                "type": "symptomatic",
                "options": [
                    "aluminum_hydroxide_magnesium_hydroxide_oxetacaine",
                    "aluminum_hydroxide_magnesium_hydroxide_simethicone",
                ],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "symptomatic",
                "options": ["domperidone", "metoclopramide"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
        ],
    },
    "gerd": {
        "name": "Gastroesophageal Reflux Disease",
        "icd_code": "K21.9",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["pantoprazole", "rabeprazole", "esomeprazole", "omeprazole"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["pantoprazole_domperidone", "rabeprazole_domperidone"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.7,
            },
            {
                "type": "symptomatic",
                "options": [
                    "aluminum_hydroxide_magnesium_hydroxide_oxetacaine",
                    "aluminum_hydroxide_magnesium_hydroxide_simethicone",
                ],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
            {
                "type": "adjunct",
                "options": ["ranitidine", "famotidine"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.2,
            },
        ],
    },
    "peptic_ulcer": {
        "name": "Peptic Ulcer Disease",
        "icd_code": "K27.9",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["pantoprazole", "rabeprazole", "esomeprazole"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["amoxicillin", "amoxicillin_clavulanate"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.6,
            },
            {
                "type": "adjunct",
                "options": ["metronidazole", "ofloxacin_ornidazole"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "symptomatic",
                "options": ["aluminum_hydroxide_magnesium_hydroxide_oxetacaine"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
        ],
    },
    "constipation": {
        "name": "Constipation",
        "icd_code": "K59.0",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["lactulose", "bisacodyl"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["pantoprazole"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.2,
            },
        ],
    },

    # ------------------------------------------------------------------
    # CARDIOVASCULAR / METABOLIC
    # ------------------------------------------------------------------
    "hypertension": {
        "name": "Essential Hypertension",
        "icd_code": "I10",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": [
                    "amlodipine",
                    "telmisartan",
                    "losartan",
                    "ramipril",
                    "amlodipine_telmisartan",
                    "losartan_hydrochlorothiazide",
                ],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["atenolol", "metoprolol", "telmisartan"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
            {
                "type": "prophylaxis",
                "options": ["aspirin", "atorvastatin_aspirin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
            {
                "type": "adjunct",
                "options": ["atorvastatin", "rosuvastatin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
        ],
    },
    "diabetes_type2": {
        "name": "Type 2 Diabetes Mellitus",
        "icd_code": "E11.9",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["metformin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": [
                    "glimepiride_metformin",
                    "sitagliptin_metformin",
                    "vildagliptin_metformin",
                    "glimepiride",
                ],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.5,
            },
            {
                "type": "adjunct",
                "options": ["voglibose", "acarbose", "dapagliflozin", "empagliflozin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
            {
                "type": "prophylaxis",
                "options": ["aspirin", "atorvastatin_aspirin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
            {
                "type": "adjunct",
                "options": ["atorvastatin", "rosuvastatin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
        ],
    },
    "dyslipidemia": {
        "name": "Dyslipidemia",
        "icd_code": "E78.5",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["atorvastatin", "rosuvastatin", "simvastatin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["fenofibrate", "atorvastatin_fenofibrate", "ezetimibe"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "prophylaxis",
                "options": ["aspirin", "atorvastatin_aspirin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
        ],
    },
    "hypothyroidism": {
        "name": "Hypothyroidism",
        "icd_code": "E03.9",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["levothyroxine"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["calcium_vitamin_d3"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.2,
            },
            {
                "type": "adjunct",
                "options": ["b_complex"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.1,
            },
        ],
    },
    "hyperthyroidism": {
        "name": "Hyperthyroidism",
        "icd_code": "E05.9",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["carbimazole", "methimazole", "propylthiouracil"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["atenolol", "metoprolol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "adjunct",
                "options": ["levothyroxine"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.1,
            },
        ],
    },

    # ------------------------------------------------------------------
    # RESPIRATORY - CHRONIC / ALLERGY
    # ------------------------------------------------------------------
    "asthma": {
        "name": "Bronchial Asthma",
        "icd_code": "J45.909",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["formoterol_budesonide", "budesonide", "salbutamol", "levosalbutamol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["montelukast", "levocetirizine_montelukast"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.5,
            },
            {
                "type": "symptomatic",
                "options": ["salbutamol_guaifenesin_bromhexine"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
            {
                "type": "adjunct",
                "options": ["prednisolone"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.2,
            },
        ],
    },
    "copd": {
        "name": "Chronic Obstructive Pulmonary Disease",
        "icd_code": "J44.9",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["formoterol_budesonide", "tiotropium", "ipratropium"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["salbutamol", "levosalbutamol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "symptomatic",
                "options": ["ambroxol", "guaifenesin", "salbutamol_guaifenesin_bromhexine"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "adjunct",
                "options": ["prednisolone"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
        ],
    },
    "allergic_rhinitis": {
        "name": "Allergic Rhinitis",
        "icd_code": "J30.9",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["cetirizine", "levocetirizine", "fexofenadine", "loratadine"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["levocetirizine_montelukast", "montelukast"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.5,
            },
            {
                "type": "symptomatic",
                "options": ["mometasone"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
            {
                "type": "symptomatic",
                "options": ["phenylephrine_chlorpheniramine_paracetamol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.2,
            },
        ],
    },

    # ------------------------------------------------------------------
    # NEUROLOGY / PSYCHIATRY
    # ------------------------------------------------------------------
    "migraine": {
        "name": "Migraine",
        "icd_code": "G43.909",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["naproxen", "diclofenac", "ibuprofen_paracetamol", "aceclofenac_paracetamol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "symptomatic",
                "options": ["domperidone", "metoclopramide", "ondansetron"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.6,
            },
            {
                "type": "prophylaxis",
                "options": ["atenolol", "metoprolol", "valproate"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
            {
                "type": "symptomatic",
                "options": ["paracetamol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
        ],
    },
    "anxiety": {
        "name": "Anxiety Disorder",
        "icd_code": "F41.1",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["alprazolam", "clonazepam", "diazepam", "lorazepam"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.7,
            },
            {
                "type": "adjunct",
                "options": ["hydroxyzine", "pregabalin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
            {
                "type": "adjunct",
                "options": ["zolpidem", "zopiclone"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.2,
            },
        ],
    },
    "insomnia": {
        "name": "Insomnia",
        "icd_code": "G47.00",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["zolpidem", "zopiclone", "alprazolam", "lorazepam"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["hydroxyzine", "promethazine"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
        ],
    },
    "epilepsy": {
        "name": "Epilepsy",
        "icd_code": "G40.909",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": [
                    "valproate",
                    "carbamazepine",
                    "phenytoin",
                    "levetiracetam",
                    "lamotrigine",
                    "clonazepam",
                ],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["folic_acid"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
        ],
    },

    # ------------------------------------------------------------------
    # MUSCULOSKELETAL / PAIN
    # ------------------------------------------------------------------
    "osteoarthritis": {
        "name": "Osteoarthritis",
        "icd_code": "M19.90",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": [
                    "paracetamol",
                    "ibuprofen_paracetamol",
                    "diclofenac_paracetamol",
                    "aceclofenac_paracetamol",
                ],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["glucosamine", "glucosamine_chondroitin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "symptomatic",
                "options": ["diclofenac", "aceclofenac", "naproxen"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "adjunct",
                "options": ["thiocolchicoside", "baclofen"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.2,
            },
            {
                "type": "adjunct",
                "options": ["methylcobalamin", "pregabalin_methylcobalamin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.2,
            },
            {
                "type": "adjunct",
                "options": ["pantoprazole"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
        ],
    },
    "rheumatoid_arthritis": {
        "name": "Rheumatoid Arthritis",
        "icd_code": "M06.9",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["ibuprofen_paracetamol", "diclofenac", "aceclofenac", "naproxen"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.9,
            },
            {
                "type": "adjunct",
                "options": ["prednisolone"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "adjunct",
                "options": ["pantoprazole"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.5,
            },
            {
                "type": "adjunct",
                "options": ["folic_acid"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
            {
                "type": "adjunct",
                "options": ["calcium_vitamin_d3"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
        ],
    },
    "low_back_pain": {
        "name": "Low Back Pain",
        "icd_code": "M54.5",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": [
                    "ibuprofen_paracetamol",
                    "diclofenac_paracetamol",
                    "aceclofenac_paracetamol",
                    "aceclofenac_paracetamol_serratiopeptidase",
                ],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": [
                    "thiocolchicoside",
                    "baclofen",
                    "cyclobenzaprine",
                    "chlorzoxazone_ibuprofen_paracetamol",
                ],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.6,
            },
            {
                "type": "adjunct",
                "options": ["pregabalin", "gabapentin", "pregabalin_methylcobalamin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
            {
                "type": "adjunct",
                "options": ["pantoprazole"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "symptomatic",
                "options": ["diclofenac"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
        ],
    },
    "gout": {
        "name": "Gout",
        "icd_code": "M10.9",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["colchicine", "naproxen", "diclofenac", "ibuprofen_paracetamol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["allopurinol", "febuxostat"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "adjunct",
                "options": ["prednisolone"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
            {
                "type": "adjunct",
                "options": ["pantoprazole"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
        ],
    },

    # ------------------------------------------------------------------
    # GYNECOLOGY
    # ------------------------------------------------------------------
    "dysmenorrhea": {
        "name": "Dysmenorrhea",
        "icd_code": "N94.4",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["mefenamic_acid", "ibuprofen_paracetamol", "diclofenac_paracetamol", "naproxen"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["tranexamic_acid_mefenamic_acid", "tranexamic_acid"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "symptomatic",
                "options": ["paracetamol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
        ],
    },

    # ------------------------------------------------------------------
    # NUTRITIONAL DEFICIENCIES
    # ------------------------------------------------------------------
    "anemia": {
        "name": "Iron Deficiency Anemia",
        "icd_code": "D50.9",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["iron_folic_acid"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["folic_acid", "vitamin_c"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.5,
            },
            {
                "type": "adjunct",
                "options": ["b_complex", "methylcobalamin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
            {
                "type": "adjunct",
                "options": ["zinc"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.2,
            },
        ],
    },
    "vitamin_d_deficiency": {
        "name": "Vitamin D Deficiency",
        "icd_code": "E55.9",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["cholecalciferol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["calcium_vitamin_d3"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.5,
            },
            {
                "type": "adjunct",
                "options": ["b_complex", "multivitamin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.2,
            },
        ],
    },
    "b12_deficiency": {
        "name": "Vitamin B12 Deficiency",
        "icd_code": "D51.0",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["methylcobalamin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["methylcobalamin_alpha_lipoic_acid_folic_acid", "b_complex"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "adjunct",
                "options": ["folic_acid"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
            {
                "type": "adjunct",
                "options": ["pregabalin_methylcobalamin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.2,
            },
        ],
    },

    # ------------------------------------------------------------------
    # DERMATOLOGY
    # ------------------------------------------------------------------
    "fungal_infection_skin": {
        "name": "Fungal Skin Infection",
        "icd_code": "B36.9",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["clotrimazole", "terbinafine", "ketoconazole", "itraconazole", "fluconazole"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["betamethasone_clotrimazole_gentamicin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
            {
                "type": "adjunct",
                "options": ["levocetirizine", "cetirizine"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "adjunct",
                "options": ["griseofulvin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.2,
            },
        ],
    },
    "scabies": {
        "name": "Scabies",
        "icd_code": "B86",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["ivermectin", "ivermectin_albendazole"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["levocetirizine", "cetirizine", "hydroxyzine"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.6,
            },
            {
                "type": "adjunct",
                "options": ["betamethasone_clotrimazole_gentamicin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
        ],
    },
    "acne": {
        "name": "Acne Vulgaris",
        "icd_code": "L70.0",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["clindamycin_adapalene", "benzoyl_peroxide", "clindamycin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["doxycycline", "azithromycin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "adjunct",
                "options": ["isotretinoin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.2,
            },
            {
                "type": "adjunct",
                "options": ["pantoprazole"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.2,
            },
        ],
    },
    "cellulitis": {
        "name": "Cellulitis",
        "icd_code": "L03.9",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["amoxicillin_clavulanate", "cephalexin", "cefuroxime", "clindamycin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "symptomatic",
                "options": ["paracetamol", "ibuprofen_paracetamol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.5,
            },
            {
                "type": "adjunct",
                "options": ["serratiopeptidase", "trypsin_chymotrypsin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "adjunct",
                "options": ["pantoprazole"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
        ],
    },

    # ------------------------------------------------------------------
    # OPHTHALMIC / OTIC / DENTAL
    # ------------------------------------------------------------------
    "conjunctivitis": {
        "name": "Conjunctivitis",
        "icd_code": "H10.9",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["moxifloxacin", "tobramycin", "chloramphenicol", "ciprofloxacin", "ofloxacin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["dexamethasone_moxifloxacin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
            {
                "type": "symptomatic",
                "options": ["cetirizine", "levocetirizine"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
        ],
    },
    "otitis_media": {
        "name": "Acute Otitis Media",
        "icd_code": "H66.9",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["amoxicillin", "amoxicillin_clavulanate", "azithromycin", "cefixime"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "symptomatic",
                "options": ["paracetamol", "ibuprofen_paracetamol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.8,
            },
            {
                "type": "adjunct",
                "options": ["ofloxacin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "symptomatic",
                "options": ["phenylephrine_chlorpheniramine_paracetamol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "adjunct",
                "options": ["pantoprazole"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
        ],
    },
    "dental_infection": {
        "name": "Dental Infection",
        "icd_code": "K04.7",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["amoxicillin", "amoxicillin_clavulanate", "metronidazole", "ofloxacin_ornidazole"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "symptomatic",
                "options": ["ibuprofen_paracetamol", "diclofenac_paracetamol", "paracetamol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["aceclofenac_paracetamol_serratiopeptidase", "serratiopeptidase"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "adjunct",
                "options": ["pantoprazole"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
        ],
    },

    # ------------------------------------------------------------------
    # INFECTIOUS DISEASE
    # ------------------------------------------------------------------
    "worm_infestation": {
        "name": "Intestinal Worm Infestation",
        "icd_code": "B82.9",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["albendazole", "mebendazole", "ivermectin_albendazole"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["ivermectin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
            {
                "type": "adjunct",
                "options": ["iron_folic_acid"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.2,
            },
        ],
    },
    "typhoid": {
        "name": "Enteric Fever (Typhoid)",
        "icd_code": "A01.0",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["cefixime", "azithromycin", "ciprofloxacin", "ceftriaxone"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "symptomatic",
                "options": ["paracetamol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["oral_rehydration_salts"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.5,
            },
            {
                "type": "adjunct",
                "options": ["pantoprazole"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "adjunct",
                "options": ["zinc"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
            {
                "type": "adjunct",
                "options": ["b_complex"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.2,
            },
        ],
    },
    "dengue": {
        "name": "Dengue Fever",
        "icd_code": "A90",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["paracetamol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["oral_rehydration_salts"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.8,
            },
            {
                "type": "adjunct",
                "options": ["zinc"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
            {
                "type": "adjunct",
                "options": ["b_complex"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
            {
                "type": "symptomatic",
                "options": ["ondansetron", "domperidone"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
        ],
    },
    "malaria": {
        "name": "Malaria",
        "icd_code": "B54",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["paracetamol"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["oral_rehydration_salts"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.6,
            },
            {
                "type": "adjunct",
                "options": ["zinc"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
            {
                "type": "adjunct",
                "options": ["folic_acid"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.2,
            },
            {
                "type": "symptomatic",
                "options": ["ondansetron", "domperidone"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.3,
            },
        ],
    },

    # ------------------------------------------------------------------
    # UROLOGY
    # ------------------------------------------------------------------
    "bph": {
        "name": "Benign Prostatic Hyperplasia",
        "icd_code": "N40.0",
        "prescription_pattern": [
            {
                "type": "primary",
                "options": ["tamsulosin"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 1.0,
            },
            {
                "type": "adjunct",
                "options": ["dutasteride", "finasteride"],
                "min_pick": 1,
                "max_pick": 1,
                "weight": 0.4,
            },
        ],
    },
}


# =============================================================================
# Advice Templates (non-drug advice commonly given in Indian prescriptions)
# =============================================================================
ADVICE_TEMPLATES = {
    "fever_viral": [
        "Take plenty of fluids",
        "Take adequate rest",
        "SOS for fever",
        "Cold compresses for fever",
        "Review after 3 days if fever persists",
    ],
    "common_cold": [
        "Take plenty of fluids",
        "Steam inhalation 2-3 times daily",
        "Take rest",
        "Avoid cold beverages",
        "Review after 5 days if not improving",
    ],
    "pharyngitis": [
        "Gargle with warm salt water",
        "Take warm fluids",
        "Complete the course of antibiotics",
        "Avoid cold beverages",
        "Voice rest",
        "Review after 3 days",
    ],
    "tonsillitis": [
        "Gargle with warm salt water",
        "Take warm fluids",
        "Complete the course of antibiotics",
        "Take soft diet",
        "Avoid cold beverages",
        "Review after 5 days",
    ],
    "acute_bronchitis": [
        "Take plenty of fluids",
        "Avoid cold beverages",
        "Complete the course of antibiotics",
        "Steam inhalation 2-3 times daily",
        "Avoid smoking",
        "Review after 5 days",
    ],
    "pneumonia": [
        "Take plenty of fluids",
        "Take adequate rest",
        "Complete the course of antibiotics",
        "Avoid smoking",
        "Review after 3 days",
        "Report immediately if breathlessness worsens",
    ],
    "uti": [
        "Take plenty of fluids",
        "Complete the course of antibiotics",
        "Maintain hygiene",
        "Avoid holding urine",
        "Review after 5 days",
    ],
    "gastroenteritis": [
        "Take ORS frequently",
        "Take bland diet",
        "Avoid outside food",
        "Avoid milk and milk products",
        "Maintain hydration",
        "Review after 3 days if symptoms persist",
    ],
    "dyspepsia": [
        "Take medication after food",
        "Avoid spicy and oily food",
        "Eat small frequent meals",
        "Avoid lying down immediately after food",
        "Review after 1 week",
    ],
    "gerd": [
        "Avoid spicy and oily food",
        "Eat small frequent meals",
        "Avoid lying down immediately after food",
        "Elevate head end of bed",
        "Avoid tea, coffee and alcohol",
        "Review after 2 weeks",
    ],
    "peptic_ulcer": [
        "Complete the course of antibiotics",
        "Avoid spicy and oily food",
        "Eat small frequent meals",
        "Avoid NSAIDs",
        "Avoid alcohol and smoking",
        "Review after 2 weeks",
    ],
    "constipation": [
        "Take plenty of fluids",
        "Take high fibre diet",
        "Regular exercise",
        "Eat fresh fruits and vegetables",
        "Review after 1 week",
    ],
    "hypertension": [
        "Monitor blood pressure regularly",
        "Reduce salt intake",
        "Regular exercise",
        "Avoid stress",
        "Take medication regularly",
        "Review after 2 weeks",
    ],
    "diabetes_type2": [
        "Check blood sugar levels regularly",
        "Avoid sweets and sugar",
        "Regular exercise",
        "Take medication regularly",
        "Maintain healthy diet",
        "Review after 1 month",
    ],
    "dyslipidemia": [
        "Avoid oily and fried food",
        "Regular exercise",
        "Take low fat diet",
        "Maintain healthy weight",
        "Review after 1 month",
    ],
    "hypothyroidism": [
        "Take medication empty stomach in morning",
        "Take medication regularly",
        "Repeat thyroid profile after 6 weeks",
        "Review after 6 weeks",
    ],
    "hyperthyroidism": [
        "Take medication regularly",
        "Avoid iodine rich food",
        "Monitor pulse regularly",
        "Repeat thyroid profile after 6 weeks",
        "Review after 6 weeks",
    ],
    "asthma": [
        "Use inhaler regularly as prescribed",
        "Avoid known triggers",
        "Avoid dust and pollen",
        "Avoid smoking",
        "Use spacer with inhaler",
        "Review after 1 month",
    ],
    "copd": [
        "Use inhaler regularly as prescribed",
        "Avoid smoking",
        "Avoid dust and pollution",
        "Breathing exercises",
        "Review after 1 month",
    ],
    "allergic_rhinitis": [
        "Avoid dust and pollen",
        "Use mask when going out",
        "Keep surroundings clean",
        "Avoid known allergens",
        "Review after 2 weeks",
    ],
    "migraine": [
        "Avoid known triggers",
        "Take adequate rest",
        "Maintain sleep hygiene",
        "Avoid bright light and loud noise",
        "Maintain headache diary",
        "Review after 1 month",
    ],
    "anxiety": [
        "Regular exercise",
        "Practice relaxation techniques",
        "Maintain sleep hygiene",
        "Avoid caffeine and alcohol",
        "Review after 2 weeks",
    ],
    "insomnia": [
        "Maintain sleep hygiene",
        "Avoid caffeine in evening",
        "Avoid screen time before bed",
        "Regular exercise",
        "Review after 2 weeks",
    ],
    "epilepsy": [
        "Take medication regularly",
        "Do not stop medication abruptly",
        "Avoid driving",
        "Avoid swimming alone",
        "Maintain sleep hygiene",
        "Review after 1 month",
    ],
    "osteoarthritis": [
        "Take medication after food",
        "Regular exercise",
        "Weight reduction",
        "Avoid squatting and stairs",
        "Hot fomentation",
        "Review after 2 weeks",
    ],
    "rheumatoid_arthritis": [
        "Take medication after food",
        "Regular exercise",
        "Joint protection",
        "Hot fomentation",
        "Review after 2 weeks",
    ],
    "low_back_pain": [
        "Take medication after food",
        "Avoid heavy lifting",
        "Maintain proper posture",
        "Hot fomentation",
        "Regular back exercises",
        "Review after 1 week",
    ],
    "gout": [
        "Avoid red meat and organ meat",
        "Avoid alcohol",
        "Take plenty of fluids",
        "Take medication after food",
        "Review after 1 week",
    ],
    "dysmenorrhea": [
        "Take medication after food",
        "Hot fomentation",
        "Regular exercise",
        "Take warm fluids",
        "Review if symptoms persist",
    ],
    "anemia": [
        "Take iron rich diet",
        "Take medication after food",
        "Avoid tea and coffee with meals",
        "Take vitamin C rich food",
        "Review after 1 month",
    ],
    "vitamin_d_deficiency": [
        "Sun exposure 15-20 minutes daily",
        "Take vitamin D rich food",
        "Take medication as prescribed",
        "Review after 1 month",
    ],
    "b12_deficiency": [
        "Take non-vegetarian food",
        "Take dairy products",
        "Take medication regularly",
        "Review after 1 month",
    ],
    "fungal_infection_skin": [
        "Keep skin clean and dry",
        "Use clean clothes",
        "Avoid sharing personal items",
        "Complete the course of medication",
        "Review after 2 weeks",
    ],
    "scabies": [
        "Wash clothes and bed linen in hot water",
        "Treat all family members",
        "Apply medication on whole body below neck",
        "Trim nails",
        "Review after 1 week",
    ],
    "acne": [
        "Wash face twice daily",
        "Avoid oily cosmetics",
        "Do not squeeze lesions",
        "Avoid oily food",
        "Review after 1 month",
    ],
    "cellulitis": [
        "Complete the course of antibiotics",
        "Elevate affected limb",
        "Mark the margin of redness",
        "Take medication after food",
        "Review after 3 days",
    ],
    "conjunctivitis": [
        "Do not touch eyes",
        "Use clean handkerchief",
        "Avoid sharing personal items",
        "Apply eye drops as prescribed",
        "Review after 5 days",
    ],
    "otitis_media": [
        "Complete the course of antibiotics",
        "Keep ear dry",
        "Avoid inserting anything in ear",
        "Take medication after food",
        "Review after 5 days",
    ],
    "dental_infection": [
        "Complete the course of antibiotics",
        "Warm saline gargles",
        "Consult dentist",
        "Take medication after food",
        "Review after 3 days",
    ],
    "worm_infestation": [
        "Take medication as single dose",
        "Maintain hygiene",
        "Wash hands before meals",
        "Repeat dose after 2 weeks",
        "Deworm all family members",
    ],
    "typhoid": [
        "Complete the course of antibiotics",
        "Take plenty of fluids",
        "Take bland diet",
        "Avoid outside food",
        "Take medication after food",
        "Review after 5 days",
    ],
    "dengue": [
        "Take plenty of fluids",
        "Take paracetamol for fever",
        "Avoid NSAIDs",
        "Monitor platelet count",
        "Report immediately if bleeding occurs",
        "Review after 3 days",
    ],
    "malaria": [
        "Complete the course of medication",
        "Take plenty of fluids",
        "Use mosquito net",
        "Monitor for complications",
        "Review after 3 days",
    ],
    "bph": [
        "Take medication at bedtime",
        "Avoid fluids at night",
        "Avoid caffeine and alcohol",
        "Regular exercise",
        "Review after 1 month",
    ],
}


# =============================================================================
# Follow-up Windows
# =============================================================================
FOLLOWUP_DAYS = {
    "fever_viral": {"min_days": 3, "max_days": 5, "note": "Review if fever persists"},
    "common_cold": {"min_days": 5, "max_days": 7, "note": "Review if symptoms persist"},
    "pharyngitis": {"min_days": 3, "max_days": 5, "note": "Review if sore throat persists"},
    "tonsillitis": {"min_days": 5, "max_days": 7, "note": "Review after antibiotic course"},
    "acute_bronchitis": {"min_days": 5, "max_days": 7, "note": "Review if cough persists"},
    "pneumonia": {"min_days": 3, "max_days": 7, "note": "Review if breathlessness worsens"},
    "uti": {"min_days": 5, "max_days": 7, "note": "Repeat urine culture if symptoms persist"},
    "gastroenteritis": {"min_days": 3, "max_days": 5, "note": "Review if diarrhea persists"},
    "dyspepsia": {"min_days": 7, "max_days": 14, "note": "Review if symptoms persist"},
    "gerd": {"min_days": 14, "max_days": 30, "note": "Routine follow-up"},
    "peptic_ulcer": {"min_days": 14, "max_days": 30, "note": "Repeat endoscopy if symptoms persist"},
    "constipation": {"min_days": 7, "max_days": 14, "note": "Review if no relief"},
    "hypertension": {"min_days": 14, "max_days": 30, "note": "Monitor BP regularly"},
    "diabetes_type2": {"min_days": 30, "max_days": 90, "note": "Check HbA1c after 3 months"},
    "dyslipidemia": {"min_days": 30, "max_days": 90, "note": "Repeat lipid profile after 3 months"},
    "hypothyroidism": {"min_days": 42, "max_days": 60, "note": "Repeat thyroid profile after 6 weeks"},
    "hyperthyroidism": {"min_days": 42, "max_days": 60, "note": "Repeat thyroid profile after 6 weeks"},
    "asthma": {"min_days": 30, "max_days": 90, "note": "Routine follow-up"},
    "copd": {"min_days": 30, "max_days": 90, "note": "Routine follow-up"},
    "allergic_rhinitis": {"min_days": 14, "max_days": 30, "note": "Review if symptoms persist"},
    "migraine": {"min_days": 30, "max_days": 60, "note": "Maintain headache diary"},
    "anxiety": {"min_days": 14, "max_days": 30, "note": "Review for medication response"},
    "insomnia": {"min_days": 14, "max_days": 30, "note": "Review for sleep improvement"},
    "epilepsy": {"min_days": 30, "max_days": 90, "note": "Routine follow-up, do not stop abruptly"},
    "osteoarthritis": {"min_days": 14, "max_days": 30, "note": "Review if pain persists"},
    "rheumatoid_arthritis": {"min_days": 14, "max_days": 30, "note": "Routine follow-up"},
    "low_back_pain": {"min_days": 7, "max_days": 14, "note": "Review if pain persists"},
    "gout": {"min_days": 7, "max_days": 14, "note": "Repeat uric acid after 2 weeks"},
    "dysmenorrhea": {"min_days": 30, "max_days": 60, "note": "Review in next cycle"},
    "anemia": {"min_days": 30, "max_days": 60, "note": "Repeat CBC after 1 month"},
    "vitamin_d_deficiency": {"min_days": 30, "max_days": 60, "note": "Repeat vitamin D levels"},
    "b12_deficiency": {"min_days": 30, "max_days": 60, "note": "Repeat B12 levels"},
    "fungal_infection_skin": {"min_days": 14, "max_days": 30, "note": "Review if lesions persist"},
    "scabies": {"min_days": 7, "max_days": 14, "note": "Review for itching and new lesions"},
    "acne": {"min_days": 30, "max_days": 60, "note": "Review for treatment response"},
    "cellulitis": {"min_days": 3, "max_days": 7, "note": "Review if redness spreads"},
    "conjunctivitis": {"min_days": 5, "max_days": 7, "note": "Review if symptoms persist"},
    "otitis_media": {"min_days": 5, "max_days": 7, "note": "Review if ear pain persists"},
    "dental_infection": {"min_days": 3, "max_days": 5, "note": "Consult dentist"},
    "worm_infestation": {"min_days": 14, "max_days": 21, "note": "Repeat dose after 2 weeks"},
    "typhoid": {"min_days": 5, "max_days": 7, "note": "Review if fever persists"},
    "dengue": {"min_days": 3, "max_days": 5, "note": "Monitor platelet count"},
    "malaria": {"min_days": 3, "max_days": 7, "note": "Review if fever persists"},
    "bph": {"min_days": 30, "max_days": 60, "note": "Routine follow-up"},
}


# =============================================================================
# Dosage Forms (Indian prescription abbreviations)
# =============================================================================
DOSAGE_FORMS = {
    "Tab": {"abbr": "Tab", "full": "Tablet", "route": "oral"},
    "Cap": {"abbr": "Cap", "full": "Capsule", "route": "oral"},
    "Syr": {"abbr": "Syr", "full": "Syrup", "route": "oral"},
    "Susp": {"abbr": "Susp", "full": "Suspension", "route": "oral"},
    "Inj": {"abbr": "Inj", "full": "Injection", "route": "IV/IM"},
    "Drops": {"abbr": "Drops", "full": "Drops", "route": "oral/ophthalmic"},
    "Eye Drops": {"abbr": "Eye Drops", "full": "Eye Drops", "route": "ophthalmic"},
    "Ear Drops": {"abbr": "Ear Drops", "full": "Ear Drops", "route": "otic"},
    "Cream": {"abbr": "Cream", "full": "Cream", "route": "topical"},
    "Oint": {"abbr": "Oint", "full": "Ointment", "route": "topical"},
    "Gel": {"abbr": "Gel", "full": "Gel", "route": "topical"},
    "Lotion": {"abbr": "Lotion", "full": "Lotion", "route": "topical"},
    "Powder": {"abbr": "Powder", "full": "Powder", "route": "topical"},
    "Inhaler": {"abbr": "Inhaler", "full": "Inhaler", "route": "inhalation"},
    "Rotacap": {"abbr": "Rotacap", "full": "Rotacap", "route": "inhalation"},
    "Respule": {"abbr": "Respule", "full": "Respule", "route": "inhalation"},
    "Spray": {"abbr": "Spray", "full": "Spray", "route": "nasal/topical"},
    "Nasal Spray": {"abbr": "Nasal Spray", "full": "Nasal Spray", "route": "nasal"},
    "Sachet": {"abbr": "Sachet", "full": "Sachet", "route": "oral"},
    "Granules": {"abbr": "Granules", "full": "Granules", "route": "oral"},
    "Chewable Tab": {"abbr": "Chewable Tab", "full": "Chewable Tablet", "route": "oral"},
    "Lozenge": {"abbr": "Lozenge", "full": "Lozenge", "route": "oral"},
    "Mouth Paint": {"abbr": "Mouth Paint", "full": "Mouth Paint", "route": "oral"},
    "Dental Paste": {"abbr": "Dental Paste", "full": "Dental Paste", "route": "dental"},
    "Supp": {"abbr": "Supp", "full": "Suppository", "route": "rectal"},
    "Vaginal Tab": {"abbr": "Vaginal Tab", "full": "Vaginal Tablet", "route": "vaginal"},
    "IV": {"abbr": "IV", "full": "IV Fluid", "route": "IV"},
    "Vial": {"abbr": "Vial", "full": "Vial", "route": "IV/IM"},
    "Cartridge": {"abbr": "Cartridge", "full": "Cartridge", "route": "subcutaneous"},
    "Pen": {"abbr": "Pen", "full": "Pen", "route": "subcutaneous"},
    "Patch": {"abbr": "Patch", "full": "Patch", "route": "transdermal"},
    "Kit": {"abbr": "Kit", "full": "Kit", "route": "oral"},
}


# =============================================================================
# Frequency Codes (Indian dosing notation)
# =============================================================================
FREQUENCY_CODES = {
    "1-0-0": {"code": "1-0-0", "meaning": "Once daily morning", "times_per_day": 1},
    "0-0-1": {"code": "0-0-1", "meaning": "Once daily night", "times_per_day": 1},
    "0-1-0": {"code": "0-1-0", "meaning": "Once daily afternoon", "times_per_day": 1},
    "1-0-1": {"code": "1-0-1", "meaning": "Twice daily morning and night", "times_per_day": 2},
    "1-1-1": {"code": "1-1-1", "meaning": "Three times daily", "times_per_day": 3},
    "0-1-1": {"code": "0-1-1", "meaning": "Twice daily afternoon and night", "times_per_day": 2},
    "1-1-0": {"code": "1-1-0", "meaning": "Twice daily morning and afternoon", "times_per_day": 2},
    "2-0-2": {"code": "2-0-2", "meaning": "Twice daily two tablets morning and night", "times_per_day": 2},
    "OD": {"code": "OD", "meaning": "Once daily", "times_per_day": 1},
    "BD": {"code": "BD", "meaning": "Twice daily", "times_per_day": 2},
    "TDS": {"code": "TDS", "meaning": "Three times daily", "times_per_day": 3},
    "QID": {"code": "QID", "meaning": "Four times daily", "times_per_day": 4},
    "HS": {"code": "HS", "meaning": "At bedtime", "times_per_day": 1},
    "SOS": {"code": "SOS", "meaning": "As needed", "times_per_day": 0},
    "PRN": {"code": "PRN", "meaning": "As required", "times_per_day": 0},
    "STAT": {"code": "STAT", "meaning": "Immediately", "times_per_day": 1},
}


# =============================================================================
# Duration Options (common duration strings in Indian prescriptions)
# =============================================================================
DURATION_OPTIONS = [
    {"text": "3 days", "days": 3},
    {"text": "5 days", "days": 5},
    {"text": "7 days", "days": 7},
    {"text": "10 days", "days": 10},
    {"text": "14 days", "days": 14},
    {"text": "2 weeks", "days": 14},
    {"text": "3 weeks", "days": 21},
    {"text": "1 month", "days": 30},
    {"text": "2 months", "days": 60},
    {"text": "3 months", "days": 90},
    {"text": "6 weeks", "days": 42},
    {"text": "Single dose", "days": 1},
    {"text": "Continue", "days": 0},
    {"text": "SOS", "days": 0},
]