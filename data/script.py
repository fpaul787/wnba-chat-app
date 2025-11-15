import requests
from bs4 import BeautifulSoup
from newspaper import Article
import time
from datetime import datetime
import json

# Websites to scrape
SOURCES = {
    "ESPN": "https://www.espn.com/wnba/",
    "Yahoo": "https://sports.yahoo.com/wnba/",
    "CBS": "https://www.cbssports.com/wnba/",
    "WNBA": "https://www.wnba.com/news/"
}

def get_links(source, url):
    """Scrape WNBA article links from a source page."""
    links = []
    try:
        resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for a in soup.find_all("a", href=True):
            href = a["href"]

            # ESPN links
            if source == "ESPN" and "/story/" in href:
                if not href.startswith("http"):
                    href = "https://www.espn.com" + href
                links.append(href)

            # Yahoo links
            if source == "Yahoo" and href.startswith("https://sports.yahoo.com/article"):
                links.append(href)

            # CBS links
            if source == "CBS" and href.startswith("/wnba"):
                if not href.startswith("http"):
                    href = "https://www.cbssports.com" + href
                links.append(href)

            # WNBA official site links
            if source == "WNBA" and "/news/" in href:
                if not href.startswith("http"):
                    href = "https://www.wnba.com" + href
                links.append(href)

    except Exception as e:
        print(f"[ERROR] Could not scrape {url}: {e}")

    return list(set(links))  # unique links

def extract_article(url, source):
    """Extract full article text with newspaper3k."""
    try:
        article = Article(url)
        article.download()
        article.parse()

        return {
            "source": source,
            "title": article.title,
            "url": url,
            "date": article.publish_date.strftime("%Y-%m-%d") if article.publish_date else str(datetime.now().date()),
            "text": article.text
        }
    except Exception as e:
        print(f"[ERROR] Failed to parse {url}: {e}")
        return None

def scrape_all():
    all_articles = []

    for source, url in SOURCES.items():
        print(f"\n[INFO] Scraping {source}...")
        links = get_links(source, url)
        print(f"  Found {len(links)} article links")

        for link in links[:15]:
            data = extract_article(link, source)
            if data:
                all_articles.append(data)
            time.sleep(5)  # delay

    return all_articles

def scrape_specific_site(source, url):
    wnba_articles = []
    print(f"\n[INFO] Scraping {source}...")

    links = get_links(source, url)
    print(f"  Found {len(links)} article links")

    for link in links[:15]:
        data = extract_article(link, source)
        if data:
            wnba_articles.append(data)
        time.sleep(5)  # delay

    return wnba_articles

if __name__ == "__main__":

    articles = scrape_all()
    print(f"\n[INFO] Scraped {len(articles)} articles.")

    # Save to JSON
    with open("wnba_news.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"\n[INFO] Scraped {len(articles)} articles. Saved to wnba_news.json")

