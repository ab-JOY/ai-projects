import streamlit as st
import asyncio
import os
from custom_functions import run_writer_pipeline

if hasattr(st, 'secrets'):
    for key, value in st.secrets.items():
        os.environ[key] = str(value)

st.set_page_config(
    page_title="Writer Multi-Agent System",
    page_icon="✍️",
    layout="wide"
)

st.title("✍️ Writer Multi-Agent System")
st.markdown("Generate well-researched articles using AI agents that research, write, and edit content.")

with st.sidebar:
    st.header("⚙️ Configuration")
    st.info("Make sure your environment variables are set correctly before running.")
    
    with st.expander("📋 Required Environment Variables"):
        st.code("""
GEMINI_MODEL_NAME
APP_NAME
USER_ID
SESSION_ID
GOOGLE_API_KEY
GOOGLE_GENAI_USE_VERTEXAI
GOOGLE_CLOUD_LOCATION
GOOGLE_CLOUD_PROJECT
        """)
    
    st.markdown("---")
    st.markdown("### How it works")
    st.markdown("""
    1. 🔍 **Research**: Searches for relevant information
    2. ✍️ **Write**: Creates comprehensive article
    3. ✅ **Edit**: Refines and polishes content
    """)

topic = st.text_input(
    "Enter a topic to research and write about:",
    placeholder="e.g., The impact of artificial intelligence on healthcare"
)

col1, col2 = st.columns([1, 5])
with col1:
    generate_btn = st.button("🚀 Generate Article", type="primary", use_container_width=True)
with col2:
    if st.button("🗑️ Clear", use_container_width=True):
        st.rerun()

if generate_btn and topic:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Progress", "🔍 Research", "✍️ Draft", "✅ Final Article"])
    
    with tab1:
        st.subheader("Generation Progress")
        progress_bar = st.progress(0)
        status_text = st.empty()

        status_text.text("🔍 Researching the topic...")
        progress_bar.progress(33)
        
        try:
            result = asyncio.run(run_writer_pipeline(topic))
    
            status_text.text("✍️ Writing the article...")
            progress_bar.progress(66)

            status_text.text("✅ Editing and refining...")
            progress_bar.progress(100)
            
            status_text.text("✅ Complete!")
     
            if isinstance(result, dict):
                with tab2:
                    st.subheader("Research Summary")
                    research = result.get("ResearcherAgent", "No research data available")
                    st.markdown(research)
                    st.download_button(
                        "📥 Download Research",
                        research,
                        file_name="research_summary.txt",
                        mime="text/plain"
                    )
                
                with tab3:
                    st.subheader("Draft Article")
                    draft = result.get("WriterAgent", "No draft available")
                    st.markdown(draft)
                    st.download_button(
                        "📥 Download Draft",
                        draft,
                        file_name="draft_article.txt",
                        mime="text/plain"
                    )
                
                with tab4:
                    st.subheader("Final Article")
                    final = result.get("EditorAgent", result)
                    st.markdown(final)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            "📥 Download as Text",
                            final if isinstance(final, str) else str(final),
                            file_name="final_article.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    with col2:
                        st.download_button(
                            "📥 Download as Markdown",
                            final if isinstance(final, str) else str(final),
                            file_name="final_article.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
            else:
                with tab4:
                    st.markdown(result)
                    st.download_button(
                        "📥 Download Article",
                        str(result),
                        file_name="article.txt",
                        mime="text/plain"
                    )
            
            st.success("Article generated successfully!")
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.exception(e)

elif generate_btn and not topic:
    st.warning("Please enter a topic first!")


st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Built with Google ADK & Gemini AI | 
        <a href='https://github.com/ab-JOY/ai-projects/tree/master/project-templates/writer-multi-agent'>GitHub</a></p>
    </div>
    """,
    unsafe_allow_html=True
)