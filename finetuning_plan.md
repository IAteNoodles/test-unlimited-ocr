# Fine-Tuning Plan: Post-OCR Correction for Medical Documents

Fine-tuning a **post-OCR correction model** for medical documents on a single RTX 4050 (6GB VRAM). Target documents: handwritten medical prescriptions (doctor handwriting) and printed medical reports (lab reports with tables, dense numeric data). Single-page inputs only. Accuracy is the priority; speed is secondary.

The primary challenge is **post-processing garbled OCR output**, not base OCR accuracy. The fine-tuning target is a small seq2seq corrector (ByT5), not the OCR model itself. OCR models run inference-only.

---

## 1. Hard Constraints

| Constraint | Implication |
|---|---|
| RTX 4050, 6GB VRAM | Cannot fine-tune anything above ~2B parameters. Full fine-tuning limited to ≤580M models. |
| Post-correction is the real challenge | OCR models are used inference-only (quantized). Fine-tuning budget goes to the corrector. |
| Data scarcity | No budget to annotate thousands of samples. Synthetic (noisy→clean) pair generation is the primary training data source. |
| Single-page documents | No multi-page stitching, no document boundary detection needed. |
| Accuracy > speed | Prefer larger corrector (ByT5-base over ByT5-small) if it fits VRAM. |

---

## 2. Architecture

```
┌─────────┐    ┌──────────────────┐    ┌─────────────────────┐    ┌────────────────────┐
│  Image  │ ─► │ OCR (inference)  │ ─► │ Post-Correction     │ ─► │ Structured         │
│         │    │ quantized, no FT │    │ (FINE-TUNED ByT5)   │    │ Extraction         │
└─────────┘    └──────────────────┘    └─────────────────────┘    └────────────────────┘
                  ~1–1.5GB VRAM            ~1.2–3.5GB VRAM           rule-based or 0.5B
```

All three stages fit in 6GB VRAM simultaneously at inference time. Only Stage 2 is fine-tuned.

### Stage 1: OCR Model (inference only, no fine-tuning)

Three options. Recommend dual-track (A + C) for best accuracy, or Option B as a single-model fallback.

| Option | Model | Size (quantized) | Best for | Notes |
|---|---|---|---|---|
| A | PaddleOCR-VL-0.9B (INT8) | ~1GB | Printed reports | SOTA on OmniDocBench v1.6 (96.33%). Not trained on handwriting. |
| B | Qwen2-VL-2B (INT4) | ~1.5GB | General / fallback | Better zero-shot VLM, handles handwriting better than A zero-shot. Single-model option. |
| C | TrOCR (base/large) | ~140M–400M | Handwriting | Dedicated handwriting recognition. Fits easily. |

**Recommendation:** Run Option A for printed reports and Option C for handwritten prescriptions (dual-track). Use a lightweight classifier (or manual routing) to pick the track. If you want a single model, use Option B.

```python
from transformers import AutoModelForCausalLM, AutoProcessor
import torch

def load_qwen2vl_2b_int4():
    model_id = "Qwen/Qwen2-VL-2B-Instruct"
    processor = AutoProcessor.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        torch_dtype=torch.float16,
        load_in_4bit=True,
    )
    return model, processor
```

```python
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

def load_trocr():
    processor = TrOCRProcessor.from_pretrained("microsoft/trocr-large-handwritten")
    model = VisionEncoderDecoderModel.from_pretrained(
        "microsoft/trocr-large-handwritten",
        torch_dtype=torch.float16,
    ).to("cuda")
    return model, processor
```

### Stage 2: Post-Correction Model (THE FINE-TUNING TARGET)

| Model | Params | VRAM (full FT, with optimizer) | Tokenization | Notes |
|---|---|---|---|---|
| **ByT5-small** (primary) | 300M | ~3.5GB | Byte-level | Proven best for noisy OCR text (Santos et al. 2024). Full FT fits 6GB. |
| **ByT5-base** (upscale) | 580M | ~5.5GB | Byte-level | Larger, still fits 6GB with gradient accumulation. Try if small underfits. |
| BART-base (alt) | 140M | ~2GB | BPE | Encoder-decoder, proven for seq2seq correction. |
| T5-small / T5-base (alt) | 60M / 220M | ~1.5GB / ~2.5GB | SentencePiece | Text-to-text, easy to fine-tune. |

