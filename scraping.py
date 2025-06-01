# Installment necessary libraries
!pip install requests beautifulsoup4

# Import libraries
import os
import requests
from bs4 import BeautifulSoup
import random
import re

# Created a directory to save articles
save_directory = "/content/articles"
os.makedirs(save_directory, exist_ok=True)

# Defined source pages for Politics, Business, Sports
topic_urls = [
    # CNN
    "https://edition.cnn.com/politics",
    "https://edition.cnn.com/business",
    "https://edition.cnn.com/sport",
    # BBC
    "https://www.bbc.com/news/politics",
    "https://www.bbc.com/news/business",
    "https://www.bbc.com/sport",
    # Sky News
    "https://news.sky.com/politics",
    "https://news.sky.com/business",
    "https://news.sky.com/sport"
]

# Function to fetch article links from a topic page
def get_links(section_url):
    try:
        page = requests.get(section_url, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")
        links = set()

        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('http'):
                links.add(href)
            elif href.startswith('/'):
                base = section_url.split('/')[0] + '//' + section_url.split('/')[2]
                links.add(base + href)
        return list(links)
    except Exception as e:
        print(f"Error getting links from {section_url}: {e}")
        return []

# Function to scrape text content from an article link
def scrape_article(url):
    try:
        page = requests.get(url, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")

        # Extracted paragraphs
        paragraphs = soup.find_all('p')
        article_text = ' '.join(p.get_text() for p in paragraphs)

        # Clean up text
        article_text = re.sub(r'\s+', ' ', article_text)
        return article_text.strip()
    except Exception as e:
        print(f"Error scraping article: {url}: {e}")
        return ""

# Main function to collect and save articles
def collect_articles(target_count=100):
    collected = 0
    all_links = []

    # Collected all links from topic pages
    for url in topic_urls:
        links = get_links(url)
        print(f"Found {len(links)} links from {url}")
        all_links.extend(links)

    random.shuffle(all_links)  # Shuffled for randomness

    for link in all_links:
        if collected >= target_count:
            break
        text = scrape_article(link)
        word_count = len(text.split())

        if word_count >= 50:
            filename = os.path.join(save_directory, f"article_{collected+1}.txt")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Saved article_{collected+1}.txt ({word_count} words)")
            collected += 1
        else:
            print(f"Skipped (too short: {word_count} words): {link}")

    print(f"\n✅ Finished collecting {collected} articles.")

# Runned the collection
collect_articles(target_count=100)
