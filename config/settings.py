# config/settings.py
# ======================================================================
# CENTRAL CONFIGURATION FOR ALL SCRAPERS
# Edit here to control: browser behavior, URLs, timeouts, daily run time.
# All scrapers import from here → single source of truth.
# ======================================================================

from datetime import time

# --------------------- BROWSER & STEALTH ---------------------
BROWSER_FALLBACK = ['chromium', 'firefox']  # Try chromium first, then firefox
HEADLESS = True                             # True = no window (production), False = debug
SCROLL_WAIT_TIME = 2.5                      # Seconds between scrolls (lazy load)
TIMEOUT = 90000                             # Page load timeout in ms (90 sec)

# Cloudflare / anti-bot detection
CLOUDFLARE_TITLE = 'Cloudflare'
ANTI_BOT_PHRASES = ["just a moment", "checking your browser"]

# --------------------- DAILY SCHEDULE ---------------------
# Set your desired daily run time (Iran local time: Asia/Tehran)
# Example: time(2, 0) → 02:00 AM
DAILY_RUN_HOUR = 2
DAILY_RUN_MINUTE = 0
TIMEZONE = "Asia/Tehran"

# --------------------- SITE URLs ---------------------
BAMA_URL = "https://bama.ir/car"

# --------------------- CSV SETTINGS ---------------------
CSV_ENCODING = 'utf-8-sig'  # Excel-friendly for Persian text
BACKUP_ENABLED = True

# Iran Proxy
IRAN_PROXY = None  # Set to "http://IP:PORT"
# IRAN_PROXY = "http://185.162.231.106:80"  # Set to "http://IP:PORT"