"""
Telemetry Visualization Module
Generates a bar chart comparing average temperatures across active devices using matplotlib.
"""

import os
import json
import argparse
import sys
import matplotlib.pyplot as plt


def load_summary_data(json_file):
    """Loads and validates aggregated device telemetry JSON data."""
    if not os.path.exists(json_file):
        raise FileNotFoundError(f"Summary JSON file not found at: {json_file}")

    with open(json_file, mode="r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Invalid JSON format: expected a list of device records.")

    return data


def generate_temperature_chart(summary_data, output_image_path="output/avg_temp_chart.png"):
    """
    Renders and saves a bar chart comparing average temperatures per device.
    Includes axis labels, value annotations on bars, and proper layout spacing.
    """
    if not summary_data:
        print("[Warning] No data available to plot.")
        return

    device_ids = [item["device_id"] for item in summary_data]
    avg_temperatures = [item["average_temperature"] for item in summary_data]

    # Plot configuration
    plt.figure(figsize=(8, 5))
    bars = plt.bar(device_ids, avg_temperatures, color="#2b5c8f", width=0.5, edgecolor="#1c3d5a")

    # Add numeric labels on top of each bar for immediate readability
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 1.2,
            f"{height:.2f}°C",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold"
        )

    plt.title("Device Average Temperature Comparison", fontsize=14, pad=15, fontweight="bold")
    plt.xlabel("Device ID", fontsize=11, labelpad=10)
    plt.ylabel("Average Temperature (°C)", fontsize=11, labelpad=10)

    # Adjust y-limit to provide breathing room for labels
    max_temp = max(avg_temperatures) if avg_temperatures else 50
    plt.ylim(0, max_temp + 15)

    # Clean horizontal grid for reference
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.gca().set_axisbelow(True)

    # Ensure labels and margins do not get clipped
    plt.tight_layout()

    # Save output
    output_dir = os.path.dirname(output_image_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    plt.savefig(output_image_path, dpi=300)
    plt.close()
    print(f"[Success] Visualization saved to: {output_image_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate Device Temperature Comparison Bar Chart")
    parser.add_argument(
        "--input", "-i",
        default="output/summary.json",
        help="Path to aggregated JSON file (default: output/summary.json)"
    )
    parser.add_argument(
        "--output", "-o",
        default="output/avg_temp_chart.png",
        help="Path to save chart image (default: output/avg_temp_chart.png)"
    )
    args = parser.parse_args()

    try:
        data = load_summary_data(args.input)
        generate_temperature_chart(data, args.output)
    except Exception as exc:
        print(f"[Error] Failed to generate chart: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
