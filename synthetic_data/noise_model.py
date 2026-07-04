"""
noise_model.py
==============

Realistic OCR noise injector for generating synthetic (noisy -> clean) training
pairs for post-OCR correction models.

Context
-------
Target domain: Indian medical documents -- printed lab reports (tables, numbers,
dense data) and handwritten prescriptions (doctor's handwriting, varying quality).

The noise model simulates errors that real OCR engines (Tesseract, PaddleOCR,
EasyOCR) make on this kind of content:
  - Character-level visual confusions (m/rn, 0/O, 1/l, 5/S, ...).
  - Deletions, insertions, transpositions.
  - Word merges / splits (OCR joining or breaking tokens).
  - Line merges / splits (OCR reading two lines as one, or breaking one line).
  - Medical-specific confusions (drug names, dosages, abbreviations).

Design
------
- Pure Python standard library only (random, string). No external dependencies.
- All noise functions take a probability `p` and are deterministic when a seed
  is set via `random.seed(...)` (done by `inject_noise` / `inject_noise_custom`).
- A named-profile pipeline (`inject_noise`) covers common scan quality tiers,
  from clean printed lab reports up to severe doctor's scrawl.
- Utility metrics (CER, WER) are provided to quantify injected noise.

Usage
-----
    from noise_model import inject_noise
    noisy = inject_noise(clean_text, profile="printed_moderate", seed=42)
"""

import random
import string


# ---------------------------------------------------------------------------
# 1. Character-level confusion matrices
# ---------------------------------------------------------------------------

# Visual similarity confusions: OCR sees similar shapes.
# Keys may be single chars or 2-char sequences (e.g. 'rn' -> 'm').
# Lists are weighted: more common confusions appear more times so
# random.choice() picks them more often.
#
# Sources: Tesseract confusion matrices, PaddleOCR known errors,
# ICDAR 2019/2021 OCR error analysis papers, common Indian Rx confusions.
CHAR_SUBS = {
    # ==================================================================
    # Multi-char <-> single char confusions (font rendering + handwriting)
    # ==================================================================
    'm':   ['rn', 'rn', 'rn', 'nn', 'in', 'ni'],   # m->rn is extremely common
    'rn':  ['m', 'm', 'm', 'nn'],
    'nn':  ['m', 'm', 'rn'],
    'cl':  ['d', 'd', 'd', 'a'],
    'd':   ['cl', 'cl', 'a', 'o', 'c', 'b', 'p'],
    'vv':  ['w', 'w'],
    'w':   ['vv', 'vv', 'u', 'n'],
    'ri':  ['n', 'n', 'm'],
    'n':   ['ri', 'ri', 'h', 'u', 'a', 'r'],
    'li':  ['h', 'h', 'u'],
    'lt':  ['k', 'k'],
    'k':   ['h', 'lt', 'lc'],
    'll':  ['H', 'h', 'u'],
    'ct':  ['d', 'd'],
    'ui':  ['w'],
    'VV':  ['W', 'W'],
    # ==================================================================
    # Digits <-> Letters
    # ==================================================================
    '0':   ['O', 'O', 'O', 'O', 'o', 'D', 'Q', 'C', '8'],
    'O':   ['0', '0', '0', '0', 'D', 'Q', 'C', 'U'],
    'o':   ['0', '0', 'O', 'a', 'e', 'c'],
    '1':   ['l', 'l', 'l', 'l', 'I', 'i', '|', '7', 't'],
    'l':   ['1', '1', '1', '1', 'I', 'i', '|', 't'],
    'I':   ['1', '1', 'l', 'l', '|', 'J'],
    'i':   ['1', '1', 'l', 'l', 'I', 'j', 't', '|'],
    '5':   ['S', 'S', 'S', 's', '3', '6', '8'],
    'S':   ['5', '5', '5', '8', 's', '3'],
    's':   ['5', '5', 'S', 'c', 'e', '8'],
    '8':   ['B', 'B', '3', 'S', '0', 's'],
    'B':   ['8', '8', '3', 'S'],
    '3':   ['8', '8', 'B', 'S', 'J', 's'],
    '2':   ['Z', 'Z', 'z', '7', '?'],
    'Z':   ['2', '2', 'z', '7'],
    'z':   ['2', '2', 'Z', 's'],
    '6':   ['G', 'G', 'b', '5', '8'],
    'G':   ['6', '6', 'C', 'O'],
    '9':   ['g', 'g', 'q', 'j', '3'],
    'g':   ['9', '9', 'q', 'y'],
    'q':   ['9', '9', 'g', 'a'],
    'C':   ['G', 'G', '6', 'O', 'L'],
    'E':   ['B', 'F', 'L', 'C'],
    'F':   ['E', 'E', 'T', 'P', 'l'],
    'T':   ['F', 'F', 'I', 'l', '1', 'J'],
    'H':   ['N', 'N', 'M', 'A', 'K'],
    'N':   ['H', 'H', 'M', 'W'],
    'M':   ['N', 'N', 'H', 'W', 'NN'],
    'U':   ['V', 'V', 'O', '0', 'LT'],
    'V':   ['U', 'U', 'Y', '\\/'],
    'W':   ['VV', 'VV', 'M', 'N'],
    'Y':   ['V', 'V', 'T', 'y'],
    '4':   ['A', 'A', 'H', '1'],
    'A':   ['4', '4', 'H', 'R'],
    '7':   ['1', '1', 'T', 'Z', '?'],
    # ==================================================================
    # Lowercase letter confusions (weighted by real PaddleOCR confusion
    # matrix on Indian Rx data from confusion_h13_paddleocr.json)
    # ==================================================================
    # Source confusion matrix measured substitutions across 729 Rx pairs.
    # Weights are raw frequency counts. Multiplied by 10 for integer weights.
    'a':   ['o']*10 + ['e']*8 + ['u']*5 + ['s']*6 + ['n']*3 + ['c']*3 + ['d']*2,
    'b':   ['h']*2 + ['d']*1 + ['a']*1,
    'c':   ['e']*12 + ['o']*4 + ['a']*3 + ['u']*1,
    'e':   ['c']*18 + ['a']*15 + ['o']*9 + ['r']*7 + ['n']*7 + ['i']*6 + ['s']*3 + ['l']*3,
    'f':   ['t']*11 + ['l']*2 + ['i']*1,
    'g':   ['y']*3 + ['q']*1 + ['j']*1,
    'h':   ['t']*10 + ['n']*4 + ['u']*2 + ['b']*2 + ['l']*1 + ['li']*1,
    'i':   ['t']*4 + ['r']*4 + ['l']*3 + ['e']*2 + ['n']*1,
    'j':   ['i']*1,
    'k':   ['h']*1 + ['lt']*1,
    'l':   ['i']*13 + ['t']*4 + ['e']*4 + ['h']*2,
    'm':   ['n']*7 + ['h']*2 + ['r']*1 + ['u']*1,
    'n':   ['r']*22 + ['h']*8 + ['a']*7 + ['u']*5 + ['m']*3,
    'o':   ['e']*14 + ['a']*6 + ['c']*3 + ['u']*1,
    'p':   ['f']*3 + ['d']*2,
    'q':   ['g']*1,
    'r':   ['n']*9 + ['l']*3 + ['i']*3 + ['t']*3 + ['s']*2,
    's':   ['c']*3 + ['o']*3 + ['e']*2 + ['a']*2,
    't':   ['l']*9 + ['n']*3 + ['f']*3 + ['h']*2 + ['i']*1 + ['s']*1 + ['r']*1,
    'u':   ['e']*9 + ['a']*4 + ['n']*2 + ['c']*1,
    'v':   ['u']*4 + ['y']*1,
    'w':   ['u']*1,
    'x':   ['k']*1 + [')']*1 + ['X']*1 + ['×']*1,
    'y':   ['v']*3 + ['g']*1 + ['j']*1 + ['u']*1,
    'z':   ['s']*1,
    # ==================================================================
    # Punctuation and symbols
    # ==================================================================
    '.':   [',', ',', "'", ' ', ':', '·'],
    ',':   ['.', '.', ' ', "'"],
    ':':   [';', ';', '.', "'"],
    ';':   [':', ',', "'"],
    "'":   ['.', ',', '`', ' '],
    '-':   [' ', '—', '–'],
    '/':   ['|', '|', 'l', '1', '7'],
    '|':   ['I', 'l', '1', '/', '|'],
    '(':   ['C', 'c', '{', '['],
    ')':   ['D', 'J', '}', ']'],
    '{':   ['(', 'C'],
    '}':   [')', 'D'],
    '[':   ['(', 'C'],
    ']':   [')', 'D'],
    '>':   [')', '7'],
    '<':   ['(', 'c'],
    '!':   ['1', 'I', 'l', '|'],
    '?':   ['7', '2', '?'],
    '@':   ['0', 'O'],
    '#':   ['H', 'h'],
    '$':   ['S', '5', 's'],
    '%':   ['0/0', 'o/o', '°'],
    '°':   ['0', 'o', '%'],
    '+':   ['t', 'l', '1', 'T'],
    '×':   ['x', 'X', '*'],
    'µ':   ['u', 'm', '\\mu'],
    '²':   ['2', '?'],
}

