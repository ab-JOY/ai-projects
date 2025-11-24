import streamlit as st
import asyncio
import os
import uuid

st.set_page_config(
    page_title="Writer Multi-Agent Chat",
    page_icon="✍️",
    layout="centered"
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key_set" not in st.session_state:
    st.session_state.api_key_set = False
if "unique_session_id" not in st.session_state:
    st.session_state.unique_session_id = f"session_{uuid.uuid4().hex[:16]}"

if "SESSION_ID" not in os.environ:
    os.environ["SESSION_ID"] = st.session_state.unique_session_id
if "USER_ID" not in os.environ:
    os.environ["USER_ID"] = f"user_{st.session_state.unique_session_id[:8]}"
if "APP_NAME" not in os.environ:
    os.environ["APP_NAME"] = "WriterMultiAgent"
if "GEMINI_MODEL_NAME" not in os.environ:
    os.environ["GEMINI_MODEL_NAME"] = "gemini-2.5-pro"
if "GOOGLE_GENAI_USE_VERTEXAI" not in os.environ:
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"
if "GOOGLE_CLOUD_LOCATION" not in os.environ:
    os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"

if hasattr(st, 'secrets'):
    for key, value in st.secrets.items():
        os.environ[key] = str(value)

try:
    from custom_functions import run_writer_pipeline
    IMPORTS_AVAILABLE = True
except ImportError as e:
    IMPORTS_AVAILABLE = False
    IMPORT_ERROR = str(e)

st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .agent-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    .researcher { background-color: #e3f2fd; color: #1976d2; }
    .writer { background-color: #f3e5f5; color: #7b1fa2; }
    .editor { background-color: #e8f5e9; color: #388e3c; }
</style>
""", unsafe_allow_html=True)

if not IMPORTS_AVAILABLE:
    st.error(f"Missing required dependencies: {IMPORT_ERROR}")
    st.info("Please make sure `google-adk` is installed in your requirements.txt")
    st.stop()

with st.sidebar:
    st.title("Configuration")
    
    api_key = st.text_input(
        "Google API Key",
        type="password",
        help="Enter your Google API key for Gemini",
        placeholder="AIza..."
    )
    
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
        st.session_state.api_key_set = True
        st.success("API Key set!")
    else:
        st.warning("Please enter your API key to continue")
    
    st.markdown("---")
    
    with st.expander("Advanced Settings"):
        model_name = st.text_input("Model Name", value="gemini-2.5-pro")
        app_name = st.text_input("App Name", value="WriterMultiAgent")
        user_id = st.text_input("User ID", value=f"user_{st.session_state.unique_session_id[:8]}")
        
        st.text_input("Session ID (Auto-generated)", value=st.session_state.unique_session_id, disabled=True)
        
        use_vertex = st.selectbox("Use Vertex AI", ["False", "True"])
        cloud_location = st.text_input("Cloud Location", value="us-central1")
        cloud_project = st.text_input("Cloud Project ID", value="")
        
        if st.button("Apply Settings"):
            os.environ["GEMINI_MODEL_NAME"] = model_name
            os.environ["APP_NAME"] = app_name
            os.environ["USER_ID"] = user_id
            os.environ["SESSION_ID"] = st.session_state.unique_session_id
            os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = use_vertex
            os.environ["GOOGLE_CLOUD_LOCATION"] = cloud_location
            if cloud_project:
                os.environ["GOOGLE_CLOUD_PROJECT"] = cloud_project
            st.success("Settings applied!")
    
    st.markdown("---")
    
    st.markdown("""
    ###How it works:
    1. **Researcher** searches for information
    2. **Writer** creates the article
    3. **Editor** refines the content
    """)
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; font-size: 0.8rem;'>
        <p>Built with Google ADK & Gemini<br/>
        <a href='https://github.com/ab-JOY/ai-projects/tree/master/project-templates/writer-multi-agent'>GitHub</a></p>
    </div>
    """, unsafe_allow_html=True)

st.title("Writer Agent Chat")
st.caption("Generate well-researched articles through conversational AI agents")

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar", None)):
        st.markdown(message["content"])

if prompt := st.chat_input("What topic would you like me to write about?", disabled=not st.session_state.api_key_set):
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "avatar": "👤"
    })

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        
        message_placeholder.markdown("**Researching your topic...**")
        
        try:
            result = asyncio.run(run_writer_pipeline(prompt))
            
            full_response = ""
            
            if isinstance(result, dict):
                if "ResearcherAgent" in result:
                    message_placeholder.markdown("**Research completed!** Now writing...\n\n")
                    research_preview = result["ResearcherAgent"][:300] + "..." if len(result["ResearcherAgent"]) > 300 else result["ResearcherAgent"]
                    
                if "WriterAgent" in result:
                    message_placeholder.markdown("**Article drafted!** Now editing...\n\n")
    
                if "EditorAgent" in result:
                    full_response = f"**Article Complete!**\n\n---\n\n{result['EditorAgent']}\n\n---\n\n"

                    with st.expander("View Research Summary"):
                        st.markdown(result.get("ResearcherAgent", "No research data available"))
                    
                    with st.expander("View Draft Article"):
                        st.markdown(result.get("WriterAgent", "No draft available"))

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.download_button(
                            "Research",
                            result.get("ResearcherAgent", ""),
                            file_name="research.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    with col2:
                        st.download_button(
                            "Draft",
                            result.get("WriterAgent", ""),
                            file_name="draft.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    with col3:
                        st.download_button(
                            "Final",
                            result["EditorAgent"],
                            file_name="final_article.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                else:
                    full_response = f"**Article Complete!**\n\n---\n\n{result.get('WriterAgent', result)}"
            else:
                full_response = f"**Article Complete!**\n\n---\n\n{str(result)}"
            
            message_placeholder.markdown(full_response)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response,
                "avatar": "🤖"
            })
            
        except Exception as e:
            error_message = f"**Error occurred:**\n\n```\n{str(e)}\n```\n\nPlease check your API key and try again."
            message_placeholder.markdown(error_message)

            st.session_state.messages.append({
                "role": "assistant",
                "content": error_message,
                "avatar": "🤖"
            })

if not st.session_state.api_key_set and len(st.session_state.messages) == 0:
    st.info("Please enter your Google API Key in the sidebar to get started!")
    
    with st.expander("How to get a Google API Key"):
        st.markdown("""
        1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Click "Create API Key"
        3. Copy your API key
        4. Paste it in the sidebar
        
        **Note:** Keep your API key secure and never share it publicly!
        """)
    
    st.markdown("---")
    st.markdown("###Example topics to try:")
    example_topics = [
        "The future of renewable energy",
        "How artificial intelligence is transforming healthcare",
        "The impact of remote work on productivity",
        "Sustainable agriculture practices"
    ]
    
    cols = st.columns(2)
    for idx, topic in enumerate(example_topics):
        with cols[idx % 2]:
            if st.button(topic, key=f"example_{idx}", disabled=not st.session_state.api_key_set):
                st.rerun()