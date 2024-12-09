import pandas as pd
from openai import OpenAI
import json

def process_job_descriptions(file_path, output_path):
    df = pd.read_csv(file_path)

    if 'JD' not in df.columns or 'Title' not in df.columns:
        raise ValueError("The uploaded file must have 'Title' and 'JD' columns.")

    all_jd_json = []

    # Loop through each job description in the DataFrame
    for index, row in df.iterrows():
        jd_title = row['Title']
        jd_text = row['JD']

        prompt = f"""
        The following text is a job description. Categorize its content into four parts as JSON without altering the original text:
        - "Role": Text related to job roles or work descriptions.
        - "Qualification": Text related to key qualifications required for the role.

        Provide only the JSON object in your response, without any additional explanation. Do not modify the text content; just categorize it. For example:

        {{
            "Role": "Original text for role here",
            "Qualification": "Original text for qualifications here"
        }}

        Job Description: {jd_text}
        """
        client = OpenAI()
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert in parsing job descriptions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )

            content = response.choices[0].message.content.strip()

            try:
                parsed_json = json.loads(content)
                parsed_json['Title'] = jd_title  # Include the title in the JSON
            except json.JSONDecodeError:
                # If parsing fails, include the raw content as a string
                parsed_json = {"RawResponse": content, "Title": jd_title}

            # Append the parsed or raw result to the list
            all_jd_json.append({
                "JDIndex": index,
                "JDJSON": parsed_json
            })

        except Exception as e:
            # Log errors for this job description
            all_jd_json.append({
                "JDIndex": index,
                "Error": str(e),
                "Title": jd_title
            })

    # Save the consolidated JSON output
    with open(output_path, "w") as f:
        json.dump({"JobDescriptions": all_jd_json}, f, indent=4)

    print(f"Processing complete. Results saved to {output_path}.")