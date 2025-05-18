# fuzzy_utils.py
from rapidfuzz import fuzz, process
from pathlib import Path

CARD_DB_DIR = Path(__file__).parent / "card_db"

def load_card_list(tcgtag: str) -> list[str]:
    file_map = {
        "Pokemon Name": "pokemon_name.txt",
        "YuGiOh": "yugioh.txt",
        "MTG": "mtg.txt"
    }
    filename = file_map.get(tcgtag)
    if not filename:
        raise ValueError(f"Unknown TCG: {tcgtag}")
    
    path = CARD_DB_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing card list: {path}")
    
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def fuzzy_match_name(name: str, card_list: list[str], threshold: int = 70) -> str:
    if not name or not card_list:
        return ""
    
    match, score, _ = process.extractOne(name, card_list, scorer=fuzz.ratio)
    return match if score >= threshold else ""
