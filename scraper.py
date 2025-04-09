from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, IndustryFilters


# Fired once for each page (25 jobs)
def linkedin_scrape(search_term, chromedriver_path, data_callback, error_callback, end_callback):
    scraper = LinkedinScraper(
        chrome_executable_path=chromedriver_path,  # Custom Chrome executable path (e.g. /foo/bar/bin/chromedriver)
        chrome_binary_location=None,  # Custom path to Chrome/Chromium binary (e.g. /foo/bar/chrome-mac/Chromium.app/Contents/MacOS/Chromium)
        chrome_options=None,  # Custom Chrome options here
        headless=True,  # Overrides headless mode only if chrome_options is None
        max_workers=1,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
        slow_mo=0.5,  # Slow down the scraper to avoid 'Too many requests 429' errors (in seconds)
        page_load_timeout=40  # Page load timeout (in seconds)    
    )

    # Add event listeners
    scraper.on(Events.DATA, data_callback)
    scraper.on(Events.ERROR, error_callback)
    scraper.on(Events.END, end_callback)

    queries = [
        Query(
            query=search_term,
            options=QueryOptions(
                locations=["Canada"],
                limit=1000,
                filters=QueryFilters(
                    relevance=RelevanceFilters.RELEVANT,
                    time=TimeFilters.DAY,
                    type=[TypeFilters.INTERNSHIP],
                    industry=[IndustryFilters.IT_SERVICES, 
                              IndustryFilters.ELECTRONIC_MANUFACTURING, 
                              IndustryFilters.INFORMATION_SERVICES, 
                              IndustryFilters.SOFTWARE_DEVELOPMENT, 
                              IndustryFilters.TECHNOLOGY_INTERNET, 
                              IndustryFilters.COMPUTER_GAMES]
                )
            )
        ),
    ]

    scraper.run(queries)
