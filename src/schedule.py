import csv
import requests
import os
import re
from datetime import datetime

# Constants
csv_file_path = './config/scotus.csv'
api_url = "https://api.transistor.fm/v1/episodes"
transistor_api_key = os.getenv('TRANSISTOR_API_KEY')
show_id = "12890"

# Function to parse the CSV file and create draft episodes
def create_draft_episodes_from_csv(csv_file_path, show_id):
    episodes = []
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            if len(row) < 2:
                continue
            title, summary = row[0], row[1]

            episode = {
                "episode[show_id]": show_id,
                "episode[title]": title.strip(),
                "episode[summary]": summary.strip()
            }
            episodes.append(episode)
    return episodes

# Headers for the API request
headers = {
    "x-api-key": transistor_api_key
}

# Function to create a draft episode in Transistor
def create_draft_episode_in_transistor(episode_data):
    endpoint = f"{api_url}/publish"
    response = requests.patch(endpoint, data=episode_data, headers=headers)
    return response

# Function to update the episode with the publish date
def update_episode_publish_date(episode_id, published_date):
    endpoint = f"{api_url}/{episode_id}"
    episode_data = {
        "episode[published_at]": published_date
    }
    response = requests.patch(endpoint, data=episode_data, headers=headers)
    return response

# Main function to process the CSV and create/update episodes in Transistor
def process_episodes(csv_file_path):
    episodes = create_draft_episodes_from_csv(csv_file_path, show_id)
    for episode_data in episodes:
        response = create_draft_episode_in_transistor(episode_data)
        if response.status_code == 201:
            print(f"Draft episode '{episode_data['episode[title]']}' created successfully.")
            
            # Get the episode ID from the response
            episode_id = response.json().get('id')
            
            # Retrieve the argument date from the CSV file
            argument_date_match = re.search(r'\[Arg:\s(\d+\.\d+\.\d+)\]', episode_data['episode[title]'])
            if argument_date_match:
                argument_date_str = argument_date_match.group(1)
                # Adjust the date format to match the input format (MM.DD.YYYY)
                argument_date = datetime.strptime(argument_date_str, '%m.%d.%Y')
                # Set the time to 22:00 UTC
                argument_date = argument_date.replace(hour=22, minute=0, second=0)
                # Format as ISO 8601
                published_date = argument_date.strftime('%Y-%m-%dT%H:%M:%SZ')
            
                # Update the episode with the publish date
                update_response = update_episode_publish_date(episode_id, published_date)
                if update_response.status_code == 200:
                    print(f"Publish date updated for episode '{episode_data['episode[title]']}'")
                else:
                    print(f"Failed to update publish date for episode '{episode_data['episode[title]']}'")
            else:
                print(f"Argument date not found for episode '{episode_data['episode[title]']}'")
        else:
            print(f"Failed to create episode '{episode_data['episode[title]']}'. Status Code: {response.status_code}, Response: {response.json()}")

process_episodes(csv_file_path)
