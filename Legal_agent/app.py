from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
from flask_cors import CORS
import traceback

# Load environment variables
load_dotenv()

# Check if API key is present
if not os.getenv('GROQ_API_KEY'):
    print("Warning: GROQ_API_KEY not found in environment variables")

app = Flask(__name__)
CORS(app)

# Initialize fitness agent
try :

    from phi.agent import Agent
    from phi.model.groq import Groq
    from phi.tools.wikipedia import WikipediaTools
    from phi.tools.duckduckgo import DuckDuckGo


    legal_agent = Agent(
    name="Legal Agent",
    model=Groq(id="llama-3.2-1b-preview"),
    tools=[
        WikipediaTools(),
        DuckDuckGo()  # Add search capability to a single agent
    ],
    instructions=[
        "You are a professional legal assistant specializing in Indian law and the Indian Constitution.",
        "All responses must strictly adhere to the Indian Constitution, IPC, CrPC, Evidence Act, and other relevant Indian legal statutes.",
        "Provide well-structured and professional answers as if given by a legal authority or a constitutional body.",
        "Ensure fairness, neutrality, and constitutional integrity in responses.",
        "Use structured formatting such as tables, bullet points, and numbered sections where applicable.",
        "When answering legal queries, provide relevant sections and articles from the Indian Constitution or statutes.",
        "Do not provide legal opinions or interpretations beyond established legal principles and precedents.",
        "If the question is beyond Indian law, politely decline and refer the user to a qualified legal professional.",
        "Cite appropriate legal sources (Indian laws, case laws, legal doctrines) to support responses.",
        "Maintain a formal and professional tone in all communications.",
        "When summarizing legal documents, extract key points and provide clear interpretations.",
        "If necessary, suggest legal remedies, precedents, or procedural steps as per Indian law."
        "ALWAYS respond using proper markdown formatting for all structured content.",
        "Use bullet points for lists and steps.",
        "Format headings using ## symbols.",
        "Use **bold** for important terms and metrics.",
        "Separate sections with horizontal rules (---)",
    ],
    show_tool_calls=True,
    markdown=True,
)

    print("Successfully initialized fitness agent")
except Exception as e:
    print(f"Error initializing fitness agent: {str(e)}")
    print(traceback.format_exc())
    fitness_agent = None

# Serve the frontend
@app.route('/')
def index():
    return render_template('index.html')

# Chatbot endpoint
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Check if fitness_agent was properly initialized
        if fitness_agent is None:
            return jsonify({'response': 'The fitness agent failed to initialize. Check server logs.'}), 500
            
        data = request.json
        if not data:
            return jsonify({'response': 'No data received'}), 400
            
        user_message = data.get('message', '')
        if not user_message:
            return jsonify({'response': 'Please provide a message'}), 400
            
        # Get response from fitness agent
        print(f"Processing message: {user_message}")
        response_obj = fitness_agent.run(user_message)
        
        # Extract the string content from the RunResponse object
        # Check the type to decide how to handle it
        print(f"Response type: {type(response_obj)}")
        
        if hasattr(response_obj, 'content'):
            # If it has a content attribute, use that
            response_text = response_obj.content
        elif hasattr(response_obj, 'text'):
            # If it has a text attribute, use that
            response_text = response_obj.text
        elif hasattr(response_obj, '__str__'):
            # If we can convert it to string, use that
            response_text = str(response_obj)
        else:
            # Fallback
            response_text = "Received a response from the AI but couldn't extract the text content."
            
        print(f"Response extracted: {response_text[:100]}...")  # Print first 100 chars
            
        # Return the response
        return jsonify({'response': response_text})
    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"Error in /chat endpoint: {str(e)}")
        print(error_traceback)
        return jsonify({'response': f'Server error: {str(e)}. Please check server logs for details.'}), 500

if __name__ == '__main__':
    # Run the app
    app.run(host='0.0.0.0', port=3000, debug=True)