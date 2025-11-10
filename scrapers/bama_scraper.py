# scrapers/bama_scraper.py
# ======================================================================
# BAMA.IR SCRAPER — FULLY DOCUMENTED & PRODUCTION READY
# Scrapes: https://bama.ir/car
# Features:
#   • Lazy loading via infinite scroll
#   • Extracts: model, year, mileage, description, price (or negotiable)
#   • Only includes ads with price or negotiable tag
#   • Saves to daily CSV: bama_2025-11-10.csv
#   • Uses fallback browser + manual stealth
#   • Full error handling and logging
#   • RETRY decorator for flaky operations
#   • asyncio imported
# ======================================================================

import asyncio
import time
import re
from pathlib import Path
from typing import List, Dict

from playwright.async_api import (
    Page, 
    TimeoutError as PWTimeout,
    async_playwright  # ← ADD THIS LINE
)

# --- Shared utils ---
from utils.helpers import (
    setup_logging, save_to_csv, get_current_date_str,
    launch_browser_with_fallback, retry
)
from config.settings import TIMEOUT, SCROLL_WAIT_TIME, BAMA_URL

# --- Selectors ---
AD_CARD_SELECTOR = '.bama-ad-holder'
AD_LINK_SELECTOR = 'a.bama-ad.listing'
YEAR_SELECTOR = '.bama-ad__detail-row span:first-child'
MILEAGE_SELECTOR = '.dir-ltr'
DESC_SELECTOR = '.bama-ad__detail-trim'
PRICE_SELECTOR = '.bama-ad__price'
NEGOTIABLE_SELECTOR = '.bama-ad__negotiable-price'

# --- Output ---
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# --- Logger ---
logger = setup_logging()

# =====================================================
# HELPER: Scroll to load all lazy content
# =====================================================
async def scroll_and_load(page: Page):
    prev_height = 0
    stable_rounds = 0
    max_rounds = 50

    logger.info("Starting lazy loading scroll...")
    for round_num in range(1, max_rounds + 1):
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(int(SCROLL_WAIT_TIME * 1000))

        cur_height = await page.evaluate("document.body.scrollHeight")
        logger.info(f"Scroll {round_num}: Height = {cur_height}")

        if cur_height == prev_height:
            stable_rounds += 1
            if stable_rounds >= 3:
                logger.info("No new content for 3 rounds → scrolling complete")
                break
        else:
            stable_rounds = 0
        prev_height = cur_height

# =====================================================
# HELPER: Extract clean price
# =====================================================
def clean_price(text: str) -> str:
    return "".join(filter(str.isdigit, text)) if text else ""

# =====================================================
# MAIN SCRAPER (with retry)
# =====================================================
@retry(max_attempts=3, delay=3.0)
async def scrape():
    start_time = time.time()
    all_data: List[Dict] = []
    today = get_current_date_str()

    async with async_playwright() as p:  # ← THIS LINE USES async_playwright()
        page, context = await launch_browser_with_fallback(p, BAMA_URL)
        if not page:
            logger.error("Browser launch failed. Exiting.")
            return

        try:
            logger.info(f"Navigating to {BAMA_URL}")
            await page.goto(BAMA_URL, wait_until="networkidle", timeout=TIMEOUT)
            await scroll_and_load(page)

            logger.info("Extracting ad cards...")
            cards = await page.query_selector_all(AD_CARD_SELECTOR)
            logger.info(f"Found {len(cards)} ad cards")

            for idx, card in enumerate(cards, 1):
                try:
                    link_elem = await card.query_selector(AD_LINK_SELECTOR)
                    if not link_elem:
                        continue
                    model = (await link_elem.get_attribute("title") or "").strip()
                    ad_url = await link_elem.get_attribute("href")
                    if ad_url and not ad_url.startswith("http"):
                        ad_url = "https://bama.ir" + ad_url

                    year_elem = await card.query_selector(YEAR_SELECTOR)
                    year = (await year_elem.inner_text()).strip() if year_elem else ""

                    mileage_elems = await card.query_selector_all(MILEAGE_SELECTOR)
                    mileage = " ".join([await e.inner_text() for e in mileage_elems]).strip()

                    desc_elem = await card.query_selector(DESC_SELECTOR)
                    description = (await desc_elem.inner_text()).strip() if desc_elem else ""

                    price_elem = await card.query_selector(PRICE_SELECTOR)
                    negotiable_elem = await card.query_selector(NEGOTIABLE_SELECTOR)

                    price = ""
                    price_status = ""

                    if price_elem:
                        price_raw = await price_elem.inner_text()
                        price = clean_price(price_raw)
                        price_status = "fixed"
                    elif negotiable_elem:
                        price_raw = await negotiable_elem.inner_text()
                        price = clean_price(price_raw) or "توافقی"
                        price_status = "negotiable"
                    else:
                        continue

                    if model and (price or price_status == "negotiable"):
                        all_data.append({
                            "model": model,
                            "year": year,
                            "mileage": mileage,
                            "description": description,
                            "price": price,
                            "price_status": price_status,
                            "source_url": ad_url or "",
                            "scrape_date": today
                        })

                    if idx % 50 == 0:
                        logger.info(f"Processed {idx}/{len(cards)} ads")

                except Exception as e:
                    logger.error(f"Error on card {idx}: {e}")
                    continue

            if all_data:
                csv_path = save_to_csv(all_data, "bama")
                logger.info(f"SCRAPING COMPLETE: {len(all_data)} vehicles saved")
            else:
                logger.warning("NO DATA COLLECTED")

        except Exception as e:
            logger.exception(f"CRITICAL ERROR: {e}")
        finally:
            if context and context.browser:
                await context.browser.close()

    elapsed = time.time() - start_time
    print(f"\n{'='*70}")
    print(f" BAMA.IR SCRAPER FINISHED ")
    print(f" Vehicles saved : {len(all_data)}")
    print(f" Time taken     : {elapsed:.1f} seconds")
    print(f" Output         : output/bama_{today}.csv")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    asyncio.run(scrape())  # ← THIS USES asyncio