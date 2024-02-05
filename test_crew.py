import os
from langchain.llms import Ollama
import crewai
from crewai import Agent, Task, Crew, Process
from langchain.agents import Tool
from langchain.agents import load_tools
from langchain_google_genai import ChatGoogleGenerativeAI
from AgoraTools import RAG

from langchain.utilities import GoogleSerperAPIWrapper

# to get your api key for free, visit and signup: https://serper.dev/
os.environ["SERPER_API_KEY"] = "5acd19df25b204ad81015cfe56b9857352376512"

search = GoogleSerperAPIWrapper()

search_tool = Tool(
    name="Scrape google searches",
    func=search.run,
    description="useful for when you need to ask the agent to search the internet",
)



ollama_openhermes =  Ollama(model="openhermes")
llm_gemini = ChatGoogleGenerativeAI(
    model="gemini-pro", verbose=True, temperature=0.1, google_api_key="AIzaSyCA-Z_DJXDhYoMKcKGreEWmYrJsRvYKePw"
)

researcher = Agent(
    role="Researcher",
    goal="Research new AI insights",
    backstory='You are an AI research assistant.',
    verbose=True,
    allow_delegation=False,
    llm=llm_gemini, #ollama_openhermes
    tools=[search_tool
           ],
)

writer = Agent(
    role="Writer",
    goal="Write a compelling and engaging blog posts about AI trends and insights",
    backstory='You are an AI blog post writer who specializes in writing post about AI trends and insights',
    verbose=True,
    allow_delegation=False,
    llm=llm_gemini, #ollama_openhermes
)


task1 = Task(description='Investigate the latest AI trend', agent=researcher)
task2 = Task(description='Write a compelling blog post based on the latest AI trends', agent=writer)

crew = Crew(
    agents=[researcher, writer],
    verbose=2,
    process=Process.sequential,
    tasks=[task1, task2]
)

crew.kickoff()