from crawler import crawl_website
from indexer import build_inverted_index, normalize_text
from storage import save_index_and_pages, load_index_and_pages
from finder import ranked_find, get_total_occurrences, get_page_word_counts

def main():
    index = None
    pages = None

    while True:
        command = input("\nEnter command (build / load /  print <word> / find <word(s)> /quit): ").strip().lower()

        if command == "build":
            pages = crawl_website()
            index = build_inverted_index(pages)
            save_index_and_pages(index, pages)
            print("Index and pages built and saved to file.")

        elif command == "load":
            temp_index, temp_pages = load_index_and_pages()
            if temp_index is not None and temp_pages is not None:
                index = temp_index
                pages = temp_pages
                print("Index loaded successfully.")
            else:
                print("Failed to load index.")

        elif command.startswith("print "):
            if not index:
                print("Please load or build the index first.")
                continue

            word = command[6:].strip()
            if word in index:
                print(f"\n'{word}' found in:")
                for page, count in index[word].items():
                    print(f"  - {page}: {count} time(s)")
            else:
                print(f"'{word}' not found in index.")

        elif command.startswith("find "):
            if index is None or pages is None:
                print("Please load or build first.")
                continue

            query_words = command[5:].strip().lower().split()
            if not query_words:
                print("No words provided for search.")
                continue

            exact, all_match, partial = ranked_find(index, query_words, pages)

            if exact:
                print("\nPages that contain all words and in same order:")
                exact_sorted = sorted(exact, key=lambda url: -get_total_occurrences(index, query_words, url))
                for page in exact_sorted:
                    counts = get_page_word_counts(index, query_words, page)
                    print(f"  - {page} [{counts}]")

            if all_match:
                print("Pages that contain all words:")
                all_sorted = sorted(all_match, key=lambda url: -get_total_occurrences(index, query_words, url))
                for page in all_sorted:
                    counts = get_page_word_counts(index, query_words, page)
                    print(f"  - {page} [{counts}]")

            if partial:
                print("Pages that contain less than all words")
                partial_sorted = sorted(partial, key=lambda url: -get_total_occurrences(index, query_words, url))
                for page in partial_sorted:
                    counts = get_page_word_counts(index, query_words, page)
                    print(f"  - {page} [{counts}]")

            if not (exact or all_match or partial):
                print("No matches found.")

        elif command == "quit":
            break
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()

