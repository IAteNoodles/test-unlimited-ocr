"""
generate_calibrated.py
======================
Generate calibrated (noisy, clean) pairs with CER distribution
~ Normal(mean=0.60, std=0.20), clipped to [0.09, 1.0].

Uses profile-tier approach: maps target CER to the nearest profile
whose mean CER is closest, plus a boosted tier for high CER targets.

Usage:
    python -m synthetic_data.generate_calibrated --n 100000 --output data/calibrated_100k.jsonl --workers 16
"""

import sys, os, json, math, random, time, argparse
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from synthetic_data.generate_data import (
    load_drug_database, _generate_patient_context, _format_medication_line_datadump,
    generate_doctor_header, generate_patient_info, generate_date,
    pick_medicines, generate_advice, generate_followup,
    PRESCRIPTION_FORMATS, LAB_FORMATS,
)
from synthetic_data.coprescription_rules import CONDITIONS
from synthetic_data.lab_report_gen import (
    LAB_PANELS, generate_lab_header,
    generate_patient_info as lab_patient_info,
    generate_date as lab_date, generate_panel,
)
from synthetic_data.noise_model import inject_noise, inject_noise_custom

# ---------------------------------------------------------------------------
# Profile-tier configuration
# ---------------------------------------------------------------------------
# Each tier: (target_cer_threshold, profile_name_or_None_for_boosted, expected_mean_cer)
# Thresholds determined from Normal(0.60, 0.20) quantiles
TIERS = [
    (0.12,   'printed_clean',           0.111),
    (0.23,   'printed_moderate',        0.247),
    (0.35,   'handwritten_moderate',    0.337),
    (0.55,   'handwritten_severe',      0.471),
    (0.78,   'handwritten_catastrophic',0.639),
    (1.01,   None,                      0.913),  # boosted
]

BOOSTED_PARAMS = {
    'substitute': 0.22, 'delete': 0.12, 'insert': 0.10,
    'transpose': 0.06, 'merge_words': 0.20, 'split_words': 0.10,
    'merge_lines': 0.15, 'split_lines': 0.10, 'medical': 0.20,
    'blank': 0.10, 'garbage': 0.10, 'repeat': 0.12, 'severe_del': 0.15,
    'hallucinate': 0.20, 'shuffle': 0.10, 'section_drop': 0.15, 'form_field': 0.10,
    'zone_chaos': 0.98,
    'prefix_deg': 0.80, 'dosage': 0.80, 'ligature': 0.75,
    'strikethrough': 1.0, 'line_merge': 0.40,
}

def _pick_tier(target_cer):
    for thr, prof, _ in TIERS:
        if target_cer < thr:
            return prof
    return None  # boosted

# ---------------------------------------------------------------------------
# Document generation (stateless, seed-driven)
# ---------------------------------------------------------------------------
CONDITIONS_KEYS = list(CONDITIONS.keys())
LAB_PANEL_KEYS = list(LAB_PANELS.keys())
PRESCRIPTION_FMT_KEYS = list(PRESCRIPTION_FORMATS.keys())
LAB_FMT_KEYS = list(LAB_FORMATS.keys())

def _levenshtein(a, b):
    m, n = len(a), len(b)
    if m == 0:
        return n
    if n == 0:
        return m
    prev = list(range(n + 1))
    for i in range(1, m + 1):
        cur = [i] + [0] * n
        ai = a[i - 1]
        for j in range(1, n + 1):
            cost = 0 if ai == b[j - 1] else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
        prev = cur
    return prev[n]

def cer(gt, pred):
    if not gt:
        return 0.0 if not pred else float('inf')
    return _levenshtein(gt, pred) / len(gt)

