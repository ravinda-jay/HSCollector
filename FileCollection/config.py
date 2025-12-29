import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("HA_API_KEY")
BASE_URL = "https://www.hybrid-analysis.com/api/v2"

HEADERS = {
    "User-Agent": "CollegeResearchProject/1.0",
    "API-Key": API_KEY,
    "Accept": "application/json"
}
