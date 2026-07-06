"""
ocr_noise_real.py
=================
Noise generator that mimics real OCR output patterns.

Based on analysis of test_100.jsonl:
- 100% have unicode artifacts (|, @, #, ~, ^, \\, etc.)
- 97% have line merges (noisy has fewer newlines than clean)
- 63% have repetition loops (same char repeated 5+ times)
- CER range: 0.176-1.018 (median 0.613)

Usage:
    from ocr_noise_real import RealOCRNoiseGenerator
    gen = RealOCRNoiseGenerator(seed=42)
    noisy_text = gen.corrupt(clean_text)
"""

import random
import re
import string


# Character similarity groups for substitution
SIMILAR_CHARS = {
    'a': 'àáâãäåæαа',
    'b': 'ḃβь',
    'c': 'çςс',
    'd': 'ďδд',
    'e': 'éêëèεе',
    'f': 'ƒφф',
    'g': 'ğγг',
    'h': 'ĥηн',
    'i': 'ìíîï1|!ιи',
    'j': 'ĵј',
    'k': 'κк',
    'l': '1|!ιл',
    'm': 'μм',
    'n': 'ñńηн',
    'o': 'òóôõö0οо',
    'p': 'ρр',
    'q': 'φq',
    'r': 'ŕřρ',
    's': 'śş5ςс',
    't': 'ţτт',
    'u': 'ùúûüμυ',
    'v': 'νv',
    'w': 'ωω',
    'x': '×χх',
    'y': 'ýγу',
    'z': 'źżζз',
    '0': 'oOοоO',
    '1': 'il!|ι1I',
    '2': '2z',
    '3': '3z',
    '5': 'sS5',
    '6': '6b',
    '8': '8B',
}

# Unicode artifacts that appear in real OCR
UNICODE_ARTIFACTS = list('!@#$%^&*(){}[]|/\\<>~`±§©®™°µ·…→←↑↓')
HEAVY_ARTIFACTS = list('!@#$%^&*(){}[]|/<>~±§©®™°µ·…→←↑↓')

# Dash-like characters for table corruption
DASH_CHARS = list('-—–━─')

# Special characters that appear in noisy OCR
NOISE_CHARS = list('!@#$%^&*(){}[]|/<>~`±§©®™°µ·…→←↑↓')


