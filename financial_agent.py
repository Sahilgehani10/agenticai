import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo

# Load environment variables
load_dotenv()

# Set both API keys
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'dummy_value')
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

# Websearch agent
websearch_agent = Agent(
    name="websearch_agent",
    role="Search the web for information",
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tools_calls=True,
    markdown=True
)

# Finance agent
finance_agent = Agent(
    name="Finance AI Agent",
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, company_news=True)],
    instructions=["use tables to display data"],
    show_tools_calls=True,
    markdown=True,  
)

multi_ai_agent = Agent(
    team=[websearch_agent, finance_agent],
    instructions=["always include sources", "use table to display the data"],
    show_tools_calls=True,
    markdown=True,
)

multi_ai_agent.print_response("Summarize analyst recommendations and share latest news for NVDA", stream=True)