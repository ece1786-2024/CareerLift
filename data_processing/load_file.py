import json


def load_data():
    with open('data/processed_job_descriptions.json', "r") as file:
        input_jd = json.load(file)

    with open('data/processed_original_resumes.json', "r") as file:
        input_resume = json.load(file)

    with open('data/combined_json.json', "r") as file:
        rag_information = json.load(file)

    return input_jd, input_resume, rag_information