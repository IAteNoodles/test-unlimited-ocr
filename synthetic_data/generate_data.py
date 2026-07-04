"""
generate_data.py
================
Orchestrator for synthetic (noisy, clean) medical document pair generation.

Pipeline:
  1. Load real Indian drug names from DataDump CSV (layer1_vocabulary.csv)
  2. Generate clean prescription text using DataDump brand names + co-prescription rules
  3. Generate clean lab report text using existing lab_report_gen
  4. Apply OCR noise model to create noisy text
  5. Output (noisy, clean) pairs as JSONL

Usage:
    python -m synthetic_data.generate_data --n 1000 --output data/pairs.jsonl
    python -m synthetic_data.generate_data --n 500 --type prescription --output data/rx.jsonl
    python -m synthetic_data.generate_data --n 500 --type lab_report --output data/lab.jsonl
    python -m synthetic_data.generate_data --n 10000 --seed 42 --stats --output data/large.jsonl
"""

import argparse
import csv
import json
import os
import random
from pathlib import Path

from .prescription_gen import (
    generate_doctor_header,
    generate_patient_info,
    generate_date,
    generate_advice,
    generate_followup,
    pick_medicines,
)
from .medicines_db import MEDICINES, FDCS
from .coprescription_rules import (
    CONDITIONS,
    FREQUENCY_CODES,
    DURATION_OPTIONS,
)
from .lab_report_gen import (
    generate_lab_header,
    generate_patient_info as gen_lab_patient,
    generate_date as gen_lab_date,
    generate_panel,
)
from .noise_model import inject_noise, char_error_rate, word_error_rate

# ---------------------------------------------------------------------------
# 1. Constants
# ---------------------------------------------------------------------------

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_DATADUMP_PATH = os.path.join(_SCRIPT_DIR, "..", "data")

FORM_MAP = {
    "tablet": "Tab",
    "tablets": "Tab",
    "tab": "Tab",
    "capsule": "Cap",
    "capsules": "Cap",
    "cap": "Cap",
    "syrup": "Syp",
    "syp": "Syp",
    "suspension": "Susp",
    "susp": "Susp",
    "injection": "Inj",
    "inj": "Inj",
    "drops": "Drops",
    "ointment": "Oint",
    "cream": "Cream",
    "gel": "Gel",
    "spray": "Spray",
    "lotion": "Lotion",
    "powder": "Powder",
    "granules": "Gran",
    "respule": "Resp",
    "inhaler": "Inh",
    "rotacap": "Rotacap",
    "sachet": "Sachet",
    "strip": "Strip",
    "eye drops": "Eye Drops",
    "ear drops": "Ear Drops",
    "nasal spray": "Nasal Spray",
    "nasal drops": "Nasal Drops",
}
_FORM_MAP_SORTED = sorted(FORM_MAP.items(), key=lambda x: -len(x[0]))

CATEGORY_TO_ATC = {
    "analgesic_antipyretic": ["PAIN ANALGESICS"],
    "nsaid": ["PAIN ANALGESICS"],
    "antigout": ["PAIN ANALGESICS"],
    "antacid": ["GASTRO INTESTINAL"],
    "anthelmintic": ["ANTI INFECTIVES", "GASTRO INTESTINAL"],
    "antibiotic": ["ANTI INFECTIVES"],
    "anticoagulant": ["BLOOD RELATED", "CARDIAC"],
    "anticonvulsant": ["NEURO CNS"],
    "antidiabetic": ["ANTI DIABETIC"],
    "antidiarrheal": ["GASTRO INTESTINAL"],
    "antiemetic": ["GASTRO INTESTINAL"],
    "antifungal": ["DERMA", "ANTI INFECTIVES"],
    "antihistamine": ["RESPIRATORY"],
    "antihypertensive": ["CARDIAC"],
    "antitussive": ["RESPIRATORY"],
    "antiviral": ["ANTI INFECTIVES"],
    "anxiolytic": ["NEURO CNS"],
    "bronchodilator": ["RESPIRATORY"],
    "cardiac": ["CARDIAC"],
    "diuretic": ["CARDIAC", "UROLOGY"],
    "enzyme": ["OTHERS"],
    "expectorant": ["RESPIRATORY"],
    "gynecological": ["GYNAECOLOGICAL"],
    "hemostatic": ["BLOOD RELATED"],
    "laxative": ["GASTRO INTESTINAL"],
    "lipid_lowering": ["CARDIAC"],
    "mineral": ["VITAMINS MINERALS NUTRIENTS"],
    "muscle_relaxant": ["NEURO CNS", "PAIN ANALGESICS"],
    "neurological": ["NEURO CNS"],
    "ophthalmic": ["OPHTHAL", "OPHTHAL OTOLOGICALS"],
    "ppi": ["GASTRO INTESTINAL"],
    "steroid": ["HORMONES", "DERMA"],
    "stimulant": ["OTHERS", "SEX STIMULANTS REJUVENATORS"],
    "supplement": ["VITAMINS MINERALS NUTRIENTS"],
    "thyroid": ["HORMONES"],
    "topical": ["DERMA"],
    "urological": ["UROLOGY"],
    "vitamin": ["VITAMINS MINERALS NUTRIENTS"],
}

VITAL_PROFILES = {
    "fever": {"temp": (100, 104), "pulse": (90, 110), "bp": "normal", "rr": "normal", "spo2": "normal"},
    "hypertension": {"temp": "normal", "pulse": "normal", "bp": "high", "rr": "normal", "spo2": "normal"},
    "respiratory": {"temp": "normal", "pulse": (80, 100), "bp": "normal", "rr": (20, 28), "spo2": (94, 97)},
    "diabetes": {"temp": "normal", "pulse": "normal", "bp": "borderline", "rr": "normal", "spo2": "normal"},
    "anemia": {"temp": "normal", "pulse": (90, 110), "bp": "normal", "rr": "normal", "spo2": "normal"},
    "dehydration": {"temp": "normal", "pulse": (90, 110), "bp": "low", "rr": "normal", "spo2": "normal"},
    "normal": {"temp": "normal", "pulse": "normal", "bp": "normal", "rr": "normal", "spo2": "normal"},
}

