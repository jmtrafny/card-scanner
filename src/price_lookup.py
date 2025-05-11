# price_lookup.py
import requests
from bs4 import BeautifulSoup
import re
import time
import csv
from pathlib import Path


def fetch_ebay_price(card_name):
    """
    Searches eBay for recently sold listings matching the card name and returns the average
    of the first 3 prices found.

    Args:
        card_name (str): The name of the trading card to search for.

    Returns:
        float or None: The average price, or None if no valid prices found.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    # Encode the search query for use in a URL
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

    # Extract price data from the first 3 sold listings
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


def update_csv_with_prices(csv_path: Path):
    """
    Reads a CSV file containing card data and appends the latest eBay price for each card.
    A new CSV file will be created with the additional column.

    Args:
        csv_path (Path): Path to the original CSV file.

    Returns:
        Path: Path to the new CSV file with price data added.
    """
    output_path = csv_path.with_name(csv_path.stem + "_with_prices.csv")

    with open(csv_path, newline="", encoding="utf-8") as infile, open(output_path, "w", newline="", encoding="utf-8") as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Read and modify header row
        header = next(reader)
        header.append("Last Sold Price (eBay)")
        writer.writerow(header)

        for row in reader:
            card_name = row[0]  # Assumes first column is the OCR name
            if card_name:
                price = fetch_ebay_price(card_name)
                print(f"{card_name} → ${price if price else 'N/A'}")
                row.append(price if price is not None else "N/A")
                writer.writerow(row)
                time.sleep(2)  # Be polite to eBay

    return output_path
