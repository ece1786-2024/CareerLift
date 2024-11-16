from prompts import ADVISOR_PERSONA
from openai import OpenAI
import json


class Advisor:
    def __init__(self, job_description, successful_candidate_resume,API_KEY):
        self.job_description = job_description
        self.successful_candidate_resume = successful_candidate_resume
        self.client = OpenAI(api_key=API_KEY)
        self.data = json.dumps({"job description": self.job_description, "successful candidate resume": self.successful_candidate_resume})

    def get_response(self, persona):
        user_prompt = "Here are the json files of the job description and the corresponding successful candidate profile:\n" + self.data
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": [{"type": "text", "text": persona}]},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_prompt
                        }
                    ]
                },
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content


with open('processed_original_resumes.json', 'r') as file:
    original_resume = json.load(file)


with open('processed_job_descriptions.json', 'r') as file:
    job_description = json.load(file)


OPENAI_API_KEY = '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'
advisor = Advisor(job_description, original_resume,OPENAI_API_KEY)
respond = advisor.get_response(ADVISOR_PERSONA)
print(respond)
