from ui.dashboard import EnterpriseArchitectDashboard
import os
from dotenv import load_dotenv


def main():
    """Main entry point for the Enterprise Architect AI application"""
    # Load environment variables
    load_dotenv()

    # Check for required API keys
    required_keys = ["GROQ_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]

    if missing_keys:
        print(f"ERROR: Missing required environment variables: {', '.join(missing_keys)}")
        print("Please set these variables in your .env file or environment")
        exit(1)

    # Initialize and render dashboard
    dashboard = EnterpriseArchitectDashboard()
    dashboard.render()


if __name__ == "__main__":
    main()