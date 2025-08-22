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

    return resume_json

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

# Example Usage
if __name__ == "__main__":
    # read base resume
    with open("/Users/calvinperumalla/personal/git/job_search_manager/jsm/jsm/base_resume/base_aug14_2025.txt", "r") as f:
        base_resume = f.read()

    # read a job description from a HTML file
    with open("/Users/calvinperumalla/personal/git/job_search_manager/jsm/jsm/job_descriptions/(17) Signal Processing Engineer _ Autonomous Healthcare _ LinkedIn.html", "r") as f:
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
        job_text = text[start_idx:end_idx].strip() if start_idx != -1 and end_idx != -1 else "Section not found."
    
    print('total number of words in job descriotion and base resume:', len(job_description.split()) + len(base_resume.split()))
    #print("Job Description:", job_text)
    #print("Base Resume:", base_resume)

     # 1. Generate tailored JSON
    resume_json = generate_resume_json(job_text, base_resume)

    # 2. Save JSON for manual review/editing
    file_id = datetime.now().strftime("%Y%m%d_%H%M")
    resume_output_path = "/Users/calvinperumalla/personal/git/job_search_manager/jsm/jsm/resume_jsons/resume_output_{}.json".format(file_id)
    resume_json_pth = "/Users/calvinperumalla/personal/git/job_search_manager/jsm/jsm/resume_jsons/resume_output.json"
    save_resume_json(resume_json, resume_json_pth)

    # 3. Render PDF from JSON + template
    output_resume_path = "/Users/calvinperumalla/personal/git/job_search_manager/jsm/jsm/output_resumes/output_resume_{}.pdf".format(file_id)
    resume_tmplt_pth = "/Users/calvinperumalla/personal/git/job_search_manager/jsm/jsm/resume_template.html"
    css_tmplt_pth = "/Users/calvinperumalla/personal/git/job_search_manager/jsm/jsm/resume.css"
    render_resume(resume_json, resume_tmplt_pth, css_tmplt_pth, output_resume_path)