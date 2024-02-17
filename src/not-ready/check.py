import csv
import os
import requests
import json

# Constants
TRANSISTOR_API_URL = "https://api.transistor.fm/v1/episodes"
TRANSISTOR_API_KEY = os.getenv('TRANSISTOR_API_KEY')
TRANSISTOR_SHOW_ID = os.getenv('TRANSISTOR_SHOW_ID')
headers = {"x-api-key": TRANSISTOR_API_KEY, "Content-Type": "application/json"}

def fetch_existing_episodes():
    """
    Fetches all existing episodes from Transistor.fm.
    """
    episodes = []
    page = 1
    while True:
        response = requests.get(f"{TRANSISTOR_API_URL}?page={page}", headers=headers)
        data = response.json()
        episodes.extend(data.get('data', []))
        if "next" not in data.get("links", {}):
            break
        page += 1
    return episodes

def filter_draft_episodes(episodes):
    """
    Filters episodes to return only those in 'draft' status.
    """
    return [episode for episode in episodes if episode.get('attributes', {}).get('status').lower() == 'draft']

def main():
    """
    Main execution function.
    """
    all_episodes = fetch_existing_episodes()
    draft_episodes = filter_draft_episodes(all_episodes)
    print(f"Total draft episodes: {len(draft_episodes)}")

    # Optionally, here you can iterate through draft_episodes to delete them or to perform other actions.

if __name__ == "__main__":
    main()
