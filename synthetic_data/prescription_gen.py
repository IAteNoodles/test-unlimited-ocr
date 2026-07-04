"""
prescription_gen.py
===================

Synthetic Indian medical prescription text generator.

Produces clean, realistic prescription text using medicines_db.py and
coprescription_rules.py.  The output is plain text that mimics what an OCR
engine would read from a handwritten or printed prescription.

Usage
-----
    from synthetic_data.prescription_gen import generate_prescription, generate_batch

    rx = generate_prescription(seed=42)
    batch = generate_batch(100, seed=0)
"""

import random

from .medicines_db import MEDICINES, FDCS
from .coprescription_rules import (
    CONDITIONS,
    ADVICE_TEMPLATES,
    FOLLOWUP_DAYS,
    DOSAGE_FORMS,
    FREQUENCY_CODES,
    DURATION_OPTIONS,
)


# ---------------------------------------------------------------------------
# Indian name pools
# ---------------------------------------------------------------------------
_MALE_FIRST = [
    "Rajesh", "Amit", "Suresh", "Ramesh", "Vijay", "Anil", "Sunil", "Sanjay",
    "Deepak", "Manoj", "Pradeep", "Rakesh", "Mohan", "Arjun", "Karthik",
    "Sridhar", "Ganesh", "Harish", "Mukesh", "Naveen", "Prakash", "Ravi",
    "Sachin", "Vikram", "Ashok", "Dinesh", "Gopal", "Kiran", "Mahesh",
    "Nitin", "Pankaj", "Rahul", "Sandeep", "Venkat", "Abhishek", "Aditya",
    "Akash", "Rohit", "Saurabh", "Varun", "Rahul", "Arun", "Balaji",
    "Chetan", "Devendra", "Farooq", "Imran", "Javed", "Kamal", "Lokesh",
]

_FEMALE_FIRST = [
    "Priya", "Sunita", "Anita", "Smita", "Kavita", "Meena", "Geeta", "Rekha",
    "Archana", "Deepa", "Jyoti", "Lata", "Manju", "Neeta", "Pooja", "Ritu",
    "Sarla", "Usha", "Vandana", "Anjali", "Bhavna", "Charu", "Divya",
    "Ekta", "Falguni", "Gauri", "Harita", "Ila", "Jigna", "Kalpana",
    "Lakshmi", "Madhuri", "Nisha", "Padma", "Radha", "Shobha", "Tara",
    "Uma", "Vaishali", "Yamuna", "Aarti", "Babita", "Chitra", "Dipali",
    "Esha", "Gita", "Hema", "Indu", "Jaya", "Kiran",
]

_LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Patel", "Reddy", "Nair", "Iyer", "Menon",
    "Pillai", "Rao", "Murthy", "Shetty", "Gowda", "Desai", "Joshi", "Kulkarni",
    "Mehta", "Shah", "Jain", "Agarwal", "Singh", "Kaur", "Khan", "Sheikh",
    "Ali", "Das", "Bose", "Banerjee", "Mukherjee", "Chatterjee", "Naidu",
    "Pandey", "Mishra", "Tiwari", "Dubey", "Saxena", "Chauhan", "Yadav",
    "Pawar", "Deshmukh", "Kamble", "Naik", "Pillai", "Kurian", "Thomas",
    "D'Souza", "Fernandes", "Pinto", "Correia", "Mascarenhas",
]

_CLINIC_NAMES = [
    "Sharma Clinic", "City Care Hospital", "Sai Hospital", "Apollo Clinic",
    "Care Hospital", "Life Line Clinic", "Health Plus Clinic", "Shree Clinic",
    "Anand Clinic", "Surya Hospital", "Metro Hospital", "Sunrise Clinic",
    "Wellness Centre", "Healing Hands Clinic", "Trinity Hospital",
    "Sanjeevani Hospital", "Dhanvantri Clinic", "Aarogya Clinic",
    "Prakash Clinic", "Sparsh Hospital", "Vatsalya Clinic", "Maa Clinic",
    "New Life Hospital", "Santosh Clinic", "Sneha Hospital", "Vinayak Clinic",
]

_CITIES = [
    "New Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Chennai", "Kolkata",
    "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Surat", "Kochi", "Coimbatore",
    "Indore", "Patna", "Bhopal", "Nagpur", "Visakhapatnam", "Vadodara",
    "Nashik", "Faridabad", "Ghaziabad", "Noida", "Gurugram",
]

