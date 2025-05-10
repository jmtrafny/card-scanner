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