CONDITION_CONTEXT = {
    "fever_viral": {
        "complaints": ["c/o fever for {days} days", "c/o fever with chills, body ache", "c/o high grade fever {days} days"],
        "diagnosis": ["K/c Viral Fever", "K/c Acute Febrile Illness"],
        "vitals": "fever",
    },
    "common_cold": {
        "complaints": ["c/o cold and nasal congestion {days} days", "c/o running nose, sneezing", "c/o nasal block, headache"],
        "diagnosis": ["K/c Common Cold", "K/c Acute Coryza"],
        "vitals": "normal",
    },
    "pharyngitis": {
        "complaints": ["c/o sore throat, difficulty swallowing {days} days", "c/o throat pain, fever"],
        "diagnosis": ["K/c Acute Pharyngitis"],
        "vitals": "fever",
    },
    "tonsillitis": {
        "complaints": ["c/o throat pain, difficulty swallowing {days} days", "c/o swollen tonsils, fever"],
        "diagnosis": ["K/c Acute Tonsillitis"],
        "vitals": "fever",
    },
    "acute_bronchitis": {
        "complaints": ["c/o cough with sputum {days} days", "c/o cough, chest discomfort, fever"],
        "diagnosis": ["K/c Acute Bronchitis"],
        "vitals": "respiratory",
    },
    "pneumonia": {
        "complaints": ["c/o fever, cough, breathlessness {days} days", "c/o productive cough, chest pain"],
        "diagnosis": ["K/c Pneumonia"],
        "vitals": "respiratory",
    },
    "uti": {
        "complaints": ["c/o burning urination, frequency {days} days", "c/o fever, lower abdominal pain"],
        "diagnosis": ["K/c Urinary Tract Infection"],
        "vitals": "fever",
    },
    "gastroenteritis": {
        "complaints": ["c/o loose stools, vomiting {days} days", "c/o diarrhea, abdominal pain, dehydration"],
        "diagnosis": ["K/c Acute Gastroenteritis"],
        "vitals": "dehydration",
    },
    "dyspepsia": {
        "complaints": ["c/o abdominal discomfort, bloating {days} days", "c/o upper abdominal pain, belching"],
        "diagnosis": ["K/c Dyspepsia"],
        "vitals": "normal",
    },
    "gerd": {
        "complaints": ["c/o heartburn, acid reflux {days} days", "c/o chest burning, regurgitation"],
        "diagnosis": ["K/c GERD", "K/c Gastroesophageal Reflux Disease"],
        "vitals": "normal",
    },
    "peptic_ulcer": {
        "complaints": ["c/o epigastric pain {days} days", "c/o abdominal pain, nausea, bloating"],
        "diagnosis": ["K/c Peptic Ulcer Disease"],
        "vitals": "normal",
    },
    "constipation": {
        "complaints": ["c/o hard stools, straining {days} days", "c/o infrequent stools, abdominal discomfort"],
        "diagnosis": ["K/c Constipation"],
        "vitals": "normal",
    },
    "hypertension": {
        "complaints": ["c/o headache, dizziness", "c/o routine checkup, elevated BP", "Asymptomatic, on routine checkup"],
        "diagnosis": ["K/c Essential Hypertension", "K/c Hypertension"],
        "vitals": "hypertension",
    },
    "diabetes_type2": {
        "complaints": ["c/o increased urination, thirst", "c/o weight loss, fatigue", "Asymptomatic, on routine checkup"],
        "diagnosis": ["K/c Type 2 Diabetes Mellitus"],
        "vitals": "diabetes",
    },
    "dyslipidemia": {
        "complaints": ["Asymptomatic, on routine checkup", "c/o routine lipid profile abnormal"],
        "diagnosis": ["K/c Dyslipidemia"],
        "vitals": "normal",
    },
    "hypothyroidism": {
        "complaints": ["c/o fatigue, weight gain, cold intolerance", "c/o lethargy, dry skin, hair fall"],
        "diagnosis": ["K/c Hypothyroidism"],
        "vitals": "normal",
    },
    "hyperthyroidism": {
        "complaints": ["c/o palpitation, weight loss, heat intolerance", "c/o tremors, anxiety, increased appetite"],
        "diagnosis": ["K/c Hyperthyroidism"],
        "vitals": "normal",
    },
    "asthma": {
        "complaints": ["c/o breathlessness, wheezing {days} days", "c/o chest tightness, cough at night"],
        "diagnosis": ["K/c Bronchial Asthma"],
        "vitals": "respiratory",
    },
    "copd": {
        "complaints": ["c/o chronic cough, breathlessness on exertion", "c/o sputum, wheezing"],
        "diagnosis": ["K/c COPD", "K/c Chronic Obstructive Pulmonary Disease"],
        "vitals": "respiratory",
    },
    "allergic_rhinitis": {
        "complaints": ["c/o sneezing, nasal itching, watery discharge", "c/o nasal block, sneezing {days} days"],
        "diagnosis": ["K/c Allergic Rhinitis"],
        "vitals": "normal",
    },
    "migraine": {
        "complaints": ["c/o unilateral headache, nausea, photophobia", "c/o throbbing headache {days} hours"],
        "diagnosis": ["K/c Migraine"],
        "vitals": "normal",
    },
    "anxiety": {
        "complaints": ["c/o worry, restlessness, sleep disturbance", "c/o palpitation, nervousness"],
        "diagnosis": ["K/c Anxiety Disorder"],
        "vitals": "normal",
    },
    "insomnia": {
        "complaints": ["c/o difficulty falling asleep", "c/o early awakening, poor sleep quality"],
        "diagnosis": ["K/c Insomnia"],
        "vitals": "normal",
    },
    "epilepsy": {
        "complaints": ["c/o seizures, loss of consciousness", "c/o episodes of convulsions"],
        "diagnosis": ["K/c Epilepsy", "K/c Seizure Disorder"],
        "vitals": "normal",
    },
    "osteoarthritis": {
        "complaints": ["c/o knee pain, stiffness, reduced mobility", "c/o joint pain worsened by activity"],
        "diagnosis": ["K/c Osteoarthritis"],
        "vitals": "normal",
    },
    "rheumatoid_arthritis": {
        "complaints": ["c/o joint pain, swelling, morning stiffness", "c/o multiple joint pain, deformity"],
        "diagnosis": ["K/c Rheumatoid Arthritis"],
        "vitals": "normal",
    },
    "low_back_pain": {
        "complaints": ["c/o low back pain radiating to leg", "c/o back pain {days} days, worsened by lifting"],
        "diagnosis": ["K/c Low Back Pain", "K/c Lumbar Radiculopathy"],
        "vitals": "normal",
    },
    "gout": {
        "complaints": ["c/o sudden severe pain in big toe", "c/o swollen, red, tender joint"],
        "diagnosis": ["K/c Gout", "K/c Acute Gouty Arthritis"],
        "vitals": "normal",
    },
    "dysmenorrhea": {
        "complaints": ["c/o painful menstruation, abdominal cramps", "c/o lower abdominal pain during periods"],
        "diagnosis": ["K/c Dysmenorrhea"],
        "vitals": "normal",
    },
    "anemia": {
        "complaints": ["c/o fatigue, weakness, pallor", "c/o shortness of breath on exertion"],
        "diagnosis": ["K/c Anemia", "K/c Iron Deficiency Anemia"],
        "vitals": "anemia",
    },
    "vitamin_d_deficiency": {
        "complaints": ["c/o bone pain, muscle weakness, fatigue", "c/o generalized body ache"],
        "diagnosis": ["K/c Vitamin D Deficiency"],
        "vitals": "normal",
    },
    "b12_deficiency": {
        "complaints": ["c/o fatigue, tingling, numbness", "c/o weakness, memory problems"],
        "diagnosis": ["K/c Vitamin B12 Deficiency"],
        "vitals": "anemia",
    },
    "fungal_infection_skin": {
        "complaints": ["c/o itching, red scaly patches on skin", "c/o ring-shaped rash, itching"],
        "diagnosis": ["K/c Tinea Corporis", "K/c Fungal Infection Skin"],
        "vitals": "normal",
    },
    "scabies": {
        "complaints": ["c/o intense itching at night", "c/o itchy rash between fingers, wrists"],
        "diagnosis": ["K/c Scabies"],
        "vitals": "normal",
    },
    "acne": {
        "complaints": ["c/o pimples, pustules on face", "c/o comedones, oily skin"],
        "diagnosis": ["K/c Acne Vulgaris"],
        "vitals": "normal",
    },
    "cellulitis": {
        "complaints": ["c/o redness, swelling, warmth on skin", "c/o painful swollen area with fever"],
        "diagnosis": ["K/c Cellulitis"],
        "vitals": "fever",
    },
    "conjunctivitis": {
        "complaints": ["c/o redness, discharge, itching in eyes", "c/o watering, foreign body sensation"],
        "diagnosis": ["K/c Conjunctivitis"],
        "vitals": "normal",
    },
    "otitis_media": {
        "complaints": ["c/o ear pain, discharge, decreased hearing", "c/o fever, ear pain {days} days"],
        "diagnosis": ["K/c Acute Otitis Media"],
        "vitals": "fever",
    },
    "dental_infection": {
        "complaints": ["c/o toothache, swelling", "c/o pain on chewing, gum swelling"],
        "diagnosis": ["K/c Dental Infection", "K/c Dental Abscess"],
        "vitals": "normal",
    },
    "worm_infestation": {
        "complaints": ["c/o abdominal pain, itching around anus", "c/o weight loss, irritability"],
        "diagnosis": ["K/c Worm Infestation", "K/c Enterobiasis"],
        "vitals": "normal",
    },
    "typhoid": {
        "complaints": ["c/o fever {days} days, abdominal pain, constipation", "c/o step-ladder fever, headache"],
        "diagnosis": ["K/c Enteric Fever", "K/c Typhoid"],
        "vitals": "fever",
    },
    "dengue": {
        "complaints": ["c/o high fever, headache, retro-orbital pain", "c/o fever, body ache, rash"],
        "diagnosis": ["K/c Dengue Fever"],
        "vitals": "fever",
    },
    "malaria": {
        "complaints": ["c/o fever with chills and rigors", "c/o high grade fever, sweating, headache"],
        "diagnosis": ["K/c Malaria"],
        "vitals": "fever",
    },
    "bph": {
        "complaints": ["c/o frequent urination, hesitancy, weak stream", "c/o nocturia, incomplete emptying"],
        "diagnosis": ["K/c Benign Prostatic Hyperplasia", "K/c BPH"],
        "vitals": "normal",
    },
    "_default": {
        "complaints": ["c/o general complaints", "c/o symptoms for {days} days"],
        "diagnosis": ["K/c Under Investigation"],
        "vitals": "normal",
    },
}

