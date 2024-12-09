from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from logic_runner import run_logic
import csv
import os

app = Flask(__name__)
CORS(app)

last_result = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process_form():
    global last_result

    # Extracting Data
    job_description = request.form.get('jobDescription', '')
    resume_data = request.form.get('resumeData', '')
    # llm_provider = request.form.get('llmProvider', '')
    api_key = request.form.get('apiKey', '')
    role_selection = request.form.get('roleSelection', '')
    action = request.form.get('action', '')

    if action == 'Run CareerLift':
        # Write Data
        data = []
        with open("data/Job_Description.csv", "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(row)
        data[1][0] = role_selection
        data[1][1] = job_description
        with open("data/Job_Description.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(data)

        data = []
        with open("data/original_resume.csv", "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(row)
        data[1][0] = resume_data
        with open("data/original_resume.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(data)

        result = run_logic(api_key)

        last_result = result
        RESULT = ("Program execution completed! \n"
                  "Press Get Resume / Get Advice")

    elif action == 'Get Resume':
        if last_result is not None:
            download_url = request.host_url.rstrip('/') + '/download_tex'
            RESULT = "Click the button below to download the generated Latex file."
            return jsonify({'combinedData': RESULT, 'download_url': download_url})

        else:
            RESULT = "No previous result available. Please press 'Run CareerLift' first."
            return jsonify({'combinedData': RESULT})

    elif action == 'Get Advice':
        if last_result is not None:
            RESULT = last_result
        else:
            RESULT = "No previous result available. Please press 'Run CareerLift' first."

    else:
        RESULT = "Unknown action."

    return jsonify({'combinedData': RESULT})


@app.route('/download_tex', methods=['GET'])
def download_tex():
    tex_file_path = "data/Result_Resume.tex"
    if os.path.exists(tex_file_path):
        return send_file(tex_file_path,
                         mimetype='text/plain',
                         as_attachment=True,
                         download_name='Result_Resume.tex')
    else:
        return "File not found", 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)