_STREETS = [
    "MG Road", "Station Road", "Main Bazaar", "Gandhi Nagar", "Nehru Marg",
    "Civil Lines", "Rajaji Marg", "Subhash Road", "Patel Chowk", "Ambedkar Road",
    "Jawahar Marg", "Indira Nagar", "Shastri Nagar", "Vivekananda Road",
    "Tagore Marg", "Bose Road", "Azad Marg", "Bhagat Singh Chowk",
]


# ---------------------------------------------------------------------------
# Helper: weighted pick from a prescription line
# ---------------------------------------------------------------------------
def _pick_from_line(line, rng):
    """Pick 0+ medicines from a prescription-pattern line dict."""
    options = line["options"]
    min_pick = line["min_pick"]
    max_pick = line["max_pick"]
    weight = line.get("weight", 1.0)

    # Decide whether to include this line at all (based on weight)
    if rng.random() > weight:
        return []

    n = len(options)
    if n == 0:
        return []
    k = min(rng.randint(min_pick, max_pick), n)
    return rng.sample(options, k)


# ---------------------------------------------------------------------------
# Doctor / patient / date helpers
# ---------------------------------------------------------------------------
def generate_doctor_header(rng):
    """Return a multi-line doctor header string."""
    specialty = rng.choice([
        "General Physician", "General Physician", "General Physician",
        "Pediatrician", "Cardiologist", "Diabetologist", "Orthopedic Surgeon",
        "Gynecologist", "Dermatologist", "ENT Specialist", "Physician",
        "General Medicine", "General Medicine",
    ])
    qual_map = {
        "General Physician": "MBBS, MD (Medicine)",
        "Pediatrician": "MBBS, MD (Pediatrics)",
        "Cardiologist": "MBBS, MD, DM (Cardiology)",
        "Diabetologist": "MBBS, MD, Fellowship (Diabetes)",
        "Orthopedic Surgeon": "MBBS, MS (Ortho)",
        "Gynecologist": "MBBS, MS (OBG)",
        "Dermatologist": "MBBS, MD (Dermatology)",
        "ENT Specialist": "MBBS, MS (ENT)",
        "Physician": "MBBS",
        "General Medicine": "MBBS, MD (Medicine)",
    }
    first = rng.choice(_MALE_FIRST)
    last = rng.choice(_LAST_NAMES)
    name = "Dr. %s %s" % (first, last)
    qual = qual_map.get(specialty, "MBBS, MD")
    reg = "%05d" % rng.randint(1, 99999)
    clinic = rng.choice(_CLINIC_NAMES)
    street = rng.choice(_STREETS)
    city = rng.choice(_CITIES)

    lines = [
        name,
        qual,
        "Reg No: %s" % reg,
        "%s, %s" % (clinic, city),
        "%s, %s" % (street, city),
    ]
    return "\n".join(lines)


def generate_patient_info(rng):
    """Return patient info lines."""
    sex = rng.choice(["M", "M", "M", "F", "F"])  # slight male skew
    if sex == "M":
        first = rng.choice(_MALE_FIRST)
    else:
        first = rng.choice(_FEMALE_FIRST)
    last = rng.choice(_LAST_NAMES)
    name = "%s %s" % (first, last)
    age = rng.randint(1, 85)
    weight = rng.randint(8, 110)

    lines = [
        "Patient: %s" % name,
        "Age: %d  Sex: %s  Wt: %d kg" % (age, sex, weight),
    ]
    return "\n".join(lines), sex, age


def generate_date(rng):
    """Return a date string in DD/MM/YYYY format."""
    d = rng.randint(1, 28)
    m = rng.randint(1, 12)
    y = rng.randint(2020, 2026)
    return "%02d/%02d/%d" % (d, m, y)


# ---------------------------------------------------------------------------
# Medication line formatting
# ---------------------------------------------------------------------------
def _get_med_entry(med_key):
    """Return the medicine dict from MEDICINES or FDCS, or None."""
    if med_key in MEDICINES:
        return MEDICINES[med_key]
    if med_key in FDCS:
        return FDCS[med_key]
    return None


