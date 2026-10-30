"""
Device Telemetry Summarizer CLI
Reads telemetry CSV logs, aggregates metrics per device, filters by temperature threshold,
prints a terminal summary table, and exports the results to JSON.
"""

import os
import csv
import json
import argparse
import sys


def parse_telemetry_csv(file_path):
    """
    Reads the CSV telemetry file and extracts records safely.
    Handles missing file, bad values, and malformed rows without crashing.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Telemetry file not found: {file_path}")

    records = []
    with open(file_path, mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        # Validate expected headers
        required_columns = {"device_id", "status", "temperature"}
        if not reader.fieldnames or not required_columns.issubset(set(reader.fieldnames)):
            raise ValueError(f"CSV header missing required columns: {required_columns}")

        row_number = 1
        for row in reader:
            row_number += 1
            device_id = row.get("device_id", "").strip()
            status = row.get("status", "").strip().upper()
            temp_str = row.get("temperature", "").strip()

            if not device_id:
                print(f"[Warning] Row {row_number}: Missing device_id. Skipping.")
                continue

            try:
                temp = float(temp_str)
            except (ValueError, TypeError):
                print(f"[Warning] Row {row_number}: Invalid temperature '{temp_str}'. Skipping.")
                continue

            records.append({
                "device_id": device_id,
                "status": status,
                "temperature": temp
            })

    return records


def aggregate_and_filter_telemetry(records, temp_limit=80.0):
    """
    Aggregates records per device and filters out devices with average temperature > temp_limit.

    Returns:
        list[dict]: List of aggregated device records meeting criteria.
    """
    device_groups = {}

    for record in records:
        dev_id = record["device_id"]
        if dev_id not in device_groups:
            device_groups[dev_id] = {
                "records": 0,
                "temp_sum": 0.0,
                "error_count": 0
            }

        device_groups[dev_id]["records"] += 1
        device_groups[dev_id]["temp_sum"] += record["temperature"]

        if record["status"] == "ERROR":
            device_groups[dev_id]["error_count"] += 1

    summary_list = []
    for dev_id, stats in sorted(device_groups.items()):
        total_records = stats["records"]
        avg_temp = round(stats["temp_sum"] / total_records, 2)
        error_count = stats["error_count"]

        # Filter out devices with average temperature above the threshold
        if avg_temp <= temp_limit:
            summary_list.append({
                "device_id": dev_id,
                "total_records": total_records,
                "average_temperature": avg_temp,
                "error_count": error_count
            })
        else:
            print(f"[Info] Device '{dev_id}' filtered out (Average Temp: {avg_temp}°C > {temp_limit}°C)")

    return summary_list


def print_summary_table(summary_data):
    """
    Renders a clean ASCII summary table in the terminal without third-party dependencies.
    """
    if not summary_data:
        print("\nNo devices matched the filtering criteria.")
        return

    headers = ["Device ID", "Total Records", "Avg Temp (°C)", "Error Count"]
    col_widths = [12, 16, 16, 14]

    separator = "+" + "+".join(["-" * (w + 2) for w in col_widths]) + "+"
    header_row = "|" + "|".join([f" {headers[i]:^{col_widths[i]}} " for i in range(len(headers))]) + "|"

    print("\n" + "=" * len(separator))
    print(" DEVICE TELEMETRY SUMMARY (Threshold: Avg Temp <= 80.0°C) ".center(len(separator)))
    print("=" * len(separator))
    print(separator)
    print(header_row)
    print(separator)

    for row in summary_data:
        avg_temp_formatted = f"{row['average_temperature']:.2f}"
        row_str = (
            f"| {row['device_id']:<{col_widths[0]}} "
            f"| {str(row['total_records']):^{col_widths[1]}} "
            f"| {avg_temp_formatted:^{col_widths[2]}} "
            f"| {str(row['error_count']):^{col_widths[3]}} |"
        )
        print(row_str)

    print(separator + "\n")


def export_to_json(summary_data, output_file):
    """
    Saves the aggregated summary into a formatted JSON file.
    """
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(output_file, mode="w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=4)

    print(f"[Success] Aggregated results exported to: {output_file}")


def process_telemetry(csv_path, output_json="output/summary.json", temp_limit=80.0):
    """
    Main processing workflow.
    """
    try:
        raw_records = parse_telemetry_csv(csv_path)
        aggregated = aggregate_and_filter_telemetry(raw_records, temp_limit=temp_limit)
        print_summary_table(aggregated)
        export_to_json(aggregated, output_json)
        return aggregated
    except Exception as exc:
        print(f"[Error] Failed to process telemetry: {exc}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Device Log Summarizer CLI")
    parser.add_argument(
        "--input", "-i",
        default="data/device_telemetry.csv",
        help="Path to input telemetry CSV file (default: data/device_telemetry.csv)"
    )
    parser.add_argument(
        "--output", "-o",
        default="output/summary.json",
        help="Path for exported summary JSON file (default: output/summary.json)"
    )
    parser.add_argument(
        "--temp-limit", "-t",
        type=float,
        default=80.0,
        help="Maximum allowed average temperature (default: 80.0)"
    )

    args = parser.parse_args()
    process_telemetry(args.input, args.output, args.temp_limit)


if __name__ == "__main__":
    main()
