# !pip install -r requirements.txt
import json
import os

from data_processing.JD_processor import process_job_descriptions
from data_processing.resume_processor import process_original_resumes
# from data_processing.combined_processor import combined_processor
from data_processing.load_file import load_data
from LLM.index_builder import build_index, combine_text_list, retrieve_top_profiles
from LLM.prompts import InstructionGeneratorPrompt, system_prompt, instructionSecond, combined_system_prompt, LatexFormat
from LLM.LLM import get_response, test_llm_1, process_llm_output
from LLM.json_to_latex import transform_json_to_latex

# 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

def run_logic(api_key):
    # Set OpenAI API
    os.environ['OPENAI_API_KEY'] = api_key
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print("OPENAI_API_KEY is set:", api_key)
    else:
        print("OPENAI_API_KEY is not set.")

    # Raw Data Processing
    process_job_descriptions("data/Job_Description.csv", "data/processed_job_descriptions.json")
    process_original_resumes("data/original_resume.csv", "data/processed_original_resumes.json")

    # Process combined SCP and job descriptions (!ONLY USE IN TRAINING PROCESS)
    # combined_processor("data/title_scp_jd.csv", "data/combined_json.json")

    # Load Processed Data
    input_jd, input_resume, rag_information = load_data()

    # RAG
    index = build_index(rag_information)
    resume_data = input_resume["Original Resumes"][0]["ResumeJSON"]
    jd_data = input_jd["JobDescriptions"][0]["JDJSON"]

    combined_text_list = combine_text_list(resume_data, jd_data)
    top_profile = retrieve_top_profiles(index, combined_text_list)

    # LLM 1
    data_zero_round = json.dumps({
        "original_resume": resume_data,
        "Job_description": jd_data,
        "Success_candidate_profile": top_profile
    })

    general_advice = get_response(InstructionGeneratorPrompt, data_zero_round)
    general_advice = general_advice.strip("```json").strip("```").strip()

    data_first_round = json.dumps({
        "original_resume": resume_data,
        "Job_description": jd_data,
        "Advise": general_advice
    })

    instruction_first_round = " Given the inputs be two json file, original resumes, job description and incorporate advice from successful candidate. give output revised resume and career development advice."
    first_round_system_prompt = system_prompt + "\n" + instruction_first_round
    optimized_output = test_llm_1(first_round_system_prompt, data_first_round)
    optimized_output = process_llm_output(optimized_output)

    # LLM 2
    data_LLM2 = json.dumps({
        "original_resume": resume_data,
        "revised_resume": optimized_output["revised_resume"],
        "skills_to_improve": optimized_output["career_development_advice"]
    })

    AISuggestion = test_llm_1(instructionSecond, data_LLM2)

    data_second_round = json.dumps({
        "original_resume": resume_data,
        "Job_description": jd_data,
        "Advise": general_advice,
        "revised_resume": optimized_output['revised_resume'],
        "career_development_advice": optimized_output['career_development_advice'],
        "suggestion": AISuggestion  # output from suggestion
    })

    # Get Result
    Result_JSON = test_llm_1(combined_system_prompt, data_second_round)

    if Result_JSON.startswith("```json"):
        Result_JSON = Result_JSON[len("```json"):].strip()
    if Result_JSON.endswith("```"):
        Result_JSON = Result_JSON[:-len("```")].strip()

    with open("data/Result_JSON.json", "w", encoding="utf-8") as f:
        f.write(Result_JSON)

    # Get Resume
    with open("data/Result_JSON.json", 'r', encoding='utf-8') as file:
        RESULT = json.load(file)

    resume_json = RESULT["Revised Resumes"][0]["ResumeJSON"]

    with open("data/Result_Resume.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(resume_json, indent=4))

    print("Resume has been saved in 'Result_Resume.json'")

    # Change Format
    with open('data/Result_Resume.json', "r") as file:
        json_str = json.load(file)

    Result_Resume_latex = transform_json_to_latex(LatexFormat, f'''{json_str}''')

    if Result_Resume_latex.startswith("```latex"):
        Result_Resume_latex = Result_Resume_latex[len("```latex"):].strip()
    if Result_Resume_latex.endswith("```"):
        Result_Resume_latex = Result_Resume_latex[:-len("```")].strip()

    with open("data/Result_Resume.tex", "w", encoding="utf-8") as file:
        file.write(Result_Resume_latex)

    print(f"LaTeX has been saved as Result_Resume.tex")

    # Get Advice
    advice_json = RESULT["Career Development Advise"]

    with open('data/Result_Advice.txt', 'w') as text_file:
        for advice in advice_json:
            skill = advice.get("Skill", "Unknown Skill")
            tips = advice.get("Advice", [])
            text_file.write(f"Skill: {skill}\n")
            for tip in tips:
                text_file.write(f"- {tip}\n")
            text_file.write("\n")

    print("Career Development Advise has been saved in 'Result_Advice.txt'")

    with open("data/Result_Advice.txt", "r", encoding="utf-8") as file:
        advice_text = file.read()

    return advice_text