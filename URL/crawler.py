import requests
import json
from pathlib import Path
from config import BASE_URL, HEADERS

def crawl_latest_submissions():
    """
    Crawls the 'Latest Submissions' feed from Hybrid Analysis 
    and saves the data to a JSON file.
    """
    # Endpoint for the global latest feed
    url = f"{BASE_URL}/feed/latest"
    
    print("Crawling latest submissions from Falcon Sandbox...")
    
    try:
        # Using POST as requested for site data collection
        response = requests.post(url, headers=HEADERS)
        
        # Check for successful response
        response.raise_for_status()
        data = response.json()
        
        # Define the output filename (save relative to this script so working dir doesn't matter)
        out_dir = Path(__file__).parent
        # create a `data` folder next to the script if you prefer storing there
        data_dir = out_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        filename = data_dir / "latest_submissions.json"

        # Save the full JSON content to a file (use utf-8 and disable ascii to preserve characters)
        with filename.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"Success! Latest submission data saved to {filename}")
        
        # Optional: Print a summary of what was crawled
        submissions = data.get('data', [])
        print(f"Total items crawled: {len(submissions)}")
        
        if submissions:
            print("\n--- Recent Submissions Snippet ---")
            for item in submissions[:3]:  # Show the first 3 items
                name = item.get('submit_name', 'Unknown')
                type_ = item.get('type', 'Unknown')
                print(f"- Type: {type_} | Name: {name}")
                
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during crawling: {e}")

if __name__ == "__main__":
    # Run the crawler to fetch and save the JSON
    crawl_latest_submissions()