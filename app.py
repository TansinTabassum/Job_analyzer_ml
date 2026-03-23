import gradio as gr
from scraper import scrape_jobs
from predictor import predict
import pandas as pd
import re


def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()



def extract_skills(text):
    skills_list = [
        "python", "java", "selenium", "appium",
        "javascript", "cucumber", "sql",
        "react", "node", "django", "flask"
    ]

    found = []
    text_lower = text.lower()

    for skill in skills_list:
        if skill in text_lower:
            found.append(skill)

    return ", ".join(found) if found else "Not specified"



def extract_info(text):
    text_lower = text.lower()

    # Experience (handles 5+ years, 3 years, etc)
    exp_match = re.search(r'\d+\+?\s*(year|years)', text_lower)
    experience = exp_match.group() if exp_match else "Not mentioned"

    # Deadline
    deadline_match = re.search(r'(apply by|deadline|closing date).*', text_lower)
    deadline = deadline_match.group() if deadline_match else "Not found"

    # Skills
    skills = extract_skills(text)

    return experience, deadline, skills



def process(url, description):

    results = []

    
    if url:
        jobs = scrape_jobs(url)

        if not jobs:
            return pd.DataFrame([{"Error": "No data found from URL"}])

        for job in jobs:
            text = job.get("title", "") + " " + job.get("description", "")
            text = clean_text(text)

            category = predict(text)
            experience, deadline, skills = extract_info(text)

            results.append({
                "Company": job.get("company", "N/A"),
                "Title": job.get("title", "N/A"),
                "Experience": experience,
                "Deadline": deadline,
                "Skills": skills,
                "Category": category
            })

    
    elif description:
        text = clean_text(description)

        category = predict(text)
        experience, deadline, skills = extract_info(description)

        results.append({
            "Company": "N/A",
            "Title": "From Text Input",
            "Experience": experience,
            "Deadline": deadline,
            "Skills": skills,
            "Category": category
        })

    else:
        return pd.DataFrame([{"Error": "Provide URL or Text"}])

    return pd.DataFrame(results)


app = gr.Interface(
    fn=process,
    inputs=[
        gr.Textbox(label="Enter Job URL"),
        gr.Textbox(label="Or Paste Job Description")
    ],
    outputs="dataframe",
    title="🔥 AI Job Scraper + Analyzer"
)

app.launch()