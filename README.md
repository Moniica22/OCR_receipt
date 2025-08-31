# OCR_receipt
Extracts text from receipt images and turn them into JSON. 

## Table of contents
- [Features](#features)
- [Project structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Install & Run](#install--run)
- [License](#license)


## Features
The script will:
- ✅ OpenCV preprocessing (grayscale + Otsu)
- ✅ Tesseract OCR (`eng` by default)
- ✅ Ask the LLM to return integer cents, then convert to floats (EUR).
- ✅ Save the result as receipt.json


## Project structure
OCR_receipt/
├─ .gitignore
├─ requirements.txt
├─ samples/
│  ├─ receipt1.jpg
│  └─ receipt2.jpg
└─ src/
   ├─ parse_receipt.py
   ├─ ocr.py
   └─ secrets.py  

     

## Prerequisites
- Python **3.x**
- Tesseract OCR (Windows)
- OpenCV
- OpenAI Python client (API key)

## Install & Run:
1) Clone the repository:
'git clone <repository-url>
cd <repository-directory>'
2)Install Python deps:
'pip install -r requirements.txt'
3) Add your data in src/secrets.py:
OPENAI_API_KEY = "sk-PASTE_YOUR_KEY_HERE"
PYTESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
-----------------------------------------------------------------------------------------------------
1) Add your testing receipt image in /samples and set it in parse_receipt.py: 'image_path = "samples/receipt1.jpg"'
and LLM model of preference (gpt-4o-mini is used to keep costs low while structuring to JSON):
'model="gpt-4o-mini"'
2) Run from the project root: python .\src\parse_receipt.py
3) The result is saved as receipt.json


## License
This project is licensed under the MIT License.
