FROM python:3.13.3-slim-bookworm

RUN useradd -ms /bin/bash runner

WORKDIR /home/runner

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y \
    libglib2.0-0 \
    libgconf-2-4 \
    libfontconfig1 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm-dev \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p ./data
RUN chown runner ./data

USER runner

COPY main.py .
COPY scraper.py .
COPY ai_query.py .
COPY notify.py .

CMD [ "python", "-u", "./main.py" ]
