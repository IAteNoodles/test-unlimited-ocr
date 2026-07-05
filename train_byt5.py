"""
train_byt5.py
=============
Fine-tune ByT5-base on synthetic noisy→clean medical document correction.

Usage:
    python train_byt5.py --data data/calibrated_100k.jsonl --output_dir models/byt5-ocr --epochs 3
"""

import json, os, sys, argparse, math, logging, hashlib
from dataclasses import dataclass, field
from typing import Optional

import torch
from datasets import Dataset, DatasetDict, concatenate_datasets, load_dataset, load_from_disk
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    DataCollatorForSeq2Seq,
    EarlyStoppingCallback,
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
_file_handler = logging.FileHandler('train_debug.log', mode='w')
_file_handler.setFormatter(logging.Formatter('%(asctime)s | %(message)s'))
logging.getLogger().addHandler(_file_handler)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# 1. Metrics
# ---------------------------------------------------------------------------

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


def char_error_rate(gt, pred):
    if not gt:
        return 0.0 if not pred else float('inf')
    return _levenshtein(gt, pred) / len(gt)


def word_error_rate(gt, pred):
    gt_words = gt.split()
    pred_words = pred.split()
    if not gt_words:
        return 0.0 if not pred_words else float('inf')
    return _levenshtein(gt_words, pred_words) / len(gt_words)


# ---------------------------------------------------------------------------
# 2. Data loading
# ---------------------------------------------------------------------------

def load_jsonl(path, max_samples=None):
    """Load JSONL file. Each line: {'noisy': ..., 'clean': ..., 'type': ...}"""
    data = {'noisy': [], 'clean': [], 'type': []}
    with open(path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if max_samples and i >= max_samples:
                break
            row = json.loads(line)
            data['noisy'].append(row['noisy'])
            data['clean'].append(row['clean'])
            data['type'].append(row.get('type', 'unknown'))
    return Dataset.from_dict(data)


# ---------------------------------------------------------------------------
# 3. Training
# ---------------------------------------------------------------------------

@dataclass
class ModelArguments:
    model_name: str = field(default="google/byt5-base")
    tokenizer_name: Optional[str] = field(default=None)


@dataclass
class DataArguments:
    data_path: str = field(default="data/calibrated_100k.jsonl")
    max_train_samples: Optional[int] = field(default=None)
    max_eval_samples: Optional[int] = field(default=None)
    max_input_length: int = field(default=1024)
    max_target_length: int = field(default=1024)


@dataclass
class TrainingArguments(Seq2SeqTrainingArguments):
    output_dir: str = field(default="models/byt5-ocr")
    num_train_epochs: float = field(default=3)
    per_device_train_batch_size: int = field(default=8)
    per_device_eval_batch_size: int = field(default=8)
    gradient_accumulation_steps: int = field(default=2)
    learning_rate: float = field(default=3e-4)
    warmup_steps: int = field(default=500)
    weight_decay: float = field(default=0.01)
    logging_steps: int = field(default=100)
    eval_steps: int = field(default=500)
    save_steps: int = field(default=1000)
    save_total_limit: int = field(default=3)
    predict_with_generate: bool = field(default=True)
    generation_max_length: int = field(default=1024)
    generation_num_beams: int = field(default=4)
    fp16: bool = field(default=True)
    bf16: bool = field(default=False)
    gradient_checkpointing: bool = field(default=True)
    optim: str = field(default="adamw_torch")
    report_to: str = field(default="none")
    dataloader_num_workers: int = field(default=4)
    ddp_find_unused_parameters: Optional[bool] = field(default=None)
    remove_unused_columns: bool = field(default=False)
    eval_strategy: str = field(default="steps")
    logging_first_step: bool = field(default=True)


def preprocess_function(examples, tokenizer, data_args):
    """Tokenize noisy→clean pairs."""
    model_inputs = tokenizer(
        examples['noisy'],
        max_length=data_args.max_input_length,
        truncation=True,
        padding=False,
    )

    labels = tokenizer(
        examples['clean'],
        max_length=data_args.max_target_length,
        truncation=True,
        padding=False,
    )

    model_inputs['labels'] = labels['input_ids']
    return model_inputs


def compute_metrics(eval_preds, tokenizer):
    """Compute CER and WER across all predictions, plus per document type."""
    predictions, labels = eval_preds

    # Clamp prediction IDs to valid ByT5 range [0, 258] before decoding
    vocab_size = tokenizer.vocab_size
    predictions = [[max(0, min(p, vocab_size - 1)) for p in pred] for pred in predictions]
    decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)
    labels = [[l for l in label if l != -100] for label in labels]
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    # Overall CER/WER
    cers = []
    wers = []
    for pred, label in zip(decoded_preds, decoded_labels):
        cers.append(char_error_rate(label, pred))
        wers.append(word_error_rate(label, pred))

    metrics = {
        'cer': sum(cers) / len(cers) if cers else 0.0,
        'wer': sum(wers) / len(wers) if wers else 0.0,
        'cer_std': (sum((c - sum(cers)/len(cers))**2 for c in cers) / len(cers))**0.5 if cers else 0.0,
    }

    return metrics


