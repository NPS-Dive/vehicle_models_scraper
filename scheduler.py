# scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
import asyncio

from config.settings import DAILY_RUN_HOUR, DAILY_RUN_MINUTE, TIMEZONE
from scrapers.bama_scraper import scrape as scrape_bama
from scrapers.divar_scraper import scrape as scrape_divar  # ← ADDED

async def daily_job():
    print(f"\n{'='*60}")
    print(f" DAILY SCRAPE STARTED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ")
    print(f"{'='*60}\n")
    await scrape_bama()
    await scrape_divar()  # ← ADDED
    print(f"\nDAILY SCRAPE FINISHED: {datetime.now().strftime('%H:%M:%S')}\n")

def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        daily_job,
        CronTrigger(hour=DAILY_RUN_HOUR, minute=DAILY_RUN_MINUTE, timezone=TIMEZONE)
    )
    next_run = datetime.now().replace(hour=DAILY_RUN_HOUR, minute=DAILY_RUN_MINUTE, second=0, microsecond=0)
    if next_run < datetime.now():
        next_run += timedelta(days=1)

    print(f"Scheduler started. Next run: {next_run.strftime('%Y-%m-%d %H:%M')} ({TIMEZONE})")
    scheduler.start()
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        scheduler.shutdown()
        print("Scheduler stopped.")

if __name__ == "__main__":
    main()