from flask import Flask, request, jsonify
from phi.assistant import Assistant
from phi.storage.assistant.postgres import PgAssistantStorage
from phi.knowledge.pdf import PDFKnowledgeBase, PDFReader
from phi.vectordb.pgvector import PgVector2
from phi.agent import Agent
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import fitz  # PyMuPDF

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load environment variables
load_dotenv()
os.environ["PHI_MODEL_PROVIDER"] = "groq"
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# Initialize storage
storage = PgAssistantStorage(table_name="pdf_assistant", db_url=db_url)

# Initialize knowledge_base and pdf_content as None
knowledge_base = None
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
        raise Exception(f"Error extracting PDF content: {str(e)}")

@app.route('/upload', methods=['POST'])
def upload_file():
    global knowledge_base, pdf_content
    
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
            print(f"Extracted PDF content: {pdf_content[:500]}...")  # Debug log
            
            # Create knowledge base with local PDF file
            knowledge_base = PDFKnowledgeBase(
                path=filepath,
                vector_db=PgVector2(collection="pdf_chat", db_url=db_url)
            )
            
            # Load the knowledge base
            knowledge_base.load()
            print("Knowledge base loaded successfully.")  # Debug log
            
            return jsonify({'message': 'File uploaded successfully'}), 200
        except Exception as e:
            return jsonify({'error': f'Error processing PDF: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/summarize', methods=['POST'])
def summarize_pdf():
    global knowledge_base, pdf_content
    
    if knowledge_base is None or pdf_content is None:
        return jsonify({'error': 'Please upload a PDF first'}), 400
    
    try:
        agent = Agent(
            knowledge=knowledge_base,
            search_knowledge=True,
            model_provider="groq"
        )
        
        summary_prompt = """Please provide a concise, well-formatted summary of this document with clear line spacing and bullet points:

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

{content}""".format(content=pdf_content)
        
        print(f"Summary prompt being sent to agent: {summary_prompt[:500]}...")  # Debug log
        
        response = agent.run(summary_prompt)
        
        # Check agent's response
        print(f"Agent response: {response}")  # Debug log

        # Extract and clean up only the content
        summary_text = response.content.strip() if hasattr(response, 'content') else str(response).strip()
        
        # Ensure proper line spacing and bullet formatting
        formatted_summary = summary_text.replace("•", "-").replace("\n", "\n\n")
        
        return jsonify({'summary': formatted_summary}), 200
    except Exception as e:
        return jsonify({'error': f'Error generating summary: {str(e)}'}), 500


@app.route('/ask', methods=['POST'])
def ask_question():
    global knowledge_base, pdf_content
    
    if knowledge_base is None or pdf_content is None:
        return jsonify({'error': 'Please upload a PDF first'}), 400
    
    data = request.json
    question = data.get('question')
    user_id = data.get('user_id', 'default_user')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        # Initialize assistant with context
        assistant = Assistant(
            user_id=user_id,
            knowledge_base=knowledge_base,
            storage=storage,
            show_tool_calls=True,
            search_knowledge=True,
            read_chat_history=True,
            model_provider="groq"
        )
        
        # Include PDF content in the context
        context_prompt = f"""Using the following PDF content as context:

{pdf_content}

Question: {question}"""
        
        # Get the response generator
        response_generator = assistant.chat(context_prompt)
        
        # Collect all chunks into a complete response
        full_response = ""
        for chunk in response_generator:
            if hasattr(chunk, 'content'):
                full_response += chunk.content
            elif isinstance(chunk, str):
                full_response += chunk
        
        return jsonify({'answer': full_response}), 200
    except Exception as e:
        return jsonify({'error': f'Error processing question: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
