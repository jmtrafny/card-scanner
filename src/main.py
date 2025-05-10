# main.py
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from datetime import datetime
from ocr_utils import extract_card_name, sanitize_card_name
from region_selector import RegionSelector
from session_logger import start_log
from excel_logger import save_card_summary_to_excel
from price_lookup import update_excel_with_prices
import sys
import io
import threading

class CardScannerApp:
    def __init__(self, root):
        self.input_path = tk.StringVar(value=r"C:\Users\jmtra\OneDrive\Desktop\input")
        self.output_path = tk.StringVar(value=r"C:\Users\jmtra\OneDrive\Desktop\output")
        self.excel_path = tk.StringVar()

        self.root = root
        self.root.title("Trading Card Scanner")

        self.setup_gui()
        self.redirect_stdout()

    def setup_gui(self):
        tk.Label(self.root, text="Input Folder:").grid(row=0, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.input_path, width=40).grid(row=0, column=1)
        tk.Button(self.root, text="Browse", command=self.select_input_folder).grid(row=0, column=2)

        tk.Label(self.root, text="Output Folder:").grid(row=1, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.output_path, width=40).grid(row=1, column=1)
        tk.Button(self.root, text="Browse", command=self.select_output_folder).grid(row=1, column=2)

        tk.Button(self.root, text="Start Scan", command=self.start_scan).grid(row=2, column=1, pady=10)

        tk.Label(self.root, text="Excel File for Price Lookup:").grid(row=3, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.excel_path, width=40).grid(row=3, column=1)
        tk.Button(self.root, text="Choose File", command=self.select_excel_file).grid(row=3, column=2)

        tk.Button(self.root, text="Fetch Prices from eBay", command=self.fetch_prices).grid(row=4, column=1, pady=10)

        self.output_text = tk.Text(self.root, height=10, width=70, state='disabled', bg='#f0f0f0')
        self.output_text.grid(row=5, column=0, columnspan=3, padx=10, pady=(0, 10))

    def redirect_stdout(self):
        class StdoutRedirector(io.StringIO):
            def write(inner_self, msg):
                self.output_text.configure(state='normal')
                self.output_text.insert(tk.END, msg)
                self.output_text.see(tk.END)
                self.output_text.configure(state='disabled')

        sys.stdout = StdoutRedirector()
        sys.stderr = sys.stdout

    def select_input_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_path.set(folder)

    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path.set(folder)

    def select_excel_file(self):
        file = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file:
            self.excel_path.set(file)

    def start_scan(self):
        self.clear_output()
        in_dir = Path(self.input_path.get())
        out_dir = Path(self.output_path.get())

        if not in_dir.exists() or not out_dir:
            messagebox.showerror("Error", "Please select valid directories.")
            return

        out_dir.mkdir(parents=True, exist_ok=True)
        images = list(in_dir.glob("*.jpg")) + list(in_dir.glob("*.png"))

        if not images:
            messagebox.showinfo("No Images", "No images found in the input folder.")
            return

        selector = RegionSelector(images)
        if not selector.coords:
            messagebox.showerror("Error", "No region selected.")
            return

        coords = selector.coords
        logs_dir = out_dir / "logs"
        logs_dir.mkdir(exist_ok=True)
        log_file = start_log(out_dir)
        log_file.write(f"Scan started at {datetime.now()}\n")
        log_file.write(f"OCR region: {coords}\n\n")

        card_counts = {}
        card_entries = []

        for img_path in images:
            log_file.write(f"[{img_path.name}] ")
            card_name = extract_card_name(img_path, coords)
            if card_name:
                card_name = card_name.strip()
                safe_name = sanitize_card_name(card_name)

                new_path = out_dir / f"{safe_name}{img_path.suffix.lower()}"
                i = 1
                base_name = safe_name
                while new_path.exists():
                    safe_name = f"{base_name}_{i}"
                    new_path = out_dir / f"{safe_name}{img_path.suffix.lower()}"
                    i += 1

                img_path.rename(new_path)
                card_counts[base_name] = card_counts.get(base_name, 0) + 1
                card_entries.append({
                    "ocr_name": card_name,
                    "file_name": safe_name,
                    "quantity": 1
                })
                log_file.write(f"→ OCR: '{card_name}' → Saved as: {new_path.name}\n")
            else:
                log_file.write("→ OCR FAILED\n")

        log_file.write(f"\nScan complete. {len(images)} images processed.\n")
        log_file.write(f"{len(card_counts)} unique cards identified.\n")
        log_file.close()

        excel_filename = save_card_summary_to_excel(out_dir, card_entries)
        self.excel_path.set(str(out_dir / excel_filename))

        messagebox.showinfo("Scan Complete", f"Processed {len(images)} cards.\n"
                                             f"Found {len(card_counts)} unique cards.\n"
                                             f"Summary saved to {excel_filename}")

    def fetch_prices(self):
        self.clear_output()
        excel_file = self.excel_path.get()
        if not excel_file:
            messagebox.showerror("Error", "Please select an Excel file first.")
            return

        def run_fetch():
            updated_path = update_excel_with_prices(Path(excel_file))
            messagebox.showinfo("Success", f"Prices updated in file:\n{updated_path}")

        threading.Thread(target=run_fetch, daemon=True).start()

    def clear_output(self):
        self.output_text.configure(state='normal')
        self.output_text.delete("1.0", tk.END)
        self.output_text.configure(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    app = CardScannerApp(root)
    root.mainloop()
