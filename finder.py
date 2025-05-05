from indexer import normalize_text

def ranked_find(index, query_words, page_texts):
    word_to_pages = [set(index.get(word, {}).keys()) for word in query_words]
    all_candidate_pages = set.union(*word_to_pages)

    exact_matches = []
    all_word_matches = []
    partial_matches = []

    for page in all_candidate_pages:
        words_found = [word for word in query_words if page in index.get(word, {})]
        match_count = len(words_found)

        # Normalize full text for matching
        full_text = " ".join(normalize_text(page_texts[page]))
        phrase = " ".join(query_words)

        if phrase in full_text:
            exact_matches.append(page)
        elif match_count == len(query_words):
            all_word_matches.append(page)
        elif match_count > 0:
            partial_matches.append((page, match_count))

    partial_matches.sort(key=lambda x: -x[1])
    partial_matches = [page for page, _ in partial_matches]

    return exact_matches, all_word_matches, partial_matches

def get_total_occurrences(index, words, url):
    return sum(index.get(word, {}).get(url, 0) for word in words)

def get_page_word_counts(index, words, url):
    counts = []
    for word in words:
        count = index.get(word, {}).get(url, 0)
        if count > 0:
            counts.append(f"{word}: {count}")
    return ", ".join(counts)