def main():
    parser = argparse.ArgumentParser(description='Fine-tune ByT5 for OCR correction')
    parser.add_argument('--data', default='data/calibrated_100k.jsonl')
    parser.add_argument('--output_dir', default='models/byt5-ocr')
    parser.add_argument('--model_name', default='google/byt5-base')
    parser.add_argument('--epochs', type=int, default=50)
    parser.add_argument('--batch_size', type=int, default=16)
    parser.add_argument('--lr', type=float, default=5e-5)
    parser.add_argument('--max_input_length', type=int, default=1024)
    parser.add_argument('--max_target_length', type=int, default=1024)
    parser.add_argument('--tokenized_data', default=None, help='Path to pre-tokenized dataset cache')
    parser.add_argument('--max_train_samples', type=int, default=None)
    parser.add_argument('--max_eval_samples', type=int, default=None)
    parser.add_argument('--val_split', type=float, default=0.02)
    parser.add_argument('--test_split', type=float, default=0.01)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--logging_steps', type=int, default=None)
    parser.add_argument('--patience', type=int, default=5, help='Early stopping patience (eval steps)')
    parser.add_argument('--no_early_stopping', action='store_true', help='Disable early stopping')
    parser.add_argument('--gradient_checkpointing', action='store_true', help='Enable gradient checkpointing (slower but less VRAM)')
    parser.add_argument('--dataloader_num_workers', type=int, default=0, help='Dataloader worker processes (2+ for prefetching)')
    args = parser.parse_args()

    # Device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    logger.info(f'Device: {device}')
    if torch.cuda.is_available():
        logger.info(f'GPU: {torch.cuda.get_device_name(0)}  VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}GB')

    # Load tokenizer and model
    tokenizer_name = args.model_name
    logger.info(f'Loading tokenizer: {tokenizer_name}')
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    logger.info(f'Loading model: {args.model_name}')
    model = AutoModelForSeq2SeqLM.from_pretrained(
        args.model_name,
        torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
        low_cpu_mem_usage=True,
    )

    # Enable gradient checkpointing
    model.gradient_checkpointing_enable()

    # Log model size
    n_params = sum(p.numel() for p in model.parameters())
    n_trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    logger.info(f'Model params: {n_params:,}  Trainable: {n_trainable:,}')

    raw_datasets = None

    # Load dataset (tokenized or raw)
    if args.tokenized_data:
        logger.info(f'Loading pre-tokenized dataset: {args.tokenized_data}')
        tokenized_datasets = load_from_disk(args.tokenized_data)
        
        # Handle plain Dataset (not DatasetDict) — clean columns then split
        if not isinstance(tokenized_datasets, DatasetDict):
            logger.info('Single dataset loaded, removing extra columns...')
            keep = [c for c in tokenized_datasets.column_names if c in ['input_ids', 'attention_mask', 'labels']]
            if len(keep) != len(tokenized_datasets.column_names):
                tokenized_datasets = tokenized_datasets.remove_columns([c for c in tokenized_datasets.column_names if c not in keep])
            logger.info('Splitting pre-tokenized dataset...')
            ds = tokenized_datasets.train_test_split(test_size=args.val_split + args.test_split, seed=args.seed)
            val_test = ds['test'].train_test_split(test_size=args.test_split / (args.val_split + args.test_split), seed=args.seed)
            tokenized_datasets = DatasetDict({
                'train': ds['train'],
                'validation': val_test['train'],
                'test': val_test['test'],
            })
        else:
            # Already a DatasetDict — clean columns per split
            missing_splits = [k for k in ['train', 'validation', 'test'] if k not in tokenized_datasets]
            if missing_splits:
                # Has keys but not the expected ones — merge, clean, re-split
                logger.info(f'Missing splits {missing_splits}, re-splitting...')
                merged = None
                for split in tokenized_datasets.keys():
                    keep = [c for c in tokenized_datasets[split].column_names if c in ['input_ids', 'attention_mask', 'labels']]
                    ds = tokenized_datasets[split]
                    if len(keep) != len(ds.column_names):
                        ds = ds.remove_columns([c for c in ds.column_names if c not in keep])
                    merged = ds if merged is None else concatenate_datasets([merged, ds])
                ds = merged.train_test_split(test_size=args.val_split + args.test_split, seed=args.seed)
                val_test = ds['test'].train_test_split(test_size=args.test_split / (args.val_split + args.test_split), seed=args.seed)
                tokenized_datasets = DatasetDict({
                    'train': ds['train'],
                    'validation': val_test['train'],
                    'test': val_test['test'],
                })
            else:
                for split in ['train', 'validation', 'test']:
                    cols = tokenized_datasets[split].column_names
                    keep = [c for c in cols if c in ['input_ids', 'attention_mask', 'labels']]
                    if len(keep) != len(cols):
                        tokenized_datasets[split] = tokenized_datasets[split].remove_columns([c for c in cols if c not in keep])
            logger.info('Split: train=%d  val=%d  test=%d' % (
                len(tokenized_datasets['train']), len(tokenized_datasets['validation']), len(tokenized_datasets['test'])))
    else:
        logger.info(f'Loading raw dataset: {args.data}')
        dataset = load_jsonl(args.data)
        logger.info(f'Total samples: {len(dataset)}')

        # Split
        dataset = dataset.train_test_split(
            test_size=args.val_split + args.test_split,
            seed=args.seed,
        )
        val_test = dataset['test'].train_test_split(
            test_size=args.test_split / (args.val_split + args.test_split),
            seed=args.seed,
        )
        raw_datasets = DatasetDict({
            'train': dataset['train'],
            'validation': val_test['train'],
            'test': val_test['test'],
        })
        logger.info('Split: train=%d  val=%d  test=%d' % (
            len(raw_datasets['train']), len(raw_datasets['validation']), len(raw_datasets['test'])))

        # Tokenize with caching (cache lives in output_dir on Drive for persistence)
        cache_key = hashlib.md5(
            f'{os.path.getmtime(args.data)}_{args.model_name}_{args.max_input_length}_{args.max_target_length}'.encode()
        ).hexdigest()
        tokenized_cache_dir = os.path.join(args.output_dir, f'.tokenized_cache_{cache_key}')

        if os.path.exists(tokenized_cache_dir):
            logger.info(f'Loading tokenized dataset from cache: {tokenized_cache_dir}')
            tokenized_datasets = load_from_disk(tokenized_cache_dir)
            # Remove any unexpected columns
            for split in tokenized_datasets:
                cols = tokenized_datasets[split].column_names
                keep = [c for c in cols if c in ['input_ids', 'attention_mask', 'labels']]
                if len(keep) != len(cols):
                    tokenized_datasets[split] = tokenized_datasets[split].remove_columns([c for c in cols if c not in keep])
        else:
            def _preprocess(examples):
                return preprocess_function(examples, tokenizer, args)

            tokenized_datasets = raw_datasets.map(
                _preprocess,
                batched=True,
                remove_columns=['noisy', 'clean', 'type'],
                desc='Tokenizing',
            )

            logger.info(f'Saving tokenized dataset to cache: {tokenized_cache_dir}')
            os.makedirs(tokenized_cache_dir, exist_ok=True)
            tokenized_datasets.save_to_disk(tokenized_cache_dir)

    if args.max_train_samples:
        tokenized_datasets['train'] = tokenized_datasets['train'].select(range(args.max_train_samples))
    if args.max_eval_samples:
        tokenized_datasets['validation'] = tokenized_datasets['validation'].select(range(args.max_eval_samples))

    # Data collator
    data_collator = DataCollatorForSeq2Seq(
        tokenizer,
        padding=True,
        pad_to_multiple_of=8,
    )

    # Training arguments
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        learning_rate=args.lr,
        gradient_accumulation_steps=2,
        warmup_steps=500,
        weight_decay=0.01,
        logging_steps=args.logging_steps if args.logging_steps is not None else 100,
        eval_steps=500,
        save_steps=500,
        predict_with_generate=True,
        generation_max_length=args.max_target_length,
        generation_num_beams=2,
        fp16=False,
        bf16=torch.cuda.is_available(),
        gradient_checkpointing=args.gradient_checkpointing,
        optim='adamw_torch',
        max_grad_norm=1.0,
        report_to='none',
        dataloader_num_workers=args.dataloader_num_workers,
        eval_strategy='steps',
        load_best_model_at_end=not args.no_early_stopping,
        metric_for_best_model='eval_loss',
        greater_is_better=False,
        save_total_limit=3,
        logging_first_step=True,
        remove_unused_columns=False,
    )

    # Trainer
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets['train'],
        eval_dataset=tokenized_datasets['validation'],
        data_collator=data_collator,
        compute_metrics=lambda preds: compute_metrics(preds, tokenizer),
        callbacks=[EarlyStoppingCallback(early_stopping_patience=args.patience)] if not args.no_early_stopping else None,
    )

    # Train (auto-resume from checkpoint if exists)
    last_checkpoint = None
    if os.path.isdir(args.output_dir) and any(f.startswith('checkpoint-') for f in os.listdir(args.output_dir)):
        checkpoints = [d for d in os.listdir(args.output_dir) if d.startswith('checkpoint-')]
        last_checkpoint = os.path.join(args.output_dir, sorted(checkpoints, key=lambda x: int(x.split('-')[-1]))[-1])
        logger.info(f'Resuming from checkpoint: {last_checkpoint}')
    logger.info('Starting training...')
    trainer.train(resume_from_checkpoint=last_checkpoint)
    logger.info('Training complete.')

    # Save final model
    final_dir = os.path.join(args.output_dir, 'final')
    trainer.save_model(final_dir)
    tokenizer.save_pretrained(final_dir)
    logger.info(f'Model saved to {final_dir}')

    # Evaluate on test set
    logger.info('Evaluating on test set...')
    test_metrics = trainer.evaluate(tokenized_datasets['test'])
    logger.info(f'Test metrics: {json.dumps(test_metrics, indent=2)}')

    # Per-document-type evaluation using raw texts (only available if tokenized from raw)
    if raw_datasets is not None:
        logger.info('Per-document-type evaluation...')
        test_raw = raw_datasets['test']
        preds = trainer.predict(tokenized_datasets['test'])
        decoded_preds = tokenizer.batch_decode(preds.predictions, skip_special_tokens=True)

        type_metrics = {}
        for raw, pred in zip(test_raw, decoded_preds):
            doc_type = raw.get('type', 'unknown')
            if doc_type not in type_metrics:
                type_metrics[doc_type] = {'cers': [], 'wers': []}
            type_metrics[doc_type]['cers'].append(char_error_rate(raw['clean'], pred))
            type_metrics[doc_type]['wers'].append(word_error_rate(raw['clean'], pred))

        logger.info('--- Per-document-type metrics ---')
        logger.info('%-15s %8s %8s %8s' % ('Type', 'CER', 'WER', 'Count'))
        logger.info('-' * 40)
        for doc_type, m in sorted(type_metrics.items()):
            cers = m['cers']
            wers = m['wers']
            logger.info('%-15s %8.4f %8.4f %8d' % (
                doc_type, sum(cers)/len(cers), sum(wers)/len(wers), len(cers)))

    # Run on test set again to print a few examples
    logger.info('\n--- Sample predictions ---')
    for i in range(min(5, len(preds.predictions))):
        clean = test_raw[i]['clean']
        noisy = test_raw[i]['noisy']
        pred = decoded_preds[i]
        logger.info(f'\nSample {i+1} ({test_raw[i].get("type", "?")}):')
        logger.info(f'  CLEAN:  {clean[:100]}...' if len(clean)>100 else f'  CLEAN:  {clean}')
        logger.info(f'  NOISY:  {noisy[:100]}...' if len(noisy)>100 else f'  NOISY:  {noisy}')
        logger.info(f'  PRED:   {pred[:100]}...' if len(pred)>100 else f'  PRED:   {pred}')
        logger.info(f'  CER:    {char_error_rate(clean, pred):.4f}')
        logger.info(f'  WER:    {word_error_rate(clean, pred):.4f}')


if __name__ == '__main__':
    main()
