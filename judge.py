from prompts import JUDGE_PERSONA
from openai import OpenAI
import json


class Judge:
    # The input should be in JSON format
    def __init__(self, revised_resume, original_resume, job_description, API_KEY):
        self.revised_resume = revised_resume
        self.job_description = job_description
        self.original_resume = original_resume
        self.persona = JUDGE_PERSONA
        try:
            with open('evaluation_0.txt', 'r', encoding='utf-8') as file:
                self.metrics = file.read()
        except FileNotFoundError:
            print("The file 'evaluation_0.txt' was not found.")
        except IOError as e:
            print(f"An error occurred: {e}")

        self.client = OpenAI(api_key=API_KEY)
        self.data = json.dumps({"revised resume": self.revised_resume, "original resume": self.original_resume,
                                "job description": self.job_description})

    def get_response(self):
        user_prompt = "Here is the JSON file of the revised resume, original resume, and the job description:\n" + self.data

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": [{"type": "text", "text": self.persona}]},
                {"role": "assistant", "content": [{"type": "text", "text": self.metrics}]},
                {"role": "user", "content": [{"type": "text", "text": user_prompt}]},
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content


# ------------------------------------------test case------------------------------------------
with open('processed_original_resumes.json', 'r') as file:
    original_resume = json.load(file)

with open('processed_job_descriptions.json', 'r') as file:
    job_description = json.load(file)

with open('revised_resumes.json', 'r') as file:
    revised_resume = json.load(file)

OPENAI_API_KEY = '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'

judge = Judge(revised_resume, original_resume, job_description, OPENAI_API_KEY)
score = judge.get_response()

print(score)

with open('test_score_0', 'w', encoding='utf-8') as file:
    file.write(score)
