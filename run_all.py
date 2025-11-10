# run_all.py
import asyncio
from scrapers.bama_scraper import scrape as scrape_bama
from scrapers.divar_scraper import scrape as scrape_divar  # ← ADDED

async def main():
    print("Starting full scrape run...")
    await scrape_bama()
    await scrape_divar()
    print("All scrapers completed.")

if __name__ == "__main__":
    asyncio.run(main())