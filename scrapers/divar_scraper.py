# scrapers/divar_scraper.py
# DIVAR.IR — WORKING FROM AZERBAIJAN — FINAL EXTRACTION

import asyncio
import time
import random
from pathlib import Path
from typing import List, Dict

from playwright.async_api import async_playwright

from utils.helpers import setup_logging, save_to_csv, get_current_date_str, retry

DIVAR_URL = "https://divar.ir/s/tehran/car"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)
logger = setup_logging()

MAIN_CARD = 'article[data-testid="post-card"]'

async def human_delay():
    await asyncio.sleep(random.uniform(3.0, 6.0))

@retry(max_attempts=1, delay=0)
async def scrape():
    start_time = time.time()
    all_data = []
    today = get_current_date_str()

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        )
        context = await browser.new_context(
            viewport=None,
            user_agent="Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            locale="fa-IR"
        )
        page = await context.new_page()

        # MANUAL STEALTH
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => false });
            Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4,5] });
            window.chrome = { runtime: {} };
            delete navigator.__proto__.webdriver;
        """)

        try:
            logger.info("Opening Divar...")
            await page.goto(DIVAR_URL, wait_until="networkidle", timeout=90000)
            await human_delay()

            # Wait for cards
            await page.wait_for_selector(MAIN_CARD, timeout=30000)
            logger.info("Cards loaded")

            # Scroll to load ALL cars (15 times)
            for i in range(15):
                await page.evaluate("window.scrollBy(0, 1400)")
                await human_delay()
                count = await page.evaluate("document.querySelectorAll('article[data-testid=\"post-card\"]').length")
                logger.info(f"Scroll {i+1}: {count} cards")

            # Extract ALL
            raw_data = await page.evaluate('''() => {
                const cards = document.querySelectorAll('article[data-testid="post-card"]');
                return Array.from(cards).map(card => {
                    const title = card.querySelector('.post-card__title');
                    const descs = card.querySelectorAll('.post-card__description');
                    if (!title || descs.length < 2) return null;
                    const model = title.innerText.trim();
                    const mileage = descs[0].innerText.trim();
                    const priceRaw = descs[1].innerText.trim();
                    const price = priceRaw.replace(/[^\\d]/g, '') || 'توافقی';
                    return { model, mileage, price };
                }).filter(x => x);
            }''')

            logger.info(f"Extracted {len(raw_data)} vehicles")

            for item in raw_data:
                all_data.append({
                    "model": item["model"],
                    "mileage": item["mileage"],
                    "price": item["price"],
                    "source_url": DIVAR_URL,
                    "scrape_date": today
                })

            if all_data:
                save_to_csv(all_data, "divar")
                logger.info(f"SAVED {len(all_data)} vehicles to output/divar_{today}.csv")
            else:
                logger.warning("No data")

        except Exception as e:
            logger.exception(f"ERROR: {e}")
        finally:
            await browser.close()

    elapsed = time.time() - start_time
    print(f"\n{'='*70}")
    print(f" DIVAR.IR SCRAPER DONE")
    print(f" Vehicles saved : {len(all_data)}")
    print(f" Time taken     : {elapsed:.1f}s")
    print(f" Output         : output/divar_{today}.csv")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    asyncio.run(scrape())