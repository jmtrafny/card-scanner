# Card Scanner - User Guide

This tool helps you quickly organize scanned trading cards (Magic, Pokémon, Yu-Gi-Oh) by reading text using OCR, renaming the images, and saving the results to a CSV file. You can also fetch the latest eBay sale prices for those cards.

- - -

## 🧰 What You Need

* A folder of scanned card images (JPG or PNG)
* A folder where renamed files and reports will go
* No internet needed until you fetch prices

- - -

## 🚀 How to Use It

### 1. **Start the App**

Double-click `CardScanner.exe`. It will open a small window.

### 2. **Pick Your Input and Output Folders**

* Input folder = where your scanned images are
* Output folder = where renamed images and CSV report will go

### 3. **Start the Scan**

Click **"Start Scan"**

* You will see the first image appear
* Click **"+ Add Capture Box"** to add a new attribute
* Use your mouse to draw a bounding box on the image
* Give the box a name (e.g., "Name", "Description", etc.)
* Repeat for as many boxes as you want to extract
* ⚠️ The **first box** is used to name the output files
* Click **OK** when finished

📝 After scanning, your renamed files and CSV sheet will be saved in the output folder

- - -

## 💰 Fetch eBay Prices

### 0. **Clean up the CSV File**

Use the time between scanning and getting prices from eBay to clean up the CSV file. Have at least one column you can search prices against that you have removed bad characters from the OCR reading.

### 1. **Select the CSV File**

Use the “Choose File” button to pick the CSV file you want to look up prices for (most likely one that was just created).

### 2. **Click “Fetch Prices from eBay”**

The tool will:

* Prompt you to choose which column (OCR attribute) to use when searching eBay
* Look up each value in that column on eBay
* Get the most recent sold prices
* Add that price info to a new version of the CSV file

💡 This step may take a few minutes. You’ll see updates in the log window while it works.

- - -

## 🧼 Tips

* Scans work best when the text is clearly visible (good lighting, no glare)
* You can rescan or retry OCR any time—just make a new folder and scan again
* Always check the CSV file afterward to make sure it looks right!
* You can zoom, pan, and scroll in the scan preview window:
    * 🖱 Scroll = vertical scroll
    * ⇧ + Scroll = horizontal scroll
    * ⌃ + Scroll = zoom in/out

- - -

## 🕵️ Trouble?

* If the app seems to hang, give it a moment. It might be working.
* If nothing happens when you click, check that you picked valid folders/files
* When fetching prices, make sure you choose a valid column name from the dropdown

- - -

## 📁 Output Example

After scanning, your output folder will include:

* Renamed image files
* A CSV file like `Scanning-Report-2025-05-11_14-36-44.csv`
* A log file showing OCR output and file renaming info

Good luck! Tell Lucia "Hi!"