# Medical-specific confusions: drug names, dosages, abbreviations.
# Some value lists include the original token (no-op) so a "substitution" may
# occasionally leave the text unchanged, which is realistic.
# Weighted: common confusions appear multiple times.
MEDICAL_SUBS = {
    # ==================================================================
    # Drug name confusions (common Indian Rx drugs)
    # ==================================================================
    'metformin':  ['metformln', 'metformln', 'metformm', 'met formin', 'metformin'],
    'amoxicillin': ['amoxicilin', 'amoxlcillin', 'amoxiciilin', 'amoxiciliin'],
    'amoxycillin': ['amoxycilin', 'amoxvcillin', 'amoxycilin'],
    'azithromycin': ['azithromycm', 'azithromycm', 'azlthromycin', 'azithromycm'],
    'cetirizine':  ['cetirzine', 'cetirzme', 'cetrizine', 'cetirizme'],
    'paracetamol': ['paracetamol', 'paracetamoI', 'paracetamoi', 'paracetarnol'],
    'pantoprazole': ['pantoprazoIe', 'pantoprazoie', 'pantoprazone', 'pantoprazle'],
    'omeprazole':  ['omeprazoIe', 'omeprazle', 'onleprazole'],
    'atorvastatin': ['atorvastatln', 'atorvastatin', 'atorvastatiin'],
    'rosuvastatin': ['rosuvastatin', 'rosuvastatln', 'rosuvastatin'],
    'amlodipine':  ['arnlodipine', 'anlodipine', 'amlodipme'],
    'atenolol':    ['atenolol', 'atenolol', 'atenolol'],
    'losartan':    ['losartan', 'losartan', 'losartan'],
    'telmisartan': ['telmisartan', 'telmisartan', 'telmisartan'],
    'diclofenac':  ['diclofenac', 'dicloienac', 'diclofenac'],
    'ibuprofen':   ['ibuprolen', 'ibuprolen', 'ibuprolen'],
    'prednisolone': ['prednisolone', 'prednisolone', 'prednisolone'],
    'levothyroxine': ['levothyroxme', 'levothyroxlne', 'levothyroxme'],
    'montelukast': ['montelukast', 'montelukast', 'montelukast'],
    'salbutamol':  ['salbutamol', 'salbutamol', 'salbutamol'],
    'metronidazole': ['metronidazole', 'metronidazole', 'metronidazole'],
    'ciprofloxacin': ['ciproloxacin', 'ciprofloxacin', 'ciprofloxacin'],
    'carbamazepine': ['carbamazepine', 'carbamazepine', 'carbamazepine'],
    # Indian brand name base confusions
    'dolo': ['d0l0', 'doIo', 'dolo'],
    'crocin': ['croc1n', 'crocin', 'crocin'],
    'ecosprin': ['ecosprln', 'ecosprin', 'ecosprin'],
    'augmentin': ['augmentm', 'augmentm', 'augmentin'],
    'azithral':  ['azlthral', 'azithral', 'azithral'],
    # ==================================================================
    # Drug prefix confusions (observed from real PaddleOCR)
    # "T." → "7." / "8y." — letter-digit confusions for Rx prefixes
    # ==================================================================
    'T.':     ['7.', '8y.', 'T.', '7.', 'l.', '1.'],
    'Syp.':   ['8p.', 'Syp.', '5yp.', 'Syp.', 'Sy.'],
    'Tab':    ['7ab', 'Iab', 'Tab', '1ab'],
    'Cap':    ['Cap', '6ap', 'Cap', 'Cdp'],
    # ==================================================================
    # Dosage form confusions
    # ==================================================================
    'tab':    ['tab', 'tah', 'tob', 'Iab', '1ab', 'Iab'],
    'tab.':   ['tab', 'tah', 'tob.'],
    'cap':    ['cap', 'cdp', 'cop', 'cap'],
    'capsule':['capsule', 'capsuIe', 'capsuie'],
    'syp':    ['syp', 'svp', '5yp', 'syp'],
    'inj':    ['inj', 'lnj', 'ini', 'rnj'],
    'susp':   ['susp', '5usp', 'susp'],
    'ointment':['omtment', 'ointrnent', 'ointment'],
    'rotacap': ['rotacap', 'rotacdp', 'rotacap'],
    'respule': ['respule', 'respule', 'respule'],
    'sachet':  ['sachet', 'sachet', 'sachet'],
    # ==================================================================
    # Unit confusions
    # ==================================================================
    'mg':     ['mg', 'mg', 'rng', 'rng', 'm9', 'rng'],
    'ml':     ['ml', 'ml', 'm1', 'm1', 'rn1', 'ml'],
    'mcg':    ['mcg', 'mc9', 'mc9', 'rncg', 'meg'],
    'mcgm':   ['mc9m', 'mcgm'],
    'g':      ['g', '9', 'g'],
    'gm':     ['gm', '9m', 'gm'],
    'l':      ['l', '1', 'I', 'l'],
    'dl':     ['dl', 'd1', 'dl', 'gl'],
    'mg/dl':  ['mg/dl', 'mg/dl', 'rng/dl', 'rng/d1'],
    'mg/dL':  ['mg/dL', 'rng/dL', 'rng/dL', 'mg/d L'],
    'iu':     ['iu', 'lu', '1u', 'iil'],
    'iu/l':   ['iu/l', 'lu/l', '1u/l'],
    '/cumm':  ['/cumm', '/curnm', '/cumm'],
    '/mm3':   ['/mm3', '/rnm3', '/mm8'],
    # ==================================================================
    # Frequency code confusions
    # ==================================================================
    'OD':    ['OD', 'OD', 'QD', '0D', '0D', 'OD.', 'O D'],
    'BD':    ['BD', 'BD', 'BID', 'B0', 'B0', '8D', 'BD.', 'B D'],
    'TDS':   ['TDS', 'TDS', 'TD5', 'TD5', 'T0S', 'TDS'],
    'QID':   ['QID', 'Q1D', '0ID', 'QID'],
    'HS':    ['HS', 'HS', 'H5', 'H5', 'h5', 'HS'],
    'SOS':   ['SOS', 'S0S', 'SO5', 'SOS.'],
    'PRN':   ['PRN', 'PRN', 'PRN.', 'P RN'],
    'STAT':  ['STAT', '5TAT', 'ST4T', 'STAT.'],
    '1-0-1': ['1-0-1', 'l-0-l', 'l-0-l', '1-O-1', '1-O-1', '1.0.1'],
    '1-0-0': ['1-0-0', 'l-0-0', 'l-0-0', '1-O-0', '1.0.0'],
    '1-1-1': ['1-1-1', 'l-1-l', 'l-1-l', '1-1-1', '1.1.1'],
    '0-0-1': ['0-0-1', '0-0-1', 'O-O-1', '0.0.1'],
    '0-1-0': ['0-1-0', '0-1-0', 'O-1-O', '0.1.0'],
    '0-0-0': ['0-0-0', 'O-O-O', '0.0.0'],
    '0-0-1/2': ['0-0-1/2', 'O-O-1/2'],
    '1/2-0-0': ['1/2-0-0', 'l/2-0-0'],
    # ==================================================================
    # Dosage pattern confusions (observed from real PaddleOCR)
    # "1-0-1" → "127" (hyphens read as digits, 'l' shaped chars)
    # ==================================================================
    # Real PaddleOCR patterns: hyphens and dashes read as digits
    '1-0-1': ['127', '1s0-1', '1 O 1', '1-0-l', 'l-0-l', '1 0 1', '1O1'],
    '1-0-0': ['100', '1s0-0', '1 O 0', 'l-0-0', '1 0 0', '1O0'],
    '1-1-1': ['111', '1s1-1', '1 1 1', 'l-l-l', '1-1-l', 'lll'],
    '0-1-0': ['010', '0s1-0', '0 1 0', 'O-1-O', '0l0'],
    '0-0-1': ['001', '0s0-1', '0 0 1', 'O-O-1', '0O1'],
    # Observed specific: '1-0-1 (5)' → '127 6'
    '1-0-1 (5)': ['127 6', '1-0-1 (5)', '1-0-l (5)', '127 (5'],
    '1-0-1 (5) A/F': ['127 6 (AF', '1-0-1 (5) A/F', '127 6 AF'],
    '1-0-0 (5) B/F': ['127 6 (B17', '1-0-0 (5) B/F', '1-0-0 (5) B/F'],
    '1 - 1 - 1': ['107070on', '1-1-1', 'l - l - l', '1 1 1', '10157 omf'],
    '2 - 2': ['29', '2-2', '2 2', '22', '2 - 2'],
    # ==================================================================
    # Dosage decimal/number confusions
    # ==================================================================
    '0.5':   ['0.5', '0.5', 'O.5', '0,5', '.5', '0 5'],
    '1.0':   ['1.0', 'l.0', '1.O', '1,0', '1 0'],
    '2.5':   ['2.5', '2,5', '2.5', 'Z.5', '2 5'],
    '5.0':   ['5.0', '5.0', 'S.0', '5,0'],
    '7.5':   ['7.5', '7,5', '7.5'],
    # ==================================================================
    # Route confusions
    # ==================================================================
    'PO':    ['PO', 'P0', 'PO.', 'p.o.'],
    'IV':    ['IV', 'lV', '1V', 'I V'],
    'IM':    ['IM', 'lM', '1M', 'I M'],
    'SC':    ['SC', '5C', 'S C'],
    'SL':    ['SL', '5L', 'S L'],
    'PR':    ['PR', 'P R'],
    'a/c':   ['a/c', 'a/c', 'a c', 'ac', 'afc'],
    'p/c':   ['p/c', 'p/c', 'p c', 'pc', 'p/c'],
    # ==================================================================
    # Common Indian prescription shorthand confusions
    # ==================================================================
    'Rx':    ['Rx', 'Rx', 'R x', 'Rc', 'Kx'],
    'c/o':   ['c/o', 'c/o', 'c.o.', 'co', 'c/0'],
    'K/c':   ['K/c', 'K/c', 'K/c.', 'K c', 'k/c'],
    'H/o':   ['H/o', 'H/o', 'H/O', 'H/o.', 'H o'],
    'O/E':   ['O/E', 'O/E', 'O/E.', '0/E', 'O E'],
    'R/v':   ['R/v', 'R/v', 'R/v.', 'R V'],
    'B/L':   ['B/L', 'B/L', 'B/L.', 'B L'],
    'Pt':    ['Pt', 'Pt', 'P1', 'PI'],
    'Dr':    ['Dr', 'Dr', 'D r'],
}