**Why ByT5:**
- Santos et al. 2024: ByT5 outperformed LLMs (Llama 1/2) for post-OCR correction.
- Byte-level tokenization handles high-noise text better than word/subword models — no UNK tokens, no tokenization failure on garbled input.
- Small enough for **full fine-tuning** on 6GB VRAM (no LoRA needed).

**Input:** garbled OCR output text.
**Output:** corrected text.
**Training data:** synthetic (noisy→clean) pairs (see Section 4).

### Stage 3: Structured Extraction

| Option | Approach | VRAM | Notes |
|---|---|---|---|
| A | Rule-based + fuzzy matching | ~0GB | Regex for dosages/numbers; RapidFuzz against medicine reference DB for drug names. Fast, deterministic. |
| B | Qwen2.5-0.5B fine-tuned (LoRA) | ~1GB | Small enough for 6GB. Outputs structured JSON. |
| C | Few-shot prompting with Qwen2.5-0.5B | ~1GB | No fine-tuning, just good prompts. Quickest to ship. |

**Recommendation:** Start with Option A (rule-based) — it is deterministic and cheap. Move to Option B only if rule-based extraction misses structured relationships.

---

## 3. Extraction Schema

### Prescription Schema

```json
{
  "document_type": "prescription",
  "patient": {"name": "string", "age": "string", "gender": "string"},
  "date": "string",
  "diagnosis": "string",
  "doctor": {"name": "string"},
  "medications": [
    {
      "drug_name": "string",
      "dosage": "string",
      "frequency": "string",
      "route": "string",
      "duration": "string",
      "refills": "integer"
    }
  ]
}
```

### Lab Report Schema

```json
{
  "document_type": "lab_report",
  "patient": {"name": "string", "dob": "string"},
  "collection_date": "string",
  "ordering_physician": "string",
  "results": [
    {
      "test_name": "string",
      "test_value": "string",
      "unit": "string",
      "reference_range": "string",
      "abnormal_flag": "string"
    }
  ]
}
```

All fields nullable — omit rather than hallucinate. `abnormal_flag` values: `"normal"`, `"high"`, `"low"`, `"critical_high"`, `"critical_low"`, or empty.

---

## 4. Data Strategy (addressing data scarcity)

### 4.1 Synthetic OCR Error Generation (PRIMARY DATA SOURCE)

Take clean medical text (from medical textbooks, drug databases, sample reports) and inject realistic OCR errors. This generates (noisy→clean) pairs **without needing real annotated data**.

**Error types to inject:**

| Error type | Example |
|---|---|
| Character substitution | `m→rn`, `cl→d`, `0→O`, `1→l`, `5→S`, `rn→m` |
| Character merge | `rn→m`, `cl→d`, `nn→m` |
| Character split | `m→rn`, `w→vv` |
| Deletion | missing characters |
| Insertion | extra characters |
| Transposition | swapped adjacent characters |
| Word merge | `once daily → oncedaily` |
| Word split | `amoxicillin → amoxi cillin` |

**Target volume:** 10,000–50,000 (noisy→clean) pairs.

