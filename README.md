
# CareerLift: An Intelligent Resume Enhancement Tool Powered by Large Language Models. 
CareerLift helps job seekers optimize their resumes by analyzing them against successful candidate profiles and specific job requirements, while also providing actionable career development advice. The tool leverages a feedback loop to ensure the reliability of its outputs, increasing candidates' chances of securing desired roles.

---
![img.png](static/img.png)
## Features

- **Intelligent Resume Optimization**: Analyzes original resumes and job descriptions to produce highly tailored and impactful resumes.
- **Career Development Suggestions**: Offers specific, actionable advice to support long-term career planning.
- **Iterative Feedback Mechanism**: Continuously refines resumes through multiple rounds to ensure professional quality and relevance.
- **Data-Driven Matching**: Uses 60 successful candidate profiles as benchmarks to deliver personalized recommendations.

---

## User Interface

The web interface provides an intuitive way to interact with CareerLift:

1. **Input Fields**:
   - Paste job descriptions and resumes in plain text.
   - Upload raw or related data directly.

2. **LLM Provider Selection**:
   - Choose from supported LLMs (e.g., OpenAI).

3. **Role Selection**:
   - Specify the target role (e.g., SDE, DS, MLE).

4. **API Key**:
   - Securely input your API key for LLM access.

5. **Actions**:
   - **Get Resume**: Generates a tailored resume.
   - **Get Advice**: Provides actionable career advice.
   - **Run CareerLift**: Runs the complete pipeline for both resume and advice.

6. **Results**:
   - The results, including optimized resumes and advice, are displayed directly in the interface.

---

## Installation

### Requirements

- Python 3.10+
- Required Python packages are listed in `requirements.txt`.

### Installation Steps

1. Clone the project repository:

   ```bash
   git clone https://github.com/your-repo/CareerLift.git
   cd CareerLift
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```


---

## Usage

### Running the Application

1. Start the application by running `app.py`:

   ```bash
   python app.py
   ```

2. Open the application in your browser:
   - Default URL: `http://127.0.0.1:5000`

3. Use the interface to input job descriptions and resumes, and obtain outputs such as:
   - Optimized Resume (`Result_Resume.json`)
   - Career Advice (`Result_Advice.txt`)

---



## Contributing

We welcome all contributions! If you have ideas or improvements, please submit an [Issue](https://github.com/your-repo/CareerLift/issues) or create a Pull Request.

---

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

