import pandas as pd
from openai import OpenAI
import json

def process_original_resumes(file_path, output_path):
    df = pd.read_csv(file_path)

    if 'Original Resume' not in df.columns:
        raise ValueError("The uploaded file must have a column named 'Original Resume'.")

    all_resumes_json = []

    # Loop through each resume in the DataFrame
    for index, row in df.iterrows():
        resume_text = row['Original Resume']

        prompt = f"""
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
        client = OpenAI()
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert in resume parsing."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            content = response.choices[0].message.content.strip()

            try:
                parsed_json = json.loads(content)
            except json.JSONDecodeError:
                # If parsing fails, include the raw content as a string
                parsed_json = {"RawResponse": content}

            # Append the parsed or raw result to the list
            all_resumes_json.append({
                "ResumeIndex": index,
                "ResumeJSON": parsed_json
            })

        except Exception as e:
            # Log errors for this resume
            all_resumes_json.append({
                "ResumeIndex": index,
                "Error": str(e)
            })

    # Save the consolidated JSON output
    with open(output_path, "w") as f:
        json.dump({"Original Resumes": all_resumes_json}, f, indent=4)

    print(f"Processing complete. Results saved to {output_path}.")