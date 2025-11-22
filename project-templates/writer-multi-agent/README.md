# Writer Multi-Agent System

A multi-agent system built with Google's Agent Development Kit (ADK) that automates the process of researching, writing, and editing high-quality articles on any given topic.

## Overview

This project implements a sequential pipeline of AI agents that work together to produce well-researched, comprehensive articles. The system consists of three specialized agents:

- **Researcher Agent**: Searches the web for relevant information and compiles a comprehensive research report
- **Writer Agent**: Creates a well-structured article based on the research findings
- **Editor Agent**: Refines and polishes the article for clarity, coherence, and quality

## Features

- **Automated Research**: Leverages Google Search to gather current, relevant information
- **Sequential Processing**: Each agent builds upon the work of the previous agent
- **Quality Assurance**: Built-in editing step ensures high-quality output
- **Flexible Integration**: Can be easily integrated into larger applications via the root agent

## Architecture

```
User Input (Topic)
      ↓
Root Agent (Orchestrator)
      ↓
Writer Pipeline
      ├── Researcher Agent → research_results
      ├── Writer Agent → comprehensive_article
      └── Editor Agent → final_article
      ↓
Final Output
```

## Project Structure

```
.
├── agent.py                # Root agent configuration
├── custom_agents.py        # Agent definitions and pipeline setup
└── custom_functions.py     # Pipeline execution function
```

## Prerequisites

- Python 3.8+
- Google ADK (Agent Development Kit)
- Access to Gemini API

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/writer-multi-agent-system.git
cd writer-multi-agent-system
```

2. Install required dependencies:
```bash
pip install google-adk
```

3. Set up environment variables:
```bash
export GEMINI_MODEL_NAME="gemini-2.5-pro"
export APP_NAME="WriterMultiAgent"
export USER_ID="your_user_id"
export SESSION_ID="your_session_id"
export GOOGLE_API_KEY="your_api_key"
export GOOGLE_GENAI_USE_VERTEXAI="False"
export GOOGLE_CLOUD_LOCATION="us-central1"
export GOOGLE_CLOUD_PROJECT="your_project_id"
```

## Usage

### Basic Usage

```python
from agent import root_agent

# Run the agent with a topic
result = await root_agent.run_async("The impact of artificial intelligence on healthcare")
print(result['final_article'])
```

### Direct Pipeline Usage

```python
from custom_functions import run_writer_pipeline

# Run the pipeline directly
output = await run_writer_pipeline("Climate change solutions")
print(output)
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_MODEL_NAME` | Gemini model to use | `gemini-2.5-pro` |
| `APP_NAME` | Application identifier | Required |
| `USER_ID` | User identifier for session management | Required |
| `SESSION_ID` | Session identifier | Required |
| `GOOGLE_API_KEY` | Your Google API key for Gemini access | Required |
| `GOOGLE_GENAI_USE_VERTEXAI` | Use Vertex AI instead of API (`True`/`False`) | `False` |
| `GOOGLE_CLOUD_LOCATION` | Google Cloud region for Vertex AI | `us-central1` |
| `GOOGLE_CLOUD_PROJECT` | Google Cloud project ID (if using Vertex AI) | Required for Vertex AI |

### Agent Customization

You can modify agent behaviors by editing their instructions in `custom_agents.py`:

```python
researcher_agent = LlmAgent(
    name="ResearcherAgent",
    model=model,
    instruction="Your custom instruction here...",
    tools=[google_search],
    output_key="research_results"
)
```

## How It Works

1. **Research Phase**: The Researcher Agent receives a topic and uses Google Search to gather relevant information, producing a comprehensive research report.

2. **Writing Phase**: The Writer Agent takes the research report and crafts a well-structured, engaging article that expands on all the topics covered in the research.

3. **Editing Phase**: The Editor Agent reviews the article, performing quality checks and making improvements to clarity, coherence, and overall quality.

4. **Output**: The final polished article is returned to the user.

## Example Output Flow

**Input**: "The future of renewable energy"

**Researcher Output**: Comprehensive report with latest statistics, trends, and developments in renewable energy

**Writer Output**: Well-structured article with introduction, body sections, and conclusion based on research

**Editor Output**: Polished, publication-ready article with improved flow and clarity

## Limitations

- Requires active internet connection for Google Search functionality
- Output quality depends on the Gemini model version used
- Research is limited to publicly available web information

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Troubleshooting

### Common Issues

**Import Errors**: Ensure Google ADK is properly installed
```bash
pip install --upgrade google-adk
```

**Session Errors**: Verify all environment variables are set correctly

**Search Tool Failures**: Check your internet connection and API credentials

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Google's Agent Development Kit (ADK)
- Powered by Gemini AI models
- Inspired by multi-agent system architectures
- Based on the tutorial: [Orchestrating Multi-Agent Systems](https://github.com/iamthuya/google-cloud-workshops/blob/main/ai-agents/agent-development-kit/orchestrating_multi_agent_systems.ipynb) by [@iamthuya](https://github.com/iamthuya)

## Contact

Allen Joy Bueza - [@allenjoybueza](www.linkedin.com/in/allenjoybueza) - allenjoybueza@gmail.com

Project Link: [https://github.com/yourusername/writer-multi-agent-system](https://github.com/yourusername/writer-multi-agent-system)

---

**Note**: This project is for educational and development purposes. Ensure compliance with Google's terms of service and API usage guidelines.
