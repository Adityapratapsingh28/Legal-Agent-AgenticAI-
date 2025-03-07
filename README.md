# AI Legal Agent :man_judge: 

A cutting-edge Legal Supervisor designed to simplify and enhance legal workflows using artificial intelligence. This repository contains an advanced AI-powered tool with two primary features:

### Legal Document Summarizer: 
Effortlessly upload complex legal documents and extract key information through natural language queries. Ask specific questions to receive concise, accurate summaries tailored to your needs.

### Legal Agent: 
An intelligent conversational assistant trained on the Indian Constitution, capable of delivering precise and contextually relevant answers to a wide range of legal questions. Whether you're seeking clarity on constitutional provisions or legal guidance, this agent is your reliable companion


## 📌 What Problem does it solve 

**1️⃣ Simplify Legal Understanding**  
Summarize complex legal docs via user questions.  

**2️⃣ Offer Reliable Guidance**  
Answer legal queries with constitutional accuracy.  

**3️⃣ Bridge Tech and Law**  
Democratize legal knowledge for all users.  

## Technology stack :keyboard: 

- :signal_strength: groq (cloud llm provider)
- :signal_strength: phidata (provide agentic framework)
- :signal_strength: flask (backend & connection)
- :signal_strength: html, css (frontend)

## Features :high_brightness:

### 1. Legal Document Summarizer
The Legal Document Summarizer enables users to upload intricate legal documents then using llama llm models, it analyzes the text and delivers detailed yet concise summaries, making complex legal information easier to understand and apply.
<img width="837" alt="image" src="https://github.com/user-attachments/assets/9c75a92d-aba1-48e2-a74a-60274e55acb5" />


### 2. Ask from Agent 
The Ask from Agent feature allows users to submit any question about a legal document they’ve provided.The AI-powered Legal Agent analyzes the document and delivers precise, context-aware answers based on its content and the Indian Constitution.
<img width="898" alt="image" src="https://github.com/user-attachments/assets/777d730c-add4-4e97-a878-41ed88c58504" />


### 3. Legal Agent Supervisor
In which the user can ask any query reagarding law, consitution, rules, different sections etc and our agent will give appropiate answer
<img width="910" alt="image" src="https://github.com/user-attachments/assets/030a28e8-e849-459a-ae0b-9b60c7a44ef8" />





## Setup ⚙️ 

Clone the repository and install the required dependencies:  

```bash
git clone https://github.com/your-username/AI-Legal-Agent.git  

LEGAL-AGENT-AGENTICAI/
│── .vscode/
│── Doc_summarizer/
│   ├── static/
│   │   ├── index.html
│   ├── venv/
│   ├── app.py
│   ├── legal.py
│   ├── requirements.txt
│   ├── t.txt
│── Legal_agent/
│   ├── templates/
│   │   ├── index.html
│   ├── venv/
│   │── .env
│   │── .gitignore
│   │── app.py
│   │── financial_agent.py
│   │── legal_agent.py
│   │── requirements.txt


Follow the steps below to set up and run **AI Legal Agent** on your local system.  

### 🛠 Prerequisites  
- Install **Python 3.10** (recommended via Conda).  
- Install **pip** for dependency management.  

---

## 🚀 Running the Project  

The project consists of **two main components**, which need to run in separate terminals:

---------------------------------------------------------------------------------------

### 📜 Terminal 1: Setting up `Doc_summarizer`  

```cmd
# Step 1: Navigate to the project folder
cd AI-Legal-Agent

# Step 2: Move into the Doc_summarizer directory
cd Doc_summarizer

# Step 3: Create a virtual environment using Conda
conda create -p venv python==3.10 -y

# Step 4: Activate the virtual environment
conda activate venv/

# Step 5: Install required dependencies
pip install -r requirements.txt

# Step 6: Set API keys for Phidata and Groq in the .env file
# Open .env and add the following lines:
# GROQ_API_KEY="___________________"
# PHI_AI_KEY="_____________________"

# Step 7: Load the API keys into the system environment variables
setx GROQ_API_KEY "___________________" & setx PHI_AI_KEY "_____________________"

# Step 8: Run the Doc Summarizer application
python app.py

-------------------------------------------------------------------------------------

### 📜 Terminal 2: Setting up `Legal_agent`  

# Step 1: Navigate to the project folder
cd AI-Legal-Agent

# Step 2: Move into the Legal_agent directory
cd Legal_agent

# Step 3: Create a virtual environment using Conda
conda create -p venv python==3.10 -y

# Step 4: Activate the virtual environment
conda activate venv/

# Step 5: Install required dependencies
pip install -r requirements.txt

# Step 6: Set API keys for Phidata and Groq in the .env file
# Open .env and add the following lines:
# GROQ_API_KEY="___________________"
# PHI_AI_KEY="_____________________"

# Step 7: Load the API keys into the system environment variables
setx GROQ_API_KEY "___________________" & setx PHI_AI_KEY "_____________________"

# Step 8: Run the Legal Agent application
python app.py


```

## Usage :mag_right:

1️⃣ Legal Research & Case Preparation Lawyers and law students can quickly analyze legal documents. Saves hours by summarizing lengthy legal texts. Provides accurate case law references based on the Indian Constitution.

2️⃣ Instant Legal Consultation Users can ask legal questions and receive accurate, constitutionally aligned answers. Helps individuals understand their rights and legal options. Assists in legal aid services by offering quick legal insights.

3️⃣ Efficient Document Review & Compliance Businesses and legal professionals can verify contracts and compliance documents. AI-driven insights help identify legal risks and obligations. Ensures legal documents adhere to Indian laws and regulations.




