import json
import os
import feedparser
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

EMBEDDED_KEYWORDS = [
    "embedded", "firmware", "microcontroller", "esp32", "stm32", 
    "arduino", "autosar", "can bus", "rtos", "iot", "hardware", 
    "driver", "pcb", "automotive", "arm cortex", "fpga"
]

def clean_html(raw_html):
    if not raw_html:
        return "No summary available."
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(separator=" ", strip=True)

def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            return json.load(f).get("rss_feeds", [])
    return []

def load_seen_links():
    if os.path.exists("seen_links.json"):
        try:
            with open("seen_links.json", "r") as f:
                content = f.read().strip()
                if not content:
                    return set()
                return set(json.loads(content))
        except json.JSONDecodeError:
            return set()
    return set()

def save_seen_links(seen_links):
    with open("seen_links.json", "w") as f:
        json.dump(list(seen_links), f, indent=4)

def filter_relevant_articles(articles):
    filtered_articles = []
    for article in articles:
        text_to_check = (article["title"] + " " + article["summary"]).lower()
        if any(keyword in text_to_check for keyword in EMBEDDED_KEYWORDS):
            filtered_articles.append(article)
    return filtered_articles

def fetch_feed_articles(url, seen_links):
    feed_articles = []
    new_links = set()
    try:
        feed = feedparser.parse(url)
        source_title = feed.feed.get("title", url)
        
        for entry in feed.entries:
            link = entry.link
            is_new = link not in seen_links

            raw_summary = entry.get("summary", entry.get("description", ""))
            clean_summary = clean_html(raw_summary)
            
            article_data = {
                "title": entry.title,
                "link": link,
                "source": source_title,
                "summary": clean_summary if clean_summary else "No summary available.",
                "is_new": is_new
            }
            feed_articles.append(article_data)
            
            if is_new:
                new_links.add(link)
    except Exception as e:
        print(f"Error fetching feed {url}: {e}")
        
    return feed_articles, new_links

def fetch_all_news():
    feeds = load_config()
    seen_links = load_seen_links()
    all_articles = []
    new_links_found = set()

    # Fetch all RSS feeds concurrently using ThreadPoolExecutor for blazing-fast speed
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(lambda url: fetch_feed_articles(url, seen_links), feeds))
        
    for feed_articles, new_links in results:
        all_articles.extend(feed_articles)
        new_links_found.update(new_links)

    if new_links_found:
        seen_links.update(new_links_found)
        save_seen_links(seen_links)

    final_articles = filter_relevant_articles(all_articles)
    return final_articles