# cli_menu.py
# ======================================================================
# CLI MENU: Choose scraper or run all
# Now includes: Bama.ir + Divar.ir
# ======================================================================

import asyncio
import importlib
import sys
import subprocess

# --- Auto-install Playwright ---
def install_playwright():
    try:
        import playwright
    except ImportError:
        print("Playwright not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
    try:
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    except:
        pass

# --- Scraper List ---
SCRAPERS = [
    {
        "name": "Bama.ir",
        "module": "scrapers.bama_scraper",
        "desc": "Scrapes vehicle models, prices, year, mileage from bama.ir/car"
    },
    {
        "name": "Divar.ir",
        "module": "scrapers.divar_scraper",
        "desc": "Scrapes vehicle models, mileage, price from divar.ir/s/tehran/car"
    }
]

async def run_scraper(scraper):
    try:
        mod = importlib.import_module(scraper["module"])
        print(f"\n{'='*60}")
        print(f" RUNNING: {scraper['name']}")
        print(f" {scraper['desc']}")
        print(f"{'='*60}\n")
        await mod.scrape()
    except Exception as e:
        print(f"\nERROR in {scraper['name']}: {e}\n")

async def run_all():
    print("\nRUNNING ALL SCRAPERS...\n")
    for s in SCRAPERS:
        await run_scraper(s)
    print("ALL DONE.")

def show_menu():
    print("\n" + " VEHICLE SCRAPERS ".center(60, "="))
    for i, s in enumerate(SCRAPERS, 1):
        print(f"{i}. {s['name']: <15} → {s['desc']}")
    print("a. Run ALL")
    print("0. Exit")
    print("=""="*60)
    return input("\nChoose: ").strip().lower()

async def main():
    install_playwright()

    if len(sys.argv) > 1:
        choice = sys.argv[1].lower()
    else:
        choice = show_menu()

    if choice in ["0", "exit", "q"]:
        print("Goodbye!")
        return
    if choice in ["a", "all"]:
        await run_all()
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(SCRAPERS):
                await run_scraper(SCRAPERS[idx])
            else:
                print("Invalid choice.")
        except ValueError:
            print("Enter number or 'a'")

if __name__ == "__main__":
    asyncio.run(main())