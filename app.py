import os
import fitz  # PyMuPDF
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# --- App Configuration ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///papers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Configure the LLM (Still needed, but not used in the workaround) ---
# genai.configure(api_key=os.getenv("API_KEY"))
# llm = genai.GenerativeModel('gemini-pro')

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# --- Database Model ---
class Paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(300), nullable=False)
    title = db.Column(db.String(500), default="Processing...")
    summary = db.Column(db.Text, default="")
    research_gaps = db.Column(db.Text, default="")

# --- Helper Functions ---
def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

# --- Routes ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'paper' not in request.files:
            return redirect(request.url)
        file = request.files['paper']
        if file.filename == '':
            return redirect(request.url)
        if file and file.filename.endswith('.pdf'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            new_paper = Paper(filename=file.filename)
            db.session.add(new_paper)
            db.session.commit()
            return redirect(url_for('paper_view', paper_id=new_paper.id))

    papers = Paper.query.order_by(Paper.id.desc()).all()
    return render_template('index.html', papers=papers)

@app.route('/paper/<int:paper_id>')
def paper_view(paper_id):
    paper = Paper.query.get_or_404(paper_id)
    
    if paper.title == "Processing...":
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], paper.filename)
        full_text = extract_text_from_pdf(filepath)
        
        if full_text:
            # --- MOCK DATA WORKAROUND (CLEAN FORMATTING) ---
            paper.title = f"Mock Analysis of {paper.filename}"
            paper.summary = """Title: Mock Paper on AI Advancements
Authors: Dr. Gemini and Prof. Bard
Abstract: This is a mock abstract describing fictional research. The methods involved creating a temporary data placeholder to ensure application functionality during development.
Key Findings:
- Mock data is a useful debugging tool.
- Application flow can be tested independently of live API services.
Methodology: The methodology involved replacing the live API call with this hardcoded text."""
            
            paper.research_gaps = """- Limitations: The study did not account for long-term AI behavior.
- Future Work: Future research should focus on cross-domain model generalization.
- Unexplored Opportunities: The application of this model in robotics has not been explored."""

            db.session.commit()
            # --- END OF MOCK DATA ---

    return render_template('paper_view.html', paper=paper)

# --- Main Execution Block ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)