```python
import random

CHAR_SUBS = {
    "m": ["rn", "nn"], "rn": ["m"], "nn": ["m"],
    "cl": ["d"], "d": ["cl"],
    "0": ["O", "o"], "O": ["0"], "o": ["0"],
    "1": ["l", "I"], "l": ["1"], "I": ["1"],
    "5": ["S"], "S": ["5"],
    "8": ["B"], "B": ["8"],
    "2": ["Z"], "Z": ["2"],
    "6": ["G"], "G": ["6"],
    "vv": ["w"], "w": ["vv"],
}

def substitute_chars(text, p=0.05):
    out = []
    i = 0
    while i < len(text):
        matched = False
        for src in sorted(CHAR_SUBS, key=len, reverse=True):
            if text[i:i+len(src)].lower() == src and random.random() < p:
                out.append(random.choice(CHAR_SUBS[src]))
                i += len(src)
                matched = True
                break
        if not matched:
            out.append(text[i])
            i += 1
    return "".join(out)

def delete_chars(text, p=0.02):
    return "".join(c for c in text if random.random() > p)

def insert_chars(text, p=0.02, charset="abcdefghijklmnopqrstuvwxyz0123456789"):
    out = []
    for c in text:
        out.append(c)
        if random.random() < p:
            out.append(random.choice(charset))
    return "".join(out)

def transpose_chars(text, p=0.01):
    chars = list(text)
    for i in range(len(chars) - 1):
        if random.random() < p:
            chars[i], chars[i+1] = chars[i+1], chars[i]
    return "".join(chars)

def merge_words(text, p=0.05):
    words = text.split()
    out = []
    i = 0
    while i < len(words):
        if i < len(words) - 1 and random.random() < p:
            out.append(words[i] + words[i+1])
            i += 2
        else:
            out.append(words[i])
            i += 1
    return " ".join(out)

def inject_errors(text):
    text = substitute_chars(text)
    text = delete_chars(text)
    text = insert_chars(text)
    text = transpose_chars(text)
    text = merge_words(text)
    return text
```

### 4.2 Real Data (MINIMAL)

- **50–100 manually corrected OCR outputs** for validation only.
- **20–30** for few-shot examples (if using Option C extraction).
- Used for final evaluation, **not** primary training.

### 4.3 Medicine Reference Database

Build from open-source drug databases:
- **RxNorm** (NIH, US drug nomenclature)
- **WHO ATC** (Anatomical Therapeutic Chemical classification)
- National formularies (country-specific)

Fields: drug name (generic + brand), common abbreviations, dosage forms.

Used for:
- Fuzzy matching in post-correction (reward signal / final pass)
- Structured extraction (drug name normalization)

```python
from rapidfuzz import process, fuzz

class MedicineDB:
    def __init__(self, names):
        self.names = names

    def best_match(self, query, threshold=85):
        match = process.extractOne(
            query, self.names, scorer=fuzz.WRatio
        )
        if match and match[1] >= threshold:
            return match[0], match[1]
        return None, 0.0
```

---

## 5. Training Plan (all fits 6GB VRAM)

### Phase 1: Post-Correction Fine-Tuning (MAIN EFFORT)

| Parameter | Value |
|---|---|
| Model | ByT5-small (300M) or ByT5-base (580M) |
| Data | 10,000–50,000 synthetic (noisy→clean) pairs |
| Method | Full fine-tuning (model small enough — no LoRA) |
| Learning rate | 3e-4 (ByT5 uses higher LR than typical) |
| Batch size | 8–16 (with gradient accumulation if needed) |
| Epochs | 5–10 |
| Max sequence length | 512 tokens |
| Optimizer | AdamW |
| Warmup | 500 steps |
| Precision | fp16 |
| Memory (ByT5-small) | ~1.2GB model + ~3.5GB with optimizer states — fits 6GB |
| Framework | HuggingFace `transformers` + `Trainer`, or `trl` |

```python
from transformers import (
    AutoTokenizer, AutoModelForSeq2SeqLM,
    Seq2SeqTrainer, Seq2SeqTrainingArguments,
    DataCollatorForSeq2Seq,
)
from datasets import Dataset
import torch

MODEL_ID = "google/byt5-small"

def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForSeq2SeqLM.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16,
    ).to("cuda")
    return tokenizer, model

def tokenize_pairs(examples, tokenizer, max_len=512):
    inputs = tokenizer(
        examples["noisy"],
        max_length=max_len,
        truncation=True,
        padding="max_length",
    )
    labels = tokenizer(
        examples["clean"],
        max_length=max_len,
        truncation=True,
        padding="max_length",
    )
    inputs["labels"] = labels["input_ids"]
    return inputs

def train(train_pairs, eval_pairs):
    tokenizer, model = load_model()
    train_ds = Dataset.from_dict({
        "noisy": [p[0] for p in train_pairs],
        "clean": [p[1] for p in train_pairs],
    }).map(lambda x: tokenize_pairs(x, tokenizer), batched=True)
    eval_ds = Dataset.from_dict({
        "noisy": [p[0] for p in eval_pairs],
        "clean": [p[1] for p in eval_pairs],
    }).map(lambda x: tokenize_pairs(x, tokenizer), batched=True)

    collator = DataCollatorForSeq2Seq(tokenizer, model=model)
    args = Seq2SeqTrainingArguments(
        output_dir="./byt5-postcorrection",
        learning_rate=3e-4,
        per_device_train_batch_size=8,
        gradient_accumulation_steps=2,
        num_train_epochs=8,
        warmup_steps=500,
        fp16=True,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        predict_with_generate=True,
        generation_max_length=512,
    )
    trainer = Seq2SeqTrainer(
        model=model,
        args=args,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        data_collator=collator,
        tokenizer=tokenizer,
    )
    trainer.train()
    trainer.save_model("./byt5-postcorrection-final")
```

