import re
import logging

logger = logging.getLogger(__name__)


def extract_mermaid_code(text):
    """Extract mermaid code from response text

    Args:
        text: The response text containing mermaid code

    Returns:
        str: Extracted mermaid code or None if not found
    """
    # Try standard regex pattern first
    match = re.search(r'```mermaid\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        logger.info("Matched mermaid code with standard pattern")
        return match.group(1).strip()

    # If no match found with standard pattern, try direct extraction
    if '```mermaid' in text and '```' in text[text.find('```mermaid') + 10:]:
        start = text.find('```mermaid') + 10
        end = text.find('```', start)
        if start > 10 and end > start:
            logger.info("Extracted mermaid code using direct string positions")
            return text[start:end].strip()

    logger.error("No mermaid code found in response")
    return None


def repair_mermaid_code(code):
    """Repair malformed mermaid code

    Args:
        code: The mermaid code to repair

    Returns:
        str: Repaired mermaid code
    """
    if not code:
        return None

    # Check if code is already properly formatted with multiple lines
    if len(code.splitlines()) > 3:
        # Fix incorrect arrow syntax -->|text|> to -->|text|
        repaired = re.sub(r'-->(\|[^|]+\|)>', r'-->\1', code)
        return repaired

    # Force line breaks between common mermaid elements
    repaired = code
    # For flowcharts
    repaired = re.sub(r'(\w+)-->', r'\n\1-->', repaired)
    repaired = re.sub(r'(\w+)-.->(\w+)', r'\n\1-.-> \2', repaired)
    # For sequence diagrams
    repaired = re.sub(r'(participant\s+\w+)', r'\n\1', repaired)
    repaired = re.sub(r'(\w+)->>', r'\n\1->>', repaired)
    # For general graph elements
    repaired = re.sub(r'(\w+)\[', r'\n\1[', repaired)

    # Fix incorrect arrow syntax -->|text|> to -->|text|
    repaired = re.sub(r'-->(\|[^|]+\|)>', r'-->\1', repaired)

    # Add proper graph type declaration if missing
    if not re.match(r'^(graph|sequenceDiagram|classDiagram|gantt|pie|flowchart)', repaired.strip()):
        if 'participant' in repaired:
            repaired = "sequenceDiagram\n" + repaired
        else:
            repaired = "graph LR\n" + repaired

    return repaired