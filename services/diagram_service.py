from core.architect_agent import DiagramSpecialist
import logging

logger = logging.getLogger(__name__)


class DiagramGenerationService:
    """Service for generating architecture diagrams"""

    def __init__(self):
        """Initialize the diagram generation service"""
        self.specialist = DiagramSpecialist()

    def generate(self, requirements, model=None):
        """Generate a diagram based on requirements

        Args:
            requirements: The requirements text
            model: Optional model override

        Returns:
            Iterator: Stream of diagram generation responses
        """
        logger.info(f"Generating diagram with requirements: {requirements[:100]}...")

        # Update model if specified
        if model and model != self.specialist.agent.model.id:
            logger.info(f"Switching model to {model}")
            self.specialist.agent.model.id = model

        # Generate diagram
        return self.specialist.generate_diagram(requirements)