CONDITION_HISTORY = {
    "diabetes_type2": ["H/o Hypertension", "H/o Dyslipidemia", "H/o CAD", "H/o Diabetic Neuropathy", "H/o Diabetic Retinopathy"],
    "hypertension": ["H/o Diabetes Mellitus", "H/o Dyslipidemia", "H/o Stroke", "H/o CAD"],
    "asthma": ["H/o Allergic Rhinitis", "H/o Atopy", "H/o Childhood Asthma"],
    "copd": ["H/o Smoking 20 pack years", "H/o Tuberculosis", "H/o Asthma"],
    "hypothyroidism": ["H/o Thyroid Surgery", "H/o Autoimmune Disease"],
    "hyperthyroidism": ["H/o Thyroid Nodule", "H/o Autoimmune Disease"],
    "epilepsy": ["H/o Seizures since childhood", "H/o Head Trauma"],
    "rheumatoid_arthritis": ["H/o Autoimmune Disease", "H/o Family History of RA"],
}

GENERAL_HISTORY = [
    "H/o Hypertension", "H/o Diabetes Mellitus", "H/o Hypothyroidism",
    "H/o Asthma", "H/o Allergic Rhinitis", "H/o CAD", "H/o Dyslipidemia",
    "H/o Smoking", "H/o Alcoholism",
]

PRESCRIPTION_NOISE_PROFILES = {
    "private_clinic": ["handwritten_moderate", "handwritten_severe"],
    "govt_hospital_opd": ["handwritten_moderate", "handwritten_severe"],
    "corporate_hospital_ehr": ["printed_clean", "printed_moderate"],
    "pediatric": ["handwritten_moderate", "handwritten_severe"],
    "chronic_followup": ["handwritten_moderate", "printed_moderate"],
    "er": ["handwritten_severe", "handwritten_moderate"],
    "nursing_home": ["handwritten_moderate", "handwritten_severe"],
    "specialist_referral": ["handwritten_moderate", "printed_moderate"],
    "telemedicine": ["printed_clean", "printed_moderate"],
    "cghs": ["printed_clean", "printed_moderate"],
    "pmjay": ["printed_clean", "printed_moderate"],
    "rural_phc": ["handwritten_severe", "handwritten_moderate"],
    "typed_outpatient": ["printed_clean", "printed_moderate", "printed_noisy"],
    "hospital_letterhead": ["printed_clean", "printed_moderate"],
    "referral_letter": ["handwritten_moderate", "printed_moderate"],
    "solo_gp_pad": ["handwritten_moderate", "handwritten_severe"],
    "gp_quick_strip": ["handwritten_severe", "handwritten_moderate"],
    "sms_digital": ["printed_clean", "handwritten_moderate"],
    "tertiary_care": ["printed_clean", "printed_moderate"],
    "ipd_orders": ["handwritten_moderate", "printed_moderate"],
    "surgical_post_op": ["handwritten_moderate", "handwritten_severe"],
    "emergency_discharge": ["handwritten_severe", "handwritten_moderate"],
    "ward_drug_chart": ["handwritten_moderate", "printed_moderate", "printed_noisy"],
    "discharge_medication": ["printed_clean", "printed_moderate"],
}

LAB_NOISE_PROFILES = [
    "printed_clean", "printed_clean", "printed_clean",
    "printed_moderate", "printed_moderate", "printed_moderate", "printed_moderate",
    "printed_noisy", "printed_noisy",
]

# ---------------------------------------------------------------------------
# 2. DataDump loader
# ---------------------------------------------------------------------------

def load_drug_database(datadump_path=None, use_cache=True):
    """Load drug database from DataDump CSV.

    Returns a dict: atc_class -> [brand_names]
    """
    if datadump_path is None:
        datadump_path = os.environ.get("DATADUMP_PATH", _DEFAULT_DATADUMP_PATH)

    csv_path = os.path.join(datadump_path, "layer1_vocabulary.csv")
    cache_path = os.path.join(os.path.dirname(__file__) or ".", "..", "data", ".datadump_cache.json")

    if use_cache and os.path.exists(cache_path) and os.path.exists(csv_path):
        if os.path.getmtime(cache_path) > os.path.getmtime(csv_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)

    if not os.path.exists(csv_path):
        print("WARNING: DataDump CSV not found at %s" % csv_path)
        print("Falling back to medicines_db.py for drug names.")
        return {}

    drug_db = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("source") != "all_india_drug_bank":
                continue
            atc = row.get("atc_class", "").strip()
            brand = row.get("brand_name", "").strip()
            if atc and brand:
                drug_db.setdefault(atc.upper(), []).append(brand)

    for atc in drug_db:
        if len(drug_db[atc]) > 1000:
            drug_db[atc] = drug_db[atc][:1000]

    if use_cache:
        cache_dir = os.path.dirname(cache_path)
        if cache_dir:
            os.makedirs(cache_dir, exist_ok=True)
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(drug_db, f, ensure_ascii=False)

    return drug_db

# ---------------------------------------------------------------------------
# 3. Helpers
# ---------------------------------------------------------------------------

def _get_med_entry(med_key):
    """Return the medicine dict from MEDICINES or FDCS, or None."""
    if med_key in MEDICINES:
        return MEDICINES[med_key]
    if med_key in FDCS:
        return FDCS[med_key]
    return None


def _parse_brand_name(brand_name):
    """Parse a DataDump brand_name into (display_name, form_abbr).

    Example: "augmentin 625 duo tablet" -> ("Augmentin 625 Duo", "Tab")
    """
    lower = brand_name.lower().strip()
    for form_key, form_abbr in _FORM_MAP_SORTED:
        if lower.endswith(" " + form_key):
            display = brand_name[:-(len(form_key) + 1)].strip().title()
            return display, form_abbr
    return brand_name.title(), "Tab"


def _pick_brand(atc_classes, drug_db, rng):
    """Pick a random brand name from DataDump for the given ATC classes."""
    brands = []
    for atc in atc_classes:
        b = drug_db.get(atc.upper(), [])
        brands.extend(b)
    if not brands:
        brands = drug_db.get("OTHERS", [])
    if not brands:
        return None
    return rng.choice(brands)


def _format_medication_line_datadump(med_key, rng, drug_db):
    """Format a medication line using a real brand name from DataDump.

    Falls back to MEDICINES brands if DataDump has no match.
    """
    entry = _get_med_entry(med_key)
    if entry is None:
        return None

    category = entry.get("category", "")
    atc_classes = CATEGORY_TO_ATC.get(category, ["OTHERS"])

    brand = _pick_brand(atc_classes, drug_db, rng)

    if brand:
        display_name, form = _parse_brand_name(brand)
    else:
        forms = entry.get("forms", ["Tab"])
        form = rng.choice(forms)
        if med_key in FDCS:
            components = entry.get("components", [])
            if components:
                display_name = " + ".join(components)
            else:
                display_name = med_key.replace("_", " ").title()
        else:
            display_name = entry.get("generic", med_key.replace("_", " ").title())

    freq_keys = list(FREQUENCY_CODES.keys())
    freq = rng.choice(freq_keys)

    duration = ""
    if rng.random() < 0.7:
        dur = rng.choice(DURATION_OPTIONS)
        if dur["days"] > 0:
            duration = " x %s" % dur["text"]

    food = ""
    if rng.random() < 0.3:
        food = " " + rng.choice(["a/c", "p/c", "a/c"])

    return "%s %s %s%s%s" % (form, display_name, freq, food, duration)