### Phase 2: Domain Adaptation (OPTIONAL)

Take the Phase 1 model and fine-tune further on medical-specific synthetic errors.

**Medical-specific error patterns:**
- Drug name confusion: `metformin → metformln`, `amoxicillin → amoxicilin`
- Dosage errors: `500mg → 500mg` (look-alike), `0.5mg → 5mg` (decimal slip — critical)
- Abbreviation expansion: `BD → BID`, `OD → QD`, `TID → TID`

**Volume:** 5,000–10,000 medical-specific pairs.

Same hyperparameters as Phase 1, lower LR (e.g., 1e-4), 3–5 epochs.

### Phase 3: Structured Extraction (OPTIONAL)

- **If using Qwen2.5-0.5B:** LoRA fine-tune on 100–200 examples.
- **If rule-based:** build regex patterns + fuzzy matching pipeline.

```python
import re

DOSAGE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(mg|mcg|ug|g|ml|units?|iu|meq)\b", re.I)
FREQ_RE = re.compile(r"\b(OD|BD|TID|QID|HS|PRN|Q\d+H|BID|QD)\b", re.I)

def extract_dosage(text):
    return DOSAGE_RE.findall(text)

def extract_frequency(text):
    return FREQ_RE.findall(text)
```

---

## 6. Evaluation

### Metrics

| Metric | What it measures | Use |
|---|---|---|
| **CER** (Character Error Rate) | Primary metric for post-correction | Lower is better. Compare raw OCR vs corrected. |
| WER (Word Error Rate) | Secondary | Lower is better. |
| Field-level accuracy | Structured extraction (drug name, dosage, frequency) | Per-field exact match. |
| Drug name accuracy | Fuzzy match against reference DB | Ratio ≥ 90 = correct. |
| Numeric accuracy | Lab values and dosages | Exact match + ±5% tolerance. |

### Baselines

1. **Raw OCR output** (no correction) — floor.
2. **SymSpell / Norvig spell checker** (traditional correction) — classical baseline.
3. **Zero-shot LLM correction** (Qwen2.5-0.5B prompted, no fine-tuning) — modern baseline.

The fine-tuned ByT5 corrector must beat all three on CER.

```python
import editdistance

def cer(reference, hypothesis):
    ref = list(reference)
    hyp = list(hypothesis)
    return editdistance.eval(ref, hyp) / len(ref) if ref else 0.0

def wer(reference, hypothesis):
    ref = reference.split()
    hyp = hypothesis.split()
    return editdistance.eval(ref, hyp) / len(ref) if ref else 0.0
```

---

## 7. Implementation Steps (Ordered)

1. **Set up environment:** Python, PyTorch (CUDA), `transformers`, `trl`, `rapidfuzz`, `editdistance`, `bitsandbytes` (for 4-bit OCR models).
2. **Choose and set up OCR model:** PaddleOCR-VL-0.9B (printed), TrOCR (handwriting), or Qwen2-VL-2B (single fallback).
3. **Build synthetic error generation pipeline** (Section 4.1).
4. **Generate 10,000–50,000 (noisy→clean) training pairs** from clean medical text sources.
5. **Download ByT5-small** from HuggingFace (`google/byt5-small`).
6. **Fine-tune ByT5** on synthetic pairs (Phase 1).
7. **Build medicine reference database** from RxNorm / WHO ATC.
8. **Evaluate on 50–100 real samples** — compute CER, WER, field accuracy.
9. **If needed:** Phase 2 domain adaptation on medical-specific errors.
10. **Build structured extraction** (rule-based regex + RapidFuzz, or Qwen2.5-0.5B).
11. **End-to-end pipeline integration:** image → OCR → corrector → extractor.
12. **Final evaluation** against baselines.

