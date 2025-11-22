from google.genai import types
from .custom_agents import pipeline_runner, session_service, user_id, session_id, app_name

async def run_writer_pipeline(topic: str):

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
    
    return output.get("EditorAgent", output)