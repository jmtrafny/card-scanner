# main.py (full un-truncated version)
import sys
import io
import csv
import threading
import shutil
from pathlib import Path
from datetime import datetime
from PIL import Image
import pytesseract

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from tkinter import filedialog, messagebox

from ocr_utils import sanitize_card_name
from region_selector import RegionSelector
from session_logger import start_log
from csv_logger import save_card_summary_to_csv
from price_lookup import update_csv_with_prices
from config_utils import load_config, save_config
from ebay_provider import EbayMedianProvider, EbayLastSoldProvider


class CardScannerApp:
    def __init__(self, root):
        config = load_config()
        self.input_path = ttk.StringVar(value=config.get("input_path", ""))
        self.output_path = ttk.StringVar(value=config.get("output_path", ""))
        self.excel_path = ttk.StringVar()
        self.provider_name = ttk.StringVar()
        self.column_name = ttk.StringVar()

        self.providers = {
            EbayMedianProvider().name(): EbayMedianProvider(),
            EbayLastSoldProvider().name(): EbayLastSoldProvider()
        }
        default_provider = config.get("price_provider", list(self.providers.keys())[0])
        self.provider_name.set(default_provider if default_provider in self.providers else list(self.providers.keys())[0])

        self.root = root
        self.root.title("Trading Card Scanner")
        self.setup_gui()
        self.redirect_stdout()

    def setup_gui(self):
        padding = {"padx": 5, "pady": 5}

        ttk.Label(self.root, text="Input Folder:").grid(row=0, column=0, sticky="e", **padding)
        ttk.Entry(self.root, textvariable=self.input_path, width=40).grid(row=0, column=1, **padding)
        ttk.Button(self.root, text="Browse", command=self.select_input_folder, bootstyle=PRIMARY).grid(row=0, column=2, **padding)

        ttk.Label(self.root, text="Output Folder:").grid(row=1, column=0, sticky="e", **padding)
        ttk.Entry(self.root, textvariable=self.output_path, width=40).grid(row=1, column=1, **padding)
        ttk.Button(self.root, text="Browse", command=self.select_output_folder, bootstyle=PRIMARY).grid(row=1, column=2, **padding)

        self.scan_button = ttk.Button(self.root, text="Start Scan", command=self.start_scan, bootstyle=SUCCESS)
        self.scan_button.grid(row=2, column=1, pady=10)
        self.spinner = ttk.Progressbar(self.root, mode='indeterminate', bootstyle="info-striped")
        self.spinner.grid(row=2, column=2, pady=10)
        self.spinner.grid_remove()

        ttk.Label(self.root, text="CSV File for Price Lookup:").grid(row=3, column=0, sticky="e", **padding)
        ttk.Entry(self.root, textvariable=self.excel_path, width=40).grid(row=3, column=1, **padding)
        ttk.Button(self.root, text="Choose File", command=self.select_excel_file, bootstyle=PRIMARY).grid(row=3, column=2, **padding)

        ttk.Label(self.root, text="Price Provider:").grid(row=4, column=0, sticky="e", **padding)
        self.provider_dropdown = ttk.Combobox(self.root, textvariable=self.provider_name, values=list(self.providers.keys()), state="readonly")
        self.provider_dropdown.grid(row=4, column=1, sticky="w", **padding)
        self.provider_dropdown.bind("<<ComboboxSelected>>", lambda e: self.save_current_config())

        ttk.Label(self.root, text="Search Column:").grid(row=5, column=0, sticky="e", **padding)
        self.column_dropdown = ttk.Combobox(self.root, textvariable=self.column_name, state="readonly")
        self.column_dropdown.grid(row=5, column=1, sticky="w", **padding)

        self.price_button = ttk.Button(self.root, text="Get Price Data", command=self.fetch_prices, bootstyle=INFO)
        self.price_button.grid(row=5, column=2, pady=10)
        self.price_spinner = ttk.Progressbar(self.root, mode='indeterminate', bootstyle="info-striped")
        self.price_spinner.grid(row=5, column=3, pady=10)
        self.price_spinner.grid_remove()

        self.output_text = ttk.Text(self.root, height=10, width=70, state='disabled')
        self.output_text.grid(row=6, column=0, columnspan=4, padx=10, pady=(0, 10))

    def redirect_stdout(self):
        class StdoutRedirector(io.StringIO):
            def write(inner_self, msg):
                self.output_text.configure(state='normal')
                self.output_text.insert("end", msg)
                self.output_text.see("end")
                self.output_text.configure(state='disabled')

        sys.stdout = StdoutRedirector()
        sys.stderr = sys.stdout

    def select_input_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_path.set(folder)
            self.save_current_config()

    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path.set(folder)
            self.save_current_config()

    def save_current_config(self):
        save_config({
            "input_path": self.input_path.get(),
            "output_path": self.output_path.get(),
            "price_provider": self.provider_name.get()
        })

    def select_excel_file(self):
        file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file:
            self.excel_path.set(file)
            self.update_column_dropdown(Path(file))

    def update_column_dropdown(self, csv_path):
        try:
            with open(csv_path, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                header = next(reader)
                self.column_dropdown.config(values=header)
                if header:
                    self.column_name.set(header[0])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load column names: {e}")

    def start_scan(self):
        self.clear_output()
        self.scan_button.config(text="Scanning...", state="disabled")
        self.spinner.grid()
        self.spinner.start(10)

        def run_scan():
            try:
                self.perform_scan()
            finally:
                self.root.after(0, self.reset_scan_button)

        threading.Thread(target=run_scan, daemon=True).start()

    def reset_scan_button(self):
        self.spinner.stop()
        self.spinner.grid_remove()
        self.scan_button.config(text="Start Scan", state="normal")

    def perform_scan(self):
        in_dir = Path(self.input_path.get())
        out_dir = Path(self.output_path.get())

        if not in_dir.exists() or not out_dir:
            messagebox.showerror("Error", "Please select valid directories.")
            return

        images_dir = out_dir / "images"
        images_dir.mkdir(parents=True, exist_ok=True)

        images = list(in_dir.glob("*.jpg")) + list(in_dir.glob("*.png"))

        if not images:
            messagebox.showinfo("No Images", "No images found in the input folder.")
            return

        selector = RegionSelector(images)
        capture_data = selector.get_capture_data()
        if not capture_data:
            messagebox.showerror("Error", "No regions selected.")
            return

        log_file = start_log(out_dir)
        log_file.write(f"Scan started at {datetime.now()}\n")
        for name, coords in capture_data:
            log_file.write(f"Capture: {name} = {coords}\n")
        log_file.write("\n")

        card_entries = []

        for idx, img_path in enumerate(images, start=1):
            log_file.write(f"[{img_path.name}] ")
            img = Image.open(img_path)
            entry = {"input_path": str(img_path)}

            for name, coords in capture_data:
                cropped = img.crop(coords).convert("L")
                text = pytesseract.image_to_string(cropped, config="--psm 7").strip()
                entry[name] = text

            primary_field = capture_data[0][0]
            card_name = entry.get(primary_field, "").strip()
            safe_name = sanitize_card_name(card_name)

            if not safe_name or safe_name.lower() == "unknowncard":
                safe_name = f"SCAN_{idx}"

            new_path = images_dir / f"{safe_name}{img_path.suffix.lower()}"
            i = 1
            base_name = safe_name
            while new_path.exists():
                safe_name = f"{base_name}_{i}"
                new_path = images_dir / f"{safe_name}{img_path.suffix.lower()}"
                i += 1

            shutil.copy(img_path, new_path)
            entry["output_path"] = str(new_path)
            log_file.write(f"→ OCR → Saved as: {new_path.name}\n")
            card_entries.append(entry)

        log_file.write(f"\nScan complete. {len(images)} images processed.\n")
        log_file.write(f"{len(card_entries)} entries recorded.\n")
        log_file.close()

        csv_filename = save_card_summary_to_csv(out_dir, card_entries)
        self.excel_path.set(str(out_dir / csv_filename))

        messagebox.showinfo("Scan Complete", f"Processed {len(images)} cards.\n"
                                             f"Summary saved to {csv_filename}")

    def fetch_prices(self):
        self.clear_output()
        csv_file = self.excel_path.get()
        provider = self.providers.get(self.provider_name.get())
        column = self.column_name.get()

        if not csv_file:
            messagebox.showerror("Error", "Please select a CSV file first.")
            return
        if not provider:
            messagebox.showerror("Error", "Invalid price provider selected.")
            return
        if not column:
            messagebox.showerror("Error", "Please select a search column.")
            return

        self.price_button.config(text="Fetching...", state="disabled")
        self.price_spinner.grid()
        self.price_spinner.start(10)

        def run_fetch():
            try:
                updated_path = update_csv_with_prices(Path(csv_file), provider, column)
                self.root.after(0, lambda: messagebox.showinfo("Success", f"Prices updated in file:\n{updated_path}"))
            finally:
                self.root.after(0, self.reset_price_button)

        threading.Thread(target=run_fetch, daemon=True).start()

    def reset_price_button(self):
        self.price_spinner.stop()
        self.price_spinner.grid_remove()
        self.price_button.config(text="Get Price Data", state="normal")

    def clear_output(self):
        self.output_text.configure(state='normal')
        self.output_text.delete("1.0", "end")
        self.output_text.configure(state='disabled')


if __name__ == "__main__":
    app = ttk.Window(themename="superhero", title="Card Scanner")
    CardScannerApp(app)
    app.mainloop()