# Device Log Summarizer CLI

A robust Python CLI tool designed to sanitize sensor readings, ingest and aggregate device telemetry logs, filter data based on operational thresholds, export structured JSON summaries, and generate comparison charts.

Built for the **Software Engineering Intern Technical Assessment**.

---

## Project Structure

```text
device_log_summarizer/
├── data/
│   └── device_telemetry.csv    # Sample telemetry dataset
├── src/
│   ├── __init__.py
│   ├── sanitizer.py            # Section 1: Sensor data cleaning & normalization
│   ├── summarizer.py           # Section 2: Core CSV ingestion, aggregation & CLI
│   └── visualize.py            # Section 3: Matplotlib visualization module
├── tests/
│   ├── __init__.py
│   └── test_sanitizer.py       # Unit tests for Section 1 sanitization logic
├── output/
│   ├── summary.json            # Generated aggregated telemetry JSON
│   └── avg_temp_chart.png      # Generated temperature comparison bar chart
├── requirements.txt            # Project dependencies
├── PROMPT_LOG.md               # Section 3 AI collaboration log
└── README.md                   # Documentation and usage guide
```

---

## Setup & Installation

### 1. Requirements
- Python 3.9+
- Standard library modules: `csv`, `json`, `argparse`, `unittest`, `os`, `sys`
- Visualization library: `matplotlib`

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Usage Instructions

### Section 1: Running Sanitization Tests
To verify the sensor normalization and edge-case handling logic:
```bash
python3 tests/test_sanitizer.py
```
**Test Coverage:**
- Type conversion of mixed types (strings, floats, ints) and dropping invalid/None entries.
- Filtering negative error flags (`< 0`).
- Clipping values exceeding `500.0` down to `500.0`.
- Graceful handling of empty or completely invalid lists without unhandled exceptions.

---

### Section 2: Running the Telemetry Summarizer CLI
Execute the CLI tool to process the telemetry CSV, display the formatted terminal summary table, and export results to JSON:

```bash
# Run with default paths (data/device_telemetry.csv -> output/summary.json)
python3 src/summarizer.py

# Or specify custom input/output and temperature threshold
python3 src/summarizer.py --input data/device_telemetry.csv --output output/summary.json --temp-limit 80.0
```

#### CLI Flags:
- `--input` / `-i`: Path to the input CSV file (default: `data/device_telemetry.csv`).
- `--output` / `-o`: Output path for the JSON summary (default: `output/summary.json`).
- `--temp-limit` / `-t`: Upper bound for average temperature filtering (default: `80.0`).

#### Terminal Output Example:
```text
[Info] Device 'DEV_C' filtered out (Average Temp: 88.75°C > 80.0°C)
[Info] Device 'DEV_E' filtered out (Average Temp: 83.5°C > 80.0°C)

=======================================================================
        DEVICE TELEMETRY SUMMARY (Threshold: Avg Temp <= 80.0°C)       
=======================================================================
+--------------+------------------+------------------+----------------+
|  Device ID   |  Total Records   |  Avg Temp (°C)   |  Error Count   |
+--------------+------------------+------------------+----------------+
| DEV_A        |        3         |      45.23       |       0        |
| DEV_B        |        4         |      68.92       |       2        |
| DEV_D        |        3         |      36.50       |       0        |
+--------------+------------------+------------------+----------------+

[Success] Aggregated results exported to: output/summary.json
```

---

### Section 3: Generating Visualizations
Generate a bar chart comparing the average temperatures of filtered devices:
```bash
python3 src/visualize.py --input output/summary.json --output output/avg_temp_chart.png
```
The resulting chart is saved to `output/avg_temp_chart.png`.

---

## Robustness & Error Handling

- **Missing Files:** Raises clear, descriptive errors if input CSV/JSON paths are invalid.
- **Corrupted / Incomplete CSV Rows:** Skips non-numeric temperatures or missing device IDs with warnings instead of failing mid-batch.
- **Zero Division Safety:** Safeguards against empty groups when calculating averages.
- **Threshold Filtering:** Correctly excludes devices operating beyond safe temperature thresholds (`> 80.0°C`).

---

## AI Collaboration Log
Refer to [`PROMPT_LOG.md`](PROMPT_LOG.md) for details on the prompt iteration and debugging process for Section 3.
