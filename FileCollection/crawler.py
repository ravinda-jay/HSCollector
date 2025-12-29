import requests
import json
from config import BASE_URL, HEADERS

def get_collection_metadata(collection_id):
    """
    Retrieves metadata for a specific file collection ID.
    """
    # Endpoint for specific collection metadata
    url = f"{BASE_URL}/file-collection/{collection_id}"
    
    print(f"Fetching metadata for ID: {collection_id}...")
    
    try:
        # File collection lookup is a GET request
        response = requests.get(url, headers=HEADERS)
        
        # Check if the ID exists (404 means it's likely a single job, not a collection)
        if response.status_code == 404:
            print("Error: ID not found or is not a 'File Collection'.")
            return
            
        response.raise_for_status()
        data = response.json()
        
        # Save to a local file
        filename = f"metadata_{collection_id}.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
            
        print(f"Success! Metadata saved to {filename}")
        
        # Displaying a snippet of the metadata
        print("\n--- Metadata Summary ---")
        print(f"Verdict: {data.get('verdict', 'N/A')}")
        print(f"File Count: {len(data.get('images', []))}")
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    COLLECTION_ID = "694fcf852801d7c5520d4a9e"
    get_collection_metadata(COLLECTION_ID)