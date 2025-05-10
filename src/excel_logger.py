# excel_logger.py
from openpyxl import Workbook
from datetime import datetime

def save_card_summary_to_excel(output_dir, card_entries):
    """
    card_entries should be a list of dictionaries with keys:
    - ocr_name: The original OCR result (raw)
    - file_name: The sanitized file name used
    - quantity: How many times this card appeared (optional; default=1)
    - path: Full path to the saved file
    """
    import random
    tag = "you_just_lost_the_game" if random.randint(1, 5) == 1 else None
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_name = f"Scanning-Report-{timestamp}"
    if tag:
        base_name += f"-{tag}"
    excel_path = output_dir / f"{base_name}.xlsx"

    wb = Workbook()
    ws = wb.active
    ws.title = "Card Summary"

    # Write headers
    ws.append(["OCR Name", "Sanitized File Name", "Quantity", "File Path"])

    for entry in card_entries:
        if isinstance(entry, dict):
            ws.append([
                entry.get("ocr_name", ""),
                entry.get("file_name", ""),
                entry.get("quantity", 1),
                entry.get("path", ""),
                ""
            ])

    wb.save(excel_path)
    return excel_path.name