# Sorted keys (longest first) so longer medical tokens match before shorter ones
# (e.g. 'metformin' before 'mg'). Computed once at import.
_MEDICAL_KEYS = sorted(MEDICAL_SUBS.keys(), key=len, reverse=True)

# Garbage symbols that PaddleOCR hallucinates on Indian Rx (from real OCR output).
GARBAGE_CHARS = ['#', '+', '!', '@', '^', '*', '~', '`', '|', '\\']

# Repeated pattern templates that real PaddleOCR gets stuck in (observed in Rx600).
REPEAT_PATTERNS = [
    '\n'.join([w] * n)
    for w in ['Adv', 'adv', 'Tab', 'tab', 'Rx', 'diag', 'c/o', 'K/c', 'O/E']
    for n in [10, 20, 50, 100]
]

# Characters that real PaddleOCR most frequently drops to blank (from confusion matrix).
BLANK_CHARS = '.e aintroslh mcpdb fgvyw,kxjqz'

# Word-level hallucination map: real PaddleOCR generates plausible-looking but wrong
# words. Based on observed Rx600 patterns + common Rx terms.
HALLUCINATION_MAP = {
    # Names
    'Abhijeet':    ['Phhijaf', 'Abhijeef', 'Abhi jeet', 'Phhijeet', 'Abhijat'],
    'Abhijit':     ['bhiji', 'Abhijit', 'Phhijit', 'bhijit', 'Ab iit'],
    'Ramesh':      ['Rarnesh', 'Rarnash', 'kamesh', 'Pamesh', 'Kamesh'],
    'Suresh':      ['Suresh', 'Suresh', 'Puresh', 'kuresh'],
    'Mahesh':      ['Mahesh', 'M ahesh', 'rnahesh', 'Mahash'],
    'Venkatesh':   ['Venkatesh', 'Venkatash', 'Venkatesh', 'venkatesh'],
    'Krishna':     ['Krishna', 'ktishna', 'Krisma', 'Rrishna', 'Krishna'],
    'Lakshmi':     ['Lakshmi', 'Lakshmi', 'Lakshmi', 'Lakshmi'],
    'Anita':       ['Anlta', 'Anlta', 'Anlta', 'Anlta'],
    'Anil':        ['Anri', 'Rnil', 'Anil', 'Aail'],
    'Sunita':      ['Sunlta', 'Sunlta', 'Punita', 'Sunlta'],
    'Geeta':       ['Geeta', 'Geota', 'Geeta', 'Seeta'],
    'Amit':        ['Rmit', 'Amit', 'Rmit', 'Amit'],
    # Drug brands (observed from real PaddleOCR v6 + VL1.6 on Indian Rx)
    'Augmentin':   ['THrmbin', 'Thaybin', 'Augmentm', 'THrmbm', 'Augrnentin'],
    'Wysolone':    ['Wystone2o', 'Wygodone', 'Wyston', 'Wysolon', 'Wygodom'],
    'Pulmoclear':  ['Phtmoler', 'Pudmorean', 'Pulmoclear', 'Pulmocleer', 'Pulrnoclear'],
    'Montair':     ['Montari', 'Monbair', 'Montarr', 'Monfair', 'Montar '],
    'Levolin':     ['Levolin', 'Le volin', 'Levolm', 'Pevolin'],
    'Otrivin':     ['Ofrivin', 'Othris', 'Otrivin', 'Ofrivi '],
    'Nasal':       ['Nosal', 'Nasol', 'Nasal', 'Nsal'],
    'Drops':       ['Drops', 'iang', 'Pony', 'Drops', 'drops'],
    'Sumol':       ['Summer', 'Sumer', 'Sumor', 'Sunol', 'Sumol', 'Surmol'],
    'Taxim':       ['Paxim', 'Paxum', 'Taxum', 'Paxim', 'Tazim', 'Paxim'],
    'Pan':         ['Pan', 'Pun', 'Pen', 'Pon', 'Pun', 'Pan', 'Pon to'],
    'Dolo':        ['Dolo', 'Dolo', 'Dolo', 'Dolo'],
    'Crocin':      ['Crocin', 'Croc in', 'Crocin', 'Croc in'],
    'Augmentin':   ['Augmenbn', 'Augrnentin', 'Augmentm', 'Augmedn'],
    'Azithral':    ['Azithral', 'Azlthral', 'Azithral', 'Azithral'],
    'Montair':     ['Montari', 'Monbair', 'Montarr', 'Monfair'],
    'Levolin':     ['Levolin', 'Le volin', 'Levolm', 'Pevolin'],
    'Ecosprin':    ['Ecosprin', 'Ecosprm', 'Ecosprrn', 'Ecosprln'],
    'Clopitab':    ['Clopitab', 'Clopltab', 'Clopitah', 'Cloplfab'],
    'Atorva':      ['Atorva', 'Atorva', 'Atorva', 'Alorva'],
    'Rosuvas':     ['Rosuvas', 'Rosuvas', 'Posuvas', 'Rosuvas'],
    'Amaryl':      ['Amaryl', 'Arnaryl', 'Amaryl', 'Amaryl'],
    'Glycomet':    ['Glycomet', 'Glycornet', 'Glycomef', 'Gtycomet'],
    'Thyronorm':   ['Thyronorm', 'Thyronorrn', 'Thyronorrn', 'thynororm'],
    # Common Rx terms
    'fever':       ['fewer', 'fever', 'fevor', 'fever'],
    'Bodyache':    ['Bodyakhe', 'Bodyache', 'Bodache', 'Body ach'],
    'cough':       ['cough', 'couph', 'kough', 'c0ugh', 'cough'],
    'Headache':    ['Headakhe', 'Headache', 'Headche', 'Headach'],
    'pain':        ['pain', 'pam', 'palu', 'paln', 'pai'],
    'diabetes':    ['diabetas', 'diabebes', 'diaberes', 'diabebes'],
    'hypertension':['hypenension', 'hypertension', 'hypenension', 'hypertensron'],
    'asthma':      ['asthrna', 'asthma', 'asthrna', 'ashma'],
    # Date/Month
    'January':     ['January', 'Januarv', 'Januarv', 'Januarv'],
    'February':    ['Pebruary', 'Februarv', 'Februarv', 'Februarv'],
    'March':       ['March', 'Mar ch', 'March', 'Mar ch'],
    'April':       ['April', 'Aprll', 'Aprii', 'Pril'],
    'May':         ['May', 'r lay', 'Ma y', 'May'],
    'June':        ['June', 'J u ne', 'Tune', 'J u ne'],
    'July':        ['July', 'J u ly', 'Juty', 'luly'],
    'August':      ['August', 'Augusb', 'Augusb', 'Pugust'],
    'September':   ['Septembef', 'Septembef', 'Septembef', 'Septembef'],
    'October':     ['October', 'Odober', 'Ocfober', 'Odober'],
    'November':    ['Novembef', 'Novembef', 'Novembef', 'Novembef'],
    'December':    ['December', 'Decembef', 'December', 'De cember'],
    # Common sections
    'Adv':         ['By', 'And', 'Add', 'Add', 'Adt', 'Ad', 'Adv', 'Advt', 'Ady'],
    'Rx':          ['R.', 'R x', 'Bx', 'Px', 'Kx', 'Rc', 'R;'],
    'c/o':         ['By', 'co', 'C/O', 'Co', 'e/o'],
    'Age':         ['Age', 'Aqe', 'A e', 'Aqe', 'A e'],
    'Sex':         ['Sex', 'S ex', 'Sex', 'S ex', 'Sex'],
    'Name':        ['Name', 'Narne', 'Name', 'Narne', 'Name'],
    'Date':        ['Date', 'Date', 'Oate', 'Date', 'Dafe'],
    # Investigations
    'CBC':         ['CBC', 'C BG', 'CBC', 'C BC', 'CBC'],
    'Widal':       ['Widal', 'Widal', 'Widal', 'W idal', 'Widal'],
    'Dengue':      ['Dengue', 'Deng ue', 'Deng ue', 'Dengue', 'Deng-ue'],
    'Malaria':     ['Malaria', 'Mala ria', 'Malaria', 'Malan a'],
    'Urine':       ['Urine', 'U rine', 'Urine', 'U rine'],
    'X-ray':       ['X-rav', 'X-ray', 'X-ra y', 'K-ray'],
    'ECG':         ['ECG', 'E CG', 'ECG', 'E CG'],
    'Echo':        ['Echo', 'E cho', 'Echo', 'E cho'],
    # Units
    'Kgs':         ['K gs', 'Kss', 'Kgs', 'K gs', 'Kss'],
    'mg':          ['rng', 'meg', 'm g', 'rn g', 'mc'],
    'mcg':         ['mcg', 'rncg', 'rrrcg', 'rneg', 'meg'],
    # Store/address
    'Available':   ['Available', 'Avallable', 'Availabie', 'Avalable'],
    'Mobile':      ['Mobile', 'Moblle', 'Mobi le', 'Mobite'],
    'Road':        ['Road', 'Road', 'R oad', 'Road', 'Roacl'],
    'Bangalore':   ['Bangalore', 'Pangalore', 'Bangaiore', 'Pangalore'],
    'Clinic':      ['Clinic', 'C liruc', 'Clinc', 'Cliruc'],
    'Hospital':    ['Hospical', 'Hespital', 'Haspitai', 'Haspitai'],
    'Signature':   ['Signabure', 'Signabure', 'Signabure', 'Signabure'],
}

