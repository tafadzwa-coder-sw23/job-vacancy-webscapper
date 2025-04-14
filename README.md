# job-vacancy-webscapper
Python script to scrape job listings from VacancyMail.co.zw. Extracts job title, company, location, expiry, description, and link, saving them to a CSV. Includes options for one-time scraping, hourly/daily scheduling, and error logging.
# VacancyMail Job Scraper

This Python script scrapes job listings from [VacancyMail.co.zw](https://vacancymail.co.zw) and saves them to a CSV file. It also includes options to run the scraper once, schedule it to run hourly or daily, and to run a persistent scheduler.

## Features

* **Scrapes Job Data:** Extracts job title, company, location, expiry date, description, and link from job listings on VacancyMail.co.zw.
* **Saves to CSV:** Stores the scraped data in a `scraped_jobs.csv` file.
* **Error Handling:** Includes robust error handling for network requests and parsing issues. Logs errors and warnings to `scraper.log`.
* **Duplicate Removal:** Removes duplicate job listings based on title, company, and location.
* **Date Formatting:** Converts the expiry date to a consistent `YYYY-MM-DD` format.
* **Scheduling Options:**
    * Run the scraper once for a specified number of jobs (default: 10).
    * Schedule the scraper to run automatically every hour.
    * Schedule the scraper to run automatically once a day at a specified time.
    * Run a persistent scheduler to execute scheduled jobs in the background.
* **User-Friendly Menu:** Provides a simple command-line interface to choose different execution modes.
* **Debugging Tools:** Saves the HTML content of the page to `page_debug.html` if no job cards are found, and `page_debug_request_failed.html` if the initial request fails, to aid in debugging.

## Prerequisites

* **Python 3.x** installed on your system.
* The following Python libraries installed:
    * `requests`
    * `beautifulsoup4`
    * `pandas`
    * `schedule`

    You can install these libraries using pip:
    ```bash
    pip install requests beautifulsoup4 pandas schedule
    ```

## Setup and Usage

1.  **Clone the Repository (Optional):** If you are using Git, you can clone this repository to your local machine:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
    (Replace `<repository_url>` and `<repository_directory>` with your repository details if applicable).

2.  **Save the Script:** Save the provided Python code as a `.py` file (e.g., `vacancy_scraper.py`).

3.  **Run the Script:** Open your terminal or command prompt, navigate to the directory where you saved the script, and run it using:
    ```bash
    python vacancy_scraper.py
    ```

4.  **Follow the Menu:** The script will display a menu with the following options:
    ```
    VacancyMail Job Scraper Scheduler
    1. Run scraper once now (for 10 jobs)
    2. Schedule scraping hourly
    3. Schedule scraping daily at a specific time (e.g., 10:00)
    4. Run the scheduler (keeps the script running for scheduled jobs)
    5. Exit
    ```
    Enter the number corresponding to your desired action.

    * **Option 1:** Runs the scraper once and saves the latest 10 job listings to `scraped_jobs.csv`.
    * **Option 2:** Schedules the scraper to run every hour. You will need to keep the script running for the scheduled jobs to execute.
    * **Option 3:** Prompts you to enter a specific time (in `HH:MM` format) for the scraper to run daily. You will need to keep the script running for the scheduled jobs to execute.
    * **Option 4:** Starts the scheduler, which will continuously check for scheduled jobs (hourly or daily) and execute them. Press `Ctrl+C` to stop the scheduler.
    * **Option 5:** Exits the script.

## Output

The scraped job data will be saved in a CSV file named `scraped_jobs.csv` in the same directory where you run the script. The CSV file will contain the following columns:

* `Job Title`
* `Company`
* `Location`
* `Expiry Date`
* `Description`
* `Link`

## Logging

The script uses the `logging` module to record information, warnings, and errors during execution. These logs are saved in a file named `scraper.log` in the same directory. This can be helpful for debugging and monitoring the script's activity.

## Important Notes

* **Website Structure Changes:** The structure of the VacancyMail website might change in the future, which could break the scraper. You may need to update the script's selectors (`soup.select()`) accordingly if this happens.
* **Respect `robots.txt`:** Always check the website's `robots.txt` file (usually found at `https://vacancymail.co.zw/robots.txt`) to understand which parts of the site are disallowed for scraping. This script currently only targets the main jobs page.
* **Rate Limiting:** Be mindful of the website's server load. Avoid making too many requests in a short period, as this could lead to your IP address being temporarily blocked. The current script has a delay only within the `schedule` library's sleep function, but if you modify it for more frequent scraping, consider adding explicit delays using `time.sleep()`.
* **Ethical Scraping:** Use this script responsibly and ethically. Do not use it to overload the website or for any malicious purposes.

## Contributing

If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on the repository.

## License

[Specify your license here, e.g., MIT License]
