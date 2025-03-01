from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import fitz  # PyMuPDF
import logging
from groq import Groq  # Groq Python SDK

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load environment variables
load_dotenv()

# Initialize Groq client
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")
groq_client = Groq(api_key=groq_api_key)

# Initialize pdf_content as None
pdf_content = None

@app.route('/')
def home():
    return app.send_static_file('index.html')

def extract_pdf_content(filepath):
    """Extract text content from PDF using PyMuPDF"""
    try:
        doc = fitz.open(filepath)
        content = []
        for page in doc:
            content.append(page.get_text())
        doc.close()
        return "\n".join(content)
    except Exception as e:
        logger.error(f"Error extracting PDF content: {str(e)}", exc_info=True)
        raise Exception(f"Error extracting PDF content: {str(e)}")

@app.route('/upload', methods=['POST'])
def upload_file():
    global pdf_content
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.pdf'):
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Extract PDF content using PyMuPDF
            pdf_content = extract_pdf_content(filepath)
            logger.debug(f"Extracted PDF content: {pdf_content[:500]}...")  # Debug log
            
            return jsonify({'message': 'File uploaded successfully'}), 200
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}", exc_info=True)
            return jsonify({'error': f'Error processing PDF: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

def generate_groq_response(prompt, model="mixtral-8x7b-32768"):
    """Generate a response using the Groq API"""
    try:
        response = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating Groq response: {str(e)}", exc_info=True)
        raise Exception(f"Error generating Groq response: {str(e)}")

@app.route('/summarize', methods=['POST'])
def summarize_pdf():
    global pdf_content
    
    if pdf_content is None:
        return jsonify({'error': 'Please upload a PDF first'}), 400
    
    try:
        summary_prompt = f"""Please provide a concise, well-formatted summary of this document with clear line spacing and bullet points:

OVERVIEW:
- Brief 2-3 line description of what this document is about.

KEY TOPICS:
- Topic 1: Main point
- Topic 2: Main point
- Topic 3: Main point

MAIN FINDINGS/CONCLUSIONS:
- Key conclusion 1
- Key conclusion 2
- Key conclusion 3

Ensure clear separation between sections, and keep bullet points succinct (1-2 lines each). Avoid extra metadata in the output.

Here is the content to summarize:

{pdf_content}"""
        
        logger.debug(f"Summary prompt being sent to Groq: {summary_prompt[:500]}...")  # Debug log
        
        # Generate summary using Groq
        summary = generate_groq_response(summary_prompt)
        
        # Ensure proper line spacing and bullet formatting
        formatted_summary = summary.replace("•", "-").replace("\n", "\n\n")
        
        return jsonify({'summary': formatted_summary}), 200
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}", exc_info=True)
        return jsonify({'error': f'Error generating summary: {str(e)}'}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    global pdf_content
    
    if pdf_content is None:
        return jsonify({'error': 'Please upload a PDF first'}), 400
    
    data = request.json
    question = data.get('question')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        # Include PDF content in the context
        context_prompt = f"""Using the following PDF content as context:

{pdf_content}

Question: {question}"""
        
        # Generate response using Groq
        answer = generate_groq_response(context_prompt)
        
        return jsonify({'answer': answer}), 200
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}", exc_info=True)
        return jsonify({'error': f'Error processing question: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)