# Pool of real medical/document words for generative hallucination fallback.
CORPUS_POOL = [
    'Tablet', 'Capsule', 'Syrup', 'Injection', 'Drops', 'Ointment', 'Cream',
    'Morning', 'Evening', 'Night', 'Daily', 'Weekly', 'Monthly',
    'Fasting', 'Random', 'Post', 'Pre', 'Before', 'After', 'With',
    'Blood', 'Sugar', 'Pressure', 'Heart', 'Liver', 'Kidney', 'Thyroid',
    'Acute', 'Chronic', 'Mild', 'Moderate', 'Severe', 'Normal',
    'Check', 'Review', 'Follow', 'Repeat', 'Continue', 'Stop', 'Start',
    'Patient', 'Doctor', 'Nurse', 'Ward', 'OPD', 'IPD', 'Emergency',
    'General', 'Medicine', 'Surgery', 'Ortho', 'Pediatric', 'Cardio',
    'Consultation', 'Prescription', 'Diagnosis', 'Treatment', 'Therapy',
    'Weight', 'Height', 'BMI', 'Temp', 'Pulse', 'Respiration', 'SPO2',
    'Report', 'Result', 'Value', 'Range', 'Normal', 'Abnormal', 'Critical',
]


# ---------------------------------------------------------------------------
# 2. Noise functions
# ---------------------------------------------------------------------------

def substitute_chars(text, p=0.05, confusion_map=None):
    """Replace characters/substrings with visually similar ones.

    Uses CHAR_SUBS by default. Scans text left-to-right; at each position checks
    if the current char (or a 2-char prefix) is in confusion_map. If yes, with
    probability p, replaces it with a random alternative. After a replacement,
    advances past the matched key to avoid overlap.
    """
    if confusion_map is None:
        confusion_map = CHAR_SUBS
    if not text:
        return text

    result = []
    i = 0
    n = len(text)
    while i < n:
        replaced = False
        # Try 2-char prefix first (longer match priority, e.g. 'rn' -> 'm').
        if i + 1 < n:
            two = text[i:i + 2]
            if two in confusion_map and random.random() < p:
                result.append(random.choice(confusion_map[two]))
                i += 2
                replaced = True
        if not replaced:
            ch = text[i]
            if ch in confusion_map and random.random() < p:
                result.append(random.choice(confusion_map[ch]))
            else:
                result.append(ch)
            i += 1
    return ''.join(result)


def delete_chars(text, p=0.02):
    """Randomly delete characters with probability p.

    Uniform p is applied to all characters (including digits and whitespace --
    OCR does drop digits and spaces). The only hard constraint: never delete the
    last character of a word, which would leave an empty token.
    """
    if not text:
        return text

    n = len(text)
    # Mark indices that are the last char of a whitespace-delimited word.
    no_delete = set()
    i = 0
    while i < n:
        if not text[i].isspace():
            j = i
            while j < n and not text[j].isspace():
                j += 1
            no_delete.add(j - 1)  # last char of this word
            i = j
        else:
            i += 1

    result = []
    for i, ch in enumerate(text):
        if i not in no_delete and random.random() < p:
            continue  # delete this char
        result.append(ch)
    return ''.join(result)


# Chars likely to appear near visually similar neighbours (for plausible inserts).
_INSERT_NEAR = {
    'l': 'iI1|', 'I': 'l1|', 'i': 'lI1', '1': 'lI|',
    'm': 'nrn', 'n': 'mr', 'r': 'nm', 'h': 'nb', 'b': 'h6',
    '0': 'Oo', 'O': '0o', 'o': '0O',
    'c': 'e', 'e': 'co', 'a': 'oe',
    'u': 'v', 'v': 'uy', 'y': 'vg',
    't': 'fi', 'f': 't',
}


def insert_chars(text, p=0.02, charset=None):
    """Randomly insert extra characters with probability p per position.

    Inserted chars are drawn from charset (default: lowercase letters + digits +
    common punctuation). Insertions are biased to be visually plausible -- e.g.
    inserting 'i' near 'l', 'n' near 'm'.
    """
    if charset is None:
        charset = string.ascii_lowercase + string.digits + ".,;:|/()- "
    if not text:
        return text

    result = []
    for ch in text:
        if random.random() < p:
            if ch in _INSERT_NEAR:
                result.append(random.choice(_INSERT_NEAR[ch]))
            else:
                result.append(random.choice(charset))
        result.append(ch)
    return ''.join(result)


