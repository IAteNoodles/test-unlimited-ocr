"""
lab_report_gen.py
=================

Synthetic Indian lab report text generator.

Produces clean, realistic lab report text using lab_tests_db.py.  The output
is plain text that mimics what an OCR engine would read from a printed lab
report (tables, numeric values, reference ranges).

Usage
-----
    from synthetic_data.lab_report_gen import generate_lab_report, generate_batch

    report = generate_lab_report(seed=42)
    batch = generate_batch(100, seed=0)
"""

import random

from .lab_tests_db import (
    LAB_TESTS,
    LAB_PANELS,
    LAB_CHAINS,
    DOCTOR_SPECIALTIES,
)


# ---------------------------------------------------------------------------
# Indian name pools (shared with prescription_gen but kept independent)
# ---------------------------------------------------------------------------
_MALE_FIRST = [
    "Rajesh", "Amit", "Suresh", "Ramesh", "Vijay", "Anil", "Sunil", "Sanjay",
    "Deepak", "Manoj", "Pradeep", "Rakesh", "Mohan", "Arjun", "Karthik",
    "Sridhar", "Ganesh", "Harish", "Mukesh", "Naveen", "Prakash", "Ravi",
    "Sachin", "Vikram", "Ashok", "Dinesh", "Gopal", "Kiran", "Mahesh",
    "Nitin", "Pankaj", "Rahul", "Sandeep", "Venkat", "Abhishek", "Aditya",
    "Akash", "Rohit", "Saurabh", "Varun", "Arun", "Balaji", "Chetan",
    "Devendra", "Farooq", "Imran", "Javed", "Kamal", "Lokesh",
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
    "Pawar", "Deshmukh", "Kamble", "Naik", "Kurian", "Thomas",
    "D'Souza", "Fernandes", "Pinto", "Correia", "Mascarenhas",
]

_DOCTOR_FIRST = [
    "Rajesh", "Amit", "Suresh", "Vijay", "Anil", "Sunil", "Sanjay",
    "Deepak", "Manoj", "Pradeep", "Rakesh", "Mohan", "Arjun", "Karthik",
    "Sridhar", "Ganesh", "Harish", "Mukesh", "Naveen", "Prakash",
]

_CITIES = [
    "New Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Chennai", "Kolkata",
    "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Surat", "Kochi", "Coimbatore",
    "Indore", "Patna", "Bhopal", "Nagpur", "Visakhapatnam", "Vadodara",
    "Nashik", "Faridabad", "Ghaziabad", "Noida", "Gurugram",
]

_AREAS = [
    "MG Road", "Station Road", "Gandhi Nagar", "Nehru Marg", "Civil Lines",
    "Rajaji Marg", "Subhash Road", "Patel Chowk", "Ambedkar Road",
    "Jawahar Marg", "Indira Nagar", "Shastri Nagar", "Vivekananda Road",
    "Tagore Marg", "Bose Road", "Azad Marg", "Brigade Road", "Anna Salai",
    "Linking Road", "Park Street",
]


# ---------------------------------------------------------------------------
# Lab header / patient / date helpers
# ---------------------------------------------------------------------------
def generate_lab_header(rng):
    """Return a multi-line lab header string."""
    chain = rng.choice(LAB_CHAINS)
    name = chain["name"]
    nabl = "NABL Accredited" if chain["nabl"] else ""
    area = rng.choice(_AREAS)
    city = rng.choice(_CITIES)
    ref = "Ref: %s%06d" % (chain["abbr"], rng.randint(1, 999999))

    lines = [name]
    if nabl:
        lines.append(nabl)
    lines.append("%s, %s" % (area, city))
    lines.append(ref)
    return "\n".join(lines)


