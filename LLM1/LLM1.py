# Read Json File
import json
from openai import OpenAI

with open('processed_job_descriptions.json', "r") as file:
    processed_job_descriptions = json.load(file)

with open('processed_original_resumes.json', "r") as file:
    processed_original_resumes = json.load(file)
    
with open('system_prompt', "r", encoding="utf-8") as file:
    system_prompt = file.read()

# User Prompt
user_prompt = f"""I am a highly experienced career advisor and resume writing expert with 15 years of specialized experience.

    Primary role: Craft exceptional resumes and cover letters tailored to specific job descriptions, optimized for both ATS systems and human readers.
    
    # Instructions for creating optimized resumes and cover letters
    1. Analyze job descriptions:
       - Extract key requirements and keywords
       - Note: Adapt analysis based on specific industry and role
    
    2. Create compelling resumes:
       - Highlight quantifiable achievements (e.g., "Engineered a dynamic UI form generator using optimal design patterns and efficient OOP, reducing development time by 87.5%")
       - Tailor content to specific job and company
       - Emphasize candidate's unique value proposition
    
    3. Craft persuasive cover letters:
       - Align content with targeted positions
       - Balance professional tone with candidate's personality
       - Use a strong opening statement, e.g., "As a marketing professional with 7 years of experience in digital strategy, I am excited to apply for..."
       - Identify and emphasize soft skills valued in the target role/industry. Provide specific examples demonstrating these skills
    
    4. Optimize for Applicant Tracking Systems (ATS):
       - Use industry-specific keywords strategically throughout documents
       - Ensure content passes ATS scans while engaging human readers
    
    5. Provide industry-specific guidance:
       - Incorporate current hiring trends
       - Prioritize relevant information (apply "6-second rule" for quick scanning)
       - Use clear, consistent formatting
    
    6. Apply best practices:
       - Quantify achievements where possible
       - Use specific, impactful statements instead of generic ones
       - Update content based on latest industry standards
       - Use active voice and strong action verbs
    
    Note: Adapt these guidelines to each user's specific request, industry, and experience level.
    
    Goal: Create documents that not only pass ATS screenings but also compellingly demonstrate how the user can add immediate value to the prospective employer.
    
    Return your output strictly in the following JSON format:
    {{
        "Revised Resumes": [
            {{
                "ResumeIndex": 0,
                "ResumeJSON": {{
                    "Education": [
                        {{
                            "Degree": "",
                            "Institution": "",
                            "CGPA": ""
                        }}
                    ],
                    "Experience": [
                        {{
                            "Role": "",
                            "Company": "",
                            "Description": ""
                        }}
                    ],
                    "Skills": [
                        ""
                    ],
                    "Projects": [
                        {{
                            "Project": "",
                            "Describe": ""
                        }}
                    ]
                }}
            }}
        ],
        "Career Development Advise": [
            {{
                "Skill": "",
                "Advice": [
                    ""
                ]
            }}
        ]
    }}
    
    Given the following inputs:

    Original Resume:
    {json.dumps(processed_original_resumes, indent=2)}

    Job Description:
    {json.dumps(processed_original_resumes, indent=2)}
"""

# RUN
client = OpenAI()

def test_llm_1(system_content, user_content):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]
    )

    return response.choices[0].message.content

optimized_output = test_llm_1(system_prompt, user_prompt)

# Save
output = optimized_output.strip("```json").strip("```").strip()

try:
    optimized_data = json.loads(output)
except json.JSONDecodeError:
    print("Error: The API response is not valid JSON.")
    print("Raw Output:", output)
    optimized_data = None

if optimized_data:
    with open("revised_resumes.json", "w") as f:
        json.dump(optimized_data["Revised Resumes"], f, indent=4)

    with open("career_development_advise.json", "w") as f:
        json.dump(optimized_data["Career Development Advise"], f, indent=4)

    print("Files 'revised_resumes.json' and 'career_development_advise.json' have been saved successfully!")
else:
    print("No valid data to save.")