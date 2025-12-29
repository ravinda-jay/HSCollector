import os
from dotenv import load_dotenv

load_dotenv()

# Loads your key from the .env file
API_KEY = os.getenv("HA_API_KEY")
BASE_URL = "https://www.hybrid-analysis.com/api/v2"

HEADERS = {
    "User-Agent": "Falcon Sandbox Crawler/1.0",
    "API-Key": API_KEY,
    "Accept": "application/json"
}