def _generate_vitals(profile_key, rng):
    """Generate a vitals string based on profile."""
    p = VITAL_PROFILES.get(profile_key, VITAL_PROFILES["normal"])

    if p["temp"] == "normal":
        temp = rng.randint(97, 99)
    elif isinstance(p["temp"], (tuple, list)):
        temp = rng.randint(p["temp"][0], p["temp"][1])
    else:
        temp = rng.randint(97, 99)

    if p["pulse"] == "normal":
        pulse = rng.randint(68, 80)
    elif isinstance(p["pulse"], (tuple, list)):
        pulse = rng.randint(p["pulse"][0], p["pulse"][1])
    else:
        pulse = rng.randint(68, 80)

    if p["bp"] == "normal":
        bp = "%d/%d" % (rng.randint(110, 130), rng.randint(70, 85))
    elif p["bp"] == "high":
        bp = "%d/%d" % (rng.randint(140, 170), rng.randint(90, 105))
    elif p["bp"] == "low":
        bp = "%d/%d" % (rng.randint(90, 105), rng.randint(60, 70))
    elif p["bp"] == "borderline":
        bp = "%d/%d" % (rng.randint(130, 145), rng.randint(85, 95))
    else:
        bp = "%d/%d" % (rng.randint(110, 130), rng.randint(70, 85))

    if p["rr"] == "normal":
        rr = rng.randint(14, 18)
    elif isinstance(p["rr"], (tuple, list)):
        rr = rng.randint(p["rr"][0], p["rr"][1])
    else:
        rr = rng.randint(14, 18)

    if p["spo2"] == "normal":
        spo2 = rng.randint(97, 100)
    elif isinstance(p["spo2"], (tuple, list)):
        spo2 = rng.randint(p["spo2"][0], p["spo2"][1])
    else:
        spo2 = rng.randint(97, 100)

    return "O/E: BP %s, Pulse %d/min, Temp %d*F, RR %d/min, SpO2 %d%%" % (bp, pulse, temp, rr, spo2)


def _generate_patient_context(condition_key, rng):
    """Generate patient context string (complaints, diagnosis, vitals, history)."""
    ctx = CONDITION_CONTEXT.get(condition_key, CONDITION_CONTEXT["_default"])

    tmpl = rng.choice(ctx["complaints"])
    days = rng.randint(1, 7)
    complaints = tmpl.format(days=days)

    diagnosis = rng.choice(ctx["diagnosis"])

    vitals = _generate_vitals(ctx["vitals"], rng)

    history = ""
    if rng.random() < 0.4:
        hist_options = CONDITION_HISTORY.get(condition_key, GENERAL_HISTORY)
        history = rng.choice(hist_options)

    parts = [complaints, diagnosis, vitals]
    if history:
        parts.append(history)

    return "\n".join(parts)

# ---------------------------------------------------------------------------
# 4. Prescription format templates (12)
# ---------------------------------------------------------------------------

def _format_private_clinic(parts):
    lines = [
        parts["header"], "",
        parts["patient"],
        "Date: %s" % parts["date"], "",
    ]
    if parts["context"]:
        lines.append(parts["context"])
        lines.append("")
    lines.append("Rx")
    for ml in parts["med_lines"]:
        lines.append(ml)
    if parts["advice"]:
        lines.append("")
        lines.append("Advice:")
        for a in parts["advice"]:
            lines.append("- %s" % a)
    lines.append("")
    lines.append(parts["followup"])
    return "\n".join(lines)


def _format_govt_hospital_opd(parts):
    opd_no = "OPD No: %d" % random.randint(10000, 99999)
    lines = [
        "Govt District Hospital",
        opd_no, "",
        parts["patient"],
        "Date: %s" % parts["date"], "",
        "Diagnosis: %s" % parts["condition_name"], "",
        "Rx",
    ]
    for i, ml in enumerate(parts["med_lines"], 1):
        lines.append("%d. %s" % (i, ml))
    lines.append("")
    lines.append(parts["followup"])
    return "\n".join(lines)


def _format_corporate_hospital_ehr(parts):
    mrn = "MRN: %s%06d" % (random.choice(["APL", "MAX", "FOR", "MED"]), random.randint(1, 999999))
    lines = [
        "Apollo Hospital",
        mrn, "",
        parts["patient"],
        "Date: %s" % parts["date"], "",
    ]
    if parts["context"]:
        lines.append(parts["context"])
        lines.append("")
    lines.append("Rx")
    for i, ml in enumerate(parts["med_lines"], 1):
        lines.append("%d. %s" % (i, ml))
    if parts["advice"]:
        lines.append("")
        lines.append("Advice:")
        for a in parts["advice"]:
            lines.append("- %s" % a)
    lines.append("")
    lines.append(parts["followup"])
    lines.append("Signature: _______________")
    return "\n".join(lines)


def _format_pediatric(parts):
    lines = [
        parts["header"], "",
        parts["patient"],
        "Date: %s" % parts["date"], "",
    ]
    if parts["context"]:
        lines.append(parts["context"])
        lines.append("")
    lines.append("Rx")
    for ml in parts["med_lines"]:
        lines.append(ml)
    if parts["advice"]:
        lines.append("")
        lines.append("Advice:")
        for a in parts["advice"]:
            lines.append("- %s" % a)
    lines.append("")
    lines.append(parts["followup"])
    return "\n".join(lines)


def _format_chronic_followup(parts):
    lines = [
        parts["header"], "",
        parts["patient"],
        "Date: %s" % parts["date"], "",
    ]
    if parts["context"]:
        lines.append(parts["context"])
        lines.append("")
    lines.append("Follow-up Rx")
    for ml in parts["med_lines"]:
        lines.append(ml)
    if parts["advice"]:
        lines.append("")
        lines.append("Advice:")
        for a in parts["advice"]:
            lines.append("- %s" % a)
    lines.append("")
    lines.append(parts["followup"])
    return "\n".join(lines)


def _format_er(parts):
    er_no = "ER No: ER%06d" % random.randint(1, 999999)
    lines = [
        "EMERGENCY DEPARTMENT",
        parts["header"].split("\n")[0] if parts["header"] else "City Care Hospital",
        er_no, "",
        parts["patient"],
        "Date: %s" % parts["date"], "",
    ]
    if parts["context"]:
        lines.append(parts["context"])
        lines.append("")
    lines.append("Rx")
    for ml in parts["med_lines"]:
        lines.append(ml)
    if parts["advice"]:
        lines.append("")
        lines.append("Advice:")
        for a in parts["advice"]:
            lines.append("- %s" % a)
    lines.append("")
    lines.append(parts["followup"])
    return "\n".join(lines)


def _format_nursing_home(parts):
    lines = [
        parts["header"].split("\n")[0] if parts["header"] else "Nursing Home",
        "", parts["patient"],
        "Date: %s" % parts["date"], "",
    ]
    if parts["context"]:
        lines.append(parts["context"])
        lines.append("")
    lines.append("Rx")
    for ml in parts["med_lines"]:
        lines.append(ml)
    lines.append("")
    lines.append(parts["followup"])
    return "\n".join(lines)


def _format_specialist_referral(parts):
    ref_to = "Ref: Dr. %s %s, %s" % (
        random.choice(["Vikram", "Sanjay", "Arun", "Deepak"]),
        random.choice(["Patel", "Mehta", "Joshi", "Rao"]),
        random.choice(["MD (Pulmonology)", "MD (Cardiology)", "MS (Ortho)", "MD (Neuro)"]),
    )
    lines = [
        parts["header"], "",
        ref_to, "",
        parts["patient"],
        "Date: %s" % parts["date"], "",
    ]
    if parts["context"]:
        lines.append(parts["context"])
        lines.append("")
    lines.append("Rx")
    for ml in parts["med_lines"]:
        lines.append(ml)
    if parts["advice"]:
        lines.append("")
        lines.append("Advice:")
        for a in parts["advice"]:
            lines.append("- %s" % a)
    lines.append("")
    lines.append(parts["followup"])
    return "\n".join(lines)


def _format_telemedicine(parts):
    tel_id = "TC%06d" % random.randint(1, 999999)
    lines = [
        "E-PRESCRIPTION",
        "Teleconsult ID: %s" % tel_id,
        "Date: %s" % parts["date"], "",
        parts["header"], "",
        parts["patient"], "",
    ]
    if parts["context"]:
        lines.append(parts["context"])
        lines.append("")
    lines.append("Rx")
    for i, ml in enumerate(parts["med_lines"], 1):
        lines.append("%d. %s" % (i, ml))
    if parts["advice"]:
        lines.append("")
        lines.append("Advice:")
        for a in parts["advice"]:
            lines.append("- %s" % a)
    lines.append("")
    lines.append(parts["followup"])
    lines.append("Digital Signature")
    return "\n".join(lines)


def _format_cghs(parts):
    lines = [
        "CGHS Wellness Centre",
        "CGHS ID: %d" % random.randint(1000000, 9999999), "",
        parts["header"].split("\n")[0] if parts["header"] else "Dr.",
        "", parts["patient"],
        "Date: %s" % parts["date"], "",
        "Diagnosis: %s" % parts["condition_name"], "",
        "Rx",
    ]
    for ml in parts["med_lines"]:
        lines.append(ml)
    if parts["advice"]:
        lines.append("")
        lines.append("Advice:")
        for a in parts["advice"]:
            lines.append("- %s" % a)
    lines.append("")
    lines.append(parts["followup"])
    return "\n".join(lines)


