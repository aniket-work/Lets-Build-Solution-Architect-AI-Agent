import logging


def setup_logging(level=logging.INFO):
    """Set up logging configuration

    Args:
        level: Logging level

    Returns:
        Logger: Configured logger
    """
    # Configure logging
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create logger
    logger = logging.getLogger("enterprise_architect")

    return logger