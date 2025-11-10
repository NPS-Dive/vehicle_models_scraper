# utils/helpers.py
# ======================================================================
# SHARED UTILITIES: Logging, CSV, Stealth Browser Launch, Retry
# Used by ALL scrapers. Manual stealth (no external libs).
# Works on Python 3.11+ with Playwright.
# Features:
#   • Auto-install Playwright
#   • Retry decorator
#   • Full stealth
# ======================================================================
import asyncio
import os
import logging
import random
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import pandas as pd

from playwright.async_api import async_playwright, Page, BrowserContext, TimeoutError as PWTimeout

# --- Import config ---
from config.settings import (
    BROWSER_FALLBACK, HEADLESS, TIMEOUT, CLOUDFLARE_TITLE,
    ANTI_BOT_PHRASES, SCROLL_WAIT_TIME
)

# ----------------------------------------------------------------------
# AUTO-INSTALL PLAYWRIGHT
# ----------------------------------------------------------------------
def install_playwright():
    """
    Installs Playwright and Chromium if not present.
    Called from cli_menu.py.
    """
    try:
        import playwright
    except ImportError:
        print("Installing Playwright...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
    try:
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    except:
        pass  # Already installed

# ----------------------------------------------------------------------
# SETUP LOGGING (File + Console)
# ----------------------------------------------------------------------
def setup_logging(log_dir: str = "logs") -> logging.Logger:
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "scraper.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("scraper")

# ----------------------------------------------------------------------
# SAVE TO CSV WITH DEDUPLICATION & UTF-8 BOM
# ----------------------------------------------------------------------
def save_to_csv(data: List[Dict], prefix: str, output_dir: str = "output") -> Optional[Path]:
    if not data:
        logging.getLogger("scraper").warning("No data to save.")
        return None

    df = pd.DataFrame(data)
    df = df.drop_duplicates(subset=["model", "year", "mileage", "price", "source_url"]).sort_values("model")
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{prefix}_{today}.csv"
    filepath = Path(output_dir) / filename
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(filepath, index=False, encoding='utf-8-sig')
    
    logger = logging.getLogger("scraper")
    logger.info(f"SAVED {len(df)} rows → {filepath}")

    # --- Backup ---
    from config.settings import BACKUP_ENABLED
    if BACKUP_ENABLED:
        backup_dir = Path("backups")
        backup_dir.mkdir(exist_ok=True)
        backup_path = backup_dir / f"{prefix}_{today}_backup.csv"
        df.to_csv(backup_path, index=False, encoding='utf-8-sig')
        logger.info(f"BACKUP → {backup_path}")

    return filepath

# ----------------------------------------------------------------------
# GET CURRENT DATE STRING
# ----------------------------------------------------------------------
def get_current_date_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")

# ----------------------------------------------------------------------
# RETRY DECORATOR
# ----------------------------------------------------------------------
def retry(max_attempts: int = 3, delay: float = 2.0):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    logger = logging.getLogger("scraper")
                    logger.warning(f"Attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt < max_attempts:
                        await asyncio.sleep(delay * attempt)
            raise last_exc
        return wrapper
    return decorator

# ----------------------------------------------------------------------
# MANUAL STEALTH BROWSER LAUNCH
# ----------------------------------------------------------------------
async def launch_browser_with_fallback(p, start_url: str) -> Tuple[Optional[Page], Optional[BrowserContext]]:
    logger = logging.getLogger("scraper")
    IRANIAN_UA = (
        "Mozilla/5.0 (Linux; Android 13; SM-G991B) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
    )

    for browser_type in BROWSER_FALLBACK:
        browser = None
        context = None
        page = None
        try:
            logger.info(f"Launching {browser_type} with stealth...")

            browser = await p[browser_type].launch(
                headless=HEADLESS,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-infobars",
                    "--disable-extensions",
                    "--start-maximized",
                    "--disable-web-security",
                    "--disable-features=IsolateOrigins,site-per-process"
                ]
            )

            context = await browser.new_context(
                viewport={"width": 390, "height": 844},
                user_agent=IRANIAN_UA,
                locale="fa-IR",
                java_script_enabled=True,
                bypass_csp=True,
                color_scheme="light"
            )

            page = await context.new_page()

            await page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', { get: () => false });
                Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4,5] });
                Object.defineProperty(navigator, 'languages', { get: () => ['fa-IR', 'fa', 'en'] });
                window.chrome = { runtime: {}, loadTimes: () => {}, csi: () => {} };
            """)

            await page.wait_for_timeout(random.uniform(2000, 4000))

            await page.goto(start_url, wait_until="domcontentloaded", timeout=TIMEOUT)
            title = await page.title()
            body = (await page.text_content("body") or "").lower()

            if any(phrase in title.lower() for phrase in [CLOUDFLARE_TITLE.lower()] + ANTI_BOT_PHRASES):
                raise PWTimeout("Anti-bot detected (title)")
            if any(phrase in body for phrase in ANTI_BOT_PHRASES):
                raise PWTimeout("Anti-bot detected (body)")

            logger.info(f"SUCCESS: {browser_type} passed anti-bot checks")
            return page, context

        except Exception as e:
            logger.warning(f"{browser_type} failed: {e} — trying next...")
            if page: await page.close()
            if context: await context.close()
            if browser: await browser.close()

    logger.error("ALL BROWSERS FAILED. Check internet, proxy, or site status.")
    return None, None