def _format_pmjay(parts):
    lines = [
        "Ayushman Bharat - PMJAY",
        "PMJAY ID: PMJAY%d" % random.randint(100000000, 999999999), "",
        parts["header"].split("\n")[0] if parts["header"] else "Dr.",
        "", parts["patient"],
        "Date: %s" % parts["date"], "",
        "Diagnosis: %s" % parts["condition_name"], "",
        "Rx",
    ]
    for ml in parts["med_lines"]:
        lines.append(ml)
    if parts["advice"]:
        lines.append("")
        lines.append("Advice:")
        for a in parts["advice"]:
            lines.append("- %s" % a)
    lines.append("")
    lines.append(parts["followup"])
    return "\n".join(lines)


def _format_rural_phc(parts):
    phc = "PHC %s" % random.choice(["Rampur", "Gandhinagar", "Sitapur", "Jaunpur", "Daltonganj"])
    lines = [
        phc,
        parts["header"].split("\n")[0] if parts["header"] else "Dr.",
        "", "Pt: %s" % parts["patient"].replace("\n", "  "),
        "Date: %s" % parts["date"], "",
        parts["condition_name"], "",
        "Rx",
    ]
    for ml in parts["med_lines"]:
        lines.append(ml)
    lines.append("")
    lines.append(parts["followup"])
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 4b. Extended prescription format templates (12 new from JSON files)
# ---------------------------------------------------------------------------

def _patient_name(parts):
    """Extract just the patient name from patient info (remove 'Patient: ' prefix)."""
    line = parts["patient"].split("\n")[0]
    return line.replace("Patient: ", "", 1).strip()

def _format_typed_outpatient(parts):
    rng = parts.get("_rng", random)
    doc_name = parts["header"].split("\n")[0] if parts["header"] else "Dr. ________"
    reg = "Reg No: %s%06d" % (rng.choice(["DEL", "MUM", "CHE", "BAN"]), rng.randint(1, 999999))
    lines = [
        doc_name,
        reg,
        "=" * 50,
        parts["patient"],
        "Date: %s" % parts["date"],
        "",
    ]
    if parts["context"]:
        lines.append(parts["context"])
        lines.append("")
    lines.append("Rx")
    for i, ml in enumerate(parts["med_lines"], 1):
        lines.append("  %d. %s" % (i, ml))
    if parts["advice"]:
        lines.append("")
        lines.append("Advice:")
        for a in parts["advice"]:
            lines.append("  - %s" % a)
    lines.append("")
    lines.append(parts["followup"])
    lines.append("=" * 50)
    lines.append("(Doctor's Signature)")
    return "\n".join(lines)


def _format_hospital_letterhead(parts):
    rng = parts.get("_rng", random)
    doc_name = parts["header"].split("\n")[0] if parts["header"] else "Dr. ________"
    clinic = rng.choice([
        "Apollo Clinic", "Fortis Healthcare", "Max Hospital", "Medanta",
        "AIIMS OPD", "Sir Ganga Ram Hospital", "Safdarjung Hospital",
    ])
    phone = "+91-%d" % rng.randint(9111111111, 9999999999)
    lines = [
        doc_name,
        clinic,
        "%s | info@%s.in" % (phone, clinic.lower().replace(" ", "")),
        "-" * 60,
        "",
        parts["patient"],
        "Date: %s" % parts["date"],
        "",
    ]
    if parts["context"]:
        lines.append(parts["context"])
        lines.append("")
    lines.append("Rx")
    for ml in parts["med_lines"]:
        lines.append(ml)
    if parts["advice"]:
        lines.append("")
        lines.append("Advice:")
        for a in parts["advice"]:
            lines.append("- %s" % a)
    lines.append("")
    lines.append(parts["followup"])
    lines.append("")
    lines.append("__________________________________")
    lines.append("Signature")
    return "\n".join(lines)


def _format_referral_letter(parts):
    rng = parts.get("_rng", random)
    specialists = [
        ("Dr. Rajesh Kumar", "MD (Cardiology)"),
        ("Dr. Anjali Sharma", "MD (Neurology)"),
        ("Dr. Suresh Patel", "MS (Orthopedics)"),
        ("Dr. Priya Singh", "MD (Pulmonology)"),
        ("Dr. Amit Verma", "MD (Gastroenterology)"),
    ]
    spec, qual = rng.choice(specialists)
    lines = [
        "REFERRAL LETTER",
        "=" * 50,
        "",
        "From: %s" % (parts["header"].split("\n")[0] if parts["header"] else "Dr. ________"),
        "To: %s, %s" % (spec, qual),
        "",
        parts["patient"],
        "Date: %s" % parts["date"],
        "Diagnosis: %s" % parts["condition_name"],
        "",
    ]
    if parts["context"]:
        lines.append(parts["context"])
        lines.append("")
    lines.append("Starter Rx:")
    for ml in parts["med_lines"]:
        lines.append(ml)
    if parts["advice"]:
        lines.append("")
        lines.append("Advice:")
        for a in parts["advice"]:
            lines.append("- %s" % a)
    lines.append("")
    lines.append(parts["followup"])
    lines.append("")
    lines.append("(Ref. Doctor's Signature)")
    return "\n".join(lines)


def _format_solo_gp_pad(parts):
    rng = parts.get("_rng", random)
    doc_name = parts["header"].split("\n")[0] if parts["header"] else "Dr. ________"
    pt_lines = parts["patient"].split("\n")
    pt_name = _patient_name(parts)
    pt_age_sex = pt_lines[1] if len(pt_lines) > 1 else ""
    times = rng.choice([
        "OPD Hours: 10 AM - 2 PM, 5 PM - 8 PM",
        "OPD Hours: 9 AM - 1 PM, 4 PM - 7 PM",
        "Clinic Timings: 10 AM - 2 PM, 6 PM - 9 PM",
    ])
    complaint = ""
    if parts["context"]:
        for cl in parts["context"].split("\n"):
            if "c/o" in cl.lower():
                complaint = cl
                break
    lines = [
        doc_name,
        times,
        "-" * 50,
        "Pt. Name: %s" % pt_name,
    ]
    if pt_age_sex:
        lines.append("Age/Sex: %s" % pt_age_sex)
    lines.append("Date: %s" % parts["date"])
    lines.append("")
    if complaint:
        lines.append("C/O: %s" % complaint)
    if parts["context"]:
        for cl in parts["context"].split("\n"):
            if cl.startswith("O/E:"):
                lines.append(cl)
        lines.append("K/C: %s" % parts["condition_name"])
    lines.append("")
    lines.append("Rx")
    for ml in parts["med_lines"]:
        lines.append("  " + ml)
    if parts["advice"]:
        lines.append("")
        lines.append("Advice:")
        for a in parts["advice"]:
            lines.append("  - %s" % a)
    lines.append("")
    lines.append(parts["followup"])
    lines.append("")
    lines.append("Signature: _________________")
    return "\n".join(lines)


def _format_gp_quick_strip(parts):
    doc_name = parts["header"].split("\n")[0] if parts["header"] else "Dr."
    doc = doc_name.replace("Dr. ", "").split(" ")[0]
    pt_name = _patient_name(parts)[:15]
    lines = [
        "Dr.%s" % doc,
        parts["date"],
        pt_name,
        "",
        "Rx",
    ]
    for ml in parts["med_lines"][:4]:
        parts_ml = ml.split(" ")
        brand = parts_ml[1] if len(parts_ml) > 1 else ml
        lines.append(" " + brand)
    lines.append("")
    lines.append(parts["followup"])
    lines.append("____")
    return "\n".join(lines)


def _format_sms_digital(parts):
    doc_name = parts["header"].split("\n")[0] if parts["header"] else "Dr."
    doc = doc_name.replace("Dr. ", "").split(" ")[0]
    pt_name = _patient_name(parts)[:10]
    lines = [
        "e-Rx: Dr.%s" % doc,
        "Pt:%s" % pt_name,
        parts["date"],
        "",
        "Rx",
    ]
    for ml in parts["med_lines"]:
        parts_ml = ml.split(" ")
        brand = parts_ml[1] if len(parts_ml) > 1 else parts_ml[0]
        rest = " ".join(parts_ml[2:]) if len(parts_ml) > 2 else ""
        lines.append(" %s %s" % (brand, rest))
    if parts["advice"]:
        lines.append("Adv: %s" % ("; ".join(parts["advice"])))
    lines.append("FU: %s" % parts["followup"])
    lines.append("")
    lines.append("(e-sig)")
    return "\n".join(lines)


