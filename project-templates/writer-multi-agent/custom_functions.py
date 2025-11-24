import os
from google.genai import types
from custom_agents import create_writer_pipeline

async def run_writer_pipeline(topic: str):
    # Load environment variables
    model = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-pro")
    app_name = os.getenv("APP_NAME", "WriterMultiAgent")
    user_id = os.getenv("USER_ID", "default_user")
    session_id = os.getenv("SESSION_ID", "default_session")
    
    # Create pipeline with current environment configuration
    pipeline_runner, session_service = create_writer_pipeline(model, app_name)
    
    # Create or get session
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    
    # Create user message
    user_message = types.Content(
        role="user",
        parts=[types.Part(text=topic)]
    )
    
    # Run the pipeline
    events = pipeline_runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_message
    )
    
    output = {}
    async for event in events:
        if event.is_final_response():
            author = event.author
            content = event.content.parts[0].text
            output[author] = content
    
    return output