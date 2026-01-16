# Fingerprint Checker

A high-performance Discord fingerprint analyzer that checks and categorizes fingerprints by age using multi-threading. I am not held liable in case of any happenings.

## Credits

Made by @ai.legend

## Features

- **Multi-threaded Processing**: Run up to 10,000+ threads simultaneously (tested up to 10k, can go higher)
- **Age Categorization**: Automatically sorts fingerprints into:
  - Fresh (< 30 days)
  - 30 Days (30-180 days)
  - 6 Months (180-365 days)
  - 1 Year+ (365+ days)
- **Real-time Monitoring**: Live speed display and progress tracking
- **Colored Output**: Enhanced terminal experience with color-coded messages
- **Batch Processing**: Optimized file writing with buffered I/O
- **Timestamp Tracking**: Accurate creation date calculation for each fingerprint

## How to Use

### Setup

1. Place your fingerprints in `input/fp.txt` (one per line)
2. Run the script:
```bash
python a.py
```

3. Enter the number of threads when prompted (recommended: 100-1000 for optimal performance)

### Input Format

Create `input/fp.txt` with Discord fingerprints:
```
123456789012345678.XXXXXXXXXX
987654321098765432.YYYYYYYYYY
```

### Output

Results are saved in the `output/` directory:
- `fresh.txt` - Fingerprints < 30 days old
- `30_days.txt` - Fingerprints 30-180 days old
- `6_month.txt` - Fingerprints 180-365 days old
- `1_year.txt` - Fingerprints 365+ days old

## Usage Example

```
Enter number of threads: 500
[12:34:56] [ * ] Starting with 500 thread(s) to check 5000 fingerprint(s)
[12:34:56] [ * ] Thread started
[12:34:57] [ + ] Checked FingerPrint [...XXXXX] | Age: 45 Days | Created: 2025-12-02 08:30:15 IST
...
```

## Performance

- Tested with up to 10,000 concurrent threads
- Scales efficiently with larger thread counts
- Real-time speed monitoring (fps counter)
- Optimized buffer flushing for file I/O

