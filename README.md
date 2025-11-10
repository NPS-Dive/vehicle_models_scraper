# Vehicle Models Scraper [car]🇮🇷

**Real-time car listing scraper** for **Bama.ir** and **Divar.ir** (Iran) using **Python + Playwright** with **anti-bot stealth**, **proxy support**, and **Pandas-powered CSV export**.

Works from **Azerbaijan (AZ)** → **Bama.ir 100% functional**  
**Divar.ir requires Iranian proxy**

---

## Tech Stack

| Module | Purpose |
|-------|--------|
| **Playwright** | Headless browser automation with human-like scrolling & interaction |
| **asyncio** | Async scraping for speed & reliability |
| **pandas** | CSV export with clean, structured data |
| **logging** | Debug & production logs |
| **pathlib** | Modern file handling |
| **retry decorator** | Auto-retry on network failures |

---

## Features

- Scrapes: **model, year, mileage, price**
- **Stealth mode**: bypasses Cloudflare & bot detection
- **Proxy support**: works via Iranian IP
- **CSV output** with timestamp
- **CLI menu** for easy selection
- **Smart scrolling** with content detection

---

## Setup

```bash
pip install -r requirements.txt


Config (config/settings.py)
pythonIRAN_PROXY = "http://your-proxy:port"  # Required for Divar.ir

Run
bashpython cli_menu.py
Choose:
text1. Bama.ir
2. Divar.ir
a. Run ALL

Output
textoutput/bama_2025-11-10.csv
output/divar_2025-11-10.csv
Sample row:
csvmodel,mileage,price,year,source_url,scrape_date
"پژو 206 تیپ ۲","۱۲۰٬۰۰۰ کیلومتر","۴۵۰٬۰۰۰٬۰۰۰","1398",https://bama.ir/car,2025-11-10

Project Structure
textvehicle_models_scraper/
├── scrapers/
│   ├── bama_scraper.py
│   └── divar_scraper.py
├── utils/helpers.py
├── config/settings.py
├── cli_menu.py
├── output/
├── requirements.txt
└── README.md

License
MIT © 2025 — Free to use, modify, and distribute.


