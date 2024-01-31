import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MS_TEAMS_WEBHOOK_URL = os.environ.get("MS_TEAMS_WEBHOOK_URL")
