LLM Research Paper Analyzer
This project is a Flask-based web application that serves as an intelligent research assistant. It allows users to upload academic papers in PDF format and receive a generated summary and research gap analysis.

Features
PDF Upload: A simple web interface to upload research papers.

Content Extraction: Extracts text content from uploaded PDF files.

AI-Powered Analysis: Generates structured summaries and identifies research gaps.

Note: This version uses a mock data workaround and does not require a live API key to function.

How to Run This Project
Prerequisites
Python 3.9+

Git

1. Clone the Repository
First, clone this repository to your local machine using Git.

Bash
```bash
git clone https://github.com/your-username/llm-research-analyzer.git
cd llm-research-analyzer
```
(Replace your-username with your actual GitHub username).

2. Create and Activate a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.

Bash

# Create the virtual environment
```bash

python -m venv venv
```
# Activate the environment
# On Windows (PowerShell):
```bash

.\venv\Scripts\activate
```
# On macOS/Linux:
```bash

source venv/bin/activate
```
You'll know it's active when you see (venv) at the beginning of your terminal prompt.

3. Install Dependencies
Install all the required Python libraries using the pip package manager.

Bash

pip install Flask Flask-SQLAlchemy PyMuPDF python-dotenv google-generativeai
4. Set Up the Environment File
This project requires a .env file for configuration, although the API key is not currently used by the mock data version.

Create a file named .env in the project's root directory.

Add the following line to it:

API_KEY=YOUR_API_KEY_HERE
(While not used in the current version, this step prevents potential errors if you switch back to the live API).

5. Run the Application
Once the setup is complete, you can run the Flask web server.

Bash
```bash

flask --app app.py run
```
The server will start, and you'll see a message indicating it's running on http://127.0.0.1:5000.

6. Use the Application
Open your web browser and navigate to http://127.0.0.1:5000. You can now upload a PDF file to see the mock analysis in action