class RealOCRNoiseGenerator:
    """
    Generates realistic OCR noise based on patterns from test_100.jsonl.

    Noise types:
    1. Character substitution with similar-looking chars
    2. Unicode artifact injection
    3. Line merging (most common - 97% of samples)
    4. Repetition loops (63% of samples)
    5. Space corruption
    6. Table structure destruction
    7. Number corruption
    8. Case corruption
    """

    def __init__(self, seed=42):
        self.rng = random.Random(seed)

    def corrupt(self, text, target_cer=None):
        """
        Apply realistic OCR noise to text.

        Args:
            text: Clean input text
            target_cer: Target CER (0.0-1.0). If None, sample from real distribution.

        Returns:
            Noisy text with CER close to target
        """
        if target_cer is None:
            # Sample from real distribution (0.2-1.0, median 0.6)
            target_cer = self.rng.betavariate(2.5, 2.0) * 0.8 + 0.2

        # Apply noise in order of frequency in real data
        result = text

        # 1. Always apply line merging (97% of real samples)
        result = self._merge_lines(result)

        # 2. Always apply character substitution (100%)
        result = self._substitute_chars(result, min(target_cer * 0.8, 0.6))

        # 3. Always apply unicode artifacts (100%)
        result = self._inject_artifacts(result, min(target_cer * 0.5, 0.4))

        # 4. Apply repetition loops (63%)
        if self.rng.random() < 0.63:
            result = self._add_repetitions(result)

        # 5. Apply space corruption
        result = self._corrupt_spaces(result, min(target_cer * 0.3, 0.25))

        # 6. Apply table destruction
        result = self._destroy_tables(result)

        # 7. Apply number corruption
        result = self._corrupt_numbers(result)

        # 8. Apply case corruption
        result = self._corrupt_case(result)

        # 9. Apply line deletion (some lines disappear in real OCR)
        result = self._delete_lines(result)

        return result

    def _merge_lines(self, text):
        """Merge adjacent lines (most common real OCR pattern - 97%)."""
        lines = text.split('\n')
        if len(lines) < 3:
            return text

        merged = []
        i = 0
        while i < len(lines):
            if i < len(lines) - 1 and self.rng.random() < 0.9:
                # Merge 2-5 lines together
                merge_count = min(self.rng.choice([2, 2, 3, 3, 4, 5]), len(lines) - i)
                merged_text = lines[i]
                for j in range(1, merge_count):
                    separator = self.rng.choice([' ', ' ', '', '', ' ', '', '', ' ', ''])
                    merged_text += separator + lines[i + j]
                merged.append(merged_text)
                i += merge_count
            else:
                merged.append(lines[i])
                i += 1

        return '\n'.join(merged)

    def _substitute_chars(self, text, intensity):
        """Substitute characters with similar-looking alternatives."""
        result = []
        for char in text:
            if char.lower() in SIMILAR_CHARS and self.rng.random() < intensity:
                # Pick a random similar character
                similar = SIMILAR_CHARS[char.lower()]
                replacement = self.rng.choice(similar)
                # Preserve case
                if char.isupper():
                    replacement = replacement.upper()
                result.append(replacement)
            else:
                result.append(char)
        return ''.join(result)

    def _inject_artifacts(self, text, intensity):
        """Inject unicode artifacts at random positions."""
        chars = list(text)
        num_artifacts = int(len(chars) * intensity * 0.5)

        for _ in range(num_artifacts):
            if chars:
                pos = self.rng.randint(0, len(chars) - 1)
                artifact = self.rng.choice(HEAVY_ARTIFACTS)
                chars.insert(pos, artifact)

        return ''.join(chars)

    def _add_repetitions(self, text):
        """Add repetition loops (common in real OCR - 63%)."""
        lines = text.split('\n')
        if not lines:
            return text

        result = []
        for line in lines:
            if self.rng.random() < 0.2 and line.strip():
                # Repeat a portion of the line
                repeat_count = self.rng.randint(3, 8)
                if len(line) > 5:
                    start = self.rng.randint(0, len(line) // 2)
                    end = min(start + self.rng.randint(2, 8), len(line))
                    segment = line[start:end]
                    line = line + '\n' + (segment + '\n') * repeat_count
            result.append(line)

        return '\n'.join(result)

    def _corrupt_spaces(self, text, intensity):
        """Corrupt spaces (missing, extra, or replaced)."""
        result = []
        for char in text:
            if char == ' ':
                r = self.rng.random()
                if r < intensity * 0.5:
                    result.append('')  # Missing space
                elif r < intensity:
                    result.append(self.rng.choice([' ', '  ', '   ']))  # Extra spaces
                else:
                    result.append(' ')
            else:
                result.append(char)
        return ''.join(result)

    def _destroy_tables(self, text):
        """Destroy table structure (columns collapse)."""
        lines = text.split('\n')
        result = []

        for line in lines:
            # Check if line looks like a table row
            if '\t' in line or '  ' in line:
                # Collapse columns
                if self.rng.random() < 0.7:
                    parts = re.split(r'\t|  +', line)
                    parts = [p for p in parts if p.strip()]
                    if parts:
                        line = self.rng.choice([' ', ' ', '', ' ', ' ']).join(parts)

            # Check if line is a separator (dashes, equals)
            if re.match(r'^[\-=]+$', line.strip()):
                if self.rng.random() < 0.5:
                    # Corrupt the separator
                    line = line[:len(line)//2] + self.rng.choice(DASH_CHARS) * (len(line)//2)

            result.append(line)

        return '\n'.join(result)

    def _corrupt_numbers(self, text):
        """Corrupt numbers (common in real OCR)."""
        def replace_number(match):
            num = match.group(0)
            if self.rng.random() < 0.4:
                # Corrupt one digit
                digits = list(num)
                if digits:
                    pos = self.rng.randint(0, len(digits) - 1)
                    if self.rng.random() < 0.4:
                        # Replace with similar digit
                        similar = {'0': 'Oo', '1': 'Il!', '2': '2z', '3': '3z',
                                   '4': '4A', '5': 'Ss5', '6': '6b', '7': '7T',
                                   '8': '8B', '9': '9g'}
                        if digits[pos] in similar:
                            digits[pos] = self.rng.choice(similar[digits[pos]])
                    elif self.rng.random() < 0.7:
                        # Delete digit
                        digits.pop(pos)
                    else:
                        # Add digit
                        digits.insert(pos, str(self.rng.randint(0, 9)))
                return ''.join(digits)
            return num

        return re.sub(r'\d{2,}', replace_number, text)

    def _corrupt_case(self, text):
        """Randomly change case of characters."""
        result = []
        for char in text:
            if char.isalpha() and self.rng.random() < 0.05:
                result.append(char.swapcase())
            else:
                result.append(char)
        return ''.join(result)

    def _delete_lines(self, text):
        """Delete some lines (common in real OCR)."""
        lines = text.split('\n')
        if len(lines) < 5:
            return text

        result = []
        for line in lines:
            # Don't delete important lines (Patient, Test, Result, etc.)
            important = any(kw in line for kw in ['Patient:', 'Test', 'Result', 'Ref:', 'Age:', 'Sex:'])
            if important or self.rng.random() > 0.1:
                result.append(line)

        return '\n'.join(result)


def generate_dataset(input_path, output_path, num_samples=None, seed=42):
    """Generate noisy dataset from clean JSONL."""
    import json

    gen = RealOCRNoiseGenerator(seed=seed)

    with open(input_path, 'r', encoding='utf-8') as fin, \
         open(output_path, 'w', encoding='utf-8') as fout:

        for i, line in enumerate(fin):
            if num_samples and i >= num_samples:
                break

            data = json.loads(line)
            clean = data['clean']

            # Generate noise
            noisy = gen.corrupt(clean)

            # Calculate CER
            from cer import char_error_rate
            cer = char_error_rate(clean, noisy)

            # Write output
            record = {
                'id': f'real_ocr_{i:06d}',
                'clean': clean,
                'noisy': noisy,
                'type': data.get('type', 'unknown'),
                'format': data.get('format', 'unknown'),
                'cer': round(cer, 4),
            }

            # Copy additional fields
            for key in ['panel', 'condition', 'format', 'noise_profile']:
                if key in data:
                    record[key] = data[key]

            fout.write(json.dumps(record, ensure_ascii=False) + '\n')

            if (i + 1) % 10000 == 0:
                print(f'Processed {i + 1} samples')

    print(f'Done. Generated {min(num_samples or float("inf"), i + 1)} samples')


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('Usage: python ocr_noise_real.py <input.jsonl> <output.jsonl> [num_samples] [seed]')
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    num_samples = int(sys.argv[3]) if len(sys.argv) > 3 else None
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 42

    generate_dataset(input_path, output_path, num_samples, seed)