def format_medication_line(med_key, rng):
    """Format a single medication line.

    Examples:
        Tab Metformin 500mg 1-0-1
        Syp Paracetamol 250mg/5ml 1-1-1 x 5 days
        Cap Omeprazole 20mg OD before food
    """
    entry = _get_med_entry(med_key)
    if entry is None:
        return None

    # Pick form
    forms = entry.get("forms", ["Tab"])
    form = rng.choice(forms)

    # Pick strength
    strengths = entry.get("strengths", ["500mg"])
    strength = rng.choice(strengths)

    # Pick frequency
    freq_keys = list(FREQUENCY_CODES.keys())
    freq = rng.choice(freq_keys)

    # Pick duration (70% chance)
    duration = ""
    if rng.random() < 0.7:
        dur = rng.choice(DURATION_OPTIONS)
        if dur["days"] > 0:
            duration = " x %s" % dur["text"]

    # Food timing (30% chance)
    food = ""
    if rng.random() < 0.3:
        food = " " + rng.choice(["after food", "before food", "after food"])

    # Determine the display name
    if med_key in FDCS:
        # Use components joined with + for FDC
        components = entry.get("components", [])
        if components:
            name = " + ".join(components)
        else:
            name = med_key.replace("_", " ").title()
    else:
        name = entry.get("generic", med_key.replace("_", " ").title())

    line = "%s %s %s %s%s%s" % (form, name, strength, freq, food, duration)
    return line


# ---------------------------------------------------------------------------
# Advice / follow-up
# ---------------------------------------------------------------------------
def generate_advice(condition_key, rng):
    """Return a list of advice strings for the condition."""
    templates = ADVICE_TEMPLATES.get(condition_key, [])
    if not templates:
        return []
    # Pick 2-4 advice items
    k = min(rng.randint(2, 4), len(templates))
    return rng.sample(templates, k)


def generate_followup(condition_key, rng):
    """Return a follow-up string."""
    fu = FOLLOWUP_DAYS.get(condition_key)
    if fu is None:
        return "Review after 7 days"
    days = rng.randint(fu["min_days"], fu["max_days"])
    note = fu.get("note", "")
    if days <= 0:
        return note
    return "Review after %d days. %s" % (days, note)


# ---------------------------------------------------------------------------
# Full prescription assembly
# ---------------------------------------------------------------------------
def pick_medicines(condition_key, rng):
    """Pick medicines for a condition using the prescription pattern.

    Returns a list of med_keys.
    """
    cond = CONDITIONS.get(condition_key)
    if cond is None:
        return []

    pattern = cond.get("prescription_pattern", [])
    picked = []
    for line in pattern:
        picks = _pick_from_line(line, rng)
        picked.extend(picks)
    return picked


def generate_prescription(rng=None, condition_key=None):
    """Generate a single full prescription as clean text.

    Parameters
    ----------
    rng : random.Random or None
        If None, a new Random is created with a random seed.
    condition_key : str or None
        If None, a random condition is chosen.

    Returns
    -------
    dict with keys:
        "text"      : full prescription text
        "condition" : condition key
        "medicines" : list of med keys used
        "sex"       : patient sex
        "age"       : patient age
    """
    if rng is None:
        rng = random.Random()

    if condition_key is None:
        condition_key = rng.choice(list(CONDITIONS.keys()))

    header = generate_doctor_header(rng)
    patient, sex, age = generate_patient_info(rng)
    date = generate_date(rng)

    meds = pick_medicines(condition_key, rng)
    med_lines = []
    for mk in meds:
        ml = format_medication_line(mk, rng)
        if ml:
            med_lines.append(ml)

    advice = generate_advice(condition_key, rng)
    followup = generate_followup(condition_key, rng)

    # Assemble
    parts = [
        header,
        "",
        patient,
        "Date: %s" % date,
        "",
        "Rx",
    ]
    for ml in med_lines:
        parts.append(ml)

    if advice:
        parts.append("")
        parts.append("Advice:")
        for a in advice:
            parts.append("- %s" % a)

    parts.append("")
    parts.append(followup)

    text = "\n".join(parts)

    return {
        "text": text,
        "condition": condition_key,
        "medicines": meds,
        "sex": sex,
        "age": age,
    }


def generate_batch(n, seed=None):
    """Generate n prescriptions.

    Returns a list of dicts (see generate_prescription).
    """
    rng = random.Random(seed)
    return [generate_prescription(rng=rng) for _ in range(n)]


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("PRESCRIPTION GENERATOR DEMO")
    print("=" * 70)

    for i in range(3):
        result = generate_prescription(rng=random.Random(100 + i))
        print("\n" + "-" * 70)
        print("Sample %d (condition: %s)" % (i + 1, result["condition"]))
        print("-" * 70)
        print(result["text"])
        print()

    # Batch
    batch = generate_batch(10, seed=42)
    print("\nGenerated %d prescriptions in batch." % len(batch))
    conditions_used = set(r["condition"] for r in batch)
    print("Conditions used: %s" % ", ".join(sorted(conditions_used)))