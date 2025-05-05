import json

INDEX_FILE = "inverted_index.json"
PAGES_FILE = "pages_text.json"

def save_index_and_pages(index, pages):
    with open(INDEX_FILE, 'w', encoding="utf-8") as f:
        json.dump(index, f, indent=2)
    with open(PAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(pages, f, indent=2)

def load_index_and_pages():
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f1:
            index = json.load(f1)
        with open(PAGES_FILE, "r", encoding="utf-8") as f2:
            pages = json.load(f2)
        return index, pages
    except FileNotFoundError:
        print("⚠️  Index or pages file not found.")
        return None, None