def generate_patient_info(rng):
    """Return patient info lines, sex, and age."""
    sex = rng.choice(["M", "M", "M", "F", "F"])
    if sex == "M":
        first = rng.choice(_MALE_FIRST)
    else:
        first = rng.choice(_FEMALE_FIRST)
    last = rng.choice(_LAST_NAMES)
    name = "%s %s" % (first, last)
    age = rng.randint(1, 85)

    doc_first = rng.choice(_DOCTOR_FIRST)
    doc_last = rng.choice(_LAST_NAMES)
    ref_by = "Dr. %s %s" % (doc_first, doc_last)

    lines = [
        "Patient: %s" % name,
        "Age: %d  Sex: %s" % (age, sex),
        "Ref by: %s" % ref_by,
    ]
    return "\n".join(lines), sex, age


def generate_date(rng):
    """Return collection and report dates."""
    d1 = rng.randint(1, 28)
    m1 = rng.randint(1, 12)
    y = rng.randint(2020, 2026)
    collected = "%02d/%02d/%d" % (d1, m1, y)

    # Report date: same day or next day
    d2 = d1 + rng.choice([0, 0, 0, 1, 1, 2])
    m2 = m1
    if d2 > 28:
        d2 = 28
        m2 = m1 + 1
        if m2 > 12:
            m2 = 1
            y += 1
    reported = "%02d/%02d/%d" % (d2, m2, y)

    return "Collected: %s\nReported: %s" % (collected, reported)


# ---------------------------------------------------------------------------
# Test result generation
# ---------------------------------------------------------------------------
def _generate_numeric_value(test_key, test_def, rng, sex):
    """Generate a realistic numeric result for a test.

    60% of the time the value is within the reference range.
    40% of the time it is abnormal (biased toward common_abnormal direction).
    """
    ref = test_def.get("ref_range")
    if ref is None:
        return None

    rr = ref.get(sex, ref.get("male", ref.get("female")))
    if rr is None:
        return None

    low = rr["low"]
    high = rr["high"]
    dp = test_def.get("decimal_places", 1)
    common_abn = test_def.get("common_abnormal", "either")

    if rng.random() < 0.6:
        # Normal value: within range, but not at the very edges
        margin = (high - low) * 0.15
        val = rng.uniform(low + margin, high - margin)
    else:
        # Abnormal value
        spread = (high - low) * 0.4
        if common_abn == "high":
            val = rng.uniform(high, high + spread)
        elif common_abn == "low":
            val = rng.uniform(low - spread, low)
        else:
            # "either" — pick a direction
            if rng.random() < 0.5:
                val = rng.uniform(high, high + spread)
            else:
                val = rng.uniform(low - spread, low)

    # Clamp to non-negative for most tests
    if val < 0:
        val = 0.0

    if dp == 0:
        return int(round(val))
    return round(val, dp)


def _generate_string_value(test_def, rng):
    """Generate a realistic string/categorical result."""
    values = test_def.get("values")
    if not values:
        return None

    # Bias toward normal values
    if "Negative" in values and rng.random() < 0.7:
        return "Negative"
    if "Nil" in values and rng.random() < 0.7:
        return "Nil"
    if "Normal" in values and rng.random() < 0.7:
        return "Normal"

    return rng.choice(values)


def generate_test_result(test_key, rng, sex):
    """Generate a single test result line.

    Returns a dict: {name, result, unit, ref_range, flag}
    """
    test_def = LAB_TESTS.get(test_key)
    if test_def is None:
        return None

    name = test_def.get("name", test_key)
    short = test_def.get("short_name", "")
    unit = test_def.get("unit", "")
    ref = test_def.get("ref_range")

    # Determine result value
    if ref is not None:
        # Numeric test
        value = _generate_numeric_value(test_key, test_def, rng, sex)
        if value is None:
            return None
        result_str = str(value)
    else:
        # String/categorical test
        result_str = _generate_string_value(test_def, rng)
        if result_str is None:
            return None

    # Format reference range string
    if ref is not None:
        rr = ref.get(sex, ref.get("male", ref.get("female")))
        if rr:
            ref_str = "%s - %s" % (_fmt_num(rr["low"]), _fmt_num(rr["high"]))
        else:
            ref_str = ""
    else:
        ref_str = ""

    # Determine flag
    flag = ""
    if ref is not None:
        rr = ref.get(sex, ref.get("male", ref.get("female")))
        if rr:
            val = float(result_str)
            if val < rr["low"]:
                flag = "L"
            elif val > rr["high"]:
                flag = "H"

    return {
        "name": name,
        "short_name": short,
        "result": result_str,
        "unit": unit,
        "ref_range": ref_str,
        "flag": flag,
    }


