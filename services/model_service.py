from typing import Dict, List, Iterator, Optional
import os
import yaml
import logging
from agno.models.groq import Groq
from agno.models.anthropic import Claude
from agno.agent import Agent, RunResponse

logger = logging.getLogger(__name__)


class ModelProviderService:
    """Service for managing LLM model providers"""

    def __init__(self, config_path: str = "config/settings.yaml"):
        """Initialize the model provider service

        Args:
            config_path: Path to configuration file
        """
        # Load configuration
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

        # Get API keys
        self.api_keys = self._load_api_keys()

        # Initialize model providers
        self.providers = {}
        self._initialize_providers()

    def _load_api_keys(self) -> Dict[str, str]:
        """Load API keys from environment variables

        Returns:
            Dict: Dictionary of API keys
        """
        return {
            "groq": os.getenv("GROQ_API_KEY"),
            "claude": os.getenv("CLAUDE_API_KEY"),
            "openai": os.getenv("OPENAI_API_KEY")
        }

    def _initialize_providers(self):
        """Initialize model providers"""
        # Initialize Groq provider if API key is available
        if self.api_keys.get("groq"):
            self.providers["groq"] = {
                "llama-3.3-70b-versatile": Groq(
                    id="llama-3.3-70b-versatile",
                    api_key=self.api_keys["groq"]
                ),
                "llama-3.3-8b-versatile": Groq(
                    id="llama-3.3-8b-versatile",
                    api_key=self.api_keys["groq"]
                )
            }
            logger.info("Initialized Groq provider")

        # Initialize Claude provider if API key is available
        if self.api_keys.get("claude"):
            self.providers["claude"] = {
                "claude-3-opus": Claude(
                    id="claude-3-opus",
                    api_key=self.api_keys["claude"]
                ),
                "claude-3-sonnet": Claude(
                    id="claude-3-sonnet",
                    api_key=self.api_keys["claude"]
                )
            }
            logger.info("Initialized Claude provider")

    def get_model(self, provider: str, model_id: str):
        """Get model instance by provider and model ID

        Args:
            provider: Provider name (groq, claude, openai)
            model_id: Model ID

        Returns:
            Model instance or None if not found
        """
        if provider in self.providers and model_id in self.providers[provider]:
            return self.providers[provider][model_id]

        logger.error(f"Model {model_id} from provider {provider} not found")
        return None

    def get_default_model(self):
        """Get default model from configuration

        Returns:
            Default model instance
        """
        default_provider = self.config.get("models", {}).get("default_provider", "groq")
        default_model = self.config.get("models", {}).get("primary", "llama-3.3-70b-versatile")

        return self.get_model(default_provider, default_model)


class EnterpriseModelService:
    """Service for managing enterprise AI models and agents"""

    def __init__(self):
        """Initialize the enterprise model service"""
        self.provider_service = ModelProviderService()
        self.specialist_templates = self._load_specialist_templates()

    def _load_specialist_templates(self) -> Dict[str, Dict]:
        """Load specialist templates from configuration

        Returns:
            Dict: Dictionary of specialist templates
        """
        # Load from config/defaults.json in a real implementation
        return {
            "diagram_specialist": {
                "name": "Diagram Specialist",
                "role": "enterprise_diagram_generation",
                "instructions": """
                You are a professional Enterprise Architect with expertise in system design.
                Create professional diagrams in Mermaid format based on requirements.

                Your response format must be a Mermaid diagram:
                ```mermaid
                [Your Mermaid diagram code here]
                ```

                CRITICAL: Each node, connection, and command must be on its own line.

                After the diagram, provide a brief explanation of the architecture.
                """
            },
            "integration_specialist": {
                "name": "Integration Specialist",
                "role": "system_integration_design",
                "instructions": """
                You are a System Integration Specialist with expertise in connecting
                enterprise systems and applications.

                Create detailed integration architectures in Mermaid format based on requirements.

                Your response must include a Mermaid diagram showing the integration flow.

                Include details on APIs, data formats, and synchronization methods.
                """
            }
        }

    def create_specialist(self, specialist_type: str, model_id: str = None) -> Agent:
        """Create a specialist agent

        Args:
            specialist_type: Type of specialist to create
            model_id: Optional model ID override

        Returns:
            Agent: Specialist agent
        """
        # Get template
        template = self.specialist_templates.get(specialist_type)
        if not template:
            logger.error(f"Specialist template {specialist_type} not found")
            raise ValueError(f"Unknown specialist type: {specialist_type}")

        # Get model
        provider = "groq"  # Default provider
        model_id = model_id or "llama-3.3-70b-versatile"  # Default model
        model = self.provider_service.get_model(provider, model_id)

        if not model:
            logger.error(f"Model {model_id} not available")
            raise ValueError(f"Model {model_id} not available")

        # Create agent
        from agno.tools.duckduckgo import DuckDuckGoTools

        agent = Agent(
            name=template["name"],
            role=template["role"],
            model=model,
            tools=[DuckDuckGoTools()],
            instructions=template["instructions"],
            markdown=True,
        )

        logger.info(f"Created {specialist_type} with model {model_id}")
        return agent

    def generate_diagram(self, requirements: str, specialist_type: str = "diagram_specialist",
                         model_id: str = None) -> Iterator[RunResponse]:
        """Generate a diagram based on requirements

        Args:
            requirements: The requirements text
            specialist_type: Type of specialist to use
            model_id: Optional model ID override

        Returns:
            Iterator: Stream of diagram generation responses
        """
        # Create specialist
        specialist = self.create_specialist(specialist_type, model_id)

        # Generate diagram
        logger.info(f"Generating diagram with {specialist_type} and model {model_id or 'default'}")
        return specialist.run(requirements, stream=True)