def generate_one(args):
    """Generate a single pair. args: (worker_id, pair_idx, datadump_path, use_cache)."""
    worker_id, pair_idx, datadump_path, use_cache = args
    rng = random.Random(pair_idx * 9973 + worker_id * 7919)

    # Draw target CER from truncated normal (shifted mean to compensate)
    target = -1.0
    while not (0.09 <= target <= 1.0):
        target = random.gauss(0.64, 0.20)

    # Pick noise tier
    profile = _pick_tier(target)

    # Load drug DB (cached per worker)
    drug_db = load_drug_database(datadump_path, use_cache)

    # Generate document - prescription or lab report
    dt = rng.choice(['prescription', 'lab_report'])

    if dt == 'prescription':
        ck = rng.choice(CONDITIONS_KEYS)
        cond = CONDITIONS[ck]
        header = generate_doctor_header(rng)
        patient, sex, age = generate_patient_info(rng)
        date = generate_date(rng)
        context = _generate_patient_context(ck, rng)
        med_keys = pick_medicines(ck, rng)
        med_lines = []
        for mk in med_keys:
            ml = _format_medication_line_datadump(mk, rng, drug_db)
            if ml:
                med_lines.append(ml)
        advice = generate_advice(ck, rng)
        followup = generate_followup(ck, rng)
        fmt = rng.choice(PRESCRIPTION_FMT_KEYS)
        parts = {
            'header': header, 'patient': patient, 'date': date,
            'context': context, 'med_lines': med_lines, 'advice': advice,
            'followup': followup, 'condition_name': cond['name'], '_rng': rng,
        }
        clean = PRESCRIPTION_FORMATS[fmt](parts)
        meta = {'type': 'prescription', 'format': fmt, 'condition': ck}
    else:
        panel_key = rng.choice(LAB_PANEL_KEYS)
        header = generate_lab_header(rng)
        patient, sex, age = lab_patient_info(rng)
        dates = lab_date(rng)
        results = generate_panel(panel_key, rng, sex)
        if rng.random() < 0.2:
            other = [p for p in LAB_PANEL_KEYS if p != panel_key]
            if other:
                p2 = rng.choice(other)
                results.extend(generate_panel(p2, rng, sex))
                panel_key = '%s+%s' % (panel_key, p2)
        fmt = rng.choice(LAB_FMT_KEYS)
        clean = LAB_FORMATS[fmt](header, patient, dates, results, panel_key)
        meta = {'type': 'lab_report', 'format': fmt, 'panel': panel_key}

    # Apply noise with retry for CER > 1.0 or CER < 0.09
    doc_seed = rng.randint(0, 2**31)
    best_cer = 999.0
    best_noisy = None
    best_seed = doc_seed

    for attempt in range(5):
        s = doc_seed + attempt * 7919
        if profile is not None:
            noisy = inject_noise(clean, profile=profile, seed=s)
        else:
            noisy = inject_noise_custom(clean, seed=s, **BOOSTED_PARAMS)
        actual_cer = cer(clean, noisy)

        if 0.09 <= actual_cer <= 1.0:
            best_cer = actual_cer
            best_noisy = noisy
            best_seed = s
            break

        # Track best in-range fallback
        if actual_cer < best_cer:
            best_cer = actual_cer
            best_noisy = noisy
            best_seed = s

    return {
        'id': 'pair_%07d' % pair_idx,
        'clean': clean,
        'noisy': best_noisy,
        'cer': round(best_cer, 4),
        'target_cer': round(target, 4),
        'tier': profile if profile else 'boosted',
        **meta,
    }

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Generate calibrated noisy/clean pairs')
    parser.add_argument('--n', type=int, default=100000, help='Number of pairs')
    parser.add_argument('--output', default='data/calibrated_100k.jsonl', help='Output JSONL path')
    parser.add_argument('--workers', type=int, default=16, help='Worker processes')
    parser.add_argument('--datadump', default=None, help='DataDump directory')
    parser.add_argument('--no-cache', action='store_true', help='Skip DataDump cache')
    args = parser.parse_args()

    out_dir = os.path.dirname(args.output) or '.'
    os.makedirs(out_dir, exist_ok=True)

    print('Loading drug database...', flush=True)
    load_drug_database(args.datadump, not args.no_cache)
    print('Drug DB loaded. Generating %d pairs with %d workers...' % (args.n, args.workers), flush=True)
    start = time.time()

    tasks = [(i % args.workers, i, args.datadump, not args.no_cache) for i in range(args.n)]

    with Pool(args.workers) as pool:
        pairs = []
        for i, pair in enumerate(pool.imap_unordered(generate_one, tasks, chunksize=100)):
            pairs.append(pair)
            if (i + 1) % 10000 == 0:
                elapsed = time.time() - start
                rate = (i + 1) / elapsed
                eta = (args.n - i - 1) / rate
                cers = [p['cer'] for p in pairs]
                print('  %d/%d (%.1f/s, ETA %.0f min) CER mean=%.3f range=[%.3f,%.3f]' % (
                    i + 1, args.n, rate, eta / 60,
                    sum(cers)/len(cers), min(cers), max(cers)), flush=True)

    elapsed = time.time() - start
    cers = [p['cer'] for p in pairs]
    m = sum(cers) / len(cers)
    s = (sum((c - m)**2 for c in cers) / len(cers))**0.5
    sorted_cer = sorted(cers)

    print('Done. %d pairs in %.1f min (%.1f/s)' % (len(pairs), elapsed / 60, len(pairs) / elapsed))
    print('CER: mean=%.4f  std=%.4f  median=%.4f  p5=%.4f  p95=%.4f  range=[%.4f, %.4f]' % (
        m, s, sorted_cer[len(cers)//2],
        sorted_cer[int(len(cers)*0.05)], sorted_cer[int(len(cers)*0.95)],
        min(cers), max(cers)))
    print('Type: presc=%d  lab=%d' % (
        sum(1 for p in pairs if p['type'] == 'prescription'),
        sum(1 for p in pairs if p['type'] == 'lab_report')))

    # Write output
    with open(args.output, 'w', encoding='utf-8') as f:
        for pair in pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + '\n')
    print('Written to %s' % os.path.abspath(args.output), flush=True)

    # Write stats
    stats_path = os.path.splitext(args.output)[0] + '_stats.json'
    stats = {
        'total': len(pairs),
        'cer': {'mean': round(m, 4), 'std': round(s, 4), 'min': round(min(cers), 4),
                'max': round(max(cers), 4), 'p5': round(sorted_cer[int(len(cers)*0.05)], 4),
                'p95': round(sorted_cer[int(len(cers)*0.95)], 4),
                'median': round(sorted_cer[len(cers)//2], 4)},
    }
    with open(stats_path, 'w') as f:
        json.dump(stats, f, indent=2)
    print('Stats written to %s' % os.path.abspath(stats_path), flush=True)

if __name__ == '__main__':
    main()
