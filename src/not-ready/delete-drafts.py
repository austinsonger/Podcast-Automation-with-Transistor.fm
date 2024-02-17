import csv
import os
import requests
import json

# Constants
TRANSISTOR_API_URL = "https://api.transistor.fm/v1/episodes"
TRANSISTOR_API_KEY = os.getenv('TRANSISTOR_API_KEY')
headers = {"x-api-key": TRANSISTOR_API_KEY, "Content-Type": "application/json"}

# Flag to enable/disable draft check
CHECK_DRAFT_STATUS = True

def fetch_existing_episodes():
    """
    Fetches existing episodes from Transistor.fm.
    """
    episodes = []
    page = 1
    while True:
        response = requests.get(f"{TRANSISTOR_API_URL}?page={page}", headers=headers)
        data = response.json()
        episodes.extend(data.get('data', []))
        if page == 1:  # Debug: Print attributes of the first few episodes for inspection
            print(data.get('data', [])[0:2])  # Adjust the range as needed
        if "next" not in data.get("links", {}):
            break
        page += 1
    return episodes

def count_draft_episodes(existing_episodes):
    """
    Counts episodes in "draft" status and returns the count.
    """
    draft_episodes = [episode for episode in existing_episodes if episode.get('attributes', {}).get('status').lower() == 'draft']
    return len(draft_episodes)

def delete_draft_episodes(existing_episodes):
    """
    Deletes episodes in "draft" status.
    """
    for episode in existing_episodes:
        if episode.get('attributes', {}).get('status').lower() == 'draft':
            episode_id = episode.get('id')
            delete_response = requests.delete(f"{TRANSISTOR_API_URL}/{episode_id}", headers=headers)
            if delete_response.status_code == 204:
                print(f"Successfully deleted draft episode: {episode.get('attributes', {}).get('title')}")
            else:
                print(f"Failed to delete draft episode: {episode.get('attributes', {}).get('title')} - {delete_response.text}")

def main():
    """
    Main execution function.
    """
    existing_episodes = fetch_existing_episodes()
    if CHECK_DRAFT_STATUS:
        draft_count = count_draft_episodes(existing_episodes)
        print(f"There are {draft_count} episodes in 'draft' status.")
        # Optionally, ask for confirmation before deleting
        proceed = input("Do you want to proceed with deletion? (yes/no): ")
        if proceed.lower() != 'yes':
            print("Deletion cancelled.")
            return
    
    delete_draft_episodes(existing_episodes)

if __name__ == "__main__":
    main()