from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo

# loading environment variables from a .env file into our Python application's environmen
from dotenv import load_dotenv
load_dotenv()

# Web searcg Agent
websearch_agent = Agent(
    name = "websearch agent",
    role ="Search the web for the information",
    model = Groq(id = "llama-3.1-8b-instant"),
    tools=[DuckDuckGo()],
    instructions = ["Alawys include sources"],
    show_tools_calls=True,
    markdown=True,
)

# Financial Agent

Finance_agent = Agent(
    name = "Finance AI Agent",
    model =Groq(id = "llama-3.1-8b-instant"),
    tools=[
        YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True,company_news=True),
    ],

    instructions=["Use tables to display the data "],
    show_tool_calls=True,
    markdown=True,
)

# Multimodel Agent by combining the responses two different agents in one new agent (this is giving late response)
'''
multi_ai_agent=Agent(
    team=[websearch_agent,finance_agent],
    model=Groq(id= "llama-3.1-8b-instant"),
    instructions=["Always include sources","use tables to display the data"],
    show_tools_calls = True,
    markdown = True,
)

multi_ai_agent.print_response(
    "Summarize analyst recoomendation and share the latest news and data in a proper tabular way for GOOGLE comapany",
    stream=False,
)
'''


# 1. Reduce parallel processing by using a single agent approach (this approach giving fast output)
finance_agent = Agent(
    name="Finance AI Agent",
    model=Groq(id="llama-3.2-1b-preview"),
    tools=[
        YFinanceTools(stock_price=True, analyst_recommendations=True, 
                     stock_fundamentals=True, company_news=True),
        DuckDuckGo()  # Add search capability to a single agent
    ],
    instructions=[
        "Use tables to display the data",
        "Always include sources",
        "Limit responses to critical information"  # Reduce token usage
    ],
    show_tool_calls=True,
    markdown=True,
)

# Then use just this agent directly
finance_agent.print_response(
    "I want to buy a stock pls suggest me which stock to  buy in 2025  and also do stock comparision in tabular manner with detailed data",
    stream=True  # Enable streaming for faster initial response
)
