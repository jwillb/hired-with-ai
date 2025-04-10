from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, IndustryFilters

def linkedin_scrape(search_term, chromedriver_path, data_callback, error_callback, end_callback, driver_options):
    scraper = LinkedinScraper(
        chrome_executable_path=chromedriver_path,
        chrome_binary_location=None,
        chrome_options=driver_options,
        max_workers=2,
        slow_mo=0.5,
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
