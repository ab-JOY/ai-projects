import os
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import google_search
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

model = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-pro")
app_name = os.getenv("APP_NAME")
user_id = os.getenv("USER_ID")
session_id = os.getenv("SESSION_ID")

# Define agents
researcher_agent = LlmAgent(
    name="ResearcherAgent",
    model=model,
    instruction="Your task is to use 'google_search' tool to find all the relevant information about a given topic and write a comprehensive report about that topic.",
    tools=[google_search],
    description="Researches about a topic",
    output_key="research_results"
)

writer = LlmAgent(
    name="WriterAgent",
    model=model,
    instruction="Your task is to write a comprehensive article using this information: {research_results}. Make sure to expand on all the topics from the provided information.",
    description="Write a comprehensive article based on the provided information",
    output_key="comprehensive_article"
)

editor = LlmAgent(
    name="EditorAgent",
    model=model,
    instruction="Your task is to edit a report: {comprehensive_article}. Perform a quality check on the text and improve it if necessary.",
    description="Perform quality check on a written article",
    output_key="final_article"
)

# Create the sequential pipeline
writer_pipeline = SequentialAgent(
    name="WriterPipeline",
    sub_agents=[researcher_agent, writer, editor],
    description="A multi-agent pipeline that researches a topic, writes an article based on the research, and then edits the article for quality."
)

# Initialize Session Service
session_service = InMemorySessionService()

# Initialize Runner
pipeline_runner = Runner(
    agent=writer_pipeline,
    app_name=app_name,
    session_service=session_service,
)