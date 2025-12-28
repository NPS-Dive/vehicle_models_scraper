Vehicle Models Scraper 🇮🇷

A Python-based, asynchronous web-scraping framework for collecting real-time car listings from Iranian online marketplaces.
The scraper extracts vehicle data, saves structured outputs, supports scheduling, and provides a command-line interface for running and managing scraping tasks.

The project is designed to be:

modular

robust against site changes

resumable and fault tolerant

suitable for both one-off runs and automated periodic execution

✨ Key Features

🚗 Scrapes multiple car listing websites

⚡ asyncio-based high-performance scraping

🧭 CLI interactive menu (cli_menu.py)

🗂 Structured CSV output

💾 Automatic backups

🕒 Built-in task scheduler

🖼 Error & debug screenshots

🧱 Clean module architecture

🛡 Graceful error handling & retries

🧭 Project Structure
vehicle_models_scraper/
├── scrapers/
│   ├── bama_scraper.py
│   └── divar_scraper.py
├── config/
│   ├── settings.py
│   └── __init__.py
├── utils/
│   ├── helpers.py
│   └── __init__.py
├── output/        # latest results
├── backups/       # archived CSV backups
├── cli_menu.py
├── run_all.py
├── scheduler.py
├── requirements.txt
└── README.md

🛠 Tech Stack

Python 3.9+

asyncio

requests / httpx / aiohttp (depending on site)

HTML parsing libraries

CSV export utilities

🚀 How to Install
git clone https://github.com/<your-username>/<repo-name>.git
cd vehicle_models_scraper


Create a virtual environment:

python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows


Install dependencies:

pip install -r requirements.txt

▶️ How to Run
Option 1 — Run all scrapers
python run_all.py

Option 2 — Use interactive CLI menu
python cli_menu.py

Option 3 — Run scheduled scraping
python scheduler.py

📦 Output

Generated data is automatically stored in:

/output


Backups are rotated into:

/backups


Formats include:

CSV exports

debug screenshots for failures

optional logs

⚙️ Configuration

Edit:

config/settings.py


You can configure:

target websites

delays & throttling

async concurrency

export locations

scheduler intervals

🧠 Scraper Modules
bama_scraper.py

Parses listing data from Bama car marketplace
Extracts:

make / model

price

year

mileage

city

divar_scraper.py

Scrapes automobile listings from Divar

Includes:

error screenshots

debug screenshots

resilience to listing format changes

🕒 Scheduler Support

Automated recurring scraping via:

python scheduler.py


Supports:

periodic execution

timestamped backups

unattended mode

🧩 Utilities

The utils/ package includes helpers for:

data normalization

timestamping

safe CSV writing

retry wrappers

🤝 Contributing

Pull requests and feature suggestions are welcome.

📄 License

This project is licensed under the MIT License unless otherwise specified in LICENSE.
