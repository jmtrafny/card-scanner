# price_lookup.py
import requests
from bs4 import BeautifulSoup
import re
import time
import csv
from pathlib import Path
import tkinter as tk
from tkinter import simpledialog, ttk

def fetch_ebay_price(card_name):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    query = requests.utils.quote(card_name + " trading card")
    url = f"https://www.ebay.com/sch/i.html?_nkw={query}&_sacat=0&LH_Sold=1&LH_Complete=1"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching eBay results for {card_name}: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    prices = []

    for item in soup.select(".s-item"):
        price_tag = item.select_one(".s-item__price")
        if price_tag:
            text = price_tag.get_text()
            match = re.search(r"\$([\d,.]+)", text)
            if match:
                price = float(match.group(1).replace(",", ""))
                prices.append(price)
        if len(prices) >= 3:
            break

    if prices:
        return round(sum(prices) / len(prices), 2)
    return None

def prompt_column_selection(columns):
    selected = None

    def submit():
        nonlocal selected
        selected = combo.get()
        root.destroy()

    root = tk.Tk()
    root.title("Select eBay Search Column")
    tk.Label(root, text="Which column should be used to search for eBay prices?").pack(padx=10, pady=10)
    combo = ttk.Combobox(root, values=columns, state="readonly")
    combo.pack(padx=10, pady=5)
    combo.current(0)
    tk.Button(root, text="OK", command=submit).pack(pady=10)
    root.mainloop()
    return selected

def update_csv_with_prices(csv_path: Path):
    output_path = csv_path.with_name(csv_path.stem + "_with_prices.csv")

    with open(csv_path, newline="", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        header = next(reader)

        column = prompt_column_selection(header)
        if not column or column not in header:
            print("Invalid or no column selected. Aborting price update.")
            return csv_path

        search_index = header.index(column)

        with open(output_path, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.writer(outfile)
            header.append("Last Sold Price (eBay)")
            writer.writerow(header)

            for row in reader:
                search_term = row[search_index]
                if search_term:
                    price = fetch_ebay_price(search_term)
                    print(f"{search_term} → ${price if price else 'N/A'}")
                    row.append(price if price is not None else "N/A")
                else:
                    row.append("N/A")
                writer.writerow(row)
                time.sleep(2)

    return output_path
