import requests
from bs4 import BeautifulSoup
import re

def scrape_jobs(url):
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers, timeout=10)
    except:
        return []

    soup = BeautifulSoup(res.text, "html.parser")

    jobs = []

    
    try:
        title = soup.find("h1").get_text(strip=True)
    except:
        title = ""

    try:
        company = soup.find("h2").get_text(strip=True)
    except:
        company = "Not found"

    description = soup.get_text(separator=" ", strip=True)

    
    exp_match = re.search(r'\d+\+?\s*(year|years)', description.lower())
    experience = exp_match.group() if exp_match else "Not mentioned"

    deadline_match = re.search(r'(apply by|deadline|closing date).*', description.lower())
    deadline = deadline_match.group() if deadline_match else "Not found"

    if title:
        jobs.append({
            "title": title,
            "company": company,
            "description": description,
            "experience": experience,
            "deadline": deadline
        })

    return jobs