def transpose_chars(text, p=0.01):
    """Swap adjacent characters with probability p.

    Never swaps across word boundaries (a char is never swapped with whitespace).
    """
    if not text:
        return text
    chars = list(text)
    i = 0
    while i < len(chars) - 1:
        a, b = chars[i], chars[i + 1]
        if a.isspace() or b.isspace():
            i += 1
            continue
        if random.random() < p:
            chars[i], chars[i + 1] = chars[i + 1], chars[i]
            i += 2  # skip past the swapped pair to avoid double-swapping
        else:
            i += 1
    return ''.join(chars)


def merge_words(text, p=0.05):
    """Merge adjacent words (remove the space between them) with probability p.

    Operates on space-separated tokens within a line. Never merges across
    newlines.
    """
    if not text:
        return text
    out_lines = []
    for line in text.split('\n'):
        tokens = line.split(' ')
        if len(tokens) <= 1:
            out_lines.append(line)
            continue
        merged = [tokens[0]]
        for tok in tokens[1:]:
            if random.random() < p:
                merged[-1] = merged[-1] + tok
            else:
                merged.append(tok)
        out_lines.append(' '.join(merged))
    return '\n'.join(out_lines)


def split_words(text, p=0.03):
    """Split words at random positions with probability p.

    Inserts a space in the middle of a word. Words shorter than 4 chars are
    never split. Never splits across newlines.
    """
    if not text:
        return text
    out_lines = []
    for line in text.split('\n'):
        tokens = line.split(' ')
        new_tokens = []
        for tok in tokens:
            if len(tok) >= 4 and random.random() < p:
                pos = random.randint(1, len(tok) - 1)  # keep both halves non-empty
                new_tokens.append(tok[:pos])
                new_tokens.append(tok[pos:])
            else:
                new_tokens.append(tok)
        out_lines.append(' '.join(new_tokens))
    return '\n'.join(out_lines)


def merge_lines(text, p=0.03):
    """Merge adjacent lines (remove newline, replace with space) with prob p.

    Simulates OCR reading two lines as one.
    """
    if not text:
        return text
    lines = text.split('\n')
    if len(lines) <= 1:
        return text
    merged = [lines[0]]
    for line in lines[1:]:
        if random.random() < p:
            merged[-1] = merged[-1] + ' ' + line
        else:
            merged.append(line)
    return '\n'.join(merged)


def split_lines(text, p=0.02):
    """Split a line at a random position into two lines with probability p.

    Simulates OCR breaking a single line into two. Very short lines are not
    split.
    """
    if not text:
        return text
    out = []
    for line in text.split('\n'):
        if len(line) >= 10 and random.random() < p:
            pos = random.randint(1, len(line) - 1)
            out.append(line[:pos])
            out.append(line[pos:])
        else:
            out.append(line)
    return '\n'.join(out)


# ---------------------------------------------------------------------------
# 3. Medical-specific noise injection
# ---------------------------------------------------------------------------

def _preserve_case(original, replacement):
    """Apply the case pattern of `original` to `replacement` where possible."""
    if not original:
        return replacement
    if original.isupper():
        return replacement.upper()
    if original.islower():
        return replacement.lower()
    if original[0].isupper():
        return replacement[:1].upper() + replacement[1:]
    return replacement


def inject_medical_noise(text, p=0.03):
    """Apply medical-specific substitutions from MEDICAL_SUBS.

    Scans text for keys in MEDICAL_SUBS (longest keys first), replacing with
    probability p. Matching is case-insensitive but the original case pattern is
    preserved on the replacement where possible. A match is skipped if it is
    clearly internal to a larger word (both neighbours are letters), to avoid
    e.g. matching 'BD' inside 'ABDOMEN'.
    """
    if not text:
        return text

    lower = text.lower()
    n = len(text)
    out = []
    i = 0
    while i < n:
        matched = False
        for key in _MEDICAL_KEYS:
            klen = len(key)
            if i + klen > n:
                continue
            if lower[i:i + klen] != key.lower():
                continue
            # Boundary guard: skip if both neighbours are letters (inside a word).
            left_is_letter = (i > 0 and text[i - 1].isalpha())
            right_is_letter = (i + klen < n and text[i + klen].isalpha())
            if left_is_letter and right_is_letter:
                continue
            original = text[i:i + klen]
            if random.random() < p:
                alt = random.choice(MEDICAL_SUBS[key])
                out.append(_preserve_case(original, alt))
            else:
                out.append(original)
            i += klen
            matched = True
            break
        if not matched:
            out.append(text[i])
            i += 1
    return ''.join(out)


def blank_out(text, p=0.02):
    """Replace characters with blank spaces (OCR returns unreadable->space).

    When real PaddleOCR cannot read a character on an Indian Rx, it often
    returns a blank space instead. This simulates that: replaces random
    characters (weighted toward BLANK_CHARS) with spaces.
    """
    if not text:
        return text
    result = []
    for ch in text:
        if ch != '\n' and random.random() < p:
            result.append(' ')
        elif ch in BLANK_CHARS and random.random() < p * 3:
            result.append(' ')
        else:
            result.append(ch)
    return ''.join(result)


def repeat_pattern(text, p=0.03):
    """Insert repeated pattern blocks (OCR gets stuck repeating text).

    Real PaddleOCR on Indian Rx sometimes repeats the same word/line
    hundreds of times (e.g. 'Adv\\nAdv\\nAdv\\n...'). This inserts random
    repeated patterns at random positions in the text.
    """
    if not text or random.random() > p:
        return text
    pattern = random.choice(REPEAT_PATTERNS)
    # Insert after a random word boundary
    words = text.split()
    if len(words) < 3:
        return text
    pos = random.randint(1, len(words) - 1)
    words.insert(pos, '\n' + pattern + '\n')
    return ' '.join(words)


def garbage_inject(text, p=0.03):
    """Insert garbage symbols (#, +, !, @) that PaddleOCR hallucinates.

    Real OCR output on Indian Rx contains random garbage symbols mixed into
    otherwise correct text (e.g. 'al+# (120)' instead of '120 mg').
    """
    if not text:
        return text
    result = []
    for ch in text:
        if random.random() < p:
            result.append(random.choice(GARBAGE_CHARS))
        result.append(ch)
    return ''.join(result)


