import os
from google.adk.agents.llm_agent import Agent
from google.adk.tools import FunctionTool
from custom_functions import run_writer_pipeline

model = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-pro")

root_agent = Agent(
    name="WriterMultiAgentRoot",
    model=model,
    description="Root agent for the Writer Multi-Agent system.",
    instruction=(
        "You are the orchestrator of a multi-agent writing system. "
        "Use the 'run_writer_pipeline' tool to research, draft, and edit "
        "a high-quality article based on the user's topic."
    ),
    tools=[FunctionTool(run_writer_pipeline)],
    output_key="final_article",
)