def _format_tertiary_care(parts):
    rng = parts.get("_rng", random)
    hospitals = [
        "All India Institute of Medical Sciences",
        "Sir Ganga Ram Hospital, New Delhi",
        "Medanta - The Medicity, Gurugram",
        "Apollo Hospitals, Chennai",
        "Fortis Memorial Research Institute",
    ]
    hospital = rng.choice(hospitals)
    uhid = "UHID: %d" % rng.randint(10000000, 99999999)
    investigations = rng.choice([
        "CBC, LFT, KFT",
        "Chest X-ray, ECG",
        "HbA1c, FBS, PPBS",
        "Lipid Profile, TSH",
        "Hb%, Peripheral Smear",
    ])
    lines = [
        hospital,
        uhid,
        "=" * 70,
        "",
        parts["patient"],
        "Date: %s" % parts["date"],
        "",
    ]
    if parts["context"]:
        lines.append(parts["context"])
        lines.append("")
    lines.append("Rx")
    for i, ml in enumerate(parts["med_lines"], 1):
        lines.append("  %d. %s" % (i, ml))
    lines.append("")
    lines.append("Investigations: %s" % investigations)
    if parts["advice"]:
        lines.append("")
        lines.append("Advice:")
        for a in parts["advice"]:
            lines.append("  - %s" % a)
    lines.append("")
    lines.append(parts["followup"])
    lines.append("")
    lines.append("MO Signature: _________________")
    return "\n".join(lines)


def _format_ipd_orders(parts):
    rng = parts.get("_rng", random)
    doc_name = parts["header"].split("\n")[0] if parts["header"] else "Dr. ________"
    ward = rng.choice(["General Ward", "Semi-Private", "Private", "ICU", "HDU"])
    bed = rng.randint(1, 30)
    diet = rng.choice(["Regular", "Soft", "Liquid", "Diabetic", "Low Salt", "High Protein"])
    nursing_items = rng.sample([
        "Vitals q4h", "I/O Chart", "Monitor SpO2", "Bed rest",
        "Catheter care", "Pressure area care", "Nebulization q6h",
    ], rng.randint(1, 3))
    lines = [
        "IPD ORDERS",
        "=" * 50,
        doc_name,
        "",
        parts["patient"],
        "Ward: %s | Bed: %d" % (ward, bed),
        "Date: %s" % parts["date"],
        "Diagnosis: %s" % parts["condition_name"],
        "",
        "Rx",
    ]
    for ml in parts["med_lines"]:
        lines.append("  " + ml)
    lines.append("")
    lines.append("Nursing: %s" % (", ".join(nursing_items)))
    lines.append("Diet: %s" % diet)
    if parts["advice"]:
        lines.append("")
        lines.append("Advice:")
        for a in parts["advice"]:
            lines.append("  - %s" % a)
    lines.append("")
    lines.append(parts["followup"])
    lines.append("")
    lines.append("Doctor's Sign: _________________")
    return "\n".join(lines)


def _format_surgical_post_op(parts):
    rng = parts.get("_rng", random)
    doc_name = parts["header"].split("\n")[0] if parts["header"] else "Dr. ________"
    procedure = rng.choice([
        "Appendectomy", "Cholecystectomy", "Herniorrhaphy",
        "Cataract Surgery", "LSCS", "Tonsillectomy",
        "ORIF # Femur", "Laparotomy", "Hemorrhoidectomy",
    ])
    pod = rng.randint(1, 5)
    wound_care = "Wound: Dressing alternate days | Suture removal on POD %d" % (pod + 5)
    lines = [
        "POST-OPERATIVE PRESCRIPTION",
        "=" * 50,
        doc_name,
        "",
        parts["patient"],
        "Date: %s" % parts["date"],
        "Procedure: %s" % procedure,
        "POD: Day %d" % pod,
        "Diagnosis: %s" % parts["condition_name"],
        "",
        "Rx",
    ]
    for i, ml in enumerate(parts["med_lines"], 1):
        lines.append("  %d. %s" % (i, ml))
    lines.append("")
    lines.append(wound_care)
    if parts["advice"]:
        lines.append("")
        lines.append("Advice:")
        for a in parts["advice"]:
            lines.append("  - %s" % a)
    lines.append("")
    lines.append(parts["followup"])
    lines.append("")
    lines.append("Surgeon's Signature: _________________")
    return "\n".join(lines)


def _format_emergency_discharge(parts):
    rng = parts.get("_rng", random)
    doc_name = parts["header"].split("\n")[0] if parts["header"] else "Dr. ________"
    warnings = rng.sample([
        "High grade fever >102F",
        "Severe headache",
        "Breathlessness",
        "Chest pain",
        "Vomiting >3 episodes",
        "Decreased urine output",
        "Increasing abdominal pain",
        "Giddiness/fainting",
    ], rng.randint(2, 3))
    lines = [
        "EMERGENCY DEPARTMENT",
        "DISCHARGE INSTRUCTIONS",
        "=" * 50,
        doc_name,
        "",
        parts["patient"],
        "Date: %s" % parts["date"],
        "Diagnosis: %s" % parts["condition_name"],
        "",
        "Rx",
    ]
    for i, ml in enumerate(parts["med_lines"], 1):
        lines.append("  %d. %s" % (i, ml))
    lines.append("")
    lines.append("RETURN TO ER IF:")
    for w in warnings:
        lines.append("  - %s" % w)
    if parts["advice"]:
        lines.append("")
        lines.append("Advice:")
        for a in parts["advice"]:
            lines.append("  - %s" % a)
    lines.append("")
    lines.append(parts["followup"])
    lines.append("")
    lines.append("ER Doctor: %s" % doc_name)
    return "\n".join(lines)


def _format_ward_drug_chart(parts):
    rng = parts.get("_rng", random)
    doc_name = parts["header"].split("\n")[0] if parts["header"] else "Dr. ________"
    ward = rng.choice(["General Ward", "Semi-Private", "Private"])
    bed = rng.randint(1, 25)
    pt_name = _patient_name(parts)
    lines = [
        "WARD DRUG CHART",
        "-" * 45,
        "%s  Ward: %s  Bed: %d  Date: %s" % (pt_name, ward, bed, parts["date"]),
        "-" * 60,
        "Time   | Drug Details",
        "-" * 60,
    ]
    times = ["06:00", "08:00", "14:00", "18:00", "20:00", "22:00"]
    for ml in parts["med_lines"]:
        t = rng.choice(times)
        lines.append("%s | %s" % (t, ml))
    lines.append("-" * 60)
    lines.append("")
    lines.append("Prescriber: %s" % doc_name)
    lines.append("Sign: _________________")
    return "\n".join(lines)


def _format_discharge_medication(parts):
    rng = parts.get("_rng", random)
    doc_name = parts["header"].split("\n")[0] if parts["header"] else "Dr. ________"
    hospital = rng.choice([
        "Apollo Hospital", "Fortis Healthcare", "Max Hospital",
        "AIIMS", "Sir Ganga Ram Hospital", "Medanta",
    ])
    adm_date = "%d/%d/%d" % (rng.randint(1, 28), rng.randint(1, 12), 2026)
    lines = [
        "DISCHARGE MEDICATION",
        "=" * 45,
        hospital,
        "",
        parts["patient"],
        "DOA: %s" % adm_date,
        "DOD: %s" % parts["date"],
        "Diagnosis: %s" % parts["condition_name"],
        "",
        "DISCHARGE Rx",
    ]
    for i, ml in enumerate(parts["med_lines"], 1):
        lines.append("  %d. %s" % (i, ml))
    if parts["advice"]:
        lines.append("")
        lines.append("Discharge Advice:")
        for a in parts["advice"]:
            lines.append("  - %s" % a)
    lines.append("")
    lines.append(parts["followup"])
    lines.append("")
    lines.append("Treating Doctor: %s" % doc_name)
    lines.append("Signature: _________________")
    lines.append("Hospital Seal")
    return "\n".join(lines)


