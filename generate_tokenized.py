"""
Generate tokenized dataset from raw JSONL using GPU acceleration.
Usage: python generate_tokenized.py --data data/calibrated_400k.jsonl --output_dir /tmp/tokenized_cache
"""

import os, sys, argparse, logging
from datasets import load_dataset
from transformers import AutoTokenizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', default='data/calibrated_400k.jsonl')
    parser.add_argument('--model_name', default='google/byt5-base')
    parser.add_argument('--max_input_length', type=int, default=1024)
    parser.add_argument('--max_target_length', type=int, default=1024)
    parser.add_argument('--output_dir', required=True)
    args = parser.parse_args()

    logger.info(f'Loading tokenizer: {args.model_name}')
    tokenizer = AutoTokenizer.from_pretrained(args.model_name, use_fast=True)

    logger.info(f'Loading raw dataset: {args.data}')
    raw_dataset = load_dataset('json', data_files=args.data, split='train')
    logger.info(f'Total samples: {len(raw_dataset)}')

    def preprocess(examples):
        inputs = examples['noisy']
        targets = examples['clean']

        model_inputs = tokenizer(
            inputs, max_length=args.max_input_length, truncation=True, padding=False
        )
        labels = tokenizer(
            targets, max_length=args.max_target_length, truncation=True, padding=False
        )

        model_inputs['labels'] = labels['input_ids']
        return model_inputs

    logger.info('Tokenizing...')
    tokenized = raw_dataset.map(
        preprocess,
        batched=True,
        remove_columns=['noisy', 'clean', 'type'],
        desc='Tokenizing',
    )

    logger.info(f'Saving to {args.output_dir}')
    os.makedirs(args.output_dir, exist_ok=True)
    tokenized.save_to_disk(args.output_dir)

    logger.info('Done!')

if __name__ == '__main__':
    main()