import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import schedule
import time
from datetime import datetime
import os

logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

BASE_URL = "https://vacancymail.co.zw"
JOBS_URL = f"{BASE_URL}/jobs"
HEADERS = {'User-Agent': 'Mozilla/5.0'}
OUTPUT_CSV = "scraped_jobs.csv"
NUM_JOBS_TO_SCRAPE = 10

def scrape_and_save_jobs(num_jobs=NUM_JOBS_TO_SCRAPE):
    try:
        logging.info(f"Starting job scrape for {num_jobs} jobs...")
        print(f" Scraping {num_jobs} jobs...")

        response = requests.get(JOBS_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        job_cards = soup.select('a.job-listing')[:num_jobs] # Limit to the specified number

        if not job_cards:
            with open("page_debug.html", "w", encoding="utf-8") as f:
                f.write(soup.prettify())
            print(" No job cards found. Dumped HTML to page_debug.html for inspection.")
            return

        print(f" Found {len(job_cards)} job listings.")
        job_list = []

        for job in job_cards:
            try:
                title_element = job.select_one('h3.job-listing-title')
                company_element = job.select_one('h4.job-listing-company')
                description_element = job.select_one('p.job-listing-text')

                title = title_element.get_text(strip=True) if title_element else "No Title"
                company = company_element.get_text(strip=True) if company_element else "No Company"
                description = description_element.get_text(strip=True) if description_element else "No Description"

                footer_items = job.select('div.job-listing-footer li')
                location = expiry = "Unknown"

                for item in footer_items:
                    text = item.get_text(strip=True)
                    if "Expires" in text:
                        expiry = text.replace("Expires", "").strip()
                    elif not location or location == "Unknown":
                        location = text

                job_list.append({
                    "Job Title": title,
                    "Company": company,
                    "Location": location,
                    "Expiry Date": expiry,
                    "Description": description,
                    "Link": f"{BASE_URL}{job['href']}"
                })

            except Exception as e:
                logging.warning(f"Could not parse one job: {e}")
                print(f" Skipped one job due to error: {e}")

        if not job_list:
            logging.error("No jobs scraped after parsing loop.")
            print(" No jobs scraped. Something went wrong.")
            return

        df = pd.DataFrame(job_list)
        df.drop_duplicates(subset=["Job Title", "Company", "Location"], inplace=True)
        df["Expiry Date"] = pd.to_datetime(df["Expiry Date"], errors='coerce').dt.strftime('%Y-%m-%d')

        df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
        logging.info(f"Job scrape successful. {len(df)} jobs saved to {OUTPUT_CSV}.")
        print(f" {OUTPUT_CSV} created with {len(df)} jobs.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        print(" Failed to retrieve the job listing page.")
        try:
            with open("page_debug_request_failed.html", "w", encoding="utf-8") as f:
                f.write(response.text if 'response' in locals() else "No response to dump.")
            print(" Dumped response HTML to page_debug_request_failed.html for inspection.")
        except Exception as dump_error:
            logging.error(f"Failed to dump response HTML: {dump_error}")
            print(" Failed to dump response HTML.")

    except Exception as e:
        logging.error(f"Scraping failed: {e}")
        print(" Something went wrong during scraping. Check scraper.log for details.")

def schedule_hourly():
    print("Scheduling job scraping to run hourly.")
    schedule.every().hour.do(scrape_and_save_jobs)

def schedule_daily(time_str="09:00"):
    print(f"Scheduling job scraping to run daily at {time_str}.")
    schedule.every().day.at(time_str).do(scrape_and_save_jobs)

def run_scheduler():
    print("Scheduler is running. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    print("VacancyMail Job Scraper Scheduler")
    print("1. Run scraper once now (for 10 jobs)")
    print("2. Schedule scraping hourly")
    print("3. Schedule scraping daily at a specific time (e.g., 10:00)")
    print("4. Run the scheduler (keeps the script running for scheduled jobs)")
    print("5. Exit")

    while True:
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            scrape_and_save_jobs()
            print("Scraping done.")
        elif choice == '2':
            schedule_hourly()
            print("Hourly scraping scheduled.")
        elif choice == '3':
            time_str = input("Enter the daily time for scraping (HH:MM): ")
            schedule_daily(time_str)
            print(f"Daily scraping scheduled for {time_str}.")
        elif choice == '4':
            run_scheduler()
            break  # Exit the menu loop when the scheduler is running
        elif choice == '5':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")