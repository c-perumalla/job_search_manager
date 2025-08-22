import openai
import markdown
from weasyprint import HTML
from bs4 import BeautifulSoup
import json
from jinja2 import Template
from datetime import datetime

resume_json = "/Users/calvinperumalla/personal/git/job_search_manager/jsm/jsm/resume_jsons/resume_output.json"

def render_resume(resume_json_filepath, template_file="resume_template.html", css_file="resume.css", output_pdf="resume.pdf"):

    resume_json = json.load(open(resume_json_filepath, "r", encoding="utf-8"))
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
    # 3. Render PDF from JSON + template
    resume_tmplt_pth = "/Users/calvinperumalla/personal/git/job_search_manager/jsm/jsm/resume_template.html"
    css_tmplt_pth = "/Users/calvinperumalla/personal/git/job_search_manager/jsm/jsm/resume.css"
    file_id = datetime.now().strftime("%Y%m%d_%H%M")
    output_resume_path = "/Users/calvinperumalla/personal/git/job_search_manager/jsm/jsm/output_resumes/output_resume_{}.pdf".format(file_id)
    render_resume(resume_json, resume_tmplt_pth, css_tmplt_pth, output_resume_path)