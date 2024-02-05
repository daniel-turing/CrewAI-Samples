import os
from langchain.llms import Ollama
import crewai
from crewai import Agent, Task, Crew, Process
from langchain.agents import Tool
from langchain.agents import load_tools
from langchain_google_genai import ChatGoogleGenerativeAI
#from AgoraTools import RAG

from langchain.utilities import GoogleSerperAPIWrapper

# to get your api key for free, visit and signup: https://serper.dev/
os.environ["SERPER_API_KEY"] = "5acd19df25b204ad81015cfe56b9857352376512"

search = GoogleSerperAPIWrapper()

search_tool = Tool(
    name="Scrape google searches",
    func=search.run,
    description="useful for when you need to ask the agent to search the internet",
)

def save_to_file(content):
    with open("output.js", 'w') as file:
        file.write(content)

save_file_tool = Tool(
    name="Save content to a file",
    func=save_to_file,
    description="useful for when you need to save content to a file",
)



ollama_mis =  Ollama(model="mistral")
llm_gemini = ChatGoogleGenerativeAI(
    model="gemini-pro", verbose=True, temperature=0.1, google_api_key="AIzaSyCA-Z_DJXDhYoMKcKGreEWmYrJsRvYKePw"
)

researcher = Agent(
    role="Expert in Explaning Code ",
    goal="Explain the functionality of a code, with every single details so that it can be re-created in another language or platform",
    backstory='You are an AI Code Explainer.',
    verbose=True,
    allow_delegation=False,
    llm=llm_gemini, #ollama_openhermes
    tools=[search_tool
           ],
)

writer = Agent(
    role="Javascript Developer",
    goal="Develop efficient and effective JavaScript code",
    backstory='You are an AI JavaScript developer who specializes in creating and optimizing JavaScript code',
    verbose=True,
    allow_delegation=False,
    #llm=llm_gemini, #ollama_openhermes
    #llm= ollama_mis,
    tools=[save_file_tool]
)


with open('code_in.py', 'r') as file:
    code = file.read()

task1 = Task(description=f'Explain the function of this code in details {code}', agent=researcher)
task2 = Task(description='Write a javascript code for the giving functionalities and save the code', agent=writer)

crew = Crew(
    agents=[researcher, writer],
    verbose=2,
    process=Process.sequential,
    tasks=[task1, task2]
)

crew.kickoff()