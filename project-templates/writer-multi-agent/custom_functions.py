import os
import uuid
from google.genai import types
from custom_agents import create_writer_pipeline

async def run_writer_pipeline(topic: str):

    if not topic or not topic.strip():
        return {"error": "Topic cannot be empty"}
    
    try: 
        # Load environment variables
        model = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-pro")
        app_name = os.getenv("APP_NAME", "WriterMultiAgent")
        user_id = os.getenv("USER_ID", "default_user")
        session_id = f"{os.getenv('SESSION_ID', 'default_session')}_{uuid.uuid4().hex[:8]}"
        
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
        
        expected_agents = ["ResearcherAgent", "WriterAgent", "EditorAgent"]
        if not all(agent in output for agent in expected_agents):
            output["warning"] = "Pipeline incomplete"

        return output
    
    except Exception as e:
        return {"error": str(e), "status": "failed"}
    finally:
        await session_service.close_session(session_id)