PRESCRIPTION_FORMATS = {
    "private_clinic": _format_private_clinic,
    "govt_hospital_opd": _format_govt_hospital_opd,
    "corporate_hospital_ehr": _format_corporate_hospital_ehr,
    "pediatric": _format_pediatric,
    "chronic_followup": _format_chronic_followup,
    "er": _format_er,
    "nursing_home": _format_nursing_home,
    "specialist_referral": _format_specialist_referral,
    "telemedicine": _format_telemedicine,
    "cghs": _format_cghs,
    "pmjay": _format_pmjay,
    "rural_phc": _format_rural_phc,
    "typed_outpatient": _format_typed_outpatient,
    "hospital_letterhead": _format_hospital_letterhead,
    "referral_letter": _format_referral_letter,
    "solo_gp_pad": _format_solo_gp_pad,
    "gp_quick_strip": _format_gp_quick_strip,
    "sms_digital": _format_sms_digital,
    "tertiary_care": _format_tertiary_care,
    "ipd_orders": _format_ipd_orders,
    "surgical_post_op": _format_surgical_post_op,
    "emergency_discharge": _format_emergency_discharge,
    "ward_drug_chart": _format_ward_drug_chart,
    "discharge_medication": _format_discharge_medication,
}

# ---------------------------------------------------------------------------
# 5. Lab report format templates (10)
# ---------------------------------------------------------------------------

def _format_lab_standard(header, patient, dates, results, panel_key):
    parts = [header, "", patient, dates, "", panel_key.upper(), "-" * 80]
    for r in results:
        name = r["name"].ljust(35)
        res = str(r["result"]).ljust(10)
        unit = r["unit"].ljust(10)
        ref = r["ref_range"].ljust(15)
        line = "%s %s %s %s" % (name, res, unit, ref)
        if r["flag"]:
            line += "  %s" % r["flag"]
        parts.append(line)
    parts.append("-" * 80)
    parts.append("End of Report")
    return "\n".join(parts)


def _format_lab_compact(header, patient, dates, results, panel_key):
    parts = [header, "", patient, dates, "", panel_key.upper()]
    for r in results:
        line = "%s %s %s %s" % (r["name"], r["result"], r["unit"], r["ref_range"])
        if r["flag"]:
            line += " %s" % r["flag"]
        parts.append(line)
    parts.append("End of Report")
    return "\n".join(parts)


def _format_lab_narrative(header, patient, dates, results, panel_key):
    parts = [header, "", patient, dates, "", "Test: Results", "-" * 60]
    for r in results:
        name = r["name"]
        if r.get("short_name"):
            name = "%s (%s)" % (name, r["short_name"])
        ref = r["ref_range"]
        if ref:
            ref = " (Ref: %s)" % ref
        line = "%s: %s%s" % (name, r["result"], ref)
        if r["unit"]:
            line += " %s" % r["unit"]
        if r["flag"]:
            line += " -- %s" % r["flag"]
        parts.append(line)
    parts.append("-" * 60)
    parts.append("End of Report")
    return "\n".join(parts)


def _format_lab_minimal(header, patient, dates, results, panel_key):
    parts = [header, "", patient, dates, "", panel_key.upper()]
    for r in results:
        parts.append("%s: %s" % (r["name"], r["result"]))
    parts.append("End of Report")
    return "\n".join(parts)


def _format_lab_detailed(header, patient, dates, results, panel_key):
    parts = [header, "", patient, dates, "", panel_key.upper(), "=" * 90]
    for r in results:
        name = r["name"].ljust(35)
        if r.get("short_name"):
            name = ("%s(%s) " % (r["name"], r["short_name"])).ljust(35)
        res = str(r["result"]).ljust(10)
        unit = r["unit"].ljust(10)
        ref = r["ref_range"].ljust(15)
        flag = r["flag"] if r["flag"] else "Normal"
        line = "%s %s %s %s %s" % (name, res, unit, ref, flag)
        parts.append(line)
    parts.append("=" * 90)
    parts.append("End of Report")
    return "\n".join(parts)


def _format_lab_letterhead(header, patient, dates, results, panel_key):
    header_lines = header.split("\n")
    if header_lines:
        org_abbr = random.choice(["APL", "DIA", "MAX", "SRL", "METRO"])
        phone = "+91-%d" % random.randint(1111111111, 9999999999)
        header_lines[0] = "%s DIAGNOSTICS" % header_lines[0].upper()
        header_lines.insert(1, "Phone: %s | Email: info@%s.in" % (phone, org_abbr.lower()))
    header_str = "\n".join(header_lines)
    parts = [header_str, "", patient, dates, "", panel_key.upper(), "=" * 80]
    for r in results:
        name = r["name"].ljust(30)
        res = str(r["result"]).ljust(8)
        unit = r["unit"].ljust(10)
        ref = r["ref_range"].ljust(15)
        line = "%s %s %s %s" % (name, res, unit, ref)
        if r["flag"]:
            line += "  %s" % r["flag"]
        parts.append(line)
    parts.append("=" * 80)
    parts.append("End of Report")
    parts.append("Lab Technician: _______________")
    parts.append("Pathologist: _______________")
    return "\n".join(parts)


def _format_lab_plain(header, patient, dates, results, panel_key):
    parts = [header, "", patient, dates, "", panel_key.upper()]
    for r in results:
        parts.append("%s" % r["name"])
        parts.append("%s %s" % (r["result"], r["unit"]))
        if r["ref_range"]:
            parts.append("Ref: %s" % r["ref_range"])
        parts.append("")
    parts.append("End of Report")
    return "\n".join(parts)


def _format_lab_tab_separated(header, patient, dates, results, panel_key):
    parts = [header, "", patient, dates, "", "Test Name\tResult\tUnit\tRef Range\tFlag", "-" * 60]
    for r in results:
        parts.append("%s\t%s\t%s\t%s\t%s" % (r["name"], r["result"], r["unit"], r["ref_range"], r["flag"]))
    parts.append("End of Report")
    return "\n".join(parts)


def _format_lab_two_column(header, patient, dates, results, panel_key):
    parts = [header, "", patient, dates, "", panel_key.upper(), "-" * 80]
    half = len(results) // 2 + len(results) % 2
    col1 = results[:half]
    col2 = results[half:]
    max_rows = max(len(col1), len(col2))
    for i in range(max_rows):
        left = ""
        right = ""
        if i < len(col1):
            r = col1[i]
            left = "%s %s %s %s" % (r["name"].ljust(25), str(r["result"]).ljust(8), r["unit"].ljust(8), r["ref_range"].ljust(12))
            if r["flag"]:
                left += " %s" % r["flag"]
        if i < len(col2):
            r = col2[i]
            right = "%s %s %s %s" % (r["name"].ljust(25), str(r["result"]).ljust(8), r["unit"].ljust(8), r["ref_range"].ljust(12))
            if r["flag"]:
                right += " %s" % r["flag"]
        parts.append("%s  %s" % (left.ljust(65), right))
    parts.append("-" * 80)
    parts.append("End of Report")
    return "\n".join(parts)


def _format_lab_with_comments(header, patient, dates, results, panel_key):
    parts = [header, "", patient, dates, "", "Test Results", "-" * 70]
    for r in results:
        comment = "Normal"
        if r["flag"] == "H":
            comment = "HIGH"
        elif r["flag"] == "L":
            comment = "LOW"
        name = r["name"]
        if r.get("short_name"):
            name = "%s (%s)" % (name, r["short_name"])
        parts.append("%s: %s %s [%s]" % (name, r["result"], r["unit"], comment))
    parts.append("-" * 70)
    parts.append("End of Report")
    return "\n".join(parts)


def _format_lab_govt_hospital(header, patient, dates, results, panel_key):
    parts = [
        "Government Medical College & Hospital",
        "Department of Laboratory Medicine", "",
        patient,
        dates, "",
        "Test                          Result",
        "-" * 50,
    ]
    for r in results:
        parts.append("%s %s" % (r["name"].ljust(30), r["result"]))
    parts.append("-" * 50)
    parts.append("End of Report")
    return "\n".join(parts)


LAB_FORMATS = {
    "standard": _format_lab_standard,
    "compact": _format_lab_compact,
    "narrative": _format_lab_narrative,
    "minimal": _format_lab_minimal,
    "detailed": _format_lab_detailed,
    "letterhead": _format_lab_letterhead,
    "plain": _format_lab_plain,
    "tab_separated": _format_lab_tab_separated,
    "two_column": _format_lab_two_column,
    "with_comments": _format_lab_with_comments,
    "govt_hospital": _format_lab_govt_hospital,
}

