import pandas as pd
import openai
import json
import re

def sanitize_text(text):
    """
    Sanitize text by escaping backslashes and removing invalid control characters.
    """
    if isinstance(text, str):
        text = text.replace("\\", "\\\\")  # Escape backslashes
        text = re.sub(r"[\x00-\x1F\x7F]", " ", text)  # Remove invalid control characters
    return text

def process_scp_and_job_descriptions(file_path, start_row, end_row, output_path):
    df = pd.read_csv(file_path)

    if 'Resume' not in df.columns or 'Job Description' not in df.columns or 'Job Title' not in df.columns:
        raise ValueError("The uploaded file must have 'Title', 'Resume', and 'Job Description' columns.")

    # Ensure the row indices are valid
    if start_row < 0 or end_row > len(df) or start_row >= end_row:
        raise ValueError("Invalid start_row and end_row indices.")


    # Preprocess the data
    df['Job Title'] = df['Job Title'].apply(sanitize_text)
    df['Resume'] = df['Resume'].apply(sanitize_text)
    df['Job Description'] = df['Job Description'].apply(sanitize_text)

    # Select the specified range of rows
    df = df.iloc[start_row:end_row]

    combined_json = []

    # Loop through each row in the DataFrame
    for index, row in df.iterrows():
        job_title = row['Job Title']
        resume_text = row['Resume']
        job_description_text = row['Job Description']

        # Generate JSON for the resume
        resume_prompt = f"""
        The following text is a resume. Categorize its content into four parts as JSON without altering the original text:
        - "Education": Text related to degrees, schools, or certifications.
        - "Experience": Text related to job roles, companies, or work descriptions.
        - "Skills": Text listing technical proficiencies or skills.
        - "Projects": Text describing project details or achievements.

        Provide only the JSON object in your response, without any additional explanation. Do not modify the text content; just categorize it. For example:

        {{
            "Education": "Original text for education here",
            "Experience": "Original text for experience here",
            "Skills": "Original text for skills here",
            "Projects": "Original text for projects here"
        }}

        Resume: {resume_text}
        """

        # Generate JSON for the job description
        jd_prompt = f"""
        The following text is a job description. Categorize its content into four parts as JSON without altering the original text:
        - "Role": Text related to job roles or work descriptions.
        - "Qualification": Text related to key qualifications required for the role.

        Provide only the JSON object in your response, without any additional explanation. Do not modify the text content; just categorize it. For example:

        {{
            "Role": "Original text for role here",
            "Qualification": "Original text for qualifications here"
        }}

        Job Description: {job_description_text}
        """

        try:
            # Parse the resume using OpenAI
            resume_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert in resume parsing."},
                    {"role": "user", "content": resume_prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            # Parse the job description using OpenAI
            jd_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert in parsing job descriptions."},
                    {"role": "user", "content": jd_prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            # Extract and parse JSON from both responses
            resume_content = resume_response['choices'][0]['message']['content'].strip()
            jd_content = jd_response['choices'][0]['message']['content'].strip()

            resume_parsed_json = json.loads(resume_content)
            jd_parsed_json = json.loads(jd_content)

            # Combine the parsed JSON
            combined_json.append({
                "job_title": job_title,
                "resume": resume_parsed_json,
                "job_description": jd_parsed_json
            })

        except Exception as e:
            # Log errors for this row
            combined_json.append({
                "job_title": job_title,
                "error": str(e)
            })

    # Save the consolidated JSON output
    #output_path = "processed_combined_scp_and_jd.json"
    with open(output_path, "w") as f:
        json.dump(combined_json, f, indent=4)

    print(f"Processing complete. Results saved to {output_path}.")

def combined_processor(file_path, output_file):
    process_scp_and_job_descriptions(file_path, start_row=0, end_row=20,
                                     output_path="output/processed_combined_scp_and_jd_DS.json")
    process_scp_and_job_descriptions(file_path, start_row=20, end_row=40,
                                     output_path="output/processed_combined_scp_and_jd_MLE.json")
    process_scp_and_job_descriptions(file_path, start_row=40, end_row=60,
                                     output_path="output/processed_combined_scp_and_jd_SDE.json")

    files = [
        "output/processed_combined_scp_and_jd_DS.json",
        "output/processed_combined_scp_and_jd_MLE.json",
        "output/processed_combined_scp_and_jd_SDE.json"
    ]

    # Combine the JSON files
    combined_data = []

    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            combined_data.extend(data)  # Add the content of each file to the list

    # Save the combined data to a new JSON file
    with open(output_file, 'w') as f:
        json.dump(combined_data, f, indent=4)

    print(f"Combined JSON file saved as {output_file}")