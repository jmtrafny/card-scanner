# Card Scanner - User Guide

This tool helps you quickly organize scanned trading cards (Magic, Pokémon, Yu-Gi-Oh) by reading text using OCR, renaming the images, and saving the results to a CSV file. You can also fetch the latest eBay sale prices for those cards.

---

## 🧰 What You Need

- A folder of scanned card images (JPG or PNG)
- A folder where renamed files and reports will go
- No internet needed until you fetch prices
- Tesseract OCR must be installed separately

---

## ⚙️ Prerequisite: Install Tesseract OCR

CardScanner uses [Tesseract OCR](https://github.com/tesseract-ocr/tesseract), which must be installed separately.

### 🪿 Windows Installation

1. Download the official installer from [GitHub Releases](https://github.com/UB-Mannheim/tesseract/wiki)
   - Recommended: **tesseract-ocr-w64-setup.exe** from the [UB Mannheim build](https://github.com/UB-Mannheim/tesseract/wiki)

2. Run the installer and **make sure you check the option** to:
   > ✅ *Add Tesseract to the system PATH*

3. After installation, open Command Prompt and test:
   ```cmd
   tesseract --version
   ```

   If it prints the version, you're good to go!

### 🧪 If It's Not Detected...

If Tesseract isn't working, you likely need to manually add it to your system PATH:

1. Open **System Properties → Advanced → Environment Variables**
2. Under **System variables**, find and edit the `Path` variable
3. Add the path to your Tesseract installation, usually:
   ```
   C:\Program Files\Tesseract-OCR
   ```
4. Restart your computer or log out/log in again


## 🚀 How to Use It

### 1. **Start the App**

Double-click `CardScanner.exe`. It will open a small window.

### 2. **Pick Your Input and Output Folders**

- Input folder = where your scanned images are
- Output folder = where renamed images and CSV report will go

### 3. **Start the Scan**

Click **"Start Scan"**

- You will see the first image appear
- Click **"+ Add Capture Box"** to add a new attribute
- Use your mouse to draw a bounding box on the image
- Give the box a name (e.g., "Name", "Description", etc.)
- Repeat for as many boxes as you want to extract
- ⚠️ The **first box** is used to name the output files
- Click **OK** when finished

📃 After scanning, your renamed files and CSV sheet will be saved in the output folder

---

## 💰 Get Price Data

### 1. **Select the CSV File**

Use the “Choose File” button to pick the CSV file you want to look up prices for (most likely one that was just created).

### 2. **Choose a Price Provider**

Use the dropdown to select your pricing strategy:
- **eBay (Median Price)** — calculates the median of recent sold listings
- **eBay (Last Sold Price)** — uses the most recent valid price

### 3. **Choose a Search Column**

Select which OCR attribute (column) from your CSV to use as the card name when searching.

### 4. **Click "Get Price Data"**

The tool will:
- Use your selected column to perform a search for each row
- Fetch and append prices to a new CSV file
- Show updates in the log window while it runs

---

## 🪨 Troubleshooting

- If the app crashes when scanning prices, make sure you selected a valid column and CSV file
- If all prices show `$20`, switch from **Last Sold** to **Median**
- If no dropdown appears for columns, re-select the CSV file

---

## 📄 Output Example

After scanning, your output folder will include:

- Renamed image files
- A CSV file like `Scanning-Report-2025-05-11_14-36-44.csv`
- A log file showing OCR output and file renaming info
- An updated CSV like `Scanning-Report-..._with_prices.csv`

---

## 📊 Tips

- Scans work best when the text is clearly visible (good lighting, no glare)
- You can rescan or retry OCR any time—just make a new folder and scan again
- Always check the CSV file afterward to make sure it looks right!
- You can zoom, pan, and scroll in the scan preview window:
    - Scroll = vertical scroll
    - Shift + Scroll = horizontal scroll
    - Ctrl  + Scroll = zoom in/out

---

## 🧡 Credits

Made with love for organizing trading card collections, and just as much love for building cool tools for my brother.