# ---------------------------------------------------------------------------
# 6. Pair generation
# ---------------------------------------------------------------------------

from .lab_report_gen import LAB_PANELS


def _generate_prescription_pair(rng, drug_db, noise_override=None):
    """Generate a single (noisy, clean) prescription pair."""
    condition_key = rng.choice(list(CONDITIONS.keys()))
    condition = CONDITIONS[condition_key]

    header = generate_doctor_header(rng)
    patient, sex, age = generate_patient_info(rng)
    date = generate_date(rng)

    context = _generate_patient_context(condition_key, rng)

    med_keys = pick_medicines(condition_key, rng)
    med_lines = []
    for mk in med_keys:
        ml = _format_medication_line_datadump(mk, rng, drug_db)
        if ml:
            med_lines.append(ml)

    advice = generate_advice(condition_key, rng)
    followup = generate_followup(condition_key, rng)

    format_name = rng.choice(list(PRESCRIPTION_FORMATS.keys()))
    format_fn = PRESCRIPTION_FORMATS[format_name]

    parts = {
        "header": header,
        "patient": patient,
        "date": date,
        "context": context,
        "med_lines": med_lines,
        "advice": advice,
        "followup": followup,
        "condition_name": condition["name"],
        "_rng": rng,
    }
    clean_text = format_fn(parts)

    if noise_override:
        noise_profile = noise_override
    else:
        noise_profile = rng.choice(PRESCRIPTION_NOISE_PROFILES.get(format_name, ["handwritten_moderate"]))

    noisy_text = inject_noise(clean_text, profile=noise_profile, seed=rng.randint(0, 2 ** 31))

    cer = char_error_rate(clean_text, noisy_text)
    wer = word_error_rate(clean_text, noisy_text)

    return {
        "type": "prescription",
        "format": format_name,
        "condition": condition_key,
        "clean": clean_text,
        "noisy": noisy_text,
        "noise_profile": noise_profile,
        "cer": round(cer, 4),
        "wer": round(wer, 4),
    }


def _generate_lab_report_pair(rng, noise_override=None):
    """Generate a single (noisy, clean) lab report pair."""
    panel_key = rng.choice(list(LAB_PANELS.keys()))

    header = generate_lab_header(rng)
    patient, sex, age = gen_lab_patient(rng)
    dates = gen_lab_date(rng)
    results = generate_panel(panel_key, rng, sex)

    if rng.random() < 0.2:
        other_panels = [p for p in LAB_PANELS if p != panel_key]
        if other_panels:
            panel2 = rng.choice(other_panels)
            results.extend(generate_panel(panel2, rng, sex))
            panel_key = "%s + %s" % (panel_key, panel2)

    format_name = rng.choice(list(LAB_FORMATS.keys()))
    format_fn = LAB_FORMATS[format_name]
    clean_text = format_fn(header, patient, dates, results, panel_key)

    if noise_override:
        noise_profile = noise_override
    else:
        noise_profile = rng.choice(LAB_NOISE_PROFILES)

    noisy_text = inject_noise(clean_text, profile=noise_profile, seed=rng.randint(0, 2 ** 31))

    cer = char_error_rate(clean_text, noisy_text)
    wer = word_error_rate(clean_text, noisy_text)

    return {
        "type": "lab_report",
        "format": format_name,
        "panel": panel_key,
        "clean": clean_text,
        "noisy": noisy_text,
        "noise_profile": noise_profile,
        "cer": round(cer, 4),
        "wer": round(wer, 4),
    }

# ---------------------------------------------------------------------------
# 7. Output
# ---------------------------------------------------------------------------

def _write_jsonl(pairs, output_path):
    """Write pairs to a JSONL file."""
    out_dir = os.path.dirname(output_path) or "."
    os.makedirs(out_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for pair in pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + "\n")


def _percentile(sorted_data, p):
    if not sorted_data:
        return 0
    k = (len(sorted_data) - 1) * p / 100
    f = int(k)
    c = k - f
    if f + 1 < len(sorted_data):
        return sorted_data[f] + (sorted_data[f + 1] - sorted_data[f]) * c
    return sorted_data[f]


def _describe(data):
    if not data:
        return {}
    s = sorted(data)
    return {
        "min": round(s[0], 4),
        "max": round(s[-1], 4),
        "mean": round(sum(data) / len(data), 4),
        "median": round(_percentile(s, 50), 4),
        "p25": round(_percentile(s, 25), 4),
        "p75": round(_percentile(s, 75), 4),
        "p90": round(_percentile(s, 90), 4),
    }


def _compute_stats(pairs):
    """Compute statistics for generated pairs."""
    stats = {
        "total": len(pairs),
        "by_type": {},
        "by_format": {},
        "by_noise_profile": {},
        "cer": {},
        "wer": {},
        "text_length": {},
    }

    for pair in pairs:
        t = pair["type"]
        f = pair["format"]
        np = pair["noise_profile"]
        stats["by_type"][t] = stats["by_type"].get(t, 0) + 1
        stats["by_format"][f] = stats["by_format"].get(f, 0) + 1
        stats["by_noise_profile"][np] = stats["by_noise_profile"].get(np, 0) + 1

    stats["cer"] = _describe([p["cer"] for p in pairs])
    stats["wer"] = _describe([p["wer"] for p in pairs])
    stats["text_length"] = _describe([len(p["clean"]) for p in pairs])

    return stats

# ---------------------------------------------------------------------------
# 8. Main pipeline
# ---------------------------------------------------------------------------

def generate_pairs(n=1000, doc_type="mixed", seed=42, noise_override=None,
                   datadump_path=None, use_cache=True, output_path=None):
    """Generate n (noisy, clean) pairs and write to JSONL.

    Parameters
    ----------
    n : int
        Number of pairs to generate.
    doc_type : str
        "prescription", "lab_report", or "mixed".
    seed : int
        Random seed for reproducibility.
    noise_override : str or None
        If set, use this noise profile for all documents.
    datadump_path : str or None
        Path to DataDump directory. Auto-detects if None.
    use_cache : bool
        Whether to use DataDump cache file.
    output_path : str or None
        Output JSONL file path. If None, pairs are not written to file.

    Returns
    -------
    (list of dicts, dict) : (pairs, statistics)
    """
    rng = random.Random(seed)

    drug_db = load_drug_database(datadump_path, use_cache)

    pairs = []
    for i in range(n):
        if doc_type == "mixed":
            dt = rng.choice(["prescription", "lab_report"])
        else:
            dt = doc_type

        if dt == "prescription":
            pair = _generate_prescription_pair(rng, drug_db, noise_override)
        else:
            pair = _generate_lab_report_pair(rng, noise_override)

        pair["id"] = "%s_%06d" % (dt[:3], i + 1)
        pairs.append(pair)

    if output_path:
        _write_jsonl(pairs, output_path)

    stats = _compute_stats(pairs)

    return pairs, stats

# ---------------------------------------------------------------------------
# 9. CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic (noisy, clean) medical document pairs"
    )
    parser.add_argument("--n", type=int, default=1000, help="Number of pairs to generate")
    parser.add_argument("--type", choices=["prescription", "lab_report", "mixed"], default="mixed")
    parser.add_argument("--output", default="data/pairs.jsonl", help="Output JSONL path")
    parser.add_argument("--datadump", default=None, help="DataDump directory path")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--noise", default=None, help="Noise profile override (e.g. handwritten_moderate)")
    parser.add_argument("--stats", action="store_true", help="Print statistics")
    parser.add_argument("--no-cache", action="store_true", help="Don't use DataDump cache")
    args = parser.parse_args()

    pairs, stats = generate_pairs(
        n=args.n,
        doc_type=args.type,
        seed=args.seed,
        noise_override=args.noise,
        datadump_path=args.datadump,
        use_cache=not args.no_cache,
        output_path=args.output,
    )

    print("Generated %d pairs -> %s" % (len(pairs), os.path.abspath(args.output)))

    if args.stats:
        print("\n=== Statistics ===")
        print(json.dumps(stats, indent=2, ensure_ascii=False))

        stats_path = os.path.splitext(args.output)[0] + "_stats.json"
        with open(stats_path, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        print("Stats saved to %s" % os.path.abspath(stats_path))


if __name__ == "__main__":
    main()
