import os
import openai
import markdown
from weasyprint import HTML
from bs4 import BeautifulSoup
import json
from jinja2 import Template
from datetime import datetime
import sys
sys.path.append("/Users/calvinperumalla/personal/git/job_search_manager/jsm")
from api_key import api_key
from jsm.prompt_template import prompt_template

# Step 1: Tailor resume using GPT
def generate_resume_json(job_description, resume_text):
    prompt = prompt_template.format(
        resume_text=resume_text,
        job_description=job_description
    )

    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}]
    )


    content = response.choices[0].message.content
    # Try to parse JSON safely
    try:
        resume_json = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("GPT output was not valid JSON. Please re-run.")

    return resume_json, content

# ---- Step 2: Save JSON for manual editing ----
def save_resume_json(resume_json, filename="resume_output.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(resume_json, f, indent=2, ensure_ascii=False)


# ---- Step 3: Render HTML + Export PDF ----
def render_resume(resume_json, template_file="resume_template.html", css_file="resume.css", output_pdf="resume.pdf"):
    # Load HTML template
    with open(template_file, "r", encoding="utf-8") as f:
        template = Template(f.read())

    # Render template with GPT/edited JSON content
    html_content = template.render(**resume_json)

    # Generate PDF
    HTML(string=html_content, base_url=".").write_pdf(output_pdf, stylesheets=[css_file])
    print(f"✅ PDF saved as {output_pdf}")

def fine_tune_resume(jd_html, link_to_url):
    # read base resume
    print('reading base resume from file: /Users/calvinperumalla/personal/git/job_search_manager/jsm/jsm/base_resume/base_aug14_2025.txt')
    with open("/Users/calvinperumalla/personal/git/job_search_manager/jsm/jsm/base_resume/base_aug14_2025.txt", "r") as f:
        base_resume = f.read()
    print('success')

    # read a job description from a HTML file
    print('reading job description from file: ', jd_html)
    with open(jd_html, "r") as f:
        job_description = f.read()
        # parse the HTML to extract the job description text
        soup = BeautifulSoup(job_description, 'html.parser')
        text = soup.get_text(separator="\n")
        # Define markers
        start_marker = "About the job"
        end_marker = "More jobs"

        # Locate markers
        start_idx = text.find(start_marker)
        end_idx = text.find(end_marker, start_idx)

        # Extract section
        print('extracting job description section between markers:', start_marker, 'and', end_marker)
        job_text = text[start_idx:end_idx].strip() if start_idx != -1 and end_idx != -1 else "Section not found."

    with open("/Users/calvinperumalla/personal/git/job_search_manager/jsm/jsm/job_descriptions/last_job_description.txt", "w") as f:
        f.write(job_text + "\n\n" + "Link to job posting: " + link_to_url)

    print('success')
    total_words = len(job_text.split()) + len(base_resume.split())
    print('total number of words in job descriotion and base resume:', total_words)
    input_tkns = total_words * 1.5
    print(f'total tokens (approx): {input_tkns}')  # Rough estimate: 1.5 tokens per word
    #print("Job Description:", job_text)
    #print("Base Resume:", base_resume)

     # 1. Generate tailored JSON
    print('generating tailored resume JSON using GPT-5...')
    start = datetime.now()
    resume_json, content = generate_resume_json(job_text, base_resume)
    end = datetime.now()
    print('success, total time taken:', (end - start).total_seconds(), 'seconds')
    output_tkns = len(content.split()) * 1.5
    print("total number of tokens in response (approx):", output_tkns)  # Rough estimate: 1.5 tokens per word
    print(f"total cost of this API call (approx): ${input_tkns*(1.25/1e6) + output_tkns*(10/1e6)} USD") 


    # 2. Save JSON for manual review/editing
    file_id = datetime.now().strftime("%Y%m%d_%H%M")
    resume_json_pth = "/Users/calvinperumalla/personal/git/job_search_manager/jsm/jsm/resume_jsons/resume_output_{}.json".format(file_id)
    print('saving tailored resume JSON to file:', resume_json_pth)
    save_resume_json(resume_json, resume_json_pth)
    print('success')

    # 3. Save job description text to a file for reference
    jd_path = os.path.join(os.basepath(jd_html), f"jd_{file_id}.txt")

    # 4. Render PDF from JSON + template
    output_resume_path = "/Users/calvinperumalla/personal/git/job_search_manager/jsm/jsm/output_resumes/output_resume_{}.pdf".format(file_id)
    resume_tmplt_pth = "/Users/calvinperumalla/personal/git/job_search_manager/jsm/jsm/resume_template.html"
    css_tmplt_pth = "/Users/calvinperumalla/personal/git/job_search_manager/jsm/jsm/resume.css"
    print('rendering final tailored resume PDF to file:', output_resume_path)
    render_resume(resume_json, resume_tmplt_pth, css_tmplt_pth, output_resume_path)
    print('success')
