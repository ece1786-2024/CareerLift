document.addEventListener("DOMContentLoaded", () => {
    const jobDescriptionInput = document.getElementById("job-description");
    const resumeUploadInput = document.getElementById("resume-upload");
    const charLimitElems = document.querySelectorAll(".char-limit");
    const apiKeyInput = document.getElementById("api-key");
    const toggleVisibilityButton = document.querySelector(".toggle-visibility");
    const resultContent = document.getElementById("result-content");
    const roleSelectionInput = document.getElementById("role-selection");
    const resumeForm = document.getElementById("resume-form");

    const updateCharCount = (inputElement, charLimitElem) => {
        charLimitElem.textContent = `${inputElement.value.length}/${inputElement.maxLength}`;
    };

    updateCharCount(jobDescriptionInput, charLimitElems[0]);
    updateCharCount(resumeUploadInput, charLimitElems[1]);

    jobDescriptionInput.addEventListener("input", () => updateCharCount(jobDescriptionInput, charLimitElems[0]));
    resumeUploadInput.addEventListener("input", () => updateCharCount(resumeUploadInput, charLimitElems[1]));

    toggleVisibilityButton.addEventListener("click", () => {
        if (apiKeyInput.type === "password") {
            apiKeyInput.type = "text";
            toggleVisibilityButton.textContent = "🙈";
        } else {
            apiKeyInput.type = "password";
            toggleVisibilityButton.textContent = "👁️";
        }
    });

    const defaultJobDescription = `Roles:
Design, build, and maintain highly scalable, robust, and efficient cloud infrastructure using Google Cloud Platform (GCP) services, including Vertex AI, BigTable, BigQuery, and Cloud Composer.
Develop automation and orchestration of ML pipelines, integrating data ingestion, feature engineering, training, and deployment processes.
Collaborate with cross-functional teams to understand their needs and build solutions that improve platform usability, scalability, and the overall development experience.
Optimize data processing pipelines and cloud resources to ensure low-latency, cost-effective operation.
Implement monitoring, alerting, and failover strategies to ensure platform reliability.
Stay updated with industry trends and best practices in cloud engineering, data engineering, and machine learning

Qualifications:
Customer-centric mindset: Passionate about delivering an exceptional experience for data scientists through a self-service platform, reducing friction in their workflows.
Collaboration: Strong communication skills to work closely with cross-functional teams, including data scientists and engineers, to ensure platform features meet user needs and expectations.
Problem-solving: Ability to identify and solve complex technical issues related to ML pipelines, cloud infrastructure, and scalability, ensuring an efficient and robust platform.
Automation-first approach: Commitment to streamlining and automating processes for scalability and reliability, enabling data scientists to focus on experimentation and model development.
Adaptability: Ability to quickly adjust to new technologies and evolving platform needs to keep the infrastructure cutting-edge and efficient.
Ownership and initiative: Comfortable taking ownership of key platform components, driving innovation and improvements that benefit the platform’s scalability and usability.
Bachelor’s or Master’s degree in Computer Science, Engineering, or a related field.
2+ years of experience in software engineering with a focus on cloud infrastructure and/or data engineering.
Hands-on experience with Google Cloud Platform services such as Vertex AI, BigTable, BigQuery, Cloud Composer, Cloud Storage, etc.
Proficiency in one or more programming languages such as Python, Java, and SQL.
Experience with orchestration tools such as Apache Airflow (Composer).
Knowledge of CI/CD pipelines and DevOps tools for continuous integration and deployment.
Familiarity with containerization and orchestration (Docker, Kubernetes).
Strong problem-solving skills and attention to detail.
Excellent communication skills and ability to work in a collaborative, fast-paced environment`;

    const defaultResumeData = `Education
Honors Bachelor of Science in Physics, Minor in Computing
Institution: University of Waterloo

Skills
Programming Languages: Python (pandas, numpy, scipy, scikit-learn, matplotlib), SQL, Java, JavaScript (including jQuery)
Machine Learning: Regression, SVM, Naïve Bayes, KNN, Random Forest, Decision Trees, Boosting techniques, Cluster Analysis, Word Embedding, Sentiment Analysis, NLP, Dimensionality Reduction, Topic Modeling (LDA, NMF), PCA, Neural Networks
Database & Visualization Tools: MySQL, SQL Server, Cassandra, HBase, Elasticsearch, D3.js, DC.js, Plotly, Kibana, matplotlib, ggplot, Tableau
Other Tools/Technologies: Regular Expressions, HTML, CSS, Angular 6, Logstash, Kafka, Flask, Git, Docker, OpenCV, Deep Learning concepts

Experience
Data Science Assurance Associate – Ernst & Young LLP
Fraud Investigations & Dispute Services
Technology Assisted Review (TAR):
Developed an automated review platform implementing predictive coding and topic modeling, reducing review costs and time.
Conducted R&D on classification models, predictive analysis, and text data mining for fraud detection.
Tools: Python, scikit-learn, tfidf, word2vec, doc2vec, Naïve Bayes, LDA, NMF, Tableau
Multiple Data Science Projects for USA Clients:
Text Analytics (Motor Vehicle Customer Reviews):
Performed sentiment analysis and time-series analysis on survey data.
Created visualizations like heat maps, word clouds, and Tableau dashboards.
Tools: Python, NLP (NLTK, spacy), scikit-learn, Tableau
Chatbot Development:
Designed a chatbot to handle customer queries, build question pipelines, and provide recommendations.
Tools: Python, JavaScript, SQL Server, NLP, topic modeling
Information Governance:
Scanned and analyzed unstructured data for metadata extraction and indexing in Elasticsearch.
Conducted ROT (Redundant, Outdated, Trivial) analysis and full-text search for identifying PII.
Tools: Python, Flask, Elasticsearch, Kibana
Fraud Analytic Platform (FAP):
Developed a platform for fraud detection using advanced analytics for ERP systems.
Tools: HTML, JavaScript, SQL Server, jQuery, Bootstrap, D3.js, DC.js`;

    const autofillJobDescBtn = document.getElementById("autofill-job-desc");

    autofillJobDescBtn.addEventListener("click", () => {
        jobDescriptionInput.value = defaultJobDescription;
        resumeUploadInput.value = defaultResumeData;

        updateCharCount(jobDescriptionInput, charLimitElems[0]);
        updateCharCount(resumeUploadInput, charLimitElems[1]);
    });

    resumeForm.addEventListener("submit", (event) => {
        event.preventDefault();

        const jobDescription = jobDescriptionInput.value.trim();
        const resumeData = resumeUploadInput.value.trim();
        const llmProvider = document.getElementById("llm-provider").value;
        const apiKey = apiKeyInput.value.trim();
        const roleSelection = roleSelectionInput.value.trim();
        const action = event.submitter.textContent.trim();

        const downloadContainer = document.getElementById("download-container");
        downloadContainer.innerHTML = "";

        if (!jobDescription || !resumeData || !apiKey) {
            alert("Please ensure all required fields are completed!");
            return;
        }

        fetch("http://127.0.0.1:5000/process", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({
                jobDescription: jobDescription,
                resumeData: resumeData,
                llmProvider: llmProvider,
                apiKey: apiKey,
                action: action,
                roleSelection: roleSelection,
            }),
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response returned an error.");
                }
                return response.json();
            })
            .then((data) => {
                resultContent.textContent = data.combinedData;

                if (action === "Get Resume" && data.download_url) {
                    const downloadButton = document.createElement("button");
                    downloadButton.textContent = "Download Resume";
                    downloadButton.className = "btn";
                    downloadButton.onclick = () => {
                        window.open(data.download_url, "_blank");
                    };
                    downloadContainer.appendChild(downloadButton);
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                resultContent.textContent = "An error occurred. Please try again later.";
            });
    });

});
