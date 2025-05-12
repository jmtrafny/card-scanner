# ebay_provider.py
import requests
import re
from bs4 import BeautifulSoup
from statistics import median, StatisticsError, mean
from price_providers import PriceProvider

COMMON_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_ebay_prices(card_name, max_items=10):
    query = requests.utils.quote(card_name + " trading card")
    url = f"https://www.ebay.com/sch/i.html?_nkw={query}&_sacat=0&LH_Sold=1&LH_Complete=1"
    print(f"Fetching eBay prices for: {card_name}")
    print(f"Search URL: {url}")

    prices = []

    try:
        response = requests.get(url, headers=COMMON_HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching eBay results: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    for item in soup.select(".s-item"):
        if "AdChoice" in item.get_text():
            continue

        title_tag = item.select_one(".s-item__title")
        if not title_tag:
            continue
        title = title_tag.get_text().lower()
        if "lot" in title or "bundle" in title or "x" in title:
            continue

        price_tag = item.select_one(".s-item__price")
        if not price_tag:
            continue

        if item.select_one(".STRIKETHROUGH"):
            continue  # skip discounted pricing blocks

        match = re.search(r"\$([\d,.]+)", price_tag.get_text())
        if match:
            try:
                price = float(match.group(1).replace(",", ""))
                if price > 0:
                    prices.append(price)
            except ValueError:
                continue

        if len(prices) >= max_items:
            break

    print(f"Collected prices: {prices}")
    return prices


class EbayMedianProvider(PriceProvider):
    def name(self):
        return "eBay (Median Price)"

    def fetch_price(self, card_name: str) -> float:
        prices = fetch_ebay_prices(card_name)
        try:
            return round(median(prices), 2)
        except StatisticsError:
            return None


class EbayLastSoldProvider(PriceProvider):
    def name(self):
        return "eBay (Last Sold Price)"

    def fetch_price(self, card_name: str) -> float:
        prices = fetch_ebay_prices(card_name, max_items=10)
        if not prices:
            return None

        avg = mean(prices)
        filtered = [p for p in prices if p < avg * 1.5]
        return round(filtered[0], 2) if filtered else round(prices[0], 2)
