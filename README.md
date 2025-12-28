# Vehicle Models Scraper

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macOS-lightgrey)

Vehicle Models Scraper is a Python-based web scraping project for collecting vehicle listings from multiple online marketplaces.  
The project supports modular scrapers, CSV export, backup handling, and optional scheduling for repeated execution.

The goal of the project is to provide a clean, extensible structure for scraping vehicle data in a maintainable way.

---

## Features

- Scrapes vehicle advertisements from multiple websites
- Modular scraper architecture
- Command line interface for running tasks
- Option to run all scrapers together
- CSV output for collected data
- Backup of previous runs
- Basic scheduling support
- Error handling for unavailable pages or network failures

---

## Project Structure

```
vehicle_models_scraper/
├── scrapers/
│   ├── bama_scraper.py
│   ├── divar_scraper.py
│   └── __init__.py
├── utils/
│   ├── helpers.py
│   └── __init__.py
├── config/
│   ├── settings.py
│   └── __init__.py
├── output/
├── backups/
├── cli_menu.py
├── scheduler.py
├── run_all.py
└── requirements.txt
```

Description of main parts:

- scrapers/ : website-specific scraper modules  
- utils/ : helper functions and common utilities  
- config/ : project configuration and constants  
- output/ : generated CSV data files  
- backups/ : archived older result files  
- cli_menu.py : text-based interactive menu  
- run_all.py : run all scrapers in one go  
- scheduler.py : periodic automated execution  

---

## Requirements

- Python 3.9 or higher

Install dependencies using:

```
pip install -r requirements.txt
```

---

## How to Run

### Run from command line

Run all scrapers:

```
python run_all.py
```

Run interactive command line menu:

```
python cli_menu.py
```

Run the scheduler:

```
python scheduler.py
```

---

## Output

Scraped data is saved as CSV files inside:

```
output/
```

Backups of previous results are stored in:

```
backups/
```

---

## Configuration

Project configuration is located in:

```
config/settings.py
```

You can modify:

- target websites
- time delays
- enabled scrapers
- output directories
- scheduling parameters

---

## Extending the Project

To add a new website scraper:

1. Create a new file in `scrapers/`
2. Implement scraping logic inside a class or functions
3. Register it in `run_all.py` or `cli_menu.py`
4. Add required configuration if needed

---

## Disclaimer

This project is intended for educational and research purposes.  
Please respect website terms of service and local laws when scraping data.

---

## License

MIT License
