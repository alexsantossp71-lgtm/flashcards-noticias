import asyncio
from services.rss_service import RSSService
from config import RSS_MAX_ITEMS

async def test_all_feeds():
    rss = RSSService()
    categories = ['Brasil', 'Mundo', 'Política', 'Esportes', 'Tecnologia', 'Economia']
    
    print(f"Testing {len(categories)} categories...")
    
    for cat in categories:
        print(f"\n--- Checking Category: {cat} ---")
        headlines = rss.fetch_headlines(cat)
        if not headlines:
            print(f"FAILED: No headlines found for {cat}")
        else:
            print(f"Found {len(headlines)} headlines.")
            # Print first 3
            for i, h in enumerate(headlines[:3]):
                print(f"  [{i+1}] {h['title']} ({h['source']})")

if __name__ == "__main__":
    asyncio.run(test_all_feeds())
