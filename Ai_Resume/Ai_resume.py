import os
from dotenv import load_dotenv
from openai import OpenAI
import fpdf
import markdown
from xhtml2pdf import pisa

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")


print("This is a python Dockerfile example")
print("Current working directory:", os.getcwd())
print("Current working directory:", __file__)




content = """

wtire an ats friendly resume for the following job description: with the following details:


Job Nature: Full time (40 hours) 

Designation: Associate Software Engineer
Salary Range: 50K-70K
Vacancy: 6-8
Experience: 0-2 years


About Orbitax

Orbitax is the world's leading international tax technology company, combining expert domain knowledge with industry leading technology, brought together by a talented team with diverse experiences, backgrounds and skills. Our extensive user base consists of tax and accounting professionals working for the largest multinationals, accounting firms and governments in the world.


Join Our Dev Team!

As an Associate Software Engineer, you will be joining a group of talented individuals and will help to build the best tax software of the world.


Job Responsibilities

You will actively seek opportunities for innovation, continuous improvement, and efficiency in all assigned tasks.
You will design, develop, modify, debug, and maintain software code based on functional, non-functional, and technical design specifications.
You will follow software engineering standards, development methodologies, and release processes to ensure code is maintainable, scalable, and supportable.
You will learn and apply new technologies as needed to support product requirements.
You will investigate issues by reviewing and debugging code, providing fixes and workarounds, and validating changes to ensure operability and maintainability of existing solutions.
You will write unit tests and basic automation scripts to ensure code stability and maintainability.
You will demonstrate proactive learning, participate in knowledge sharing, and contribute to team discussions.
You will maintain a positive, team-focused mindset while seeking mentorship and feedback to grow as a software engineer.


Skills and Qualifications

Bachelor’s degree in Computer Science, Computer Engineering, Software Engineering, or a related field.
Solid understanding of programming fundamentals, object-oriented programming (OOP), and core data structures and algorithms.
Strong analytical and problem-solving skills.
Experience with C#, .NET, Python, Go, Angular, MongoDB, RabbitMQ, Redis, and microservices architecture is a plus.
Familiarity with machine learning, data science, artificial intelligence (AI), or prompt engineering is an added advantage.
Good communication and collaboration skills, with a willingness to learn and adapt in a fast-paced environment.
Openness to constructive feedback and a mindset of continuous improvement in coding and problem-solving capabilities.


Benefits

Open, collaborative and empowering company culture 
Competitive salary and bonus structure.
Annual performance bonus 
Annual salary increments based on performance
Revenue sharing bonus
3 years DPS scheme
Health and Life Insurance
Two Annual Company Trips – One international and one domestic (domestic trip includes family).
State of the art office environment including indoor community space (Table Tennis, Pool, Foosball) & Gym room
Daily complimentary breakfast, lunch and evening meal
5 day work week 
17 days annual leave
Office Transportation Facilities
"""

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key,
)

completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  extra_body={},
  model="openrouter/cypher-alpha:free",
  # model="deepseek/deepseek-r1:free",
  messages=[
    {
      "role": "user",
      "content": content
    }
  ]
)

print(completion.choices[0].message.content,"\n\n\n\n\n\n")





# Convert Markdown to HTML
html = markdown.markdown(completion.choices[0].message.content)

# Optional: Add basic CSS for better style
html = f"""
<html>
<head>
<style>
body {{
    font-family: Arial, sans-serif;
    line-height: 1.5;
}}
h1, h2, strong {{
    color: #000;
}}
</style>
</head>
<body>
{html}
</body>
</html>
"""


# Save path (save to current script directory for easy access)
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, "resume_styled.pdf")

# Convert HTML to PDF
with open(save_path, "w+b") as result_file:
    pisa_status = pisa.CreatePDF(html, dest=result_file)

if pisa_status.err:
    print("❌ Failed to generate PDF")
else:
    print(f"✅ Styled Resume saved at: {save_path}")
