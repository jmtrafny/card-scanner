# csv_logger.py
import csv
from datetime import datetime
from pathlib import Path


def save_card_summary_to_csv(output_dir: Path, card_entries):
    """
    Saves card scanning results to a CSV file. Each entry includes:

    - OCR Name: The card name obtained from OCR
    - Sanitized File Name: A file-safe version of the OCR name
    - Quantity: How many times this card was found
    - File Path: Location where the renamed image was saved

    Args:
        output_dir (Path): Directory where the CSV will be saved.
        card_entries (list of dict): Data for each scanned card.

    Returns:
        str: The name of the saved CSV file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_path = output_dir / f"Scanning-Report-{timestamp}.csv"

    # Open the CSV file for writing
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Write the header row
        writer.writerow(["OCR Name", "Sanitized File Name", "Quantity", "File Path"])

        # Write each card entry as a row
        for entry in card_entries:
            writer.writerow([
                entry.get("ocr_name", ""),
                entry.get("file_name", ""),
                entry.get("quantity", 1),
                entry.get("path", "")
            ])

    return csv_path.name
