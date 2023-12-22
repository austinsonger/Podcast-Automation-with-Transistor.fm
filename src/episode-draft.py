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

def create_draft_episode(data):
    """
    Creates a draft episode in Transistor.fm with the given data.
    """
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
    Processes each row in the CSV file and creates a draft episode.
    Then updates the CSV with the episode ID.

    :param csv_path: The path to the CSV file.
    :type csv_path: str
    """
    rows = []
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            episode_data = {
                "title": row["Title"],
                "summary": row["Summary"]
            }

            response = create_draft_episode(episode_data)
            print(f"Draft episode created: {response}")

            # Extract the episode ID from the response and add it to the row
            row["Episode ID"] = response.get("data", {}).get("id", "Not Found")
            rows.append(row)

    # Now, write the updated data back to the CSV file
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = reader.fieldnames + ['Episode ID'] if 'Episode ID' not in reader.fieldnames else reader.fieldnames
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(rows)

# Main execution
process_csv(csv_file_path)
