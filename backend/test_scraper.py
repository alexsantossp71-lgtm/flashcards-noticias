# Test Article Scraper
# Usage: python test_scraper.py <URL>

import sys
import requests

if len(sys.argv) < 2:
    print("Usage: python test_scraper.py <URL>")
    sys.exit(1)

url = sys.argv[1]

from services.scraper_service import article_scraper

print(f"\n=== Testing Article Scraper ===")
print(f"URL: {url}\n")

article_data = article_scraper.scrape_article(url)

if article_data:
    print(f"✅ SUCCESS!\n")
    print(f"Title: {article_data.get('title', 'N/A')}")
    print(f"Author: {article_data.get('author', 'N/A')}")
    print(f"Date: {article_data.get('publish_date', 'N/A')}")
    print(f"\nContent Length: {len(article_data.get('content', ''))} characters")
    print(f"\n{'='*80}")
    print(f"FULL CONTENT:")
    print(f"{'='*80}\n")
    print(article_data.get('content', 'No content'))
    print(f"\n{'='*80}\n")
else:
    print("❌ FAILED to scrape article")
