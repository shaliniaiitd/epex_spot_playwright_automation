"""
Write scraped market data to CSV file.

Args:
    data: List of rows containing market data.
    output_path: File path where CSV will be written.

"""

import csv
from pathlib import Path

HEADERS = ["Hour", "Low", "High", "Last", "Weight Avg"]

def write_csv(data, output_path)-> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)
        writer.writerows(data)