---

## 8. Risk Mitigation

| Risk | Mitigation |
|---|---|
| Synthetic errors don't match real OCR errors | Use diverse error types; validate on real samples early (step 8). Iterate on error generator. |
| ByT5 too small for medical vocabulary | Try ByT5-base (580M) — still fits 6GB. Fall back to BART-base or T5-base. |
| OCR model too slow on 4050 | Use INT8/INT4 quantization; batch inference; route printed docs to PaddleOCR-VL-0.9B (fast). |
| Post-correction changes correct text | Add confidence thresholding; only correct low-confidence tokens. Compare input vs output edit distance; skip if below threshold. |
| Drug names still wrong after correction | Fuzzy match against medicine DB as final pass (Section 4.3). |
| 6GB VRAM OOM during training | Reduce batch size to 4, increase gradient accumulation to 4. Enable gradient checkpointing. Use ByT5-small not base. |
| Decimal/dosage corruption (0.5mg → 5mg) | Numeric-preservation regex guard: detect dosage tokens pre-correction, verify post-correction, revert if numeric value changed beyond tolerance. |

```python
def safe_correct(text, corrector, tokenizer, max_delta=0.3):
    corrected = corrector(text, tokenizer)
    delta = cer(text, corrected)
    if delta > max_delta:
        return text
    return corrected
```

---

## 9. Hardware Summary

| Component | VRAM | Notes |
|---|---|---|
| OCR model (inference) | ~1–1.5GB | PaddleOCR-VL-0.9B INT8, or Qwen2-VL-2B INT4, or TrOCR fp16. |
| Post-corrector (training) | ~3.5–5.5GB | ByT5-small full FT ~3.5GB; ByT5-base ~5.5GB. |
| Post-corrector (inference) | ~1.2–2GB | fp16. |
| Structured extraction | ~0–1GB | Rule-based = 0; Qwen2.5-0.5B = ~1GB. |
| **Total inference** | **~3–4.5GB** | All three stages fit 6GB simultaneously. |

- All training: ByT5-small/base on RTX 4050 6GB — **full fine-tuning possible**.
- All inference: OCR (quantized) + corrector + extractor — all fit 6GB.
- **No cloud GPU needed.**
- **No LoRA needed** (models small enough for full FT).

---

## 10. Timeline

| Week | Work |
|---|---|
| 1 | Environment setup + synthetic data pipeline + OCR model setup |
| 2 | ByT5 fine-tuning + initial evaluation |
| 3 | Domain adaptation + medicine DB + structured extraction |
| 4 | Integration + final evaluation + iteration |

---

## 11. Key Research Backing

1. **Santos et al. 2024** — ByT5 outperformed LLMs (Llama 1/2) for post-OCR correction; smaller LMs more efficient and cheaper. Primary justification for ByT5 as corrector.
2. **Thomas et al. 2024** — Fine-tuned Llama 2 achieved 54.51% CER reduction (but 7B, too large for 6GB). Shows fine-tuning works; motivates smaller model.
3. **Bhandari 2026** — Compact specialized seq2seq beat GPT-4o zero-shot for post-correction. Validates small-model approach.
4. **Boros et al. 2024** — 14 foundation LLMs evaluated; "anything but efficient" at post-correction. Motivates not using large LLMs.
5. **Cao 2026** — LoRA + small LLM, 32% CER reduction, hierarchical framework for low-resource. Relevant for Phase 2/3.
6. **SynthOCR-Gen 2026** — Open-source synthetic OCR dataset generator, 25+ augmentation techniques. Reference for error generation pipeline.
7. **ELLMW 2026** — CNN-LSTM + LLM post-correction achieved 97.8% accuracy on handwriting. Validates pipeline architecture (OCR + correction).