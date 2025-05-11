# csv_logger.py
import csv
from datetime import datetime
from pathlib import Path

def save_card_summary_to_csv(output_dir: Path, card_entries):
    """
    Saves card scanning results to a CSV file.

    Each entry includes:
    - OCR Name: The card name obtained from OCR (optional fallback)
    - Sanitized File Name
    - Quantity
    - File Path
    - Dynamic attributes extracted from bounding boxes

    Args:
        output_dir (Path): Directory where the CSV will be saved.
        card_entries (list of dict): Data for each scanned card.

    Returns:
        str: The name of the saved CSV file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_path = output_dir / f"Scanning-Report-{timestamp}.csv"

    # Collect all attribute keys used in entries
    dynamic_keys = set()
    for entry in card_entries:
        dynamic_keys.update(entry.keys())
    dynamic_keys.difference_update({"ocr_name", "file_name", "quantity", "path"})
    dynamic_keys = sorted(dynamic_keys)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Write header
        header = ["OCR Name", "Sanitized File Name", "Quantity", "File Path"] + dynamic_keys
        writer.writerow(header)

        for entry in card_entries:
            row = [
                entry.get("ocr_name", ""),
                entry.get("file_name", ""),
                entry.get("quantity", 1),
                entry.get("path", "")
            ] + [entry.get(k, "") for k in dynamic_keys]
            writer.writerow(row)

    return csv_path.name
