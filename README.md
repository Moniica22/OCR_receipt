Project pipeline:

1) Preprocess image (grayscale + Otsu)
2) OCR with Tesseract (English by default)
3) Ask an LLM to return a clean JSON
4) Parse output and save to 'receipt.json'