def _fmt_num(v):
    """Format a number nicely (strip trailing .0)."""
    if v == int(v):
        return str(int(v))
    return str(v)


# ---------------------------------------------------------------------------
# Panel / report assembly
# ---------------------------------------------------------------------------
def generate_panel(panel_key, rng, sex):
    """Generate all test results for a panel.

    Returns a list of result dicts.
    """
    test_keys = LAB_PANELS.get(panel_key, [])
    results = []
    for tk in test_keys:
        r = generate_test_result(tk, rng, sex)
        if r:
            results.append(r)
    return results


def _format_result_line(result):
    """Format a single test result as a text line.

    Format: "Test Name          Result  Unit   Ref Range   Flag"
    """
    name = result["name"]
    res = result["result"]
    unit = result["unit"]
    ref = result["ref_range"]
    flag = result["flag"]

    # Pad name to 35 chars for alignment
    name_padded = name.ljust(35)
    res_padded = str(res).ljust(10)
    unit_padded = unit.ljust(10)
    ref_padded = ref.ljust(15)

    line = "%s %s %s %s" % (name_padded, res_padded, unit_padded, ref_padded)
    if flag:
        line += "  %s" % flag
    return line


def generate_lab_report(rng=None, panel_key=None):
    """Generate a single full lab report as clean text.

    Parameters
    ----------
    rng : random.Random or None
    panel_key : str or None
        If None, a random panel is chosen. Sometimes 2 panels are combined.

    Returns
    -------
    dict with keys:
        "text"  : full lab report text
        "panel" : panel key
        "sex"   : patient sex
        "age"   : patient age
    """
    if rng is None:
        rng = random.Random()

    if panel_key is None:
        panel_key = rng.choice(list(LAB_PANELS.keys()))

    header = generate_lab_header(rng)
    patient, sex, age = generate_patient_info(rng)
    dates = generate_date(rng)

    results = generate_panel(panel_key, rng, sex)

    # Sometimes add a second panel (20% chance)
    if rng.random() < 0.2:
        other_panels = [p for p in LAB_PANELS if p != panel_key]
        if other_panels:
            panel2 = rng.choice(other_panels)
            results2 = generate_panel(panel2, rng, sex)
            results.extend(results2)
            panel_key = "%s + %s" % (panel_key, panel2)

    # Assemble
    parts = [
        header,
        "",
        patient,
        dates,
        "",
        panel_key.upper(),
        "-" * 80,
    ]

    for r in results:
        parts.append(_format_result_line(r))

    parts.append("-" * 80)
    parts.append("End of Report")

    text = "\n".join(parts)

    return {
        "text": text,
        "panel": panel_key,
        "sex": sex,
        "age": age,
    }


def generate_batch(n, seed=None):
    """Generate n lab reports.

    Returns a list of dicts (see generate_lab_report).
    """
    rng = random.Random(seed)
    return [generate_lab_report(rng=rng) for _ in range(n)]


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("LAB REPORT GENERATOR DEMO")
    print("=" * 70)

    for i in range(3):
        result = generate_lab_report(rng=random.Random(200 + i))
        print("\n" + "-" * 70)
        print("Sample %d (panel: %s)" % (i + 1, result["panel"]))
        print("-" * 70)
        print(result["text"])
        print()

    # Batch
    batch = generate_batch(10, seed=42)
    print("\nGenerated %d lab reports in batch." % len(batch))
    panels_used = set(r["panel"] for r in batch)
    print("Panels used: %s" % ", ".join(sorted(panels_used)))