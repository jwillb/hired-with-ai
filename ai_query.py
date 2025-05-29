import openai

def jobQuery(api_key, base_url, model_name, criteria, company, job_desc):
    client = openai.OpenAI(api_key=api_key, base_url=base_url)
    query_string = f"I am looking for a job in my field. I am going to give you a description of a job and you need to tell me if the job fits my criteria. Respond with 'true' if it fits or 'false' if it does not. Additionally, write a short phrase about why it does or does not fit, separated from the boolean with only a newline character. The criteria will come first and the job description will follow.\nJob Criteria: {criteria}\nCompany: {company}\nJob Description: {job_desc}"

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": query_string}
        ],
        temperature=0,
        stream=False
    )

    return response.choices[0].message.content[:4].strip() == 'true', response.choices[0].message.content.split('\n')[1]

def jobSummary(api_key, base_url, model_name, company, job_desc, link):
    client = openai.OpenAI(api_key=api_key, base_url=base_url)

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": f"Summarize the following job description in 2 or 3 sentences. Do not add any extra fluff about the company or any extra whitespace. Just talk about the requirements for the job. Additionally, don't make up any information.\nJob Description: {job_desc}"}
        ],
        temperature=0.5,
        stream=False
    )
    desc_summary = response.choices[0].message.content
    return f"**Company**: {company}\n**Summary**: {desc_summary}\nLink: [View on LinkedIn]({link})"
