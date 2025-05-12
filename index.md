# CardScanner

CardScanner is a free, open-source OCR tool for scanned Pokémon, Magic: The Gathering, and Yu-Gi-Oh cards. It extracts card names from images and appends real-time pricing data from eBay — no login, no fees, no internet required (except for price lookup).

---

## ✨ Features

- 🔍 **OCR Recognition** — Uses Tesseract to extract text from card images  
- 🏷 **File Renaming** — Automatically names images using the first OCR field  
- 📊 **CSV Report** — Generates structured spreadsheet output with all captured attributes  
- 💵 **eBay Price Lookup** — Fetches real sold prices using:  
  - Median of recent listings  
  - Last sold non-outlier listing  
- 💻 **No Install Required** — Ships as a portable `.exe` (Windows only)  
- 🧾 **MIT Licensed** — Free to use, hack, and share  

---

## 🛠 How It Works

1. Select an **input folder** of scanned card images  
2. Select an **output folder** where renamed files and reports go  
3. Draw OCR capture boxes and label them ("Name", "Set", etc.)  
4. Choose a **price provider** and a **column** to search  
5. Generate pricing-enhanced CSV output in seconds  

---

## 📸 Screenshots

| OCR Setup | Final CSV Output |
|-----------|------------------|
| ![region selector](screenshots/selector.png) | ![csv](screenshots/output_csv.png) |

---

## 📥 Downloads

- Windows Executable: [Releases](https://github.com/jmtrafny/card-scanner/releases)  
- Source Code: [View on GitHub](https://github.com/jmtrafny/card-scanner)  

---

## 💬 Testimonials

> *"This replaced a subscription tool I was paying for."*  
> – Someone, probably  
>
> *"Works better than CollX for bulk sorting."*  
> – My mom said  
>
> *"I finally cleaned up my shoebox of rares."*  
> – Me  

---

## 📄 License

MIT License — see [LICENSE.txt](./LICENSE.txt)  

---

## 🙌 Built For

My brother — and now, the rest of the collecting community.  

Feel free to fork, clone, or contribute. ❤️
