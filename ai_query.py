import openai

def jobQuery(api_key, base_url, model_name, base_query, criteria, company, job_desc):
    client = openai.OpenAI(api_key=api_key, base_url=base_url)

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": f"{base_query}\nJob Criteria: {criteria}\nCompany: {company}\nJob Description: {job_desc}"}
        ],
        temperature=0,
        stream=False
    )

    return response.choices[0].message.content.strip() == 'true'

def jobSummary(api_key, base_url, model_name, company, job_desc, link):
    client = openai.OpenAI(api_key=api_key, base_url=base_url)

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": f"Summarize the following job description in 2 or 3 sentences. Do not add any extra fluff about the company or any extra whitespace. Just talk about the requirements for the job. Additionally, don't make up any information.\nJob Description: {job_desc}"}
        ],
        temperature=0.5,
        stream=False
    )
    desc_summary = response.choices[0].message.content
    return f"**Company**: {company}\n**Summary**: {desc_summary}\nLink: [View on LinkedIn]({link})"