def severe_deletion(text, p=0.05):
    """Delete entire word or line segments (OCR drops large text chunks).

    Real PaddleOCR on Indian Rx frequently omits entire words, lines, or
    sections. This deletes whole words (not just characters).
    """
    if not text or random.random() > p:
        return text
    words = text.split()
    if len(words) < 5:
        return text
    # Delete a contiguous block of words (1 to ~20% of total)
    n_del = max(1, random.randint(1, max(2, len(words) // 5)))
    start = random.randint(0, max(0, len(words) - n_del - 1))
    del words[start:start + n_del]
    return ' '.join(words)


def word_hallucinate(text, p=0.05):
    """Replace entire words with plausible-looking alternatives (OCR hallucination).

    Real PaddleOCR doesn't just substitute characters -- it generates whole words
    that look like they COULD be correct but are completely wrong:
      'Sumol 650 1-1-1' -> 'Summer Plays for ⑥'
      'Abhijeet'        -> 'Phhijaf'
      'Adv'             -> 'By'
      'BP - 110/80'     -> 'D-110%8'

    Strategy:
      1. Check HALLUCINATION_MAP for known word -> hallucination pairs.
      2. If word is not in the map, generate a plausible hallucination by
         scrambling characters using the real CHAR_SUBS confusion weights on
         all characters at once (not independently per char), then check if
         the result is in CORPUS_POOL.
      3. If generation fails, pick a random CORPUS_POOL word of similar length.
    """
    if not text or p <= 0:
        return text
    words = text.split()
    if len(words) < 2:
        return text
    result = []
    _words_lo = {w.lower() for w in CORPUS_POOL}
    _hallu_lo = {k.lower(): [v.lower() for v in vs]
                 for k, vs in HALLUCINATION_MAP.items()}
    for w in words:
        if random.random() >= p:
            result.append(w)
            continue
        wl = w.lower()
        skip_stripped = w.strip('.,;:!?()[]')
        if not skip_stripped or not skip_stripped[0].isalpha():
            result.append(w)
            continue
        # 1. Check hallucination map
        if wl in _hallu_lo:
            alt = random.choice(_hallu_lo[wl])
            # Preserve case pattern of original
            if w[0].isupper():
                alt = alt[0].upper() + alt[1:] if len(alt) > 1 else alt.upper()
            result.append(alt)
            continue
        # 2. Generate plausible hallucination: apply char subs to ENTIRE word
        #    using a flat list of all possible substitutions from CHAR_SUBS
        hallucinated = []
        for ch in skip_stripped:
            cl = ch.lower()
            if cl in CHAR_SUBS and random.random() < 0.6:
                hallucinated.append(random.choice(CHAR_SUBS[cl]))
            elif random.random() < 0.3:
                hallucinated.append(random.choice(string.ascii_lowercase))
            else:
                hallucinated.append(cl)
        alt = ''.join(hallucinated)
        # Ensure it looks word-like (has a vowel, no triple consonants)
        vowels = set('aeiou')
        alt_chars = [c for c in alt if c.isalpha()]
        has_vowel = any(c in vowels for c in alt_chars)
        if has_vowel and len(alt_chars) >= 2:
            # Preserve original case
            if w[0].isupper():
                alt = alt[0].upper() + alt[1:]
            result.append(alt)
        else:
            # 3. Fallback: pick a corpus word of similar length
            similar = [cw for cw in CORPUS_POOL
                       if abs(len(cw) - len(skip_stripped)) <= 2]
            if similar:
                alt = random.choice(similar)
                if w[0].isupper() != alt[0].isupper():
                    alt = alt[0].upper() + alt[1:] if w[0].isupper() else alt[0].lower() + alt[1:]
                result.append(alt)
            else:
                result.append(w)
    return ' '.join(result)


def shuffle_lines(text, p=0.05):
    """Shuffle line order within blocks (OCR reads sections out of order).

    Real PaddleOCR often outputs lines in the wrong order -- mixing sections,
    repeating some, skipping others. This shuffles lines within each
    blank-line-separated block independently.
    """
    if not text or random.random() > p:
        return text
    blocks = text.split('\n\n')
    out = []
    for block in blocks:
        lines = block.split('\n')
        if len(lines) >= 3 and random.random() < p * 2:
            random.shuffle(lines)
        out.append('\n'.join(lines))
    return '\n\n'.join(out)


def section_dropout(text, p=0.05):
    """Drop entire contiguous line groups (OCR ignores whole sections).

    Real PaddleOCR frequently omits entire sections -- patient complaints,
    examination notes, entire drug lists. This drops a random block of lines.
    """
    if not text or random.random() > p:
        return text
    lines = text.split('\n')
    if len(lines) < 4:
        return text
    n_drop = max(1, random.randint(1, max(2, len(lines) // 4)))
    start = random.randint(0, max(0, len(lines) - n_drop))
    del lines[start:start + n_drop]
    return '\n'.join(lines)


def form_field_noise(text, p=0.05):
    """Replace filled form fields with blank underscores (OCR reads form blanks).

    Real PaddleOCR on form-style prescriptions reads underscores/blanks instead
    of filled values: 'Name : Abhijeet' -> 'Name: _____', 'Date : 21/3/24' -> 'Date: _____'.
    """
    if not text or p <= 0:
        return text
    FIELD_LABELS = ['Name', 'Date', 'Age', 'Wt', 'Weight', 'Sex',
                    'BP', 'Pulse', 'Temp', 'Temperature', 'SPO2',
                    'Height', 'BMI']
    lines = text.split('\n')
    out = []
    for line in lines:
        if random.random() < p:
            for label in FIELD_LABELS:
                if label + ' ' in line or label + ':' in line:
                    line = _re.sub(r'(:\s*).+', r'\1_____', line)
                    line = _re.sub(r'(\s+-+\s*).+', r'\1______', line)
                    break
        out.append(line)
    return '\n'.join(out)


import re as _re

def strikethrough_scramble(text):
    """Replace ~~...~~ and ~...~ content with random alphanumeric garbage.

    Real PaddleOCR on crossed-out/deleted Rx lines produces abstract
    alphanumeric noise instead of the struck-through text.
    """
    if not text or '~' not in text:
        return text
    def _scramble(m):
        content = m.group(1)
        length = max(1, len(content))
        return ''.join(random.choice("127890c1h+Aerh ") for _ in range(random.randint(length, length + 5)))
    return _re.sub(r'~{1,2}(.*?)~{1,2}', _scramble, text)


def prefix_degradation(text, p=0.3):
    """Degrade Rx prefixes: T.→7., Syp.→8y., Inj.→I j, c/o→R40,CO,C6.

    Capital letters and prefixes mutate into numbers/symbols because their
    cursive ascenders/descenders break down in OCR (observed from real v6/VL1.6).
    """
    if not text or p <= 0:
        return text
    PREFIX_SWAPS = [
        (r'(?<![a-zA-Z])T\.(?=\s)', ['7.', '1.', 'T.']),
        (r'(?<![a-zA-Z])Syp\.(?=\s)', ['8y.', '8p.', '8.']),
        (r'(?<![a-zA-Z])Inj\.(?=\s)', ['I j', '1nj', '1n]']),
        (r'\bc/o\b(?=\s)', ['R40,', 'CO', 'C6']),
        (r'\bTab\b(?=\s)', ['7ab', 'Iab', '1ab']),
        (r'\bCap\b(?=\s)', ['6ap', 'Cap', 'Cdp']),
    ]
    lines = text.split('\n')
    out = []
    for line in lines:
        if random.random() < p:
            for pattern, replacements in PREFIX_SWAPS:
                if _re.search(pattern, line):
                    line = _re.sub(pattern, lambda m, r=replacements: random.choice(r), line, count=1)
                    break
        out.append(line)
    return '\n'.join(out)


def dosage_collapse(text, p=0.3):
    """Collapse dosage patterns: 1-0-1→127, (5)→bracket corruption, /→2/7/|.

    The dashes and slashes in standard Indian dosage frequencies (1-0-1, c/o)
    routinely flip into 2, 7, 6, or o in real PaddleOCR output.
    """
    if not text or p <= 0:
        return text
    tokens = text.split(' ')
    out = []
    for token in tokens:
        if random.random() >= p:
            out.append(token)
            continue
        # Pattern 1: "1-0-1 (5) A/F" → "127 6 (AF" (full bracket+dash collapse)
        m = _re.match(r'^(\d+)[-–](\d+)[-–](\d+)\s*\((\d+)\)\s*([A-Za-z/]+)$', token)
        if m:
            a, b, c, d, suf = m.groups()
            collapsed = ''.join([
                random.choice(['1', '7', '']),
                a, random.choice(['1', '7', '']),
                b, random.choice(['1', '7', '']),
                c, ' ',
                random.choice(['6', '(', '']),
                d
            ])
            out.append(collapsed + ' (' + suf)
            continue
        # Pattern 2: "1-0-1" → "127" (hyphens collapse to digits)
        m = _re.match(r'^(\d+)[-–](\d+)[-–](\d+)$', token)
        if m:
            a, b, c = m.groups()
            collapsed = ''.join([
                random.choice(['1', '7', '']) if random.random() < 0.5 else '',
                a,
                random.choice(['1', '7', '']) if random.random() < 0.5 else '',
                b,
                random.choice(['1', '7', '']) if random.random() < 0.5 else '',
                c
            ])
            if not collapsed:
                collapsed = token
            out.append(collapsed)
            continue
        # Pattern 3: "1-0-0 (5) B/F" style
        m = _re.match(r'^(\d+)[-–](\d+)[-–](\d+)\s*\((\d+)\)\s+(\S+)$', token)
        if m:
            a, b, c, d, suf = m.groups()
            collapsed = ''.join([
                a, random.choice(['1', '7']),
                b, random.choice(['1', '7']),
                c, ' (', d,
            ])
            out.append(collapsed)
            continue
        # Pattern 4: standalone (5) bracket corruption
        m = _re.match(r'^\((\d+)\)$', token)
        if m:
            d = m.group(1)
            out.append(random.choice([d, '6', f'({d}', f'6(']))
            continue
        # Pattern 5: slashes in dosage/timing
        if '/' in token:
            token = _re.sub(r'/', lambda m: random.choice(['2', '7', '|']), token)
        # Pattern 6: standalone dashes in dosage context
        if '-' in token and any(c.isdigit() for c in token):
            token = _re.sub(r'[-–]', lambda m: random.choice(['1', '7', ' ', '']), token)
        out.append(token)
    return ' '.join(out)


def ligature_swaps(text, p=0.3):
    """Apply structural character cluster swaps from cursive handwriting ligature fails.

    When cursive letters blend together, the OCR engine maps the combined shape to
    a completely different, structurally similar character cluster (e.g., ulmo→udmo,
    lo→to). Based on real PaddleOCR pattern observations.
    """
    if not text or p <= 0:
        return text
    LIGATURE_MAP = {
        'A': ['TH', '4', 'A'],
        'u': ['r', 'n', 'v'],
        'g': ['r', 'm', 'i'],
        'm': ['rn', 'nt', 'm'],
        's': ['r', 'o', 's'],
        'o': ['e', '0', 'o'],
        'l': ['t', '1', 'i'],
        'c': ['d', 'c', '1'],
        'e': ['a', 'o', 'e'],
        'D': ['P', 'i', 'D'],
        'r': ['n', 'i', 'a'],
        'p': ['n', 'g', 'y'],
        '5': [')', '6', 's'],
        'b': ['h', '6', 'b'],
        'h': ['n', 'b', 'h'],
        'n': ['r', 'h', 'n'],
        't': ['f', 'l', 't'],
        'w': ['u', 'vv', 'w'],
        'y': ['v', 'g', 'y'],
        'f': ['t', 'f', 'l'],
    }
    result = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch in LIGATURE_MAP and random.random() < p:
            result.append(random.choice(LIGATURE_MAP[ch]))
        else:
            result.append(ch)
        i += 1
    return ''.join(result)


def line_merging(text, p=0.15):
    """Aggressively collapse newlines (indentations disappear, lines randomly merge).

    Real PaddleOCR on Indian Rx often loses line structure entirely — indentation
    vanishes, multiple lines merge into one, short lines get absorbed.
    """
    if not text or p <= 0:
        return text
    lines = text.split('\n')
    if len(lines) <= 1:
        return text
    out = [lines[0]]
    for line in lines[1:]:
        # More aggressive merging for short lines or lines with leading whitespace
        merge_prob = p
        if len(line.strip()) < 15:
            merge_prob = min(1.0, p * 2)
        if line.startswith(' ') or line.startswith('\t'):
            merge_prob = min(1.0, p * 1.5)
        if random.random() < merge_prob:
            out[-1] = out[-1] + ' ' + line.strip()
        else:
            out.append(line)
    return '\n'.join(out)


_HALLU_LO = {k.lower(): v for k, v in HALLUCINATION_MAP.items()}

def zone_chaos(text, p=0.1, p_clean=0.2):
    """Apply ZONE-DEPENDENT noise: some zones stay clean, others get trashed.

    Real PaddleOCR produces 'clean islands' (header, labels, addresses) and
    'hallucination zones' (patient data, drug names, numbers) simultaneously.
    This splits text on blank lines, applies heavy noise to selected zones,
    and leaves others untouched.

    p: probability this function fires at all
    p_clean: probability a selected zone stays entirely clean anyway
    """
    if not text or random.random() > p:
        return text
    blocks = text.split('\n\n')
    out = []
    for block in blocks:
        if random.random() < p_clean:
            out.append(block)
        else:
            lines = block.split('\n')
            n_keep = max(1, len(lines) * 3 // 4)
            keep = sorted(random.sample(range(len(lines)), min(n_keep, len(lines))))
            lines = [lines[i] for i in keep]
            if random.random() < 0.5 and len(lines) > 1:
                random.shuffle(lines)
            # Build corpus index by first letter + length for fast lookup
            _corpus_by_ll = {}
            for cw in CORPUS_POOL:
                key = (cw[0].lower(), len(cw))
                _corpus_by_ll.setdefault(key, []).append(cw)

            noisy_lines = []
            for line in lines:
                # Medical substitutions on clean text FIRST (e.g., T. -> 7.)
                med_line = inject_medical_noise(line, p=0.5)
                # Word-level hallucination: replace with REAL words only
                words = med_line.split()
                for wi, w in enumerate(words):
                    if not w or len(w) <= 2:
                        continue
                    w_stripped = w.strip('.,;:!?()[]')
                    if not w_stripped:
                        continue
                    wl = w_stripped.lower()
                    # 1) Check hallucination map first
                    if wl in _HALLU_LO and random.random() < 0.7:
                        alt = random.choice(_HALLU_LO[wl])
                        if w[0].isupper() and alt:
                            alt = alt[0].upper() + alt[1:]
                        words[wi] = alt
                    elif random.random() < 0.35 and len(w_stripped) >= 3:
                        # 2) Replace with a REAL corpus word of same length+first letter
                        key = (w_stripped[0].lower(), len(w_stripped))
                        candidates = _corpus_by_ll.get(key, [])
                        if not candidates:
                            # fallback: any word of similar length
                            for (fl, ln), cw_list in _corpus_by_ll.items():
                                if abs(ln - len(w_stripped)) <= 2:
                                    candidates.extend(cw_list)
                        if candidates:
                            alt = random.choice(candidates)
                            if w[0].isupper():
                                alt = alt[0].upper() + alt[1:]
                            words[wi] = alt
                # NO char subs in zone_chaos — let the pipeline handle tiny char noise
                noisy_lines.append(' '.join(words))
            if random.random() < 0.4 and noisy_lines:
                idx = random.randint(0, len(noisy_lines) - 1)
                noisy_lines.insert(idx, noisy_lines[idx])
            out.append('\n'.join(noisy_lines))
    return '\n\n'.join(out)


# ---------------------------------------------------------------------------
# 4. Composite noise pipeline
# ---------------------------------------------------------------------------

NOISE_PROFILES = {
    "printed_clean": {
        "substitute": 0.02, "delete": 0.005, "insert": 0.005,
        "transpose": 0.005, "merge_words": 0.01, "split_words": 0.005,
        "merge_lines": 0.01, "split_lines": 0.005, "medical": 0.01,
        "blank": 0.005, "garbage": 0.005, "repeat": 0.0, "severe_del": 0.0,
        "hallucinate": 0.01, "shuffle": 0.0, "section_drop": 0.0, "form_field": 0.0,
        "zone_chaos": 0.0,
        "prefix_deg": 0.05, "dosage": 0.05, "ligature": 0.05,
        "strikethrough": 1.0, "line_merge": 0.02,
    },
    "printed_moderate": {
        "substitute": 0.05, "delete": 0.02, "insert": 0.02,
        "transpose": 0.01, "merge_words": 0.03, "split_words": 0.02,
        "merge_lines": 0.03, "split_lines": 0.02, "medical": 0.02,
        "blank": 0.02, "garbage": 0.02, "repeat": 0.01, "severe_del": 0.02,
        "hallucinate": 0.02, "shuffle": 0.01, "section_drop": 0.02, "form_field": 0.01,
        "zone_chaos": 0.0,
        "prefix_deg": 0.10, "dosage": 0.10, "ligature": 0.10,
        "strikethrough": 1.0, "line_merge": 0.04,
    },
    "printed_noisy": {
        "substitute": 0.10, "delete": 0.05, "insert": 0.04,
        "transpose": 0.02, "merge_words": 0.05, "split_words": 0.04,
        "merge_lines": 0.05, "split_lines": 0.03, "medical": 0.04,
        "blank": 0.04, "garbage": 0.04, "repeat": 0.02, "severe_del": 0.04,
        "hallucinate": 0.04, "shuffle": 0.02, "section_drop": 0.04, "form_field": 0.02,
        "zone_chaos": 0.0,
        "prefix_deg": 0.15, "dosage": 0.15, "ligature": 0.10,
        "strikethrough": 1.0, "line_merge": 0.06,
    },
    "handwritten_moderate": {
        "substitute": 0.08, "delete": 0.04, "insert": 0.03,
        "transpose": 0.02, "merge_words": 0.05, "split_words": 0.03,
        "merge_lines": 0.04, "split_lines": 0.03, "medical": 0.03,
        "blank": 0.03, "garbage": 0.03, "repeat": 0.02, "severe_del": 0.03,
        "hallucinate": 0.03, "shuffle": 0.02, "section_drop": 0.03, "form_field": 0.02,
        "zone_chaos": 0.05,
        "prefix_deg": 0.20, "dosage": 0.20, "ligature": 0.20,
        "strikethrough": 1.0, "line_merge": 0.08,
    },
    "handwritten_severe": {
        "substitute": 0.12, "delete": 0.06, "insert": 0.04,
        "transpose": 0.03, "merge_words": 0.08, "split_words": 0.05,
        "merge_lines": 0.06, "split_lines": 0.04, "medical": 0.05,
        "blank": 0.04, "garbage": 0.04, "repeat": 0.04, "severe_del": 0.06,
        "hallucinate": 0.06, "shuffle": 0.04, "section_drop": 0.06, "form_field": 0.04,
        "zone_chaos": 0.10,
        "prefix_deg": 0.35, "dosage": 0.35, "ligature": 0.35,
        "strikethrough": 1.0, "line_merge": 0.12,
    },
    "handwritten_catastrophic": {
        "substitute": 0.005, "delete": 0.002, "insert": 0.002,
        "transpose": 0.002, "merge_words": 0.01, "split_words": 0.005,
        "merge_lines": 0.01, "split_lines": 0.005, "medical": 0.06,
        "blank": 0.002, "garbage": 0.002, "repeat": 0.04, "severe_del": 0.04,
        "hallucinate": 0.06, "shuffle": 0.04, "section_drop": 0.06, "form_field": 0.04,
        "zone_chaos": 0.90,
        "prefix_deg": 0.50, "dosage": 0.50, "ligature": 0.45,
        "strikethrough": 1.0, "line_merge": 0.20,
    },
}


# Module-level aliases for functions whose names collide with parameter names
# in inject_noise_custom.
_merge_words_fn = merge_words
_split_words_fn = split_words
_merge_lines_fn = merge_lines
_split_lines_fn = split_lines
_blank_out_fn = blank_out
_repeat_pattern_fn = repeat_pattern
_garbage_inject_fn = garbage_inject
_severe_deletion_fn = severe_deletion
_word_hallucinate_fn = word_hallucinate
_shuffle_lines_fn = shuffle_lines
_section_dropout_fn = section_dropout
_form_field_noise_fn = form_field_noise
_zone_chaos_fn = zone_chaos
_strikethrough_scramble_fn = strikethrough_scramble
_prefix_degradation_fn = prefix_degradation
_dosage_collapse_fn = dosage_collapse
_ligature_swaps_fn = ligature_swaps
_line_merging_fn = line_merging


def inject_noise(text, profile="printed_moderate", seed=None):
    """Apply the full noise pipeline using a named profile.

    Pipeline order: strikethrough -> zone_chaos -> prefix_deg ->
    dosage -> medical -> hallucinate -> substitute -> delete ->
    blank_out -> garbage -> insert -> transpose -> ligature ->
    merge_words -> split_words -> merge_lines -> line_merge ->
    split_lines -> severe_deletion -> shuffle_lines ->
    section_dropout -> form_field_noise -> repeat_pattern

    If seed is provided, sets random.seed(seed) for reproducibility.
    Returns the noisified text.
    """
    if profile not in NOISE_PROFILES:
        raise ValueError(
            "Unknown profile %r. Available: %s"
            % (profile, ", ".join(sorted(NOISE_PROFILES)))
        )
    if seed is not None:
        random.seed(seed)
    params = NOISE_PROFILES[profile]
    # seed already set above; pass seed=None so inject_noise_custom does not reseed.
    return inject_noise_custom(text, seed=None, **params)


def inject_noise_custom(text, substitute=0.05, delete=0.02, insert=0.02,
                        transpose=0.01, merge_words=0.05, split_words=0.03,
                        merge_lines=0.03, split_lines=0.02, medical=0.02,
                        blank=0.02, garbage=0.02, repeat=0.02, severe_del=0.03,
                        hallucinate=0.03, shuffle=0.02, section_drop=0.03,
                        form_field=0.02, zone_chaos=0.0,
                        prefix_deg=0.0, dosage=0.0, ligature=0.0,
                        strikethrough=1.0, line_merge=0.0, seed=None):
    """Apply noise with custom parameters. Each param controls a noise type.

    Pipeline:
      strikethrough -> zone_chaos -> prefix_deg -> dosage -> medical ->
      hallucinate -> substitute -> delete -> blank_out -> garbage_inject ->
      insert -> transpose -> ligature -> merge_words -> split_words ->
      merge_lines -> line_merge -> split_lines -> severe_deletion ->
      shuffle_lines -> section_dropout -> form_field_noise -> repeat_pattern
    """
    if seed is not None:
        random.seed(seed)
    # strikethrough always fires first: catch ~~...~~ before anything touches them
    if strikethrough > 0:
        text = _strikethrough_scramble_fn(text)
    # zone_chaos creates clean islands + hallucinated zones
    text = _zone_chaos_fn(text, p=zone_chaos)
    # Prefix degradation: T.→7., Syp.→8y., c/o→R40, before subs
    text = _prefix_degradation_fn(text, p=prefix_deg)
    # Dosage collapse: 1-0-1→127 before char subs corrupt the hyphens
    text = _dosage_collapse_fn(text, p=dosage)
    # Medical + word hallucination
    text = inject_medical_noise(text, p=medical)
    text = _word_hallucinate_fn(text, p=hallucinate)
    text = substitute_chars(text, p=substitute)
    text = delete_chars(text, p=delete)
    text = _blank_out_fn(text, p=blank)
    text = _garbage_inject_fn(text, p=garbage)
    text = insert_chars(text, p=insert)
    text = transpose_chars(text, p=transpose)
    # Ligature swaps after basic char noise
    text = _ligature_swaps_fn(text, p=ligature)
    text = _merge_words_fn(text, p=merge_words)
    text = _split_words_fn(text, p=split_words)
    text = _merge_lines_fn(text, p=merge_lines)
    # Aggressive line merging after standard merge_lines
    text = _line_merging_fn(text, p=line_merge)
    text = _split_lines_fn(text, p=split_lines)
    text = _severe_deletion_fn(text, p=severe_del)
    text = _shuffle_lines_fn(text, p=shuffle)
    text = _section_dropout_fn(text, p=section_drop)
    text = _form_field_noise_fn(text, p=form_field)
    text = _repeat_pattern_fn(text, p=repeat)
    return text


# ---------------------------------------------------------------------------
# 5. Utility metrics
# ---------------------------------------------------------------------------

def _levenshtein(a, b):
    """Levenshtein edit distance between two sequences."""
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


def char_error_rate(ground_truth, predicted):
    """Calculate CER between two strings.

    CER = (substitutions + deletions + insertions) / len(ground_truth)
    Uses Levenshtein distance at character level. Returns 0.0 for empty ground
    truth (and empty predicted), or float('inf') if ground truth is empty but
    predicted is not.
    """
    m = len(ground_truth)
    if m == 0:
        return 0.0 if len(predicted) == 0 else float('inf')
    return _levenshtein(ground_truth, predicted) / m


def word_error_rate(ground_truth, predicted):
    """Calculate WER between two strings.

    WER = (substitutions + deletions + insertions) / len(ground_truth words)
    Tokenisation is whitespace-based. Returns 0.0 for empty ground truth (and
    empty predicted), or float('inf') if ground truth is empty but predicted
    is not.
    """
    gt = ground_truth.split()
    pr = predicted.split()
    m = len(gt)
    if m == 0:
        return 0.0 if len(pr) == 0 else float('inf')
    return _levenshtein(gt, pr) / m


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    prescription = (
        "Rx\n"
        "Tab Metformin 500mg BD\n"
        "Tab Pantoprazole 40mg OD\n"
        "Tab Cetirizine 5mg HS\n"
        "Syp Paracetamol 1-0-1\n"
    )

    lab_report = (
        "PATIENT: John Doe\n"
        "AGE: 45 SEX: M\n"
        "TEST: COMPLETE BLOOD COUNT\n"
        "Hemoglobin: 13.5 g/dL\n"
        "WBC: 8200 /cumm\n"
        "Platelets: 2.5 lakhs/cumm\n"
        "Glucose (Fasting): 110 mg/dL\n"
    )

    print("=" * 70)
    print("OCR NOISE MODEL DEMO")
    print("=" * 70)

    for label, text in (("PRESCRIPTION (handwritten)", prescription),
                        ("LAB REPORT (printed)", lab_report)):
        print("\n" + "-" * 70)
        print(label)
        print("-" * 70)
        print("\n--- CLEAN ---\n")
        print(text)

        profile = "handwritten_severe" if "PRESCRIPTION" in label else "printed_moderate"
        noisy = inject_noise(text, profile=profile, seed=7)

        print("--- NOISY (profile=%s) ---\n" % profile)
        print(noisy)

        cer = char_error_rate(text, noisy)
        wer = word_error_rate(text, noisy)
        print("CER: %.4f  |  WER: %.4f" % (cer, wer))

    # Reproducibility check.
    a = inject_noise(prescription, profile="printed_moderate", seed=123)
    b = inject_noise(prescription, profile="printed_moderate", seed=123)
    print("\nReproducibility (same seed -> identical output):", a == b)