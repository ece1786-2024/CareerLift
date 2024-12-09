import json

from openai import OpenAI


def get_response(persona, data):
    client = OpenAI()
    user_prompt = "Here are the json files of the job description and the corresponding successful candidate profile:\n" + data
    response = client.chat.completions.create(
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


def test_llm_1(system_content, user_content):
    client = OpenAI()
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def process_llm_output(output):
    """
    Processes the LLM output and extracts the revised resume and career development advice.

    Args:
        optimized_output (str): The output string from the LLM, assumed to be JSON-formatted.

    Returns:
        dict: A dictionary containing:
            - "revised_resume": The revised resume (if available).
            - "career_development_advice": The career development advice (if available).
            - "error": Error message if the output is invalid or missing.
    """
    output = output.strip("```json").strip("```").strip()
    if output:
        try:
            # Parse the JSON output from the LLM
            first_round_results = json.loads(output)

            # Extract individual parts
            revised_resume = first_round_results.get("Revised Resumes")
            career_development_advice = first_round_results.get("Career Development Advise")

            return {
                "revised_resume": revised_resume,
                "career_development_advice": career_development_advice,
                "error": None
            }
        except json.JSONDecodeError as e:
            return {
                "revised_resume": None,
                "career_development_advice": None,
                "error": f"Failed to parse JSON: {str(e)}"
            }
    else:
        return {
            "revised_resume": None,
            "career_development_advice": None,
            "error": "Failed to get valid response from the LLM"
        }
