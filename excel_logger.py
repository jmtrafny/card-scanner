# excel_logger.py
from openpyxl import Workbook
from datetime import datetime

def save_card_summary_to_excel(output_dir, card_entries):
    """
    card_entries should be a list of dictionaries with keys:
    - ocr_name: The original OCR result (raw)
    - file_name: The sanitized file name used
    - quantity: How many times this card appeared (optional; default=1)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    excel_path = output_dir / f"scan_summary_{timestamp}_ul0stehg4m3.xlsx"

    wb = Workbook()
    ws = wb.active
    ws.title = "Card Summary"

    # Write headers
    ws.append(["OCR Name", "Sanitized File Name", "Quantity", "Price (TBD)"])

    for entry in card_entries:
        if isinstance(entry, dict):
            ws.append([
                entry.get("ocr_name", ""),
                entry.get("file_name", ""),
                entry.get("quantity", 1),
                ""
            ])

    wb.save(excel_path)
    return excel_path.name
