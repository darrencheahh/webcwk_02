import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://quotes.toscrape.com"

def get_soup(url):
    print(f"Crawling: {url}")
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

def crawl_website():
    visited = set()
    to_visit = ["/"]
    all_pages_text = {}

    while to_visit:
        relative_url = to_visit.pop(0)
        full_url = urljoin(BASE_URL, relative_url)

        if full_url in visited:
            continue

        visited.add(full_url)
        soup = get_soup(full_url)
        time.sleep(6) # politeness period

        quotes = soup.find_all("div", class_="quote")
        if quotes:
            text = " ".join(q.get_text(separator=" ") for q in quotes)
            all_pages_text[full_url] = text.strip()

            # Add "Next" page in pagination
            next_btn = soup.select_one("li.next > a")
            if next_btn:
                next_href = next_btn["href"]
                to_visit.append(urljoin(relative_url, next_href))

            # Add author links
            author_links = soup.select("small.author ~ a[href]")
            for link in author_links:
                href = link.get("href")
                if href.startswith("/author/"):
                    to_visit.append(href)

            # Add tag links (in tag cloud or quote tags)
            tag_links = soup.select("a.tag[href]")
            for link in tag_links:
                href = link.get("href")
                to_visit.append(href)

        # For author/tag pages (no quotes), just get text content
        else:
            page_text = soup.get_text(separator=" ", strip=True)
            all_pages_text[full_url] = page_text

    return all_pages_text

