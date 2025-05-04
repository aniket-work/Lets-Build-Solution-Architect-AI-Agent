from core.architect_agent import DiagramSpecialist
from agno.playground import Playground, serve_playground_app
from dotenv import load_dotenv
import os
import yaml


def initialize_sandbox():
    """Initialize development sandbox environment"""
    # Load environment variables
    load_dotenv()

    # Load configuration
    with open('config/settings.yaml', 'r') as file:
        config = yaml.safe_load(file)

    # Validate API keys
    groq_api_key = os.getenv("GROQ_API_KEY")
    development_api_key = os.getenv("DEVELOPMENT_API_KEY")

    if not (groq_api_key and development_api_key):
        raise ValueError("Please provide proper API key credentials")
        exit(1)

    # Create diagram specialist
    diagram_specialist = DiagramSpecialist()

    # Create and serve playground
    playground = Playground(agents=[diagram_specialist.agent])
    app = playground.get_app()

    return app


app = initialize_sandbox()

if __name__ == "__main__":
    serve_playground_app("sandbox:app", reload=True)