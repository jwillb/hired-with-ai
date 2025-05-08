# hired-with-ai
An AI-Powered job curator that saves and sends jobs from LinkedIn via ntfy.

## Introduction
I found the job search process to be tedious and time-consuming, so I devised a way to have it done automatically.
## Requirements
To use this program, you must install Python, and the `pip` package manager. Then, you must install the requirements with `pip install -r requirements.txt`
Alternatively, you can run the program using Docker.
## Usage
### Manual
After this is done, copy the `sample-env` file and rename it to `.env`. Then, set all of the environment variables to your liking.
### Docker
Edit the provided Compose file and sample-env file to your liking, then run `docker compose up -d`. Installing and using Docker is out of the scope of this guide, but there are many resources available online to help with this.
## Credits
[spinlud/py-linkedin-jobs-scraper](https://github.com/spinlud/py-linkedin-jobs-scraper) for the excellent LinkedIn web scraper.
