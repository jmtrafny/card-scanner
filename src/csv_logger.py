# csv_logger.py
import csv
from datetime import datetime
from pathlib import Path

def save_card_summary_to_csv(output_dir: Path, card_entries):
    """
    Saves card scanning results to a CSV file.

    Each entry includes:
    - Input File Path
    - Output File Path
    - Dynamic attributes extracted from bounding boxes

    Args:
        output_dir (Path): Directory where the CSV will be saved.
        card_entries (list of dict): Data for each scanned card.

    Returns:
        str: The name of the saved CSV file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_path = output_dir / f"Scanning-Report-{timestamp}.csv"

    # Determine dynamic attribute keys from bounding boxes
    if not card_entries:
        return None

    fixed_keys = {"input_path", "output_path"}
    dynamic_keys = sorted(set().union(*(entry.keys() for entry in card_entries)) - fixed_keys)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Write header
        header = ["Input File Path", "Output File Path"] + dynamic_keys
        writer.writerow(header)

        for entry in card_entries:
            row = [
                entry.get("input_path", ""),
                entry.get("output_path", "")
            ] + [entry.get(k, "") for k in dynamic_keys]
            writer.writerow(row)

    return csv_path.name
