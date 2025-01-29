
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Load configuration
JIRA_NUMBERS_CSV = os.getenv("JIRA_NUMBERS_CSV")
DIRECTORY_PATH = os.getenv("DIRECTORY_PATH")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_USERNAME = os.getenv("JIRA_USERNAME")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

# Validate configuration
def validate_config():
    missing = []
    if not JIRA_NUMBERS_CSV:
        missing.append("JIRA_NUMBERS_CSV")
    if not DIRECTORY_PATH:
        missing.append("DIRECTORY_PATH")
    if not JIRA_BASE_URL:
        missing.append("JIRA_BASE_URL")
    if not JIRA_USERNAME:
        missing.append("JIRA_USERNAME")
    if not JIRA_API_TOKEN:
        missing.append("JIRA_API_TOKEN")
    if missing:
        raise ValueError(f"Missing required configuration: {', '.join(missing)}")

validate_config()
