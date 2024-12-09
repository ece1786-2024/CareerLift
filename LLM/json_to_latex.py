from openai import OpenAI

def transform_json_to_latex(LatexFormat, json_str):
    client = OpenAI()
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": LatexFormat},
                {"role": "user", "content": json_str}
            ],
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
