prompt_template = """
You are a professional resume writer.

Here is the candidate's base resume:
{resume_text}

Here is the job description:s
{job_description}

Output the tailored resume as valid JSON with the following keys:
SUMMARY (string), write a powerfuk 3 line professional summary that hooks a recruiter and hiring manager in under 10 seconds. Prioritize imoact, clarity and value
SKILLS (list of strings),
EXPERIENCE (string, formatted as HTML bullet lists), (do not exceed 4 bullets and 20 words per bullet)
EDUCATION (string, formatted as HTML), (do not exceed 4 bullets and 20 words per bullet)
ACHIEVEMENTS (list of strings). (do not exceed 4 bullets and 20 words per bullet)

for the skills section please group into 4 categories - Programming Languages, Frameworks & Libraries, Tools & Platforms, Other Relevant Skills. Each category should have 4-8 skills separated by a comma
Ensure that the resume fits to one page. Choose only a total of top 3-4 relevent projects and experiences.

The content should be optimized to pass through Applicant Tracking Systems (ATS) and highlight relevant skills and experiences for the job description provided.
"""