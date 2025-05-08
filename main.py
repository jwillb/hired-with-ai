import sqlite3
import logging
from os import getenv, path, environ, makedirs
from dotenv import load_dotenv
from time import sleep
from selenium.webdriver.chrome.options import Options

load_dotenv()
from scraper import *
from ai_query import *
from notify import *


data_dir = "./data/"
table_name = path.join(data_dir, "jobs.db")
base_query = getenv("AI_QUERY")
driver_path = getenv("CHROMEDRIVER_PATH")
search_query = getenv("SEARCH_QUERY")
criteria = getenv("JOB_CRITERIA")
model_name_filter = getenv("MODEL_NAME_FILTER")
model_name_summary = getenv("MODEL_NAME_SUMMARY")
api_key_filter = getenv("AI_API_KEY_FILTER")
api_key_summary = getenv("AI_API_KEY_SUMMARY")
base_url_filter = getenv("AI_BASE_URL_FILTER")
base_url_summary = getenv("AI_BASE_URL_SUMMARY")
ntfy_url = getenv("NTFY_BASE_URL")
ntfy_topic = getenv("NTFY_TOPIC")
sleep_interval = int(getenv("INTERVAL_MIN")) * 60

options = Options()
options.add_argument("--no-sandbox")
options.add_argument(f"--user-data-dir={data_dir}driver_data")
options.add_argument("--headless=new")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

makedirs(data_dir, exist_ok=True)

if not path.exists(table_name):
    with sqlite3.connect(table_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""
                CREATE TABLE jobs (
                        id INTEGER PRIMARY KEY,
                        link TEXT NOT NULL,
                        title TEXT NOT NULL,
                        company TEXT NOT NULL,
                        description TEXT NOT NULL,
                        valid BOOL NOT NULL,
                        sent BOOL NOT NULL
                )""")
        conn.commit()

# Fired once for each successfully processed job
def on_data(data):
    print(f"Found job from {data.company} ({data.date_text})")
    with sqlite3.connect(table_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM jobs WHERE title = ? AND company = ? LIMIT 1)", (data.title, data.company))
    if cursor.fetchone()[0] == 0:
        valid = jobQuery(api_key_filter, base_url_filter, model_name_filter, base_query, criteria, data.company, data.description)
        with sqlite3.connect(table_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                    INSERT OR IGNORE INTO jobs (
                        link, title, company, description, valid, sent
                    )
                    VALUES (
                        ?,?,?,?,?,?
                    )
                    """, (data.link, data.title, data.company, data.description, valid, False))
            conn.commit()
    else:
        print("Already found.")

def send_job(job_tuple):
    summary = jobSummary(api_key_summary, base_url_summary, model_name_summary, job_tuple[3], job_tuple[4], job_tuple[1])
    print(f"Sending job from {job_tuple[3]}...")
    notify(ntfy_url, ntfy_topic, summary)
    with sqlite3.connect(table_name) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE jobs SET sent = 1 WHERE id = ?", (job_tuple[0],))
        conn.commit()

def on_error(error):
    pass

def on_end():
    print("Finished scraping.")
    with sqlite3.connect(table_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs WHERE sent = 0 AND valid = 1")
        jobs_to_send = cursor.fetchall()
        for job in jobs_to_send:
            send_job(job)

print(f"""
### SETTINGS ###
Search query: {search_query}
Chromedriver path: {driver_path}
Filtering model: {model_name_filter}
Summarizing model: {model_name_summary}
Notifications via {ntfy_url}/{ntfy_topic}
Run every {sleep_interval // 60} minutes
""")

while True:
    linkedin_scrape(search_query, driver_path, on_data, on_error, on_end, options)
    sleep(sleep_interval)
