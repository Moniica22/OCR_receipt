import json

from ocr import preprocess_image, extract_text
from openai import OpenAI
from secrets import OPENAI_API_KEY  # from your local file. Ignored by .gitignore


def ai_extract(text_content: str, client: OpenAI) -> dict:
    """
    Ask the model to convert the OCR text into a JSON structure
    If the model adds extra text, we slice between the first '{' and the last '}'
    """
    prompt = ("""You are a receipts parser for Spain/Europe. I will provide you extracted text from an image
              of a store receipt. Return only a JSON object matching this schema: {“total”, “business”, 
              “items”: [{“title”, “quantity”, “price”}], “transaction_timestamp”}. 
              `total` and `price` must be integers, and `transaction_timestamp` must be ISO8601
              Here is the OCR text: """ + text_content)

    # We ask the model for the JSON
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    raw = resp.choices[0].message.content.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Slice from first '{' to last '}' and parse that snippet
        start, end = raw.find("{"), raw.rfind("}")
        if start != -1 and end != -1 and end > start:
            snippet = raw[start:end + 1]
            try:
                return json.loads(snippet)
            except json.JSONDecodeError:
                raise ValueError(f'Model returned invalid JSON')


def to_float(x):
    """
    Convert integer cents to float EUR with 2 decimals.
    """
    return round(float(x) / 100.0, 2)


def normalize_prices(data: dict) -> dict:
    """
    Convert 'total' and each 'items[*].price' to floats in EUR.
    If 'total' is missing or invalid, recompute from items as a fallback.
    """
    data['total'] = float(data['total']) / 100.0
    for i in data['items']:
        i['price'] = to_float(i['price'])

    return data


def main():
    """
    Reads OPENAI_API_KEY from the environment, processes the image path in the current directory,
    and saves the parsed JSON
    """
    image_path = "../samples/receipt2.jpg"

    client = OpenAI(api_key=OPENAI_API_KEY)

    preprocessed = preprocess_image(image_path)

    text = extract_text(preprocessed, lang='eng')

    data = ai_extract(text, client)
    data = normalize_prices(data)

    with open('receipt.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
