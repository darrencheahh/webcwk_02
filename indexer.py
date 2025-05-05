import re
from collections import defaultdict

def normalize_text(text):
    text = text.replace("-", " ")
    text = re.sub(r"[^\w\s]", "", text)
    return text.lower().split()

def build_inverted_index(pages_dict):
    index = defaultdict(lambda: defaultdict(int))

    for url, text in pages_dict.items():
        words = normalize_text(text)
        for word in words:
            index[word][url] += 1

    return dict(index)

