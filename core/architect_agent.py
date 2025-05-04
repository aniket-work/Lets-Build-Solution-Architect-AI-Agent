from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
import yaml
import os


class DiagramSpecialist:
    """Specialist agent for diagram generation"""

    def __init__(self, config_path="config/settings.yaml"):
        """Initialize with configuration"""
        # Load configuration
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

        # Get API keys from environment
        self.groq_api_key = os.getenv("GROQ_API_KEY")

        # Initialize agent
        self.agent = self._create_agent()

    def _create_agent(self):
        """Create the specialized agent"""
        return Agent(
            name="Diagram Specialist",
            role="enterprise_diagram_generation",
            model=Groq(
                id=self.config["models"]["primary"],
                api_key=self.groq_api_key
            ),
            tools=[DuckDuckGoTools()],
            instructions=self._get_instructions(),
            markdown=True,
        )

    def _get_instructions(self):
        """Get agent instructions"""
        return """
        You are a professional Enterprise Architect with expertise in system design.
        Create professional diagrams in Mermaid format based on requirements.

        Your response format must be a Mermaid diagram:
        ```mermaid
        [Your Mermaid diagram code here]
        ```

        CRITICAL: Each node, connection, and command must be on its own line.

        After the diagram, provide a brief explanation of the architecture.
        """

    def generate_diagram(self, requirements):
        """Generate a diagram based on requirements"""
        return self.agent.run(requirements, stream=True)