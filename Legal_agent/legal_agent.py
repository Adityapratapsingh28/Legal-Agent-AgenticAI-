from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.wikipedia import WikipediaTools
from phi.tools.duckduckgo import DuckDuckGo

# Loading environment variables from a .env file into our Python application's environment
from dotenv import load_dotenv
load_dotenv()

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
    ],
    show_tool_calls=True,
    markdown=True,
)

# Then use just this agent directly
legal_agent.print_response(
    "Help me to solve a murder case in which my friend aastha is accused",
    stream=True  # Enable streaming for faster initial response
)
