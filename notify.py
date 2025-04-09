import requests

def notify(ntfy_url, ntfy_topic, job_summary):
    requests.post(ntfy_url + "/" + ntfy_topic,
    data=job_summary.encode(encoding='utf-8'), headers={ "Markdown": "yes" })
