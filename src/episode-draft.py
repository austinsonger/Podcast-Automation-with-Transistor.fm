import csv
import os
import requests
import json

# Constants
csv_file_path = './config/scotus.csv'
TRANSISTOR_API_URL = "https://api.transistor.fm/v1/episodes"
TRANSISTOR_API_KEY = os.getenv('TRANSISTOR_API_KEY')
TRANSISTOR_SHOW_ID = os.getenv('TRANSISTOR_SHOW_ID')
headers = {"x-api-key": TRANSISTOR_API_KEY, "Content-Type": "application/json"}

def fetch_existing_episodes():
    """
    Fetches existing episodes from Transistor.fm, potentially filtering by draft status.
    """
    episodes = []
    page = 1
    status_filter = 'draft'  # Speculative: Adjust based on actual API capability for filtering
    while True:
        response = requests.get(f"{TRANSISTOR_API_URL}?page={page}&status={status_filter}", headers=headers)
        data = response.json()
        episodes.extend(data.get('data', []))
        if "next" not in data.get("links", {}):
            break
        page += 1
    return episodes


def episode_exists(title, existing_episodes):
    """
    Checks if an episode with the given title already exists.
    """
    return any(episode.get('attributes', {}).get('title').lower() == title.lower() for episode in existing_episodes)

def create_draft_episode(data, existing_episodes):
    """
    Creates a draft episode in Transistor.fm with the given data if no episode with the same title exists.
    """
    if episode_exists(data['title'], existing_episodes):
        return {"error": "Episode with this title already exists."}
    
    payload = {
        "episode": {
            "show_id": TRANSISTOR_SHOW_ID,
            "title": data['title'],
            "description": data['summary']
        }
    }
    response = requests.post(TRANSISTOR_API_URL, headers=headers, json=payload)
    return response.json()

def process_csv(csv_path):
    """
    Processes each row in the CSV file, checks for existing episodes, and creates a draft episode if no matching title is found.
    Then updates the CSV with the episode ID.
    """
    existing_episodes = fetch_existing_episodes()
    rows = []
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            episode_data = {
                "title": row["Title"],
                "summary": row["Summary"]
            }

            response = create_draft_episode(episode_data, existing_episodes)
            if "error" not in response:
                print(f"Draft episode created: {response}")
                row["Episode ID"] = response.get("data", {}).get("id", "Not Found")
            else:
                print(response["error"])
                row["Episode ID"] = "Skipped due to duplicate title"
            rows.append(row)

    # Now, write the updated data back to the CSV file
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = reader.fieldnames + ['Episode ID'] if 'Episode ID' not in reader.fieldnames else reader.fieldnames
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(rows)

# Main execution
process_csv(csv_file_path)
