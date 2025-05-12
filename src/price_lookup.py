# price_lookup.py
import csv
import time
from pathlib import Path

def update_csv_with_prices(csv_path: Path, provider, column):
    output_path = csv_path.with_name(csv_path.stem + "_with_prices.csv")

    with open(csv_path, newline="", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        header = next(reader)

        if column not in header:
            print("Selected column not found in CSV header. Aborting price update.")
            return csv_path

        search_index = header.index(column)

        with open(output_path, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.writer(outfile)
            header.append(f"Price ({provider.name()})")
            writer.writerow(header)

            for row in reader:
                search_term = row[search_index]
                if search_term:
                    price = provider.fetch_price(search_term)
                    print(f"{search_term} → ${price if price is not None else 'N/A'}")
                    row.append(price if price is not None else "N/A")
                else:
                    row.append("N/A")
                writer.writerow(row)
                time.sleep(2)

    return output_path

def prompt_column_selection(columns):
    import tkinter as tk
    from tkinter import ttk

    selected = None

    def submit():
        nonlocal selected
        selected = combo.get()
        root.quit()
        root.destroy()

    root = tk.Tk()
    root.title("Select Column for Price Lookup")
    tk.Label(root, text="Which column should be used to search for prices?").pack(padx=10, pady=10)

    combo = ttk.Combobox(root, values=columns, state="readonly")
    combo.pack(padx=10, pady=5)
    combo.current(0)

    tk.Button(root, text="OK", command=submit).pack(pady=10)
    root.mainloop()

    return selected
