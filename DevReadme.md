# Card Scanner - Developer Guide

This project is a simple OCR-based GUI tool for scanning trading cards (Magic, Pokémon, Yu-Gi-Oh), renaming the scanned files, generating Excel reports, and fetching last-sold eBay prices. This guide explains how to set up your local environment, make changes, build an executable, and push to GitHub.

---

## 🔧 Setup (First Time Only)

### 1. Clone the Repo
```bash
git clone https://github.com/jmtrafny/card-scanner.git
cd card-scanner
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv .venv
```

#### On PowerShell (temporary script bypass):
```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

#### On CMD:
```cmd
.venv\Scripts\activate.bat
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🛠 Making Changes
- Edit code inside the `src/` folder (e.g., `src/main.py`, etc.)
- You can run the app directly:
  ```bash
  python src/main.py
  ```
---
To add new fuzzy matching sources:

1. Place your `.txt` list of names in the following directory:
   ```
   src/card_db/
   ```
   Each file must have one card name per line. Example:
   ```
   Dark Magician
   Blue-Eyes White Dragon
   Red-Eyes B. Dragon
   ```

2. Open `fuzzy_utils.py` and locate the `file_map` in the `load_card_list()` function.

3. Add a new entry using the fuzzy dropdown label as the key and your filename as the value:
   ```python
   file_map = {
       "Pokemon Name": "pokemon.txt",
       "YuGiOh": "yugioh.txt",  # ← Add new entries like this
   }
   ```

This allows the dropdown in the region selector to dynamically associate your fuzzy match type with a specific card list.

Once added, the fuzzy match logic in `main.py` will automatically pick it up and apply corrections during scanning.

Make sure filenames match exactly, and remember that fuzzy match type values in the dropdown must match the keys you use in `file_map`.

---

## 🧪 Local Testing
1. Make changes to the code.
2. Run `python src/main.py` inside your venv to test it.
3. Verify OCR, Excel output, and eBay pricing work as expected.

---

## 🏗 Building the Executable
Make sure your virtual environment is activated:

```bash
pyinstaller --onefile --windowed --name CardScanner src/main.py
```

Output is saved to:
```
dist/CardScanner.exe
```

You can now give this `.exe` to others without needing Python installed.

---

## 📂 Project Structure
```
card-scanner/
├── src/                 # All source files
├── dist/                # Final executable
│   └── CardScanner.exe  # <- Commit this to GitHub
├── build/               # PyInstaller temp files (ignored)
├── .venv/               # Local virtual environment (ignored)
├── requirements.txt     # Dependencies
├── .gitignore
└── README.md
```

---

## 🚀 Pushing to GitHub
```bash
git add .
git commit -m "Update features and rebuild executable"
git push origin main
```

The `.gitignore` is configured to:
- Ignore all build artifacts (`build/`, `.venv/`, `.spec` files)
- Only commit `dist/CardScanner.exe` (final product)

---

## 🧹 Cleaning Up (Optional)
```bash
rmdir /s /q build
rmdir /s /q __pycache__
del *.spec
```

---

## 🤝 Contributions
This tool is maintained by @jmtrafny for personal use, but contributions, suggestions, and brotherly feedback are welcome 😄
